import os
import time
from pydantic import BaseModel, Field
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_litellm import ChatLiteLLM


class Configuration(BaseModel):
    """Configuration for the Delivery Management Multi-Agent System."""

    # Primary models for different agent types (OpenRouter via LiteLLM)
    coordinator_model: str = Field(
        default="google/gemini-2.5-flash-lite",
        metadata={
            "description": "Model for the Project Coordinator agent (master orchestrator) - OpenRouter format"
        },
    )

    specialist_model: str = Field(
        default="google/gemini-2.5-flash-lite",
        metadata={
            "description": "Model for specialist agents (Project Manager, Task Coordinator, Technical) - OpenRouter format"
        },
    )

    document_model: str = Field(
        default="google/gemini-2.5-flash",
        metadata={
            "description": "Model for document generation (PRDs, reports, credentials) - OpenRouter format"
        },
    )

    analysis_model: str = Field(
        default="google/gemini-2.5-flash-lite",
        metadata={
            "description": "Model for historical analysis and pattern recognition - OpenRouter format"
        },
    )

    # LLM Provider Configuration
    use_openrouter: bool = Field(
        default=True,
        metadata={
            "description": "Use OpenRouter as LLM provider (via LiteLLM) instead of direct Gemini API"
        },
    )

    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        metadata={
            "description": "OpenRouter API base URL"
        },
    )

    # System configuration
    max_conversation_length: int = Field(
        default=50,
        metadata={"description": "Maximum number of conversation turns allowed"},
    )

    max_concurrent_agents: int = Field(
        default=15,
        metadata={"description": "Maximum number of concurrent agent executions"},
    )

    # Project creation settings
    project_creation_timeout_minutes: int = Field(
        default=10,
        metadata={"description": "Timeout for project creation workflow in minutes"},
    )

    # Task management settings
    thursday_reminder_hour: int = Field(
        default=14,  # 2 PM
        metadata={"description": "Hour of day (24h format) for Thursday reminders"},
    )

    # Document generation settings
    max_document_length: int = Field(
        default=10000,
        metadata={"description": "Maximum characters for generated documents"},
    )

    # Data storage settings
    json_data_directory: str = Field(
        default="./json_data",
        metadata={"description": "Directory for JSON data persistence"},
    )

    # Temperature settings for different operations
    coordinator_temperature: float = Field(
        default=0.1,
        metadata={"description": "Temperature for coordinator routing decisions"},
    )

    document_temperature: float = Field(
        default=0.3,
        metadata={"description": "Temperature for document generation"},
    )

    analysis_temperature: float = Field(
        default=0.2,
        metadata={"description": "Temperature for analysis operations"},
    )

    # API quota management
    api_call_delay_seconds: int = Field(
        default=120,
        metadata={"description": "Delay in seconds between API calls to prevent quota exhaustion"},
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        return cls(**values)


class DelayedLLM:
    """
    Universal delayed LLM wrapper that supports both OpenRouter (via LiteLLM) and direct Gemini API.
    
    This wrapper automatically applies a delay before each LLM call to respect API rate limits.
    It can work with either ChatLiteLLM (for OpenRouter) or ChatGoogleGenerativeAI (direct).
    """
    
    def __init__(self, delay_seconds: int = 60, use_openrouter: bool = True, **kwargs):
        """
        Initialize the delayed LLM wrapper.
        
        Args:
            delay_seconds: Seconds to delay before each API call
            use_openrouter: If True, use OpenRouter via LiteLLM; if False, use direct Gemini API
            **kwargs: Passed through to the underlying LLM class
        """
        self._delay_seconds = delay_seconds
        self._last_call_time = 0.0
        self._use_openrouter = use_openrouter
        
        # Remove our custom parameters from kwargs before passing to LLM
        filtered_kwargs = {
            k: v for k, v in kwargs.items() 
            if k not in ['delay_seconds', 'use_openrouter']
        }
        
        if use_openrouter:
            # Configure for OpenRouter via LiteLLM
            openrouter_kwargs = {
                **filtered_kwargs,
                "base_url": "https://openrouter.ai/api/v1",
                "custom_llm_provider": "openrouter",
                "api_key": os.getenv("OPEN_ROUTER_API_KEY")
            }
            self.llm = ChatLiteLLM(**openrouter_kwargs)
        else:
            # Configure for direct Gemini API
            gemini_kwargs = {
                **filtered_kwargs,
                "api_key": os.getenv("GEMINI_API_KEY")
            }
            self.llm = ChatGoogleGenerativeAI(**gemini_kwargs)
    
    def invoke(self, input, config=None):
        """Override invoke to add delay before API calls."""
        current_time = time.time()
        time_since_last_call = current_time - self._last_call_time
        
        if time_since_last_call < self._delay_seconds:
            sleep_time = self._delay_seconds - time_since_last_call
            provider = "OpenRouter" if self._use_openrouter else "Gemini API"
            print(f"⏱️  Applying {sleep_time:.1f}s delay for {provider}...")
            time.sleep(sleep_time)
        
        self._last_call_time = time.time()
        return self.llm.invoke(input, config)
    
    async def ainvoke(self, input, config=None):
        """Override async invoke to add delay before API calls."""
        import asyncio
        
        current_time = time.time()
        time_since_last_call = current_time - self._last_call_time
        
        if time_since_last_call < self._delay_seconds:
            sleep_time = self._delay_seconds - time_since_last_call
            provider = "OpenRouter" if self._use_openrouter else "Gemini API"
            print(f"⏱️  Applying {sleep_time:.1f}s async delay for {provider}...")
            await asyncio.sleep(sleep_time)
        
        self._last_call_time = time.time()
        return await self.llm.ainvoke(input, config)


# Backward compatibility alias
DelayedChatGoogleGenerativeAI = DelayedLLM