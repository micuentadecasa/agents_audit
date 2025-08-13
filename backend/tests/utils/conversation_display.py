"""
DMMAS Conversation Display Utilities
Implements mandatory conversation display requirements from guidelines

CRITICAL: NO TRUNCATION POLICY
- NEVER truncate agent responses with [:100] or ...
- ALWAYS display complete tool outputs
- Show full error messages and stack traces

This module provides standardized display functions for:
1. Tool interactions with full input/output display
2. Agent conversations with complete response display
3. Multi-agent workflows with routing context display
4. Error scenarios with complete error message display
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union


class ConversationDisplayManager:
    """
    Centralized conversation display manager for DMMAS testing
    Implements all mandatory display requirements from guidelines
    """
    
    def __init__(self, test_name: str = "DMMAS_Test", verbose: bool = True):
        self.test_name = test_name
        self.verbose = verbose
        self.conversation_turns = 0
        self.total_interactions = 0
        self.start_time = time.time()
        
    def display_test_header(self, test_description: str):
        """Display standardized test header"""
        if not self.verbose:
            return
            
        print(f"\n{'='*100}")
        print(f"🧪 {self.test_name.upper()}")
        print(f"📋 {test_description}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*100}")
    
    def display_conversation_turn(self, turn_num: int, user_msg: str, 
                                agent_response: str, agent_name: str = "AGENT",
                                context: Optional[Dict] = None):
        """
        MANDATORY: Display full conversation turn with NO TRUNCATION
        Implements guideline requirements for complete response display
        """
        if not self.verbose:
            return
            
        self.conversation_turns = turn_num
        
        print(f"\n{'='*80}")
        print(f"🔄 CONVERSATION TURN {turn_num}")
        print(f"🤖 AGENT: {agent_name}")
        print(f"{'='*80}")
        
        # Display user message
        print(f"👤 USER MESSAGE:")
        print(f"   {user_msg}")
        
        # Display context if provided
        if context:
            print(f"\n📋 CONTEXT:")
            for key, value in context.items():
                print(f"   {key}: {value}")
        
        # Display agent response - COMPLETE, NO TRUNCATION
        print(f"\n🤖 {agent_name} FULL RESPONSE:")
        print(f"{'-'*80}")
        
        # CRITICAL: Display complete response without any truncation
        print(agent_response)
        
        print(f"{'-'*80}")
        
        # Display response metrics
        response_lines = agent_response.split('\n')
        print(f"📊 RESPONSE METRICS:")
        print(f"   📏 Character Count: {len(agent_response)}")
        print(f"   📝 Line Count: {len(response_lines)}")
        print(f"   ⏱️  Response Time: {time.time() - self.start_time:.2f}s")
        
    def display_tool_interaction(self, tool_name: str, tool_input: Dict[str, Any],
                               tool_output: Any, execution_time: float = 0.0,
                               error: Optional[str] = None):
        """
        MANDATORY: Display complete tool interaction
        Shows full input/output with NO TRUNCATION
        """
        if not self.verbose:
            return
            
        self.total_interactions += 1
        
        print(f"\n{'='*60}")
        print(f"🔧 TOOL INTERACTION #{self.total_interactions}")
        print(f"🛠️  Tool: {tool_name}")
        print(f"{'='*60}")
        
        # Display tool input - COMPLETE
        print(f"📥 TOOL INPUT:")
        for key, value in tool_input.items():
            print(f"   {key}: {value}")
        
        # Display execution time
        if execution_time > 0:
            print(f"\n⏱️  Execution Time: {execution_time:.3f}s")
        
        # Display tool output or error - COMPLETE, NO TRUNCATION
        if error:
            print(f"\n❌ TOOL ERROR:")
            print(f"{'-'*40}")
            print(error)  # COMPLETE error message
            print(f"{'-'*40}")
        else:
            print(f"\n📤 TOOL OUTPUT:")
            print(f"{'-'*40}")
            
            # CRITICAL: Display complete output without truncation
            if isinstance(tool_output, (dict, list)):
                import json
                print(json.dumps(tool_output, indent=2))
            else:
                print(str(tool_output))
                
            print(f"{'-'*40}")
            
        # Display output metrics
        output_str = str(tool_output) if not error else error
        print(f"📊 OUTPUT METRICS:")
        print(f"   📏 Character Count: {len(output_str)}")
        print(f"   📝 Type: {type(tool_output).__name__}")
        
    def display_agent_conversation(self, agent_name: str, user_message: str,
                                 agent_response: str, context: Optional[Dict] = None,
                                 state_changes: Optional[Dict] = None):
        """
        MANDATORY: Display complete agent conversation
        Implements NO TRUNCATION policy for agent responses
        """
        if not self.verbose:
            return
            
        print(f"\n{'='*70}")
        print(f"🤖 AGENT CONVERSATION")
        print(f"👨‍💼 Agent: {agent_name}")
        print(f"{'='*70}")
        
        # User message
        print(f"👤 USER:")
        print(f"   {user_message}")
        
        # Context display
        if context:
            print(f"\n📋 CONVERSATION CONTEXT:")
            for key, value in context.items():
                print(f"   {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
        
        # Agent response - COMPLETE, NO TRUNCATION
        print(f"\n🤖 {agent_name.upper()} RESPONSE:")
        print(f"{'-'*70}")
        
        # CRITICAL: Always display complete response
        print(agent_response)
        
        print(f"{'-'*70}")
        
        # State changes
        if state_changes:
            print(f"\n🔄 STATE CHANGES:")
            for key, value in state_changes.items():
                print(f"   {key}: {value}")
                
        # Response analysis
        print(f"\n📊 RESPONSE ANALYSIS:")
        print(f"   📏 Response Length: {len(agent_response)} characters")
        print(f"   📝 Response Lines: {len(agent_response.split('\\n'))} lines")
        
        # Check for key indicators
        indicators = {
            "🎯 Actions": ["create", "update", "generate", "analyze", "schedule"],
            "🔗 References": ["project", "task", "document", "team", "client"],
            "⚠️  Concerns": ["error", "issue", "problem", "failure", "warning"]
        }
        
        response_lower = agent_response.lower()
        for category, keywords in indicators.items():
            found = [kw for kw in keywords if kw in response_lower]
            if found:
                print(f"   {category}: {', '.join(found)}")
    
    def display_multi_agent_flow(self, workflow_name: str, agent_sequence: List[str],
                               routing_decisions: List[Dict], final_result: Any):
        """
        MANDATORY: Display complete multi-agent workflow
        Shows routing decisions and complete conversation flow
        """
        if not self.verbose:
            return
            
        print(f"\n{'='*90}")
        print(f"🔄 MULTI-AGENT WORKFLOW")
        print(f"📋 Workflow: {workflow_name}")
        print(f"🔗 Agent Sequence: {' → '.join(agent_sequence)}")
        print(f"{'='*90}")
        
        # Display routing decisions
        print(f"🧭 ROUTING DECISIONS:")
        for i, decision in enumerate(routing_decisions, 1):
            print(f"   {i}. {decision.get('from_agent', 'unknown')} → {decision.get('to_agent', 'unknown')}")
            print(f"      Reason: {decision.get('routing_reason', 'not specified')}")
            if 'context' in decision:
                print(f"      Context: {decision['context']}")
        
        # Display final result - COMPLETE, NO TRUNCATION
        print(f"\n📤 FINAL WORKFLOW RESULT:")
        print(f"{'-'*90}")
        
        # CRITICAL: Display complete final result
        if isinstance(final_result, dict):
            import json
            print(json.dumps(final_result, indent=2))
        else:
            print(str(final_result))
            
        print(f"{'-'*90}")
        
        # Workflow metrics
        print(f"\n📊 WORKFLOW METRICS:")
        print(f"   🔢 Total Agents: {len(agent_sequence)}")
        print(f"   🔄 Routing Steps: {len(routing_decisions)}")
        print(f"   ⏱️  Total Time: {time.time() - self.start_time:.2f}s")
        
    def display_error_scenario(self, error_type: str, error_message: str,
                             stack_trace: Optional[str] = None,
                             recovery_action: Optional[str] = None):
        """
        MANDATORY: Display complete error information
        Shows full error messages and stack traces - NO TRUNCATION
        """
        if not self.verbose:
            return
            
        print(f"\n{'='*80}")
        print(f"❌ ERROR SCENARIO")
        print(f"🏷️  Type: {error_type}")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*80}")
        
        # Display complete error message - NO TRUNCATION
        print(f"📋 ERROR MESSAGE:")
        print(f"{'-'*50}")
        print(error_message)  # COMPLETE error message
        print(f"{'-'*50}")
        
        # Display stack trace if provided - COMPLETE
        if stack_trace:
            print(f"\n📚 STACK TRACE:")
            print(f"{'-'*50}")
            print(stack_trace)  # COMPLETE stack trace
            print(f"{'-'*50}")
        
        # Display recovery action if provided
        if recovery_action:
            print(f"\n🔧 RECOVERY ACTION:")
            print(f"   {recovery_action}")
            
        # Error metrics
        print(f"\n📊 ERROR METRICS:")
        print(f"   📏 Message Length: {len(error_message)} characters")
        if stack_trace:
            print(f"   📚 Stack Trace Length: {len(stack_trace)} characters")
    
    def display_performance_metrics(self, operation_name: str, execution_time: float,
                                  memory_usage: Optional[float] = None,
                                  token_usage: Optional[Dict] = None):
        """Display detailed performance metrics"""
        if not self.verbose:
            return
            
        print(f"\n{'='*60}")
        print(f"📊 PERFORMANCE METRICS")
        print(f"🎯 Operation: {operation_name}")
        print(f"{'='*60}")
        
        print(f"⏱️  Execution Time: {execution_time:.3f}s")
        
        if memory_usage:
            print(f"💾 Memory Usage: {memory_usage:.2f} MB")
            
        if token_usage:
            print(f"🎫 Token Usage:")
            for key, value in token_usage.items():
                print(f"   {key}: {value}")
                
        # Performance assessment
        if execution_time < 5.0:
            print(f"✅ Performance: EXCELLENT (< 5s)")
        elif execution_time < 15.0:
            print(f"⚠️  Performance: ACCEPTABLE (< 15s)")
        else:
            print(f"❌ Performance: SLOW (> 15s)")
    
    def display_test_summary(self, total_tests: int, passed: int, failed: int,
                           total_time: Optional[float] = None):
        """Display comprehensive test summary"""
        if not self.verbose:
            return
            
        print(f"\n{'='*80}")
        print(f"📋 TEST SUMMARY - {self.test_name}")
        print(f"{'='*80}")
        
        print(f"🎯 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Success Rate: {(passed/total_tests*100):.1f}%")
        
        if total_time:
            print(f"⏱️  Total Time: {total_time:.2f}s")
            print(f"⚡ Average Time per Test: {(total_time/total_tests):.2f}s")
            
        print(f"💬 Conversation Turns: {self.conversation_turns}")
        print(f"🔧 Tool Interactions: {self.total_interactions}")
        
        print(f"\n🏁 Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")


# Convenience functions for direct use
def display_conversation_turn(turn_num: int, user_msg: str, agent_response: str, 
                            agent_name: str = "AGENT", context: Optional[Dict] = None):
    """Direct function for conversation turn display"""
    display_manager = ConversationDisplayManager()
    display_manager.display_conversation_turn(turn_num, user_msg, agent_response, agent_name, context)


def display_tool_interaction(tool_name: str, tool_input: Dict[str, Any], 
                           tool_output: Any, execution_time: float = 0.0,
                           error: Optional[str] = None):
    """Direct function for tool interaction display"""
    display_manager = ConversationDisplayManager()
    display_manager.display_tool_interaction(tool_name, tool_input, tool_output, execution_time, error)


def display_agent_conversation(agent_name: str, user_message: str, agent_response: str,
                             context: Optional[Dict] = None, state_changes: Optional[Dict] = None):
    """Direct function for agent conversation display"""
    display_manager = ConversationDisplayManager()
    display_manager.display_agent_conversation(agent_name, user_message, agent_response, context, state_changes)


def display_multi_agent_flow(workflow_name: str, agent_sequence: List[str],
                           routing_decisions: List[Dict], final_result: Any):
    """Direct function for multi-agent workflow display"""
    display_manager = ConversationDisplayManager()
    display_manager.display_multi_agent_flow(workflow_name, agent_sequence, routing_decisions, final_result)


def display_error_scenario(error_type: str, error_message: str,
                         stack_trace: Optional[str] = None, recovery_action: Optional[str] = None):
    """Direct function for error scenario display"""
    display_manager = ConversationDisplayManager()
    display_manager.display_error_scenario(error_type, error_message, stack_trace, recovery_action)


# Template functions for standardized display patterns
def create_test_display_manager(test_name: str) -> ConversationDisplayManager:
    """Factory function to create display manager with test name"""
    return ConversationDisplayManager(test_name=test_name, verbose=True)


def display_with_emoji_prefix(message: str, prefix_type: str = "info") -> None:
    """Display message with standardized emoji prefix"""
    prefixes = {
        "user": "👤",
        "agent": "🤖", 
        "tool": "🔧",
        "context": "📋",
        "result": "📊",
        "input": "📥",
        "output": "📤",
        "error": "❌",
        "success": "✅",
        "info": "ℹ️",
        "warning": "⚠️",
        "workflow": "🔄",
        "performance": "⚡",
        "summary": "📋"
    }
    
    emoji = prefixes.get(prefix_type, "ℹ️")
    print(f"{emoji} {message}")


# Constants for consistent formatting
DISPLAY_SEPARATORS = {
    "major": "=" * 80,
    "minor": "-" * 40,
    "section": "=" * 60,
    "subsection": "-" * 30
}

DISPLAY_EMOJIS = {
    "user": "👤",
    "agent": "🤖",
    "tool": "🔧",
    "context": "📋", 
    "result": "📊",
    "input": "📥",
    "output": "📤",
    "error": "❌",
    "success": "✅",
    "workflow": "🔄",
    "performance": "⚡"
}