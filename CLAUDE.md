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

**Phase 3: Testing & Validation**
- Unit, integration, and scenario testing
- Real LLM conversation validation
- Error resolution with knowledge capture
- Add new learnings to `docs/tips.md`

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

### Phase 3: Testing & Validation

**3.1 Unit Testing**
- Individual tools and functions
- Agent function signatures and responses
- State management patterns

**3.2 Integration Testing**
- Graph compilation and server startup
- Agent routing and state passing
- Error handling and recovery

**3.3 Scenario Testing**
- Complete conversation flows with real LLMs
- Business workflow validation
- Edge case handling

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