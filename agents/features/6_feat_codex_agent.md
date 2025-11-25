# 6 - FEATURE: Codex Agent

Always follow the definition in `AGENT.md` file and `README.md` file.
Use `MEMORY.md` is the memory bank of the changes.

## Task description

In the `agent_copilot.py` file we have a variable called prompt that contains the prompt message that should be sent to agent.
Create a file called `prompt.py` that will contain a variable with the prompt text.
Replace the variable prompt on `agent_copilot.py` with the variable created on `prompt.py`
Create a new agent file for codex, `agent_codex.py`.
The business logic will be similar, the main difference will be how you call the prompt.
Instead of `f'copilot -p "{prompt}" --allow-all-tools',` you will run `f'codex "{prompt}"`
Move the function that parse the result to `prompt.py` and reuse in both agents, copilot and codex.
By the end, write a detailed description of all steps that you did to do this feature on MEMORY.md

In summary, steps to do:

1. Create `prompt.py` file
2. Move method `parse_copilot_output` from `agent_copilot.py` to `prompt.py`
3. Rename the method to `parse_output_message`
4. Refactor `agent_copilot.py` to use `parse_output_message` instead of `parse_copilot_output`
5. Create `agent_codex.py` file
6. Write the method `generate_commit_message_with_codex` that will work similar as `generate_commit_message_with_copilot`, but focusing on codex agent. Using the command line `codex "{prompt}"` to run and get the message
7. Write a detailed description of the steps used to do this feature on `MEMORY.md`
