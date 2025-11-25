# 6_1 FIX: fix feature codex agent

Follow instructions on `AGEND.md` and definitions on `README.md`
Write a detailed description of the changes in `MEMORY.md`.

## Task Description

In the implementation of the previous feature `6_feat_code_agent.md` it breaks the implementation for save and update.

This is the response.

```
Traceback (most recent call last):
  File "/Users/chicao/Workspace/studies/cli/meerkat/meerkat.py", line 7, in <module>
    sys.exit(main())
  File "/Users/chicao/Workspace/studies/cli/meerkat/src/main.py", line 80, in main
    return handle_save_command(args, config, quiet)
  File "/Users/chicao/Workspace/studies/cli/meerkat/src/handle_save.py", line 42, in handle_save_command
    commit_message = get_ai_commit_message(config, getattr(args, 'story', None), quiet)
  File "/Users/chicao/Workspace/studies/cli/meerkat/src/message.py", line 41, in get_ai_commit_message
    from .agent_copilot import generate_commit_message_with_copilot
  File "/Users/chicao/Workspace/studies/cli/meerkat/src/agent_copilot.py", line 11, in <module>
    from .prompt import prompt, parse_output_message
  File "/Users/chicao/Workspace/studies/cli/meerkat/src/prompt.py", line 31, in <module>
    def parse_output_message(output: str) -> str | None:
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

Fix the error and write a detailed description on `MEMORY.md` about the solution.
