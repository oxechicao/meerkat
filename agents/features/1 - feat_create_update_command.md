# FEATURE: create update command

Always follow the definitions on `README.md`

## TODO: 

- Follow the definitions on README.md
- Create a new command called update.
- Refactor command save removing the push feature, only doing add and commits

## Steps

### 1. Rename Save function to UPDATE

Change the of the current function for the command `save` to be used for the new command `update`

### 2. Create a new function Save

Create a new function for the save command.  
On this function you should only do the steps for `add` and `commit`.

1. Add all changes: `git add .`
2. Generate the git message using AI
3. Do the commit: `git commit $ai_message`

### 3. Refactor the command UPDATE

After create the new function `save`. Call this function before do the push.

Since the UPDATE function has basically 3 steps: add, commit, push; you can use the save function to do the first 2 steps.

### 4. Update MEMORY.md

When finish every changes, update the steps to do this task on MEMORY.md file. Detailing all changes made to make this feature.
