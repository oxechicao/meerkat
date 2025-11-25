# 3 - Refactor: Split in files

Always follow the definition in `AGENT.md` file and `README.md` file.

## Task Description

Currently the project is using only one python file to run everything.
I want to split the current code in `meerkat.py` into different files.
The code should be copy and paste into the files.

Follow the sequence of tasks:

1. Create `src` directory
2. Create `git.py` file
3. Move the code related to the git commands from `meerkat.py` to `git.py`.
4. Create `message.py` file
5. Move the code related to build messages from `meerkat.py` to `message.py`.
6. Create `input.py` file
7. Move the code related to input validations and strategy definition for the commands from `meerkat.py` to `input.py`
8. Create `main.py` file
9. Move the entry code from `meerkat.py` to `main.py`
10. Refactor `meerkat.py` to call `main.py` entry method

Be sure to follow the file structure context defined bellow:

| filename     | description                                                         |
| ------------ | ------------------------------------------------------------------- |
| `main.py`    | Contain the entry code that will call the other methods             |
| `git.py`     | Contain all methods that call git commands                          |
| `message.py` | Contain the methods that build the message to be committed          |
| `input.py`   | Contain all methods that parse, validate the arguments and commands |
| `meerkat.py` | It should call `main.py` and it is used by the mrkt script          |

