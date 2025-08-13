# agentic creator Roadmap

generator of agentic solutions


## Development Workflow

### ⚠️ **MANDATORY TESTING-FIRST DEVELOPMENT WORKFLOW** ⚠️

**ABSOLUTE REQUIREMENT**: Every step in the development workflow MUST include comprehensive testing. No component is considered complete without tests.

1. **Pre-Development Validation (MANDATORY)**

- **API Key Check**: Validate OPENROUTER_API_KEY and GEMINI_API_KEY before ANY work
- **Environment Setup**: Ensure test collections and LangWatch scenario are configured
- **Baseline Tests**: Run existing tests to ensure system stability
- **IF KEYS MISSING**: STOP immediately and ask user to configure API keys

2. **Task Planning with Test Strategy**

- Study the existing codebase and understand the current state
- Update `ROADMAP.md` to include the new task
- **MANDATORY**: Define test requirements for each component
- Priority tasks should be inserted after the last completed task
- **Test Categories Required**: Specify which of the 6 critical testing categories apply

3. **Task Creation with Testing Specifications**

- Study the existing codebase and understand the current state
- Create a new task file in the `/tasks` directory
- Name format: `XXX-description.md` (e.g., `001-db.md`)
- Include high-level specifications, relevant files, acceptance criteria, and implementation steps
- **MANDATORY**: Include comprehensive testing requirements for each component:
  - Individual tool functionality testing
  - Agent-specific behavior testing  
  - Multi-agent routing testing
  - ChromaDB integration testing
  - Real conversation workflow testing
  - Error handling and recovery testing
- Refer to last completed task in the `/tasks` directory for examples
- **Test File Planning**: Specify which test files need to be created
- **API Dependency**: Document required API keys and usage

4. **Test-Driven Implementation (MANDATORY)**

- **STEP 1**: Write test files FIRST, before implementation
- **STEP 2**: Implement the component to satisfy the tests
- **STEP 3**: Validate with real API calls (no mocks)
- **STEP 4**: Check performance benchmarks
- **STEP 5**: Update task progress and document any issues
- **IF TESTS FAIL**: STOP immediately and fix before proceeding
- **Performance Gate**: All components must meet response time requirements

5. **Component Validation Gates**

**Gate 1: Unit Testing**
- All @tool functions have comprehensive unit tests
- All agent functions have behavior and integration tests
- Tests pass with real API calls and data
- ChromaDB integration validated

**Gate 2: Integration Testing**
- Multi-agent routing works correctly
- State management validated across agent transitions
- Error handling and recovery tested
- Performance benchmarks met

**Gate 3: Scenario Testing**  
- End-to-end workflows tested with LangWatch
- Real conversation quality validated
- User experience meets standards
- System performance under load verified

6. **Mandatory Testing Checkpoints**

**Before Moving to Next Task:**
- [ ] All tests written and passing
- [ ] Real API integration validated
- [ ] Performance benchmarks met
- [ ] Error scenarios handled gracefully
- [ ] Documentation updated with testing results
- [ ] Tips.md updated with any solutions discovered

**IF ANY CHECKPOINT FAILS:**
- **STOP all development**
- Fix the failing component
- Re-run all related tests
- Only proceed when ALL tests pass

7. **Roadmap Updates with Testing Status**

- Mark completed tasks with ✅ in the roadmap
- Add reference to the task file (e.g., `See: /tasks/001-db.md`)
- **MANDATORY**: Include testing completion status:
  - ✅ Unit Tests: [X/X] passing
  - ✅ Integration Tests: [X/X] passing  
  - ✅ Scenario Tests: [X/X] passing
  - ✅ Performance: All benchmarks met
  - ✅ API Keys: Validated and working

### **Testing Workflow Enforcement**

#### **Before ANY Development:**
```bash
# MANDATORY: Check API keys
python -c "
import os, sys
or_key = os.getenv('OPENROUTER_API_KEY')
gem_key = os.getenv('GEMINI_API_KEY')
if not or_key and not gem_key:
    print('❌ CRITICAL: No API keys configured')
    print('Set OPENROUTER_API_KEY or GEMINI_API_KEY in .env')
    sys.exit(1)
print('✅ API keys validated')
"
```

#### **For Each Component Developed:**
1. **Create test file**: `tests/unit/test_[component].py`
2. **Write test methods**: All 6 categories as applicable
3. **Run tests**: `pytest tests/unit/test_[component].py -v`
4. **Validate performance**: Check response times
5. **Test with real APIs**: No mocks allowed
6. **Update documentation**: Record test results

#### **Test File Requirements:**

**CRITICAL RULE: Distribute Tools by Agent**
- **NEVER** create monolithic test files with all tools together
- **ALWAYS** create separate test files for each agent's specific tools  
- **ORGANIZE** test files by agent responsibility and tool ownership
- **MAINTAIN** manageable file sizes (max 15-20 tools per file)

**Test File Structure:**
- `test_coordinator_tools.py` - Coordinator agent tools only
- `test_project_manager_tools.py` - Project Manager agent tools only
- `test_document_generator_tools.py` - Document Generator agent tools only  
- `test_task_coordinator_tools.py` - Task Coordinator agent tools only
- `test_technical_infrastructure_tools.py` - Technical Infrastructure agent tools only
- `test_historical_analysis_tools.py` - Historical Analysis agent tools only

**Every tool requires:**
- `test_valid_input_cases()` - WITH full input/output display
- `test_invalid_input_cases()` - WITH error scenario display
- `test_chromadb_integration()` - WITH data persistence display
- `test_error_handling()` - WITH complete error message display
- `test_performance_benchmarks()` - WITH timing and metrics display
- `display_tool_interaction()` - MANDATORY conversation display function

**Every agent requires:**
- `test_domain_expertise()` - WITH full agent response display
- `test_tool_integration()` - WITH tool execution display
- `test_conversation_quality()` - WITH complete conversation flow display
- `test_error_recovery()` - WITH recovery action display
- `display_agent_conversation()` - MANDATORY conversation display function

**Every workflow requires:**
- `test_coordinator_routing()` - WITH routing decision display
- `test_state_management()` - WITH state change display
- `test_end_to_end_workflow()` - WITH complete workflow display
- `display_multi_agent_flow()` - MANDATORY multi-agent conversation display

**CRITICAL CONVERSATION DISPLAY REQUIREMENTS:**

1. **NO TRUNCATION POLICY**: 
   - NEVER truncate agent responses with `[:100]` or `...`
   - ALWAYS display complete tool outputs
   - Show full error messages and stack traces

2. **MANDATORY DISPLAY FUNCTIONS**: Each test file MUST include:
   ```python
   def display_conversation_turn(self, turn_num, user_msg, agent_response, agent_name="AGENT"):
       """REQUIRED: Display full conversation turn"""
       print(f"\n{'='*80}")
       print(f"TURN {turn_num}: {agent_name}")
       print(f"{'='*80}")
       print(f"👤 USER: {user_msg}")
       print(f"🤖 {agent_name} FULL RESPONSE:")
       print("-"*80)
       print(agent_response)  # COMPLETE response, NO truncation
       print("-"*80)
   ```

3. **FORMATTING STANDARDS**:
   - Use consistent emoji prefixes: 👤 (user), 🤖 (agent), 🔧 (tool), 📋 (context)
   - Include response metrics: character count, line count, response time
   - Show state changes and context preservation

4. **MULTI-AGENT DISPLAY**:
   - Display each agent handoff with routing context
   - Show complete conversation flow across agents
   - Include workflow summaries and state persistence

#### **Failure Protocols:**
**Test Failures:**
1. STOP development immediately
2. Fix the failing component
3. Re-run ALL related tests
4. Update tips.md with solution
5. Only proceed when tests pass

**API Key Failures:**
1. STOP all development
2. Display clear error message
3. Ask user to configure proper keys
4. Validate keys work with test call
5. Only proceed when validated

**Performance Failures:**
1. STOP development immediately
2. Optimize the failing component
3. Re-test performance benchmarks
4. Document optimization approach
5. Only proceed when benchmarks met

### **Testing Success Criteria**
- **100% test coverage** for all implemented components
- **All tests pass** with real API calls and data
- **Performance benchmarks** met for all components
- **Error scenarios** handled gracefully
- **Documentation complete** with test results
- **User experience** validated through scenario testing

## Development Phases


- **Advanced Diff Algorithms**

  - Multiple diff granularity options (character, line, sentence level)
  - Configurable diff sensitivity settings
  - Whitespace and case-insensitive diff options
  - Performance optimization for large documents

- **Syntax-Aware Diff Highlighting**

  - Markdown syntax highlighting in diff view
  - Code block syntax highlighting within diffs
  - Preserve formatting and links in diff display
  - Rich text diff visualization

- **Interactive Diff Navigation**

  - Jump to next/previous change controls
  - Change filtering (additions, deletions, modifications)
  - Synchronized scrolling for side-by-side mode
  - Keyboard shortcuts for diff navigation
  - Change statistics and summary dashboard

- **Content Import/Scraping**

  - URL content extraction service
  - Metadata parsing
  - Multiple content type support

- **Advanced Prompt Templates**

  - Template variables and substitution
  - Prompt validation and versioning
  - Conditional logic in prompts
  - Prompt performance analytics

### Phase 4: Polish & Enhancement

- **Advanced Version Control**

  - Detailed version timeline
  - Advanced diff visualization
  - Conflict resolution

- **Advanced Search & Filtering**

  - Global search
  - Advanced filtering
  - Search result highlighting

- **Export Features**
  - Basic format exports (Markdown, HTML)
  - Platform-specific exports
  - Batch export

### Phase 5: Advanced Features

- **Advanced AI Editing Features**

  - Enhanced editing commands with more options (rewrite, formalize, casual, fix-grammar, add-examples, restructure)
  - Paragraph-level editing: users can select specific paragraphs to apply targeted edits
  - Advanced diff visualization before applying changes (side-by-side, interactive)
  - Separate system prompt management for editing commands (different from post creation)
  - Enhanced content extraction: better parsing of AI responses including markdown code blocks
  - Custom editing command creation and templates
  - Command template management and sharing system
  - Command execution history and analytics
  - Database-driven command management system

### Phase 6: Team & Collaboration

- **Archive System**

  - Archive/unarchive posts
  - Archived posts view
  - Permanent deletion

- **Team Collaboration**
  - Team member roles
  - Collaborative editing
  - Comment system

## Enhanced Development Phases

### Phase 0: Workspace Initialization (MANDATORY)
- Clean slate preparation with dependency reset
- Tips consultation for known patterns  
- Environment setup validation

### Phase 0.5: Granular Task Generation (NEW - MANDATORY)
**Purpose**: Replace monolithic task files with detailed, trackable component-level tasks

**Requirements**:
- [ ] **Complete Action Extraction**: Apply 5-layer methodology from docs/planning.md
  - [ ] Entity-driven analysis (CRUD + status actions for all data entities)
  - [ ] UI-specification extraction (all dashboard/page interactions)
  - [ ] Function description mapping (all PRD agent functions)
  - [ ] Workflow-based discovery (all user journey steps)
  - [ ] Cross-reference validation (ensure 100% requirement coverage)

- [ ] **Task File Architecture Setup**: Create `/tasks/` directory structure
  - [ ] `agents/` subdirectory for individual agent action tasks
  - [ ] `frontend/` subdirectory for individual page implementation tasks
  - [ ] `integration/` subdirectory for infrastructure component tasks
  - [ ] Master coordination file for dependency tracking

- [ ] **Agent Task Generation**: Create individual task file per agent action
  - [ ] Use Agent Tool Task Template from CLAUDE.md
  - [ ] Include detailed implementation phases with time estimates
  - [ ] Map dependencies between agent actions clearly
  - [ ] Add comprehensive acceptance criteria per action

- [ ] **Frontend Task Generation**: Create individual task file per UI page
  - [ ] Extract pages from PRD UI specifications section
  - [ ] Use Frontend Page Task Template from CLAUDE.md
  - [ ] Include API integration requirements per page
  - [ ] Plan component reuse from existing frontend

- [ ] **Integration Task Generation**: Create infrastructure component tasks
  - [ ] State schema design and validation
  - [ ] ChromaDB collections setup and configuration  
  - [ ] LangGraph assembly and routing
  - [ ] End-to-end testing and validation

- [ ] **Master Coordination Creation**: Generate dependency tracking file
  - [ ] Map all task dependencies and execution order
  - [ ] Create progress dashboard with completion percentages
  - [ ] Define parallel vs sequential execution opportunities
  - [ ] Establish realistic timeline with milestones

**Quality Gate**: Must validate before Phase 1:
- [ ] All PRD requirements have corresponding task files
- [ ] All discovered agent actions have individual task files
- [ ] All frontend pages have individual task files
- [ ] All infrastructure needs have individual task files
- [ ] Master coordination shows complete system overview
- [ ] Task dependencies are clearly mapped and validated

### Phase 1: Architecture Planning & Specification
- Analyze PRD and reference previous implementations
- Apply comprehensive action extraction methodology  
- Consult `docs/tips.md` for similar business cases
- **Result**: Comprehensive action inventory ready for task generation

### Phase 2: Implementation & Code Generation
- Follow granular task file specifications exactly
- Update individual task progress after each step
- Apply lessons from `docs/tips.md`
- Generate components using detailed task guidance

### Phase 3: Testing & Validation  
- Unit, integration, and scenario testing
- Real LLM conversation validation
- Error resolution with knowledge capture
- Add new learnings to `docs/tips.md`

### Phase 4: Frontend Dashboard Development (NEW)
**Prerequisites**: All backend agents validated, LangGraph server working, chat interface complete

**Purpose**: Extend existing React/Vite frontend with dashboard pages while preserving chat interface

**Requirements**:
- [ ] **Preserve Existing**: Keep current chat interface intact and functional
- [ ] **Add Routing**: Implement React Router for multi-page navigation
- [ ] **Dashboard Pages**: Implement all pages identified in PRD UI specifications
  - [ ] Main Dashboard with project cards and action items
  - [ ] Projects View with filtering and project selection
  - [ ] Checkpoints View with progress tracking (from missing actions)
  - [ ] Suggestions View with priority-based management  
  - [ ] Tasks View with weekly reminders and completion tracking
- [ ] **API Integration**: Connect dashboard pages to validated LangGraph endpoints
- [ ] **Real-time Updates**: Implement WebSocket integration for live data updates
- [ ] **Chat Integration**: Ensure all dashboard actions redirect to chat interface
- [ ] **Responsive Design**: Maintain consistent UI/UX across all devices

## Current Development Status

- [ ] **Task 001**: Delivery Management Multi-Agent System (DMMAS) Implementation
  - Domain: Project delivery management and coordination
  - Architecture: Coordinator + 4 specialist agents pattern
  - Priority: High - Complete implementation from PRD specification
  - Status: Phase 0.5 - Granular Task Generation Required
  - Current Task Files: 1 monolithic file (needs decomposition)
  - Target Task Files: ~25-30 granular component files
  - See: /tasks/001-delivery-management-system.md (to be decomposed)