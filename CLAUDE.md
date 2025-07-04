# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a fullstack agentic application generator built on LangGraph, React, and Google Gemini. The system creates intelligent agents that can coordinate complex business workflows. The project includes both a working example (backend/) and a generation system (backend_gen/) for creating new agent architectures.

## Key Architecture

### Dual Backend Structure
- `backend/` - Working LangGraph research agent (web search + reflection) used as base
- `backend_gen/` - Generated agent workspace for new business cases
- `frontend/` - React/Vite interface for both backends

### Agent Generation System

1. Reads business requirements from `/docs/planning.md`
2. Generates complete LangGraph applications in `backend_gen/`
3. Follows structured phases with comprehensive testing
4. Accumulates knowledge in `/docs/tips.md`

## Development Commands

### Main Development
```bash
# Start both frontend and working backend (research agent)
make dev

# Start frontend and generated backend (use case implementation)
make gen

# Frontend only
make dev-frontend

# Working backend only  
make dev-backend

# Generated backend only
make dev-backend-gen
```

**CRITICAL**: For generated agent development, ALWAYS use `make gen` not `make dev`. The `make gen` command works with the generated backend in `backend_gen/` folder.

### Backend Development (Python/LangGraph)
```bash
cd backend  # or backend_gen
pip install -e .           # Install in editable mode
langgraph dev             # Start LangGraph dev server (port 2024)
python -m pytest tests/  # Run comprehensive tests
ruff check src/          # Lint code
```

### Frontend Development (React/TypeScript)
```bash
cd frontend
npm install              # Install dependencies
npm run dev             # Start Vite dev server (port 5173)
npm run build           # Build for production
npm run lint            # ESLint code
```

## Important File Patterns

### LangGraph Agent Structure
Required files in any backend implementation:
- `src/agent/state.py` - OverallState TypedDict definition
- `src/agent/graph.py` - Graph assembly with absolute imports
- `src/agent/nodes/` - Individual agent node functions
- `src/agent/tools_and_schemas.py` - Pydantic models and tools
- `src/agent/configuration.py` - LLM model configuration
- `langgraph.json` - Deployment configuration

### Critical Development Patterns

#### LLM Configuration Pattern
Always use configuration-based model selection:
```python
from agent.configuration import Configuration
from langchain_core.runnables import RunnableConfig

def node_function(state: OverallState, config: RunnableConfig) -> dict:
    configurable = Configuration.from_runnable_config(config)
    llm = ChatGoogleGenerativeAI(
        model=configurable.answer_model,  # Use configured model
        temperature=0,
        api_key=os.getenv("GEMINI_API_KEY")
    )
```

#### Import Requirements
- Use ABSOLUTE imports in graph.py: `from agent.nodes.x import y`
- Never use relative imports: `from .nodes.x import y` (breaks langgraph dev)
- Keep agent/__init__.py minimal to prevent circular imports

#### State Management
All agents share OverallState TypedDict with consistent field patterns:
```python
from langgraph.graph import add_messages
from typing_extensions import Annotated

class OverallState(TypedDict):
    messages: Annotated[list, add_messages]
    document_path: str
    questions_status: Dict[str, str]  # question_id -> "answered"|"pending"|"needs_improvement"
    current_question: Optional[str]
    user_context: Dict[str, Any]
    language: str
    conversation_history: List[Dict[str, Any]]
```

## Testing Strategy

### Comprehensive Testing Phases
1. **Unit Testing** - Individual agent functions with real LLM calls
2. **Graph Compilation** - Import validation and graph building
3. **Server Testing** - LangGraph dev server with real execution
4. **API Integration** - REST endpoint validation
5. **Scenario Testing** - LangWatch Scenario framework for complex flows, make multiple files with multiple scenarios

### Critical Testing Commands
```bash
# Pre-server validation (prevents runtime failures)
python -c "from agent.graph import graph; print('Graph loads successfully')"
pip install -e .

# Server testing with proper cleanup
langgraph dev > langgraph.log 2>&1 &
SERVER_PID=$!
# ... testing logic ...
kill $SERVER_PID
```

**CRITICAL SERVER VALIDATION**: After ANY changes to agent code, ALWAYS check console output:
```bash
# 1. Start server in background and monitor logs
nohup langgraph dev > langgraph.log 2>&1 & 
sleep 5

# 2. Check for import/runtime errors in console
tail -10 langgraph.log | grep -i "error\|exception\|failed"

# 3. Test actual endpoint execution
curl -X POST "http://127.0.0.1:2024/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "test"}]}, "stream_mode": "values"}'

# 4. Verify no errors in response (should not contain "error" event)
```

The server may start successfully but still have runtime errors when graph execution begins. Always test actual execution, not just server startup.

## Environment Setup

### Required Environment Variables
```bash
# Backend (.env file)
GEMINI_API_KEY=your_gemini_api_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional for tracing
```

### API Key Configuration
The system requires Google Gemini API key. LLM libraries do NOT automatically load from .env, so explicitly pass:
```python
api_key=os.getenv("GEMINI_API_KEY")
```

## Business Case Generation Protocol

The `/docs/planning.md` contains a comprehensive protocol for autonomous agent generation:

1. **Business Case Creation** - Generate diverse business scenarios
2. **Architecture Planning** - Design agent networks and workflows  
3. **Implementation** - Generate complete LangGraph applications
4. **Testing & Validation** - Comprehensive multi-phase testing
5. **Knowledge Accumulation** - Document patterns in `/docs/tips.md`

### Key Execution Principle
The system is designed for FULL AUTONOMY - no user confirmation required once started. Each business case follows structured phases with clear success criteria.

## Deployment

### Docker Build
```bash
docker build -t gemini-fullstack-langgraph -f Dockerfile .
```

### Production Server
```bash
GEMINI_API_KEY=<key> LANGSMITH_API_KEY=<key> docker-compose up
# Access at http://localhost:8123/app/
```

## Common Patterns

### Error Prevention
- Always test graph imports before server startup
- Use absolute imports in all graph files
- Validate environment variables before LLM calls
- Implement proper process cleanup in testing

### Agent Node Structure
Each agent node follows consistent patterns:
- Takes OverallState and RunnableConfig parameters
- Uses Configuration.from_runnable_config() for models
- Returns dict with state updates
- Handles errors gracefully with fallbacks

### Router vs Node Distinction
- Routers return string literals for graph navigation
- Nodes return dict state updates or None
- Only routers determine graph flow paths

This architecture enables systematic generation of complex multi-agent systems while maintaining consistency and reliability across different business domains.

## 🔄 MAJOR ARCHITECTURE SHIFT: Modern LLM-First Agent Design

### **⚡ BREAKING CHANGE: From Script-Based to Conversation-Native Design**

**CRITICAL PARADIGM SHIFT**: We discovered that traditional agent architectures over-engineer what modern LLMs can handle naturally. This represents a fundamental change in how we build conversational agents.

#### **📊 Impact Summary:**
- **Code Reduction**: 70% less code (350+ lines → 135 lines)
- **Better UX**: More natural, flexible conversations
- **Faster Development**: Focus on domain expertise, not conversation engineering
- **Easier Maintenance**: Single prompt updates vs. multiple helper functions

### **Conversational-First Approach**

**CRITICAL PRINCIPLE**: Modern LLMs are capable of natural conversation understanding. Avoid over-engineering with scripted conversation flows, intent detection, or complex routing logic.

#### **✅ DO: Let LLMs Handle Conversation Naturally**

```python
# ✅ PREFERRED: Single comprehensive prompt with embedded expertise
def audit_coordinator_agent(state: OverallState, config: RunnableConfig) -> Dict[str, Any]:
    # Get configuration and LLM
    configurable = Configuration.from_runnable_config(config)
    llm = ChatGoogleGenerativeAI(
        model=configurable.reflection_model,
        temperature=0.1,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    # Get current audit status using tools
    questions_status, questions_list = get_audit_status()
    
    # Extract user message with proper LangChain message handling
    messages = state.get("messages", [])
    latest_user_message = "Hola"
    for msg in messages:
        if hasattr(msg, 'type') and msg.type == "human":
            latest_user_message = msg.content
        elif isinstance(msg, dict) and msg.get("role") == "user":
            latest_user_message = msg.get("content", "Hola")
    
    # Single comprehensive prompt with embedded NES expertise
    prompt = f"""Eres un asistente experto en auditorías de seguridad según el estándar NES (Esquema Nacional de Seguridad) de España.

ESTADO ACTUAL DEL CUESTIONARIO:
{questions_status}

CONOCIMIENTO NES PARA EVALUAR RESPUESTAS:
- Copias de seguridad: Requiere tipo de sistema, frecuencia, verificación, ubicación (local/remota), retención, plan de recuperación
- Control de acceso: Autenticación implementada, políticas de contraseñas, MFA, gestión de privilegios, revisiones periódicas, logs
- Monitoreo: Herramientas de red, sistemas de detección, análisis de logs, procedimientos de respuesta, escalación, informes

INSTRUCCIONES:
1. SIEMPRE responde en español, tono conversacional y profesional
2. Si es primer saludo: Da bienvenida y muestra primera pregunta pendiente  
3. Si usuario responde a pregunta: Evalúa completitud contra requisitos NES arriba
4. Si respuesta completa: Di que la guardarás y muestra siguiente pregunta
5. Si respuesta incompleta: Pide específicamente qué falta según NES

MENSAJE DEL USUARIO: {latest_user_message}

Analiza el mensaje y responde apropiadamente."""

    response = llm.invoke(prompt)
    return {"messages": state.get("messages", []) + [{"role": "assistant", "content": response.content}]}
```

#### **❌ AVOID: Over-Engineered Conversation Management**

```python
# ❌ WRONG: Complex intent detection and routing
def old_style_agent(state, config):
    intent = analyze_user_intent(user_message)  # Unnecessary
    
    if intent == "greeting":
        return generate_greeting_response()
    elif intent == "question": 
        return generate_question_response()
    elif intent == "answer":
        return generate_answer_enhancement()
    # ... complex routing logic
```

### **Expertise Integration Patterns**

#### **Embed Domain Knowledge in Prompts**

Instead of creating separate "tool" classes for domain logic, embed expertise directly:

```python
# ✅ PREFERRED: Embedded expertise from actual backend_gen implementation
NES_EXPERTISE = """
- Copias de seguridad: Requiere tipo de sistema, frecuencia, verificación, ubicación (local/remota), retención, plan de recuperación
- Control de acceso: Autenticación implementada, políticas de contraseñas, MFA, gestión de privilegios, revisiones periódicas, logs
- Monitoreo: Herramientas de red, sistemas de detección, análisis de logs, procedimientos de respuesta, escalación, informes
- Continuidad: Plan documentado, procedimientos de recuperación, RTO definido, pruebas regulares, documentación actualizada
- Formación: Contenidos específicos, frecuencia, evaluación de efectividad, registros de cumplimiento, certificaciones
- Vulnerabilidades: Herramientas de análisis, frecuencia de evaluaciones, procedimientos de parcheo, tiempos de respuesta
- Cifrado: Algoritmos utilizados, gestión de claves, datos en tránsito/reposo, cumplimiento RGPD, clasificación de datos
- Auditorías internas: Frecuencia, alcance, personal responsable, seguimiento de hallazgos, documentación de evidencias
"""

prompt = f"""Eres un asistente experto en auditorías de seguridad según el estándar NES (Esquema Nacional de Seguridad) de España.

CONOCIMIENTO NES PARA EVALUAR RESPUESTAS:
{NES_EXPERTISE}

Evalúa las respuestas del usuario contra estos estándares y pide detalles específicos cuando falten."""
```

```python
# ❌ AVOID: Separate tool classes for simple logic
class SecurityExpertiseTool:
    def analyze_backup_answer(self, answer):
        # This is just structured data, not a real tool
        return {"missing": ["frequency", "verification"]}
```

### **Tool Usage Guidelines**

#### **Use Tools for Actual Operations, Not Logic**

Tools should perform concrete actions, not replace LLM reasoning:

```python
# ✅ CORRECT: Tools for actual operations from backend_gen
class DocumentReaderTool:
    """Tool for reading and parsing audit questionnaire MD files"""
    
    @staticmethod
    def read_document(file_path: str) -> Dict[str, Any]:
        """Read and parse the audit questionnaire"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            questions = DocumentReaderTool._parse_questions(content)
            return {"success": True, "questions": questions, "document_path": file_path}
        except Exception as e:
            return {"success": False, "error": str(e), "questions": []}

class AnswerSaverTool:
    """Tool for saving and loading audit answers"""
    
    @staticmethod
    def save_answer(question_id: str, answer: str, questions: List[AuditQuestion]) -> Dict[str, Any]:
        """Save answer to JSON file"""
        try:
            # Load existing answers
            answers_data = AnswerSaverTool._load_answers_file()
            answers_data[question_id] = answer
            
            # Save to file
            with open("audit_answers.json", "w", encoding="utf-8") as f:
                json.dump(answers_data, f, ensure_ascii=False, indent=2)
            
            return {"success": True, "message": f"Answer saved for {question_id}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

```python
# ❌ WRONG: Tools for simple logic/formatting
@tool
def analyze_user_intent(message: str) -> str:
    """This should be handled by LLM naturally"""
    if "hello" in message.lower():
        return "greeting"
    # LLM can do this better naturally
```

### **State Management Simplification**

#### **Minimal State, Maximum LLM Intelligence**

```python
# ✅ PREFERRED: Simple state, let LLM manage conversation (from backend_gen)
class OverallState(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history
    document_path: str                       # MD file path
    questions_status: Dict[str, str]         # question_id -> status
    current_question: Optional[str]          # Currently active question
    user_context: Dict[str, Any]             # Minimal context only
    language: str                            # Spanish for NES audits
    conversation_history: List[Dict[str, Any]]  # Brief interaction log
```

```python
# ❌ AVOID: Complex state tracking that LLM can handle
class OverallState(TypedDict):
    messages: List[Dict[str, Any]]
    current_intent: str             # LLM can detect this
    conversation_stage: str         # LLM can track this
    last_question_type: str         # LLM remembers context
    user_engagement_level: str      # LLM can assess this
```

### **Testing with Configuration Standards**

#### **Always Use Configuration Defaults in Tests**

```python
# ✅ CORRECT: Use Configuration class defaults
def setup_test_config():
    default_config = Configuration()
    return RunnableConfig(
        configurable={
            "answer_model": default_config.answer_model,
            "reflection_model": default_config.reflection_model,
            # Use all defaults from Configuration class
        }
    )
```

```python
# ❌ WRONG: Hardcoded model names in tests
def setup_test_config():
    return RunnableConfig(
        configurable={
            "answer_model": "gemini-1.5-flash-latest",  # Hardcoded
            "reflection_model": "gemini-2.5-flash-preview-04-17",  # Hardcoded
        }
    )
```

### **Implementation Guidelines**

1. **Start with Single Comprehensive Prompt**: All domain expertise and instructions in one place
2. **Let LLM Handle Intent**: No artificial intent detection or conversation routing
3. **Tools for Actions Only**: Use tools for file operations, API calls, data persistence - not logic
4. **Embedded Expertise**: Put domain knowledge directly in prompts, not separate classes
5. **Natural Flow**: Let LLM determine conversation flow based on context and expertise
6. **Configuration-Driven Tests**: Always use Configuration class defaults in test setup
7. **Minimal State**: Only track what LLM can't naturally remember across turns

### **Benefits of LLM-First Approach**

- **70% Less Code**: Eliminate complex routing and intent detection
- **More Natural Conversations**: LLM handles nuanced user inputs better than scripts
- **Easier Maintenance**: Single prompt to update instead of multiple helper functions
- **Better User Experience**: More flexible and understanding responses
- **Faster Development**: Focus on domain expertise instead of conversation engineering

This approach leverages the natural conversation capabilities of modern LLMs instead of over-engineering with traditional scripted approaches.

## 📚 LESSONS LEARNED: Critical Agent Design Discoveries

### **🚨 Major Mistakes We Made (And How to Avoid Them)**

#### **❌ MISTAKE #1: Over-Engineering Intent Detection**

**What We Did Wrong:**
```python
# ❌ WRONG: Complex intent analysis
def _analyze_user_intent(user_message, questions, state):
    if any(keyword in user_lower for keyword in ["estado", "progreso"]):
        return {"intent": "status_check", "type": "progress"}
    elif any(keyword in user_lower for keyword in ["siguiente", "próxima"]):
        return {"intent": "next_question", "type": "navigation"}
    # ... 50+ lines of scripted logic
```

**Why This Was Wrong:**
- LLMs naturally understand user intent from context
- Rigid keyword matching misses nuanced user expressions
- Creates unnecessary complexity and maintenance burden
- Forces unnatural conversation patterns

**✅ CORRECT APPROACH:**
```python
# Let LLM handle intent naturally in comprehensive prompt (actual backend_gen code)
prompt = f"""Eres un asistente experto en auditorías de seguridad según el estándar NES.

ESTADO ACTUAL DEL CUESTIONARIO:
{questions_status}

INSTRUCCIONES:
1. SIEMPRE responde en español, tono conversacional y profesional
2. Si es primer saludo: Da bienvenida y muestra primera pregunta pendiente  
3. Si usuario responde a pregunta: Evalúa completitud contra requisitos NES
4. Si respuesta completa: Di que la guardarás y muestra siguiente pregunta
5. Si respuesta incompleta: Pide específicamente qué falta según NES

MENSAJE DEL USUARIO: {latest_user_message}

Analiza el mensaje y responde apropiadamente."""
```

**🎯 LESSON**: Modern LLMs excel at intent understanding. Don't script what they can reason.

#### **❌ MISTAKE #2: Tool Classes for Simple Logic**

**What We Did Wrong:**
```python
# ❌ WRONG: Tool class for domain knowledge
class AnswerEnhancementTool:
    NES_EXPERTISE = {"backup": {"requirements": [...]}}
    
    @staticmethod
    def enhance_answer(question, answer):
        # Just structured data comparison
        return {"missing": [...], "suggestions": [...]}
```

**Why This Was Wrong:**
- Tools should perform actions, not replace LLM reasoning
- Domain knowledge belongs in prompts where LLM can use it flexibly
- Creates false abstraction for simple data structures

**✅ CORRECT APPROACH:**
```python
# Embed expertise directly in prompt (actual backend_gen implementation)
NES_EXPERTISE = """
- Copias de seguridad: Requiere tipo de sistema, frecuencia, verificación, ubicación (local/remota), retención, plan de recuperación
- Control de acceso: Autenticación implementada, políticas de contraseñas, MFA, gestión de privilegios, revisiones periódicas, logs
- Monitoreo: Herramientas de red, sistemas de detección, análisis de logs, procedimientos de respuesta, escalación, informes
- Continuidad: Plan documentado, procedimientos de recuperación, RTO definido, pruebas regulares, documentación actualizada
"""

prompt = f"""Eres un asistente experto en auditorías de seguridad según el estándar NES.

CONOCIMIENTO NES PARA EVALUAR RESPUESTAS:
{NES_EXPERTISE}

Evalúa esta respuesta del usuario: {user_answer}
Si falta información según los requisitos NES, pide detalles específicos en español."""
```

**🎯 LESSON**: Tools are for operations (save/load), not for domain logic that LLMs can reason about.

#### **❌ MISTAKE #3: Complex Conversation Routing**

**What We Did Wrong:**
```python
# ❌ WRONG: Multiple response generators
def _generate_spanish_response(llm, context, questions, state, user_message):
    intent = context["intent"]
    if intent == "status_check":
        return _generate_progress_response(questions)
    elif intent == "next_question":
        return _generate_next_question_response(questions, state)
    elif intent == "answer_question":
        return _generate_answer_enhancement_response(...)
    # ... complex routing logic
```

**Why This Was Wrong:**
- Creates rigid conversation paths
- Prevents natural topic transitions
- Requires maintaining multiple response generators
- LLM can handle all scenarios in single comprehensive prompt

**✅ CORRECT APPROACH:**
```python
# Single prompt handles all scenarios (actual backend_gen implementation)
prompt = f"""Eres un asistente experto en auditorías de seguridad según el estándar NES (Esquema Nacional de Seguridad) de España.

ESTADO ACTUAL DEL CUESTIONARIO:
{questions_status}

CONOCIMIENTO NES PARA EVALUAR RESPUESTAS:
- Copias de seguridad: Requiere tipo de sistema, frecuencia, verificación, ubicación (local/remota), retención, plan de recuperación
- Control de acceso: Autenticación implementada, políticas de contraseñas, MFA, gestión de privilegios, revisiones periódicas, logs

INSTRUCCIONES:
1. SIEMPRE responde en español, tono conversacional y profesional
2. Si es primer saludo: Da bienvenida y muestra primera pregunta pendiente  
3. Si usuario responde a pregunta: Evalúa completitud contra requisitos NES arriba
4. Si respuesta completa: Di que la guardarás y muestra siguiente pregunta
5. Si respuesta incompleta: Pide específicamente qué falta según NES
6. Si pide progreso: Resumen desde estado actual arriba

MENSAJE DEL USUARIO: {latest_user_message}

Analiza el mensaje y responde apropiadamente según los requisitos NES."""
```

**🎯 LESSON**: One intelligent prompt > multiple specialized functions.

### **✅ KEY ARCHITECTURAL DISCOVERIES**

#### **🔍 DISCOVERY #1: LLMs as Natural Conversation Managers**

**Before**: Scripted conversation flows with explicit state tracking
```python
state["current_intent"] = "answer_question"
state["conversation_stage"] = "collecting_details"
state["last_question_type"] = "backup_procedures"
```

**After**: Let LLM track conversation context naturally (backend_gen approach)
```python
# Simple state - LLM manages conversation flow from messages[] and context
class OverallState(TypedDict):
    messages: Annotated[list, add_messages]  # LLM reads conversation history
    document_path: str                       # Current audit questionnaire
    questions_status: Dict[str, str]         # Data state only
    # No conversation flow state needed - LLM handles this
```

**Impact**: Eliminated 60% of state management code.

#### **🔍 DISCOVERY #2: Embedded Expertise > Tool Abstraction**

**Before**: Domain knowledge in separate tool classes
```python
class SecurityExpertise:
    def get_backup_requirements(self): return [...]
    def validate_access_control(self): return [...]
    def assess_monitoring(self): return [...]
```

**After**: Knowledge directly in prompts where LLM can reason (backend_gen approach)
```python
# Embedded in single comprehensive prompt - actual NES expertise
NES_EXPERTISE = """
- Copias de seguridad: Requiere tipo de sistema, frecuencia, verificación, ubicación (local/remota), retención, plan de recuperación
- Control de acceso: Autenticación implementada, políticas de contraseñas, MFA, gestión de privilegios, revisiones periódicas, logs
- Monitoreo: Herramientas de red, sistemas de detección, análisis de logs, procedimientos de respuesta, escalación, informes
"""
# LLM uses this knowledge flexibly based on user input context
```

**Impact**: More flexible application of domain knowledge.

#### **🔍 DISCOVERY #3: Configuration-Driven Testing**

**Before**: Hardcoded model names in tests
```python
config = RunnableConfig(configurable={
    "answer_model": "gemini-1.5-flash-latest",  # Hardcoded
})
```

**After**: Use Configuration class defaults
```python
default_config = Configuration()
config = RunnableConfig(configurable={
    "answer_model": default_config.answer_model,  # Dynamic
})
```

**Impact**: Tests automatically use latest configuration defaults.

### **📈 MEASURABLE IMPROVEMENTS**

#### **Code Metrics:**
- **Lines of Code**: 350+ → 135 (61% reduction)
- **Functions**: 15+ → 4 (73% reduction)
- **Complexity**: High → Low (single prompt vs. multiple paths)

#### **User Experience:**
- **Conversation Flow**: Rigid → Natural
- **Response Flexibility**: Limited → Adaptive
- **Error Handling**: Scripted → Intelligent

#### **Developer Experience:**
- **Maintenance**: Update multiple functions → Update single prompt
- **Testing**: Mock complex interactions → Test real conversations
- **Debugging**: Track complex state → Readable conversation history

### **🎯 IMPLEMENTATION PRINCIPLES LEARNED**

1. **Trust LLM Intelligence**: Modern LLMs handle conversation nuances better than scripts
2. **Tools for Actions**: Use tools for file operations, API calls, persistence - not logic
3. **Prompts for Knowledge**: Embed domain expertise where LLM can reason flexibly
4. **Configuration Standards**: Always use Configuration class defaults, never hardcode
5. **Minimal State**: Only track what LLM can't remember across conversation turns
6. **Natural Flow**: Let conversations evolve organically based on context

### **⚠️ ANTI-PATTERNS TO AVOID**

1. **Intent Detection Functions**: LLM understands intent naturally
2. **Response Route Switching**: Single comprehensive prompt handles all cases
3. **Tool Classes for Logic**: Tools should perform operations, not reasoning
4. **Complex State Tracking**: LLM remembers conversation context
5. **Hardcoded Configurations**: Use Configuration class for consistency

### **🚀 FUTURE APPLICATIONS**

These lessons apply to any conversational agent:
- **Customer Support**: Natural problem resolution vs. scripted decision trees
- **Educational Tutors**: Adaptive teaching vs. rigid lesson plans  
- **Medical Assistants**: Flexible consultations vs. checkbox interviews
- **Legal Advisors**: Contextual guidance vs. form-based interactions

The shift from script-based to conversation-native design represents a fundamental evolution in how we build intelligent agents.

## Using Gemini CLI for Large Codebase Analysis

When analyzing large codebases or multiple files that might exceed context limits, use the Gemini CLI with its massive context window. Use `gemini -p` to leverage Google Gemini's large context capacity.

### File and Directory Inclusion Syntax

Use the `@` syntax to include files and directories in your Gemini prompts. The paths should be relative to WHERE you run the gemini command:

#### Examples:

**Single file analysis:**
```bash
gemini -p "@src/main.py Explain this file's purpose and structure"
```

**Multiple files:**
```bash
gemini -p "@package.json @src/index.js Analyze the dependencies used in the code"
```

**Entire directory:**
```bash
gemini -p "@src/ Summarize the architecture of this codebase"
```

**Multiple directories:**
```bash
gemini -p "@src/ @tests/ Analyze test coverage for the source code"
```

**Current directory and subdirectories:**
```bash
gemini -p "@./ Give me an overview of this entire project"

# Or use --all_files flag:
gemini --all_files -p "Analyze the project structure and dependencies"
```

### Implementation Verification Examples

**Check if a feature is implemented:**
```bash
gemini -p "@src/ @lib/ Has dark mode been implemented in this codebase? Show me the relevant files and functions"
```

**Verify authentication implementation:**
```bash
gemini -p "@src/ @middleware/ Is JWT authentication implemented? List all auth-related endpoints and middleware"
```

**Check for specific patterns:**
```bash
gemini -p "@src/ Are there any React hooks that handle WebSocket connections? List them with file paths"
```

**Verify error handling:**
```bash
gemini -p "@src/ @api/ Is proper error handling implemented for all API endpoints? Show examples of try-catch blocks"
```

**Check for rate limiting:**
```bash
gemini -p "@backend/ @middleware/ Is rate limiting implemented for the API? Show the implementation details"
```

**Verify caching strategy:**
```bash
gemini -p "@src/ @lib/ @services/ Is Redis caching implemented? List all cache-related functions and their usage"
```

**Check for specific security measures:**
```bash
gemini -p "@src/ @api/ Are SQL injection protections implemented? Show how user inputs are sanitized"
```

**Verify test coverage for features:**
```bash
gemini -p "@src/payment/ @tests/ Is the payment processing module fully tested? List all test cases"
```

### When to Use Gemini CLI

Use `gemini -p` when:
- Analyzing entire codebases or large directories
- Comparing multiple large files
- Need to understand project-wide patterns or architecture
- Current context window is insufficient for the task
- Working with files totaling more than 100KB
- Verifying if specific features, patterns, or security measures are implemented
- Checking for the presence of certain coding patterns across the entire codebase

### Important Notes

- Paths in `@` syntax are relative to your current working directory when invoking gemini
- The CLI will include file contents directly in the context
- No need for --yolo flag for read-only analysis
- Gemini's context window can handle entire codebases that would overflow Claude's context
- When checking implementations, be specific about what you're looking for to get accurate results

## Autonomous Development Instructions

The following sections contain the comprehensive instructions for autonomous development of LangGraph applications based on planning_old.md and tips.md.

### ENHANCED LANGGRAPH PROJECT CONFIGURATION & CLI INTEGRATION

#### 0. ITERATIVE BUSINESS CASE EXECUTION PROTOCOL

##### Master Execution Loop

1. **Business Case Generation Phase**
   - Think creatively about this agentic business case
   - create examples for the llms, think about what can fail, extreme cases, etc.
   - Document the business case rationale and expected challenges
   - Create `/tasks/business_case.md` with detailed specification

2. **Implementation Phase**
   - Follow standard execution phases (0-3) for the business case
   - Apply lessons learned from `/docs/tips.md` proactively
   - Document new patterns and solutions discovered

3. **Error Learning Phase**
   - Every time an error is encountered and fixed, update `/docs/tips.md`
   - Follow the Enhanced Tips Format
   - Review existing tips before writing new code or tests

4. **Knowledge Accumulation Phase**
   - After creating the solution, update `/docs/patterns_learned.md`
   - Document successful architectural decisions
   - Note business case complexity vs implementation patterns

For  each phase write a file in /tasks indicating the steps that have to be done and the instructions for each specific phase, and then follow what that file says. Include all the examples of code or tips for each phase in the file.

**NEVER use mock APIs, never, period.**

USE CASE -----------------------------

the use case to implement is a conversational flow where you can ask for the next question and the agents
  help you interactively.  for helping the user when working in an audit, there should be a .md file with the qeustions to fill, and the agents will help the user to fill the answers, they don´t generate answers, the answers should be answered by the user, the agents can help the user to know what questions are still in the file without answer, or suggest how to write down the answers in a more formal way, for example if the question is how the compnay does backups and the user answer with a NAS, ask details to the user and at the end provide the user a better answer that "just a NAS". 
The agents should be experts in security audits in the NES national security estandard in Spain, and the solution should ask the quesitons and fill the document in spanish.
the agents have to work with the .md file and help the user to answer the questions.
create a .md file in the backend_gen folder with some example questions and use this path for the solution, dont need to ask the user , you have the path, read the document at the beginning of the solution and pass the questions to the agent, so it can start asking questions to the user. no need to use "keywords" like "siguiente pregunta" with the communication with the client, just use the llm conversation

make the lesser number of agents required.
use few agents, only the needed, better one agent with more tools than many agents.
there will be an agent coordinator that will help the user to make work the use case, if it is possible only use this agent to make everything.


#### 1. EXECUTION PHASES & SUCCESS CRITERIA

##### Phase -1: Business Case Generation
**Objective**: enhance the business case for current use case
**Success Criteria**:
- Business case documented in `/tasks/business_case.md`
- Case fits variety matrix requirements
- Clear agent roles and responsibilities defined
- Expected technical challenges identified
- Success metrics established

##### Phase 0: Workspace Initialization
**Objective**: Clean slate preparation with tips consultation. **This phase and all subsequent phases proceed automatically, without user confirmation.**
```bash
# 1. Hard reset tasks directory
rm -rf /tasks
mkdir -p /tasks/artifacts

# 2. Hard reset backend_gen directory  
rm -rf /backend_gen

# 3. Copy backend to backend_gen
cp -r /backend /backend_gen

# 4. Verify structure
ls -la /backend_gen/src/agent/

# 5. Install dependencies
cd /backend_gen && pip install -e .
```

##### Phase 1: Architecture Planning & Specification
**Objective**: Complete project specification before any implementation, incorporating lessons learned.

**Critical Tips for Node Implementation**:
- **TIP #012**: Use Configuration.from_runnable_config() instead of hardcoded models
- **TIP #008**: LangGraph Agent Function Signature must use RunnableConfig
- **TIP #010**: State management with None values using safe patterns
- **TIP #006**: Use absolute imports in graph.py to avoid server startup failures

**MANDATORY LLM Call Pattern (Using Configuration - TIP #012)**:
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableConfig
import os
from agent.state import OverallState
from agent.configuration import Configuration

def audit_coordinator_agent(state: OverallState, config: RunnableConfig) -> dict:
    # ✅ CRITICAL: Get configuration from RunnableConfig (TIP #012)
    configurable = Configuration.from_runnable_config(config)
    
    # ✅ CRITICAL: Use configured model, not hardcoded
    llm = ChatGoogleGenerativeAI(
        model=configurable.reflection_model,  # Use configured model!
        temperature=0.1,  # For consistent responses
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    # ✅ CRITICAL: Handle LangChain message objects properly (TIP #013)
    messages = state.get("messages", [])
    latest_user_message = "Hola"
    for msg in messages:
        if hasattr(msg, 'type') and msg.type == "human":
            latest_user_message = msg.content
        elif isinstance(msg, dict) and msg.get("role") == "user":
            latest_user_message = msg.get("content", "Hola")
    
    # Format prompt using state and domain expertise
    questions_status, questions_list = get_audit_status()
    prompt = f"""Eres un asistente experto en auditorías de seguridad según el estándar NES.

ESTADO ACTUAL: {questions_status}
MENSAJE DEL USUARIO: {latest_user_message}

Responde apropiadamente según los requisitos NES."""
    
    result = llm.invoke(prompt)
    return {"messages": state.get("messages", []) + [{"role": "assistant", "content": result.content}]}
```

**CRITICAL: Use ABSOLUTE imports only (relative imports will fail in langgraph dev)**:
```python
# ❌ WRONG - Relative imports (will cause server startup failure)
# from .nodes.audit_coordinator import audit_coordinator_agent

# ✅ CORRECT - Absolute imports (required for langgraph dev server)
from agent.nodes.audit_coordinator import audit_coordinator_agent
```

##### Phase 2: Implementation & Code Generation
**Objective**: Generate all required code components using accumulated knowledge.

**Mandatory Files Checklist**:
- [ ] `state.py` - OverallState TypedDict
- [ ] `tools_and_schemas.py` - Pydantic models/tools
- [ ] `nodes/` directory with individual node files
- [ ] `graph.py` - Complete graph assembly
- [ ] `langgraph.json` - Deployment configuration
- [ ] `tests/` directory with comprehensive unit tests

##### Phase 3: Testing & Validation
**Objective**: Comprehensive testing and error resolution with knowledge capture.

###### Phase 3.1: Unit Testing & Component Validation
**Success Criteria**:
- All unit tests pass with real LLM calls, file operations, and computations
- Individual agent functions work correctly with proper signatures
- Pydantic models handle data validation and conversion properly
- **LLM conversations logged** for debugging and verification
- Error handling mechanisms tested with fallback data

###### Phase 3.2: Graph Compilation & Import Validation  
**Success Criteria**:
- Graph compiles and imports successfully without errors
- All node imports execute without circular dependencies
- State schema is valid TypedDict structure
- **Pre-server validation** prevents import errors at runtime
- Package installation completes successfully

###### Phase 3.3: LangGraph Server Testing & Real Execution
**CRITICAL LESSONS LEARNED**: Import errors only surface when server actually runs, not during unit tests.

**MANDATORY PRE-SERVER CHECKS**:
```bash
# 1. CRITICAL: Fix relative imports in graph.py BEFORE server testing
# 2. CRITICAL: Fix fake LLM imports in utils.py
# 3. CRITICAL: Test graph loading BEFORE server
cd /backend_gen
python -c "from agent.graph import graph; print('Graph loads:', type(graph))"
# 4. CRITICAL: Install package in editable mode
pip install -e .
```

**Success Criteria**:
- `langgraph dev` server starts without errors on port 2024
- Server logs show no ImportError, ModuleNotFoundError, or relative import issues
- **Real LLM execution** processes requests with actual API calls (not mocks)
- Graph execution transitions through all states successfully

### LangGraph Development Tips & Error Solutions

#### Tips Consultation Protocol
**MANDATORY**: Before writing any code or tests, consult this file for:
1. **Pre-Code Review**: Check tips related to the component being implemented
2. **Error Pattern Matching**: When an error occurs, first check if it's documented
3. **Solution Application**: Apply documented solutions before creating new ones
4. **Pattern Recognition**: Identify if the current business case matches previous patterns

#### Critical Development Tips

##### TIP #001: Project Initialization Template
**Category**: Architecture | **Severity**: Critical

**Solution Implementation**:
```bash
# Always start with clean reset
rm -rf tasks
mkdir -p tasks/artifacts
rm -rf backend_gen
cp -r backend backend_gen
cd backend_gen && pip install -e .
```

##### TIP #006: Critical LangGraph Server Import Errors and Solutions
**Category**: Development | **Severity**: Critical

**Problem Description**: Multiple specific import errors that only surface when `langgraph dev` server actually runs:
1. **Relative Import Error**: `ImportError: attempted relative import with no known parent package`
2. **Fake Model Import Errors**: Cannot import FakeListChatModel, FakeChatModel
3. **Module Path Errors**: `No module named 'langchain_core.language_models.llm'`

**Solution Implementation**:

Fix Relative Imports in graph.py:
```python
# ❌ WRONG - Relative imports (will fail in server)
from .nodes.audit_coordinator import audit_coordinator_agent

# ✅ CORRECT - Absolute imports (works in server)
from agent.nodes.audit_coordinator import audit_coordinator_agent
```

Fix Fake LLM Imports:
```python
def get_llm():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # Try real LLM first
    if os.getenv("GEMINI_API_KEY"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0,
            api_key=os.getenv("GEMINI_API_KEY")
        )
    
    # Fallback to working fake model
    try:
        from langchain_core.language_models.fake import FakeListLLM
        return FakeListLLM(responses=["Mock response"])
    except ImportError:
        class SimpleFakeLLM:
            def invoke(self, prompt):
                class Response:
                    content = "Mock LLM response for testing"
                return Response()
        return SimpleFakeLLM()
```

##### TIP #012: Proper Configuration Usage in LangGraph Nodes
**Category**: Development | **Severity**: High

**Problem Description**: Nodes that hardcode LLM model names instead of using the configuration system create inflexible applications.

**Solution Implementation**:
```python
# ❌ WRONG - Hardcoded model
def my_agent_node(state: OverallState, config: Dict[str, Any]) -> Dict[str, Any]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",  # HARDCODED - BAD!
        temperature=0.1,
        api_key=os.getenv("GEMINI_API_KEY"),
    )

# ✅ CORRECT - Use configuration
from agent.configuration import Configuration

def my_agent_node(state: OverallState, config: RunnableConfig) -> Dict[str, Any]:
    configurable = Configuration.from_runnable_config(config)
    llm = ChatGoogleGenerativeAI(
        model=configurable.answer_model,  # Use configured model
        temperature=0.1,
        max_retries=2,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
```

**Configuration Fields Available**:
- `query_generator_model`: Default "gemini-2.0-flash"
- `reflection_model`: Default "gemini-2.5-flash-preview-04-17" 
- `answer_model`: Default "gemini-1.5-flash-latest"
- `number_of_initial_queries`: Default 3
- `max_research_loops`: Default 2

##### TIP #005: The Critical Gap Between Unit Tests and Real LLM Endpoint Testing
**Category**: Testing | **Severity**: Critical

**Problem Description**: Mock tests can pass while real API endpoints fail catastrophically. Unit tests use mocked dependencies, so they pass even when import statements are incorrect for the actual runtime environment.

**Solution Implementation**:
```bash
# STEP 1: Test graph loading in server context BEFORE unit tests
cd /backend_gen
python -c "from agent.graph import graph; print('✅ Graph loads successfully:', type(graph))"

# STEP 2: Start server and check logs for import errors
nohup langgraph dev > langgraph.log 2>&1 &
sleep 10

# CRITICAL: Check for import errors in server logs
if grep -q "ImportError\|ModuleNotFoundError" langgraph.log; then
    echo "❌ CRITICAL: Server has import errors"
    grep -A3 -B3 "Error" langgraph.log
    exit 1
fi
```

**Prevention Strategy**: Always test in this order:
1. **Graph import test** in server context first
2. **Server startup** with log monitoring for import errors  
3. **Real endpoint calls** with actual data payloads
4. **LLM response validation** in final state
5. **Only then** run unit tests as confirmation

##### Additional Key Tips

**TIP #008**: LangGraph Agent Function Signature Inconsistencies - Some agents require `config` parameter while others don't.

**TIP #009**: Pydantic Model Mutability - Use `.model_dump()` for dictionary conversion in Pydantic v2.

**TIP #010**: State management with None values - Always check for None before list operations: `existing_errors = state.get("errors") or []`

**TIP #011**: LangGraph Server Port Conflicts - Use port cleanup and dynamic port selection for testing.

##### TIP #013: LangChain Message Object Handling in State
**Category**: Development | **Severity**: High  

**Problem Description**: In LangGraph runtime, messages in state are converted to LangChain message objects (HumanMessage, AIMessage) which don't have dictionary methods like `.get()`.

**Error Example**: `'HumanMessage' object has no attribute 'get'`

**Solution Implementation**:
```python
# ❌ WRONG - Treating messages as dictionaries
user_messages = [msg for msg in state.get("messages", []) if msg.get("role") == "user"]
latest_user_message = user_messages[-1]["content"] if user_messages else "Hola"

# ✅ CORRECT - Handle both dict and LangChain message objects  
messages = state.get("messages", [])
user_messages = []
for msg in messages:
    if hasattr(msg, 'type') and msg.type == "human":
        user_messages.append(msg)
    elif isinstance(msg, dict) and msg.get("role") == "user":
        user_messages.append(msg)

if user_messages:
    latest_msg = user_messages[-1]
    if hasattr(latest_msg, 'content'):
        latest_user_message = latest_msg.content
    else:
        latest_user_message = latest_msg.get("content", "Hola")
else:
    latest_user_message = "Hola"
```

**Key Points**:
- Messages start as dicts but become LangChain objects during execution
- Always check for both formats using `hasattr()` and `isinstance()`
- Use `.content` attribute for LangChain objects, `.get("content")` for dicts
- Human messages have `type == "human"`, AI messages have `type == "ai"`

#### Current Development Status

