# CLAUDE.md - LangGraph Agent Generation System

This guide helps Claude Code generate LangGraph agents for ANY use case defined in docs/prd.md.

## System Overview

This is a generic agent generation system that:
- **Reads** the use case from `docs/prd.md`
- **Generates** appropriate agents in `backend_gen/`
- **Uses** `backend/` as a template starting point
- **Follows** three core architectural pillars for consistency

### Project Structure
- `backend/` - Template LangGraph agent (never modify for testing)
- `backend_gen/` - Generated agents for your use case
- `frontend/` - React/Vite interface
- `docs/prd.md` - Defines the current use case to implement
- `docs/planning.md` - Detailed implementation patterns
- `docs/tips.md` - Accumulated lessons and solutions
- `docs/roadmap.md` - Development workflow and phase tracking
- `/tasks/` - Task files for tracking implementation progress

## Development Tracking System

### Phase-Based Development Approach

This system follows a structured 4-phase approach with comprehensive tracking:

**Phase 0: Workspace Initialization**
- Clean slate preparation with dependency reset
- Tips consultation for known patterns
- Environment setup validation

**Phase 1: Architecture Planning & Specification**  
- Analyze PRD and reference previous implementations
- Apply comprehensive action extraction methodology
- Consult `docs/tips.md` for similar business cases

**Phase 1.5: Granular Task File Generation (MANDATORY)**
- Generate individual task files for each agent action
- Create detailed task files for each frontend page
- Generate integration component task files
- Create master coordination and dependency tracking file

**Phase 2: Implementation & Code Generation**
- Follow granular task file specifications exactly
- Update individual task progress after each step
- Apply lessons from `docs/tips.md` 
- Generate components using detailed task guidance

**Phase 3: Testing & Validation (MANDATORY)**
- Unit, integration, and scenario testing
- Real LLM conversation validation
- Error resolution with knowledge capture
- Add new learnings to `docs/tips.md`

## ⚠️ CRITICAL: MANDATORY TESTING REQUIREMENTS

### **ABSOLUTE RULE: NO COMPONENT WITHOUT TESTS**
**If you complete any component without proper testing, expect significant consequences. Testing is not optional - it's mandatory for every tool, agent, and workflow.**

### **API KEY VALIDATION PROTOCOL (MANDATORY)**
**Before ANY development or testing:**
1. **Check API Keys**: Validate OPENROUTER_API_KEY and GEMINI_API_KEY in .env file
2. **If Keys Missing**: STOP IMMEDIATELY and ask user to configure keys
3. **Display Message**: "Missing API key [KEY_NAME]. Please configure [KEY_NAME] in .env file before proceeding."
4. **DO NOT Continue**: Never proceed with development until keys are properly configured
5. **Test First**: Always test API key functionality before implementing features

### **Six Critical Testing Categories (ALL MANDATORY)**

#### 1. Individual Tool Functionality Testing
**REQUIREMENT**: Every @tool function MUST have corresponding unit tests
**PROTOCOL**: Test creation immediately after tool implementation
**VALIDATION**: 
- Input parameter validation and edge cases
- Output format and data integrity
- ChromaDB integration and data persistence
- Error handling for all failure scenarios
- Performance benchmarks for acceptable response times

#### 2. Agent-Specific Behavior Testing
**REQUIREMENT**: Every specialist agent MUST have dedicated test suite
**PROTOCOL**: Test domain expertise, tool integration, conversation quality
**VALIDATION**:
- LLM response quality and domain accuracy
- Tool integration and execution correctness
- Conversation flow and context management
- Error recovery and graceful degradation
- Agent routing accuracy and confidence levels

#### 3. Multi-Agent Routing Testing
**REQUIREMENT**: Test coordinator → specialist transitions with real conversations
**PROTOCOL**: Validate routing decisions, state management, handoffs
**VALIDATION**:
- Routing accuracy based on user intent
- State preservation across agent transitions
- Conversation continuity and context retention
- Performance of routing decision logic
- Error handling during agent handoffs

#### 4. ChromaDB Integration Testing
**REQUIREMENT**: Test data persistence across all tools with real data
**PROTOCOL**: Collection initialization, CRUD operations, concurrent access
**VALIDATION**:
- Collection setup and schema validation
- Data persistence and retrieval accuracy
- Concurrent access patterns and performance
- Error handling for database failures
- Data integrity across tool executions

#### 5. Real Conversation Workflow Testing
**REQUIREMENT**: End-to-end scenario testing with LangWatch and real LLM calls
**PROTOCOL**: Complete user journeys, multi-turn conversations, domain expertise
**VALIDATION**:
- Natural conversation flow and user experience
- Specialist expertise demonstration
- Goal completion and task success rates
- Context retention across long conversations
- Performance under realistic usage patterns

#### 6. Error Handling and Recovery Testing
**REQUIREMENT**: Test API failures, tool failures, edge cases, and recovery paths
**PROTOCOL**: Mock failures, test graceful degradation, validate error messages
**VALIDATION**:
- API quota exhaustion and rate limiting
- Network failures and timeout handling
- Invalid user input and malformed requests
- Tool execution failures and rollback
- User-friendly error messages and guidance

### **MANDATORY TESTING WORKFLOW**

#### **STEP 1: Pre-Implementation Validation**
```bash
# MANDATORY: Check API keys before any development
python -c "import os; print('✅ OPENROUTER_API_KEY:', bool(os.getenv('OPENROUTER_API_KEY'))); print('✅ GEMINI_API_KEY:', bool(os.getenv('GEMINI_API_KEY')))"
```
**IF KEYS MISSING**: STOP and ask user to configure keys

#### **STEP 2: Test-Driven Development**
- **Write tests FIRST** before implementing tools/agents
- **Test with REAL APIs** - never use mocks for LLM calls
- **Validate with REAL data** - use actual ChromaDB collections
- **Test REAL conversations** - use LangWatch scenario framework

### **MANDATORY CONVERSATION DISPLAY IN TESTS**

**CRITICAL REQUIREMENT**: All agent and tool tests MUST display full conversations for debugging and validation

#### **Conversation Display Rules**

1. **User Messages**: Always print with 👤 prefix and clear formatting
2. **Agent Responses**: Always print FULL response with 🤖 prefix (NO truncation)
3. **Tool Inputs/Outputs**: Display parameters and complete results
4. **Context Information**: Show state changes, routing decisions, and handoffs
5. **Multi-turn Conversations**: Display turn numbers and context preservation
6. **Error Scenarios**: Print error messages and recovery actions

#### **Mandatory Display Template for ALL Tests**

```python
def display_conversation_turn(turn_num, user_msg, agent_response, context=None, agent_name="AGENT"):
    """MANDATORY: Use this template in ALL agent tests"""
    print(f"\n{'='*80}")
    print(f"CONVERSATION TURN {turn_num}")
    print(f"{'='*80}")
    
    # User message
    print(f"\n👤 USER MESSAGE:")
    print(f"   {user_msg}")
    
    # Context if provided
    if context:
        print(f"\n📋 CONTEXT:")
        print(f"   {context}")
    
    # Agent response (ALWAYS FULL, NO TRUNCATION)
    print(f"\n🤖 {agent_name} FULL RESPONSE:")
    print("-"*80)
    print(agent_response)  # CRITICAL: Always print complete response
    print("-"*80)
    
    # Response metrics
    print(f"\n📊 RESPONSE METRICS:")
    print(f"   - Length: {len(agent_response)} characters")
    print(f"   - Lines: {len(agent_response.split(chr(10)))} lines")
```

#### **Tool Testing Display Requirements**

```python
def test_tool_with_conversation_display(self):
    """Example tool test with mandatory conversation display"""
    
    # Input parameters
    print(f"\n🔧 TOOL TEST: {tool_name}")
    print(f"📥 INPUT PARAMETERS:")
    print(f"   - param1: {value1}")
    print(f"   - param2: {value2}")
    
    # Execute tool
    result = tool_function(param1, param2)
    
    # Display complete output
    print(f"\n📤 TOOL COMPLETE OUTPUT:")
    print("-"*60)
    if isinstance(result, dict):
        import json
        print(json.dumps(result, indent=2))
    else:
        print(result)
    print("-"*60)
    
    # Analysis
    print(f"\n📊 TOOL ANALYSIS:")
    print(f"   - Success: {result.get('success', 'N/A')}")
    print(f"   - Output type: {type(result)}")
```

#### **Agent Testing Display Requirements**

```python
def test_agent_with_full_conversation_display(self):
    """Example agent test with mandatory conversation display"""
    
    user_message = "Test message for agent"
    
    print(f"\n🧠 AGENT TEST: {agent_name}")
    print(f"👤 USER MESSAGE:")
    print(f"   {user_message}")
    
    # Execute agent
    result = agent_function(state, config)
    agent_response = result["messages"][-1]["content"]
    
    # MANDATORY: Display FULL response
    print(f"\n🤖 {agent_name.upper()} FULL RESPONSE:")
    print("="*80)
    print(agent_response)  # NEVER truncate agent responses
    print("="*80)
    
    # State analysis
    print(f"\n📋 STATE CHANGES:")
    state_changes = []
    if result.get("current_project_id"):
        state_changes.append(f"Project ID: {result['current_project_id']}")
    if result.get("routing_context"):
        state_changes.append(f"Routing: {result['routing_context']}")
    
    for change in state_changes:
        print(f"   - {change}")
```

#### **Multi-Agent Routing Display Requirements**

```python
def test_multi_agent_routing_with_display(self):
    """Example multi-agent test with complete handoff display"""
    
    print(f"\n🔄 MULTI-AGENT ROUTING TEST")
    print(f"{'='*80}")
    
    # Coordinator processing
    print(f"\n📍 STEP 1: COORDINATOR PROCESSING")
    coordinator_result = coordinator_agent(state, config)
    
    print(f"🤖 COORDINATOR RESPONSE:")
    print("-"*40)
    print(coordinator_result["messages"][-1]["content"])
    print("-"*40)
    
    # Handoff decision
    print(f"\n📍 STEP 2: ROUTING DECISION")
    routing_info = coordinator_result.get("routing_context", {})
    print(f"   Target Agent: {routing_info.get('target_agent', 'determined dynamically')}")
    print(f"   Routing Reason: {routing_info.get('reason', 'context-based')}")
    
    # Specialist processing
    print(f"\n📍 STEP 3: SPECIALIST PROCESSING")
    specialist_result = specialist_agent(coordinator_result, config)
    
    print(f"🤖 SPECIALIST FULL RESPONSE:")
    print("="*60)
    print(specialist_result["messages"][-1]["content"])
    print("="*60)
    
    # Complete workflow summary
    print(f"\n📊 WORKFLOW SUMMARY:")
    print(f"   - Total messages: {len(specialist_result['messages'])}")
    print(f"   - Routing successful: ✓")
    print(f"   - Context preserved: {'✓' if 'context' in str(specialist_result) else '✗'}")
```

#### **CRITICAL ENFORCEMENT RULES**

1. **NO TRUNCATION**: Never use `[:100]` or `...` on agent responses
2. **COMPLETE OUTPUT**: Always show full tool results and agent responses
3. **CLEAR FORMATTING**: Use consistent prefixes (👤🤖📋📊📥📤🔧🧠🔄)
4. **ERROR DISPLAY**: Print complete error messages and stack traces
5. **PERFORMANCE METRICS**: Include response times and character counts
6. **STATE TRACKING**: Show all state changes and context preservation

**VIOLATION CONSEQUENCES**: Tests that do not display full conversations will be considered incomplete and must be rewritten.

#### **STEP 3: Component Testing Requirements**
**For EVERY Tool (@tool function):**
```python
# tests/unit/test_[tool_name].py
def test_[tool_name]_valid_input():
    # Test with valid inputs
def test_[tool_name]_invalid_input():
    # Test with invalid/edge case inputs
def test_[tool_name]_chromadb_integration():
    # Test database operations
def test_[tool_name]_error_handling():
    # Test failure scenarios
def test_[tool_name]_performance():
    # Test response times and efficiency
```

**For EVERY Agent (specialist function):**
```python
# tests/unit/test_[agent_name].py  
def test_[agent_name]_domain_expertise():
    # Test agent provides accurate domain knowledge
def test_[agent_name]_tool_integration():
    # Test agent uses tools correctly
def test_[agent_name]_conversation_quality():
    # Test natural conversation flow
def test_[agent_name]_error_recovery():
    # Test graceful error handling
```

**For EVERY Multi-Agent Flow:**
```python  
# tests/scenarios/test_[workflow_name].py
async def test_[workflow_name]_routing():
    # Test coordinator → specialist routing
async def test_[workflow_name]_state_management():
    # Test state preservation across agents
async def test_[workflow_name]_conversation_flow():
    # Test complete user journey
```

#### **STEP 4: Testing Gates (MANDATORY CHECKPOINTS)**
**Gate 1: Unit Tests Pass**
- All individual tools tested with real data
- All agents tested with real LLM calls  
- 100% test coverage for new components
- Performance benchmarks met

**Gate 2: Integration Tests Pass**
- Multi-agent routing working correctly
- ChromaDB integration validated
- State management across agent transitions
- Error handling and recovery tested

**Gate 3: Scenario Tests Pass**
- End-to-end workflows complete successfully
- Real conversation quality validated with LangWatch
- User experience meets acceptance criteria
- System performance under load validated

#### **STEP 5: Failure Protocol**
**IF ANY TEST FAILS:**
1. **STOP development immediately**
2. **Fix the failing component**
3. **Re-run ALL related tests**
4. **Update docs/tips.md with solution**
5. **Only proceed when ALL tests pass**

**IF API KEYS FAIL:**
1. **STOP all development**
2. **Display clear error message**  
3. **Ask user to configure proper API keys**
4. **Validate keys work with simple test**
5. **Only proceed when keys validated**

### **Testing Tools Configuration**

#### **LangWatch Scenario Setup**
```python
scenario.configure(
    default_model="google/gemma-2-9b-it:free",  # Use configured model
    cache_key=f"{project_name}_tests_v1", 
    verbose=True,
    use_openrouter=True  # Match production config
)
```

#### **ChromaDB Test Collections**
```python
# Use separate test collections to avoid data contamination
test_collections = {
    "projects_test", "tasks_test", "documents_test", 
    "technical_requests_test", "checkpoints_test", "suggestions_test"
}
```

#### **API Key Validation Template**
```python
def validate_api_keys():
    """MANDATORY: Validate API keys before any testing"""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not openrouter_key and not gemini_key:
        raise EnvironmentError(
            "CRITICAL: No API keys configured. Please set OPENROUTER_API_KEY or GEMINI_API_KEY in .env file"
        )
    
    if not openrouter_key:
        print("⚠️ WARNING: OPENROUTER_API_KEY not set. Using Gemini API instead.")
    
    if not gemini_key:
        print("⚠️ WARNING: GEMINI_API_KEY not set. Using OpenRouter API instead.")
    
    return True
```

### Granular Task File Management System

**CRITICAL: Never create monolithic task files. Always generate multiple detailed task files.**

### Task Directory Structure (MANDATORY)

```
/tasks/
├── 000-master-[project-name].md           # Master overview & dependencies
├── agents/
│   ├── [XXX]a-[agent]-[action-name].md    # One file per agent action
│   ├── [XXX]b-[agent]-[action-name].md
│   └── ...
├── frontend/
│   ├── [XXX]-[page-name]-page.md          # One file per frontend page
│   ├── [XXX]-[component]-integration.md
│   └── ...
└── integration/
    ├── [XXX]-state-schema.md              # Infrastructure components
    ├── [XXX]-chromadb-setup.md
    └── [XXX]-graph-assembly.md
```

### Individual Agent Tool Task Template

**Use this template for each agent action:**

```markdown
# Task [XXX]a: [Agent Name] - [Action Name]

## Tool Specification
**Function**: `[action_name](parameters) -> return_type`
**Agent**: [Agent Name]
**Dependencies**: [List prerequisite tasks or "None"]
**Complexity**: [Low/Medium/High]
**Estimated Time**: [X-Y hours]

## Detailed Implementation Steps

### Phase 1: Analysis & Design (X minutes)
- [ ] Read PRD requirements for this specific action
- [ ] Identify required input parameters and validation rules
- [ ] Define return value structure and error conditions
- [ ] Document integration points with other agents
- [ ] Create function signature with proper type hints

### Phase 2: Data Layer Integration (X minutes)
- [ ] Study relevant ChromaDB collection schema
- [ ] Create data access functions (CRUD operations)
- [ ] Implement data validation and sanitization
- [ ] Add error handling for database operations
- [ ] Test data layer independently

### Phase 3: Business Logic Implementation (X minutes)
- [ ] Implement core business logic for the action
- [ ] Add domain-specific validation rules
- [ ] Implement state transitions if applicable
- [ ] Add logging and monitoring hooks
- [ ] Handle edge cases and error scenarios

### Phase 4: LLM Integration (if applicable) (X minutes)
- [ ] Design conversational prompts
- [ ] Implement LLM call with proper configuration
- [ ] Add response parsing and validation
- [ ] Implement retry logic for LLM failures
- [ ] Test with various input scenarios

### Phase 5: Testing & Validation (X minutes)
- [ ] Unit tests with valid inputs
- [ ] Unit tests with invalid inputs and edge cases
- [ ] Integration tests with dependent systems
- [ ] Mock tests for external dependencies
- [ ] Performance testing with realistic data volumes

### Phase 6: Documentation & Integration (X minutes)
- [ ] Add comprehensive docstring
- [ ] Document error conditions and responses
- [ ] Add usage examples
- [ ] Integrate function into agent node file
- [ ] Update agent interface documentation

## Acceptance Criteria
- [ ] Function implements exact PRD specifications
- [ ] All input validation working correctly
- [ ] Error handling covers all failure scenarios
- [ ] 100% test coverage achieved
- [ ] Integration with agent node successful
- [ ] Performance meets requirements

## Files to Modify/Create
- `backend_gen/src/agent/tools.py` (add function)
- `backend_gen/src/agent/nodes/[agent_name].py` (integrate)
- `backend_gen/tests/unit/test_[action_name].py` (create)
- `backend_gen/tests/integration/test_[agent]_tools.py` (update)

## Dependencies
**Prerequisite Tasks**: [List task IDs that must complete first]
**Blocking Tasks**: [List task IDs that depend on this task]
**Next Tasks**: [Suggested next task after this completes]

## Time Tracking
- [ ] Started: ___________
- [ ] Analysis Complete: ___________
- [ ] Implementation Complete: ___________
- [ ] Testing Complete: ___________
- [ ] Completed: ___________

## Notes & Discoveries
[Space for implementation notes, gotchas, and lessons learned]
```

### Frontend Page Task Template

**Use this template for each frontend page:**

```markdown
# Task [XXX]: [Page Name] Implementation

## Page Specification
**Route**: `/[route-name]`
**Purpose**: [Brief description of page purpose]
**PRD Reference**: [Section and line numbers]
**Dependencies**: [Required backend APIs]
**Estimated Time**: [X-Y hours]

## UI Requirements Analysis
- [ ] [Specific UI element 1 from PRD]
- [ ] [Specific UI element 2 from PRD]
- [ ] [Specific interaction requirement 1]
- [ ] [Real-time update requirements]

## Detailed Implementation Steps

### Phase 1: Component Architecture (X minutes)
- [ ] Analyze existing UI components for reuse
- [ ] Design component hierarchy for page layout
- [ ] Create TypeScript interfaces for data structures
- [ ] Plan state management approach
- [ ] Design responsive layout breakpoints

### Phase 2: API Integration Layer (X minutes)
- [ ] Create API service functions for page data
- [ ] Implement real-time update mechanisms
- [ ] Add loading states and error handling
- [ ] Create data transformation utilities
- [ ] Test API integration with mock data

### Phase 3: Core Components (X minutes)
- [ ] Implement main page component structure
- [ ] Create child components for specific features
- [ ] Add proper TypeScript typing
- [ ] Implement responsive design
- [ ] Add accessibility features

### Phase 4: Interactive Features (X minutes)
- [ ] Implement user interaction handlers
- [ ] Add form validation (if applicable)
- [ ] Create "Go to Chat" integration
- [ ] Add filtering and sorting functionality
- [ ] Implement navigation features

### Phase 5: Real-time Updates (X minutes)
- [ ] Connect to WebSocket for live updates
- [ ] Implement optimistic UI updates
- [ ] Handle connection loss and reconnection
- [ ] Add visual indicators for updates
- [ ] Test update performance

### Phase 6: Testing & Polish (X minutes)
- [ ] Unit tests for all components
- [ ] Integration tests with API
- [ ] Visual regression tests
- [ ] Accessibility testing
- [ ] Performance optimization

## Acceptance Criteria
- [ ] Page displays all required data correctly
- [ ] All interactive features work as specified
- [ ] Real-time updates function properly
- [ ] Responsive design works on all devices
- [ ] Accessibility requirements met
- [ ] Performance meets standards

## Files to Create/Modify
- `frontend/src/pages/[PageName].tsx` (create)
- `frontend/src/components/[Component].tsx` (create)
- `frontend/src/services/[api-service].ts` (create)
- `frontend/src/hooks/use[DataHook].ts` (create)
- `frontend/src/App.tsx` (add routing)

## API Dependencies
- [List required API endpoints with methods]

## Time Tracking
- [ ] Started: ___________
- [ ] Architecture Complete: ___________
- [ ] Components Complete: ___________
- [ ] Integration Complete: ___________
- [ ] Testing Complete: ___________
- [ ] Completed: ___________

## Notes & Discoveries
[Implementation notes and lessons learned]
```

### Master Coordination Task Template

**Create one master file to coordinate all tasks:**

```markdown
# Task 000: Master - [Project Name] Coordination

## System Overview
- **Domain**: [Business domain]
- **Architecture**: [Pattern description]
- **Backend**: [Technology stack]
- **Frontend**: [Technology stack]

## Task Dependencies & Execution Order

### Phase 1: Foundation (Parallel Execution)
**Prerequisites**: None
- [ ] [Task ID]: [Foundation task 1]
- [ ] [Task ID]: [Foundation task 2]

### Phase 2: Agent Tools (Dependency-Ordered)
**Prerequisites**: Phase 1 complete

**Foundation Tools (No Dependencies)**:
- [ ] [Task ID]: [Agent action 1]
- [ ] [Task ID]: [Agent action 2]

**Dependent Tools (Sequential)**:
- [ ] [Task ID]: [Dependent action 1] (needs [prerequisite tasks])
- [ ] [Task ID]: [Dependent action 2] (needs [prerequisite tasks])

### Phase 3: Agent Integration
**Prerequisites**: All Phase 2 complete
- [ ] [Task ID]: Graph assembly
- [ ] [Task ID]: End-to-end testing

### Phase 4: Frontend (After Backend Validation)
**Prerequisites**: Phase 3 validated
- [ ] [Task ID]: [Page 1]
- [ ] [Task ID]: [Page 2]

## Progress Dashboard

### Agent Tools: 0/[X] (0%)
**[Agent 1]**: 0/[Y] actions
**[Agent 2]**: 0/[Z] actions

### Frontend Pages: 0/[X] (0%)
**Core Pages**: 0/[Y]
**Integration**: 0/[Z]

### Integration: 0/[X] (0%)

## Current Status
- **Active Phase**: [Current phase]
- **Next Milestone**: [Next major milestone]
- **Blocking Issues**: [Any current blockers]
- **Estimated Completion**: [Date estimate]
```

### Phase 1.5 Implementation Protocol

**MANDATORY STEPS for Phase 1.5:**

1. **Complete Action Extraction**: Apply all 5 layers from `docs/planning.md`
   - Entity-driven analysis (all CRUD + status actions)
   - UI-specification extraction (all dashboard interactions)
   - Function description mapping (all PRD agent functions)
   - Workflow-based discovery (all user journey steps)
   - Cross-reference validation (ensure 100% coverage)

2. **Generate Agent Task Files**: 
   - One task file per agent action discovered
   - Use Individual Agent Tool Task Template above
   - Number sequentially: `001a-agent-action.md`, `001b-agent-action.md`
   - Include detailed time estimates and dependencies

3. **Generate Frontend Task Files**:
   - One task file per frontend page from PRD UI section
   - Use Frontend Page Task Template above  
   - Number in 100s: `101-main-dashboard.md`, `102-projects-view.md`
   - Include API dependencies and component requirements

4. **Generate Integration Task Files**:
   - State schema design task
   - ChromaDB collections setup task
   - Graph assembly task
   - End-to-end testing task
   - Number in 200s: `201-state-schema.md`, `202-chromadb-setup.md`

5. **Create Master Coordination File**:
   - Always create `000-master-[project-name].md`
   - Map all task dependencies clearly
   - Include progress dashboard with percentages
   - Define execution phases with prerequisites

**Quality Gate**: Before proceeding to Phase 2, validate that:
- [ ] All PRD requirements have corresponding task files
- [ ] All agent actions have individual task files
- [ ] All frontend pages have individual task files  
- [ ] All task dependencies are clearly mapped
- [ ] Master coordination file shows complete overview

## Tool/Action Planning

### Agent Tool Inventory
```markdown
## Agent: [Agent Name 1]
### Actions:
- action_name(param1, param2) -> return_type
- action_name_2(param) -> return_type

## Agent: [Agent Name 2]  
### Actions:
- action_name_3(param) -> return_type
- action_name_4(param1, param2) -> return_type
```

### Tool Dependencies
```markdown
## Tool Dependencies:
- Agent2.action_name_3() NEEDS Agent1.action_name()
- Agent1.action_name_2() NEEDS Agent2.action_name_4()
```

### Scenario Workflows
```markdown
### Scenario: [Primary User Workflow]
User: "[Example user request]"

**Tool Execution Order:**
1. Agent1.action_name("param") → Returns: result1
2. Agent2.action_name_3(result1) → Returns: result2
3. Agent1.action_name_2(result2) → Returns: final_result

**Prerequisites Check:**
- [ ] All tools can be implemented independently
- [ ] No circular dependencies detected
- [ ] Clear data flow between agents
```

## Acceptance Criteria
- [ ] All individual tools tested and working
- [ ] Tool dependency chains validated
- [ ] Graph compiles successfully
- [ ] Server starts without errors
- [ ] All scenario workflows complete successfully

## Summary of Changes
[Updated during implementation]
```

## Three Core Pillars

### Pillar 1: Conversational-First Agent Design

**Principle**: Never hardcode agent behavior - leverage LLM natural language understanding.

#### ✅ CORRECT Pattern
```python
def agent_function(state: OverallState, config: RunnableConfig) -> dict:
    # Get configuration
    configurable = Configuration.from_runnable_config(config)
    llm = DelayedLLM(
        delay_seconds=configurable.api_call_delay_seconds,
        model=configurable.specialist_model,
        use_openrouter=True,
        temperature=0.1,
        api_key=os.getenv("OPEN_ROUTER_API_KEY")
    )
    
    # Single comprehensive prompt with domain expertise
    prompt = f"""You are an expert in {domain_from_prd}.
    
    DOMAIN KNOWLEDGE:
    {embedded_expertise}
    
    CURRENT CONTEXT:
    {relevant_state_fields}
    
    USER REQUEST: {extracted_user_message}
    
    Analyze and respond naturally using your expertise."""
    
    response = llm.invoke(prompt)
    return {"messages": [...], "relevant_field": updated_value}
```

#### ❌ AVOID These Anti-Patterns
- Keyword matching: `if "create" in message.lower()`
- Intent detection functions: `def detect_intent(msg)`
- Hardcoded routing: `if intent == "task_creation"`
- Scripted responses: `responses = {"greeting": "Hello..."}`

**Key Insight**: Modern LLMs understand context better than any scripted logic.

### Pillar 2: LangWatch Scenario Testing

**Principle**: Test agents with real LLM conversations, not mocks.

#### Test Pattern
```python
import scenario

# Configure with OpenRouter
scenario.configure(
    default_model="google/gemini-2.5-flash-lite",
    cache_key="your-domain-tests-v1",
    verbose=True
)

class YourDomainAgent(scenario.AgentAdapter):
    """Adapter for testing your agent with scenarios"""
    
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        # Convert scenario input to your agent's state format
        state = {
            "messages": [{"role": m.role, "content": m.content} for m in input.messages],
            # Add domain-specific state fields
        }
        
        # Execute your agent
        result = your_agent_function(state, self.config)
        
        # Return the response
        return result["messages"][-1]["content"]

# Test complete conversations
@pytest.mark.asyncio
async def test_domain_workflow():
    result = await scenario.run(
        name="domain_workflow_test",
        description="Test agent handles domain-specific workflow",
        agents=[YourDomainAgent(), scenario.UserSimulatorAgent()],
        max_turns=6
    )
    assert result.success
```

### Pillar 3: OpenRouter/LiteLLM with Quota Management

**Principle**: Use DelayedLLM for automatic rate limiting and provider flexibility.

#### Configuration Setup
```python
# backend_gen/src/agent/configuration.py
from agent.configuration import DelayedLLM, Configuration

class Configuration(BaseModel):
    # Models via OpenRouter
    specialist_model: str = Field(
        default="google/gemini-2.5-flash-lite",
        metadata={"description": "Primary model for agents"}
    )
    
    # Quota management
    api_call_delay_seconds: int = Field(
        default=120,
        metadata={"description": "Delay between API calls"}
    )
    
    use_openrouter: bool = Field(
        default=True,
        metadata={"description": "Use OpenRouter vs direct API"}
    )
```

#### Usage in Agents
```python
# Always use DelayedLLM with configuration
configurable = Configuration.from_runnable_config(config)
llm = DelayedLLM(
    delay_seconds=configurable.api_call_delay_seconds,
    model=configurable.specialist_model,
    use_openrouter=configurable.use_openrouter,
    temperature=0.1,
    api_key=os.getenv("OPEN_ROUTER_API_KEY")
)
```

## Phase-Based Implementation Process

### Phase 0: Workspace Initialization (AUTOMATIC)

**MANDATORY:** Start every new use case with clean environment:

```bash
# 1. Hard reset tasks directory
rm -rf /tasks
mkdir -p /tasks/artifacts

# 2. Hard reset backend_gen directory  
rm -rf /backend_gen

# 3. Copy backend template to backend_gen
cp -r backend backend_gen
cd backend_gen && pip install -e .
```

**Validation:**
- [ ] `backend_gen/` directory exists
- [ ] Dependencies installed successfully
- [ ] `python -c "from agent.graph import graph"` works

### Phase 1: Architecture Planning & Specification

**Objectives:**
1. **Create task file** following `/tasks/XXX-description.md` format
2. **Analyze PRD** for domain, users, workflows, data, integrations
3. **Consult `docs/tips.md`** for similar business cases and patterns
4. **Design minimal architecture** following agent design principles
5. **Plan individual tools/actions** for each agent with dependency mapping

**PRD Analysis Checklist:**
- [ ] **Domain**: What business area? (Finance, HR, Delivery, etc.)
- [ ] **Users**: Who will interact with the system?
- [ ] **Workflows**: What tasks need to be accomplished?
- [ ] **Data**: What information needs to be managed?
- [ ] **Integrations**: What external systems to connect?

**Agent Design Principles:**
1. **Minimize agent count**: Prefer 1-3 agents maximum
2. **Single coordinator**: One agent orchestrates when possible  
3. **Tools for operations**: CRUD, integrations, calculations
4. **Natural conversations**: No scripted flows

**Architecture Patterns:**

**Pattern A: Single Agent + Tools** (Preferred)
```
Coordinator Agent
├── Data Tools (CRUD operations)
├── Integration Tools (APIs, external systems)
└── Generation Tools (documents, reports)
```

**Pattern B: Coordinator + Specialists** (Complex domains)
```
Coordinator Agent (Router)
├── Specialist Agent 1 (Domain area 1)
└── Specialist Agent 2 (Domain area 2)
```

### 1.5 Agent Tools/Actions Planning (MANDATORY)

**Before implementing any agents, systematically plan their individual capabilities:**

#### **Tool/Action Inventory Process**
1. **For each agent**, list all specific actions it needs to perform:
   ```markdown
   ## Agent: Project Manager
   ### Actions:
   - create_project(name, client, type) -> project_id
   - update_project_status(project_id, status)
   - assign_team_member(project_id, member_id, role)
   - generate_status_report(project_id) -> report_text
   - schedule_meeting(project_id, participants, date)
   
   ## Agent: Document Generator  
   ### Actions:
   - create_document_template(template_type) -> template_id
   - populate_template(template_id, data) -> document_content
   - save_document(project_id, content, type) -> document_id
   - generate_summary(document_id) -> summary_text
   ```

2. **Map dependencies between agents**:
   ```markdown
   ## Tool Dependencies:
   - Document Generator.populate_template() NEEDS Project Manager.get_project_data()
   - Document Generator.save_document() NEEDS Project Manager.validate_project_exists()  
   - Project Manager.generate_status_report() NEEDS Document Generator.create_document_template()
   ```

#### **Scenario-Based Workflow Planning**
**For each major user workflow, trace the exact sequence of tool calls:**

**Example: "Create new project with initial documentation"**
```markdown
### Scenario: New Project Creation
User: "I need to start a new project for ClientX, it's a web development project"

**Tool Execution Order:**
1. Project Manager.create_project("ClientX Website", "ClientX", "web_development") 
   → Returns: project_id="proj_123"
   
2. Project Manager.assign_team_member(proj_123, "user_456", "project_lead")
   → Returns: success=true
   
3. Document Generator.create_document_template("project_charter")
   → Returns: template_id="tmpl_789" 
   
4. Project Manager.get_project_data(proj_123)
   → Returns: {name: "ClientX Website", client: "ClientX", ...}
   
5. Document Generator.populate_template(tmpl_789, project_data)
   → Returns: charter_content="# Project Charter..."
   
6. Document Generator.save_document(proj_123, charter_content, "project_charter")
   → Returns: document_id="doc_101"

**Prerequisites Check:**
- ✅ All tools can be implemented independently
- ✅ No circular dependencies detected
- ✅ Clear data flow between agents
```

#### **Tool-Level Implementation Roadmap**
**Instead of implementing full agents first, create individual tasks for each tool:**

```markdown
## Implementation Order (Based on Dependencies):

### Phase 2.1: Foundation Tools (No Dependencies)
- [ ] Task 002a: Implement Project Manager.create_project()
- [ ] Task 002b: Implement Project Manager.get_project_data()  
- [ ] Task 002c: Implement Document Generator.create_document_template()

### Phase 2.2: Dependent Tools  
- [ ] Task 002d: Implement Document Generator.populate_template() 
  - Requires: Project Manager.get_project_data()
- [ ] Task 002e: Implement Document Generator.save_document()
  - Requires: Project Manager project validation

### Phase 2.3: Complex Tools
- [ ] Task 002f: Implement Project Manager.generate_status_report()
  - Requires: Multiple document generation tools
```

#### **Tool Testing Strategy**
**Each tool gets individual testing before agent integration:**

```markdown
## Testing Approach:

### Unit Tests (Per Tool):
- test_create_project_valid_input()
- test_create_project_duplicate_name()
- test_populate_template_missing_data()
- test_save_document_invalid_project_id()

### Integration Tests (Tool Chains):
- test_project_creation_workflow()
- test_document_generation_workflow() 
- test_end_to_end_project_setup()

### Dependency Tests:
- test_dependent_tool_failure_handling()
- test_tool_chain_error_recovery()
```

**Benefits of Tool-First Planning:**
- ✅ **Predictable Development**: Each tool is a concrete, testable unit
- ✅ **Clear Dependencies**: Know exactly which tools need which other tools  
- ✅ **Better Testing**: Test individual tools before complex agent interactions
- ✅ **Incremental Progress**: Each tool completion is measurable progress
- ✅ **Risk Reduction**: Catch integration issues during planning, not coding

### Phase 2: Implementation & Code Generation

**Generate all components systematically:**

**2.1 State Design**
```python
class OverallState(TypedDict):
    # Always include these
    messages: Annotated[list, add_messages]
    user_context: dict
    
    # Add domain-specific fields
    current_entity_id: Optional[str]
    domain_specific_data: dict
```

**2.2 Tools Development**
Tools should perform concrete operations, not logic:
```python
@tool
def create_entity(name: str, details: dict) -> dict:
    """Create entity in database"""
    # Actual database operation
    return {"success": True, "id": entity_id}

@tool
def generate_document(template: str, data: dict) -> str:
    """Generate document from template"""
    # Actual document generation
    return formatted_content
```

**2.3 Agent Implementation**
Follow Pillar 1 (Conversational-First) patterns with comprehensive domain prompts.

### Phase 2.5: Mandatory Testing Gates (Universal)

**Critical Principle**: No agent implementation can proceed until its prerequisites pass comprehensive testing. Use the same models and configuration as production to ensure behavior consistency.

#### **Configuration-Driven Testing Protocol**

**Step 1: Import Production Configuration**
```python
from agent.configuration import Configuration, DelayedLLM
import langwatch_scenario as scenario

def setup_testing_with_production_config():
    """Setup testing using exact production configuration"""
    
    # Load same configuration as production agents
    config = Configuration()
    
    # Configure langwatch scenario with production models
    scenario.configure(
        # Use coordinator model for test orchestration
        default_model=config.coordinator_model,
        cache_key=f"{project_name}_tests_{config.coordinator_model.replace('/', '_')}_v1",
        verbose=True,
        log_level="DEBUG",
        
        # Mirror production LLM settings
        use_openrouter=config.use_openrouter,
        openrouter_base_url=config.openrouter_base_url,
        api_call_delay_seconds=config.api_call_delay_seconds,
        
        # Testing-specific settings
        capture_all_interactions=True,
        performance_metrics=True,
        token_tracking=True,
        save_conversations=True,
        export_format="json"
    )
```

#### **Universal Agent Testing Categories**

**1. Foundation Agent Testing (No Dependencies)**
- **Applies to**: Coordinator agents, primary orchestrators, independent specialists
- **Requirement**: Must pass ALL tests before dependent agents can be implemented

**2. Dependent Agent Testing (After Prerequisites)**
- **Applies to**: Agents that rely on other agents or shared state
- **Requirement**: Prerequisites must have passing test gates

#### **Model-Specific Testing Requirements**

**For Each Agent Type, Test with Its Configured Model:**

```python
class UniversalAgentTester:
    """Base class for testing any agent with its configured model"""
    
    def __init__(self, agent_function, agent_type: str):
        self.config = Configuration()
        self.agent_function = agent_function
        self.agent_type = agent_type
        
        # Select model based on agent type from configuration
        model_mapping = {
            "coordinator": self.config.coordinator_model,
            "specialist": self.config.specialist_model, 
            "document_generator": self.config.document_model,
            "analysis": self.config.analysis_model
        }
        
        self.model = model_mapping.get(agent_type, self.config.coordinator_model)
        self.temperature = self._get_temperature_for_agent_type(agent_type)
        
        # Initialize DelayedLLM with same config as production
        self.llm = DelayedLLM(
            delay_seconds=self.config.api_call_delay_seconds,
            model=self.model,
            use_openrouter=self.config.use_openrouter,
            temperature=self.temperature
        )
```

#### **Universal Test Categories (Any Agent Type)**

**Category 1: Core Functionality Testing**
```python
@scenario.test("agent_core_functionality")
async def test_basic_operations(self):
    """Test agent's primary functions work correctly"""
    # Test happy path scenarios
    # Verify state management
    # Validate output format and quality
    pass

@scenario.test("agent_configuration_compliance") 
async def test_uses_correct_configuration(self):
    """Verify agent uses configured models and settings"""
    # Confirm correct model is being used
    # Validate temperature settings
    # Check delay compliance
    # Verify API provider usage
    pass
```

**Category 2: Conversational Flow Testing**
```python
@scenario.test("conversation_flow_happy_path")
async def test_normal_conversation(self):
    """Test expected user interaction patterns"""
    # Multi-turn conversation coherence
    # Context preservation across turns
    # Natural response quality
    pass

@scenario.test("conversation_interruption_recovery")
async def test_conversation_resilience(self):
    """Test conversation interruption and resumption"""
    # Stop mid-conversation → resume later
    # Context switching → return to original topic
    # State preservation across interruptions
    pass
```

**Category 3: Edge Cases & Error Handling**
```python
@scenario.test("input_validation_edge_cases")
async def test_unusual_inputs(self):
    """Test response to unusual or invalid inputs"""
    # Empty inputs → helpful prompting
    # Invalid data formats → validation and correction
    # Extreme values (very long/short inputs)
    # Special characters, emojis, non-English text
    # Malformed requests → graceful error handling
    pass

@scenario.test("error_recovery_scenarios")
async def test_failure_handling(self):
    """Test graceful handling of various failures"""
    # Network failures during LLM calls
    # API quota exhaustion scenarios
    # Database connection failures  
    # Malformed LLM responses
    # State corruption recovery
    pass
```

**Category 4: Performance & Stress Testing**
```python
@scenario.test("performance_under_load")
async def test_agent_performance(self):
    """Test agent performance characteristics"""
    # Single user sustained conversation (20+ turns)
    # Response time consistency
    # Memory usage under load
    # Token usage optimization
    pass

@scenario.test("concurrent_usage")
async def test_concurrent_conversations(self):
    """Test multiple simultaneous conversations"""
    # State isolation between users
    # Resource sharing and limits
    # Performance degradation under load
    pass
```

**Category 5: Security & Safety Testing**
```python
@scenario.test("security_validation")
async def test_security_measures(self):
    """Test security and safety measures"""
    # Prompt injection prevention
    # Data leakage prevention
    # Unauthorized action attempts
    # Privacy preservation in logs
    # Input sanitization effectiveness
    pass
```

#### **Dependent Agent Additional Tests**

**Category 6: Inter-Agent Communication Testing**
```python
@scenario.test("agent_handoff_validation")
async def test_inter_agent_communication(self):
    """Test communication between agents"""
    # Proper data handoff between agents
    # State consistency across agent transitions
    # Error propagation handling
    # Agent routing accuracy
    pass

@scenario.test("dependency_failure_handling")
async def test_dependency_failures(self):
    """Test behavior when prerequisite agents fail"""
    # Graceful degradation when services unavailable
    # Fallback behavior testing
    # Error message propagation to user
    # Recovery after dependency restoration
    pass
```

#### **Enhanced Logging with Model Information**

```python
def log_model_interaction(agent_type: str, model: str, query: str, response: str, 
                         tokens: dict, timing: dict, config: dict):
    """Universal logging for model interactions"""
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent_type": agent_type,
        "model_used": model,
        "temperature": config.get("temperature"),
        "use_openrouter": config.get("use_openrouter"),
        
        # Complete interaction log
        "interaction": {
            "query": query,
            "response": response,
            "tokens": {
                "input": tokens.get("input_tokens", 0),
                "output": tokens.get("output_tokens", 0),
                "cost_estimate": tokens.get("cost", 0.0)
            }
        },
        
        # Performance metrics
        "timing": {
            "response_time_ms": timing.get("response_time"),
            "delay_applied_ms": timing.get("delay_applied")
        },
        
        # Configuration snapshot
        "config_snapshot": {
            "api_call_delay": config.get("api_call_delay_seconds"),
            "max_conversation_length": config.get("max_conversation_length"),
            "max_concurrent_agents": config.get("max_concurrent_agents")
        }
    }
    
    scenario.log("🤖 MODEL_INTERACTION", log_entry)
```

#### **Mandatory Testing Gates**

**Gate 1: Foundation Agent Validation**
- ✅ Configuration compliance (uses correct models/settings)
- ✅ Core functionality works with production models
- ✅ Conversation flow natural and coherent
- ✅ Error handling graceful and informative
- ✅ Performance within acceptable limits
- ✅ Security measures effective
- ✅ Real LLM integration successful (no mocks)

**Gate 2: Dependent Agent Validation**
- ✅ All Foundation Agent requirements
- ✅ Proper integration with prerequisite agents
- ✅ State consistency across agent handoffs
- ✅ Dependency failure handling
- ✅ Complex workflow completion

**Gate 3: Multi-Agent Workflow Validation**
- ✅ End-to-end scenarios work correctly
- ✅ State persistence across agent transitions
- ✅ User journey completion rates acceptable
- ✅ Performance acceptable under realistic load
- ✅ Cost efficiency within budget constraints

### Phase 3: Production Validation

**3.1 LangGraph Server Testing**
- Graph compilation without errors
- Server startup validation  
- API endpoint functionality
- Real-time conversation testing

**3.2 Comprehensive Integration Testing**
- Complete user journeys from start to finish
- Cross-agent data consistency
- Performance under realistic load
- Cost and quota management validation

**3.3 Production Readiness Validation**
- All agents pass their testing gates
- System performs within SLA requirements
- Monitoring and observability working
- Error recovery and graceful degradation validated

## Essential Commands

```bash
# Development
make gen                    # Run generated backend + frontend
make dev-backend-gen       # Run only generated backend
langgraph dev              # Start LangGraph server (port 2024)

# Testing
cd backend_gen
pip install -e .           # Install in editable mode
pytest tests/              # Run all tests
pytest tests/scenarios/    # Run conversation tests

# Validation
python -c "from agent.graph import graph; print('Graph loads successfully')"
```

## Required File Structure

```
backend_gen/src/agent/
├── state.py               # OverallState TypedDict
├── graph.py              # Graph assembly (ABSOLUTE IMPORTS ONLY!)
├── configuration.py      # DelayedLLM and settings
├── nodes/               # Agent functions
│   └── coordinator.py   # Main agent logic
├── tools.py             # Domain-specific tools
└── __init__.py          # Minimal, just exports
```

## Critical Implementation Patterns

### Configuration Management
```python
# Always use configuration
configurable = Configuration.from_runnable_config(config)
# Never hardcode model names or delays
```

### Message Handling
```python
# Handle both dict and LangChain objects
messages = state.get("messages", [])
for msg in messages:
    if hasattr(msg, 'type') and msg.type == "human":
        content = msg.content
    elif isinstance(msg, dict) and msg.get("role") == "user":
        content = msg.get("content", "")
```

### Import Requirements
```python
# graph.py MUST use absolute imports
from agent.nodes.coordinator import coordinator_agent  # ✅
# from .nodes.coordinator import coordinator_agent    # ❌ BREAKS!
```

### Tool Integration
```python
# Tools for operations only
@tool
def perform_action(params):  # ✅ Actual operation
    return result

# Not for logic
def analyze_intent(msg):     # ❌ LLM should handle this
```

## Quick Debugging

```bash
# Check for import errors
cd backend_gen
python -c "from agent.graph import graph"

# Start server and check logs
langgraph dev > langgraph.log 2>&1 &
sleep 5
grep -i "error\|exception" langgraph.log

# Test actual execution
curl -X POST "http://127.0.0.1:2024/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{"assistant_id": "agent", "input": {"messages": [{"role": "user", "content": "test"}]}}'
```

## References - Active Usage Instructions

### Before Starting Any Implementation:

1. **`docs/prd.md`** - Current Use Case Definition
   - **READ FIRST**: Understand domain, users, workflows, data requirements
   - **ANALYZE**: Extract agent architecture needs and business logic
   - **REFERENCE**: Throughout implementation for requirement validation

2. **`docs/tips.md`** - Accumulated Knowledge Base  
   - **CONSULT BEFORE CODING**: Search for similar business cases and patterns
   - **APPLY SOLUTIONS**: Use documented patterns for common problems
   - **UPDATE AFTER COMPLETION**: Add new learnings and error solutions

3. **`docs/planning.md`** - Implementation Patterns & Examples
   - **REFERENCE**: For detailed architecture examples and code patterns
   - **FOLLOW**: Established patterns for consistent implementation
   - **ADAPT**: Patterns to current use case requirements

4. **`docs/roadmap.md`** - Development Tracking & Phases
   - **UPDATE FIRST**: Add new task after last completed task
   - **TRACK PROGRESS**: Mark phases with ✅ when complete
   - **MAINTAIN**: Development history and current status

### During Implementation:

5. **`/tasks/XXX-description.md`** - Current Task Tracking
   - **CREATE**: At start of each new use case implementation
   - **UPDATE**: Checkbox progress after each implementation step
   - **COMPLETE**: Summary of changes when task finished

### Workflow Integration:
```bash
# 1. Study existing codebase
ls -la backend_gen/src/agent/

# 2. Read and analyze PRD
cat docs/prd.md

# 3. Consult tips for similar cases
grep -i "domain_keyword" docs/tips.md

# 4. Update roadmap with new task
echo "- [ ] New Task: Description" >> docs/roadmap.md

# 5. Create task file
cp tasks/000-sample.md tasks/001-new-task.md

# 6. Implement following task file steps
# 7. Update tips.md with learnings
# 8. Mark roadmap task complete
```

## Development Workflow - Complete Process

### Mandatory Pre-Implementation Checklist

**Before writing any code:**
- [ ] **Study existing codebase** - Understand current state and patterns
- [ ] **Read PRD thoroughly** - Extract all requirements and constraints  
- [ ] **Consult tips.md** - Search for similar business cases and solutions
- [ ] **Update roadmap.md** - Add new task after last completed item
- [ ] **Create task file** - Document all implementation steps with checkboxes

### Step-by-Step Implementation Flow

1. **Workspace Preparation**
   ```bash
   rm -rf tasks backend_gen
   mkdir -p tasks/artifacts  
   cp -r backend backend_gen
   cd backend_gen && pip install -e .
   ```

2. **Architecture Planning**
   ```bash
   # Create task file from template
   cp tasks/000-sample.md tasks/001-new-use-case.md
   
   # Study PRD and analyze requirements
   cat docs/prd.md | grep -i "domain\|agent\|workflow"
   
   # Check for similar implementations in tips
   grep -i "business_domain" docs/tips.md
   ```

3. **Tool-Level Task Creation** (**NEW APPROACH**)
   - **Instead of implementing full agents, create individual tasks for each tool/action**
   - **Each tool becomes a separate feature/task that can be tested independently**
   - **Update roadmap.md with tool-level tasks, not just agent-level tasks**
   
   ```bash
   # Example: Instead of "Task 002: Implement Project Manager Agent"
   # Create multiple tool-level tasks:
   echo "- [ ] Task 002a: Implement create_project() tool" >> docs/roadmap.md
   echo "- [ ] Task 002b: Implement update_project_status() tool" >> docs/roadmap.md  
   echo "- [ ] Task 002c: Implement assign_team_member() tool" >> docs/roadmap.md
   echo "- [ ] Task 002d: Implement generate_status_report() tool" >> docs/roadmap.md
   ```

4. **Tool-First Implementation Sequence**
   - **Phase 2.1**: Implement foundation tools (no dependencies)
   - **Phase 2.2**: Implement dependent tools (require other tools)
   - **Phase 2.3**: Assemble agents using pre-tested tools
   - Test each tool individually before proceeding
   - Apply documented patterns from tips.md

5. **Knowledge Capture**
   ```bash
   # Add tool-specific learnings to tips.md
   echo "## TIP #XXX: Tool Implementation Pattern" >> docs/tips.md
   
   # Mark individual tool tasks complete in roadmap.md
   sed -i 's/- \[ \] Task 002a/- \[✅\] Task 002a/' docs/roadmap.md
   ```

**Benefits of Tool-Level Task Management:**
- ✅ **Granular Progress Tracking**: Each tool completion is visible progress
- ✅ **Independent Testing**: Tools can be tested in isolation before integration
- ✅ **Clear Dependencies**: Roadmap shows which tools depend on others
- ✅ **Risk Reduction**: Problems caught at tool level, not agent level
- ✅ **Better Estimation**: Tool-level tasks are easier to estimate accurately

### Error Resolution Protocol

**When errors occur:**
1. **Search tips.md first** - Look for documented solutions
2. **Apply existing patterns** - Don't reinvent solutions
3. **Debug systematically** - Use provided debugging commands
4. **Document new solutions** - Add to tips.md for future reference

## Phase Tracking Example - Delivery Management System

### Real Implementation Example:

**Task: 001-delivery-management-system.md**

#### Phase 1: Planning ✅
- [✅] Analyze PRD requirements (Chat-centric delivery management)
- [✅] Design agent architecture (Coordinator + 4 specialists) 
- [✅] Create state schema (Projects, Tasks, Documents, Requests)
- [✅] Identify ChromaDB collections needed

#### Phase 2: Implementation (In Progress)
- [✅] Create state.py with delivery management TypedDict
- [✅] Create configuration.py with DelayedLLM settings
- [ ] Create coordinator agent (orchestrator)
- [ ] Create project manager agent  
- [ ] Create document generation agent
- [ ] Create weekly task coordinator agent
- [ ] Create technical infrastructure agent
- [ ] Create tools.py with ChromaDB collections
- [ ] Create graph.py with proper routing

#### Phase 3: Testing (Pending)
- [ ] Unit tests for all agents
- [ ] Integration tests for graph compilation
- [ ] Scenario tests with real conversations
- [ ] Validate with `make gen` command

**Progress Tracking in Roadmap:**
```markdown
### Current Development Status

✅ Phase 0: Workspace Initialization - Clean environment setup
✅ Phase 1: Architecture Planning - Delivery management spec complete  
🔄 Phase 2: Implementation - 2/9 components complete (22%)
⏳ Phase 3: Testing - Awaiting implementation completion

**Next Steps:**
- Complete coordinator agent implementation
- Add ChromaDB tools for data persistence
- Create conversation flow testing
```

**Tips.md Updates:**
```markdown
## TIP #XXX: Delivery Management Chat-Centric Architecture ✅

**Category**: Business Process Management
**Domain**: Project Delivery
**Architecture**: Coordinator + 4 Specialists

### Success Pattern
- Single coordinator orchestrates all user interactions
- Specialists handle domain-specific operations
- Dashboard is read-only, all actions via chat
- Document generation creates text for manual copy-paste

### Critical Implementation Details
- Use ChromaDB for persistence across collections
- Templates embedded in agents for document generation
- JIRA ticket automation with team assignment logic
- Weekly task coordination with reminder system
```

## Key Success Factors

1. **Follow the Workflow**: Use the tracking system religiously
2. **Trust LLM Intelligence**: Don't script what LLMs can reason
3. **Test with Real Models**: Use actual LLMs in tests, not mocks
4. **Manage Quotas**: Always use DelayedLLM for rate limiting
5. **Keep It Simple**: Fewer agents, more comprehensive prompts
6. **Document Everything**: Update tips.md with every discovery

Remember: The goal is to generate agents that have natural conversations while performing real operations, with comprehensive tracking of every step. Let the LLM's intelligence shine through systematic development and knowledge accumulation.