# 5 - FEATURE: Write reference file and isolate copilot agent

Always follow the definition in `AGENT.md` file and `README.md` file.

## Task Description

Currently in `message.py` before run the prompt in the AI, all reference are saved into a variable.

I want to save the reference context into a temporary file called `temp_git_message_reference.md`.

When the command finish, if success or not, the file should be removed.

Also the prompt command should be specific for each agent. For now, do only for copilot.

Steps to follow.

1. create a function in `message.py` that get the prompt and save it into `temp_git_message_reference.md`
   1. This file should contain the `gif diff` result.
2. create a file `agent_copilot.py`
3. write a new function on `agent_copilot,py`, the function should receive the path of story file.
   1. The prompt message will be: `Generate a git commit message for the following changes in @{path_to_temp_git_message_reference.md}`
   2. If has the path for the story file, add in the end ` and uses as context reference @{path_to_story_file}`
   3. Then call the prompt by `copilot -p {prompt} --allow-all-tools`
4. Write all changes in the `MEMORY.md` file. Add the agent used, the model used, prompt used.
