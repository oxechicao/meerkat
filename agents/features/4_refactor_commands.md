# 4 - REFACTOR: split commands into files

Always follow the definition in `AGENT.md` file and `README.md` file.

## Task Description

Currently the the methods for `start`, `save`, `update`, and `help` are on `main.py` file.

You should do:

1. create `handle_start.py` file
2. move the methods related to `start` command from `main.py` to `handle_start.py`
3. create `handle_save.py` file
4. move the methods related to `save` command from `main.py` to `handle_save.py`
5. create `handle_update.py`
6. move the methods related to `update` command from `main.py` to `handle_update.py`
7. create `handle_help.py`
8. move the methods related to `help` command from `main.py` to `handle_help.py`
9. write all steps used to do the refactor into `MEMORY.md` file. Be explicit which agent was used.

Be sure to follow the file structure context defined bellow:

| filename           | description                             |
| ------------------ | --------------------------------------- |
| `handle_start.py`  | contains methods for the command start  |
| `handle_save.py`   | contains methods for the command save   |
| `handle_update.py` | contains methods for the command update |
| `handle_help.py`   | contains methods for the command help   |
