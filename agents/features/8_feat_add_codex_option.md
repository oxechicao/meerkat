# 8 - FEATURE: add codex options to generate message

Follow instructions on `AGENTS.md` and definitions on `README.md`
Write a detailed description of the changes in `MEMORY.md`.

## Task description

### Files reference

- src/message.py
- src/agent_codex.py
- src/agent_copilot.py
- tests/test_message.py
- tests/test_agent_modules.py

### TODO

- Refactor the method `get_ai_commit_message`
    - create a new method callend `get_agent_message`:
    - If no `agent_name` is defined do `return generate_simple_commit_message(diff)`
    - If `agent_name` is defined:
        - Call `get_agent_message`:
            - print logs independent of the agent to be used
            - if `agent_name` is `copilot`:
                - return the message from `generate_commit_message_with_copilot`
            - if `agent_name` is `codex`:
                - return the message from `generate_commit_message_with_codex`
            - default return `return generate_simple_commit_message(diff)`
- Update tests and write new tests for the new cases.
- Write in the `MEMORY.md` a detailed description of how you did the solution.
