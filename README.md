# agents_audit
testing agents for security audit


how to create a new solution

create a .env with the gemini key
go to frontend folder and do npm install


modify the business case in claude.md
delete the folders backend_gen and tasks

use claude to go through claude.md instructions.

when the solution is ready, make gen,  and go to   http://localhost:5173/app


# Tests 
python -m pytest
      tests/scenarios/test_audit_flow_scenarios.py::TestBasicAuditScenarios::test_backup_question_direct
       -v -s

