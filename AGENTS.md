# Agents definitions

This file describe the context for agents to works. It is divided into project, contexts, coding standards.

- [Project Overview](#project-overview)
    - [TLDR](#tldr)
    - [Tech stack$$](#tech-stack)
    - [Files structure](#files-structure)
- [Commands](#commands)
- [Development instructions](#development-instructions)
    - [DO](#do)
        - [Code style guidelines](#code-style-guidelines)
        - [Test guidelines](#test-guidelines)
    - [DON'T](#dont)
- [Memory instruction](#memory-instruction)


## Project Overview

### TLDR

The project is a command-line tool built in python to help developer write git messages based in the diff file and some context reference file.

### Tech stack$$

- Python 3.14
- venv
- argparse
- pytest
- pep8

### Files structure

| File/Directory     | Description                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------- |
| `AGENT.md`         | Instructions that the Agents have to follow                                                   |
| `README.md`        | File with the context about the project                                                       |
| `agents/MEMORY.md` | Work as a MEMORY BANK. It contains everything made by agents. Should be updated all the time. |
| `agents/features/` | Directory that contains all feature references used for agents to                             |
| `src/`             | Source code of the project                                                                    |
| `tests/`           | Tes folder                                                                                    |

## Commands

- USE `.venv/bin/python` to run python command;
- USE `.venv/bin/flake8` to run flake8;
- USE `.venv/bin/pytest` to run tests;

## Development instructions

### DO

- USE Testing Driven Development approach;
- ALWAYS write the test first;
- ALWAYS run `pytest` only for the current `file:function` during the development;
- ONLY run a complete test when finish the development: `.venv/bin/pytest`

#### Code style guidelines

- USE limit characters per line = 99
- ADD a blank line after the end of if conditionals 
- ADD a blank line after the end of loops 
- ADD two blank lines after methods
- ALWAYS do line break before Math operations IF 
- ALWAYS use self for the first argument to instance methods.
- ALWAYS use cls for the first argument to class methods.
- ALWAYS do `return None` instead of `return` if the method is void.
- ALWAYS create a function with early return to represent IF...ELSE condition;
    ```python
        def my_conditional_function(self, value):
            if (value is true):
                # Do something
            
            # Do something else

        def my_function():
            response = my_conditional_function
            if (!response):
                # Something wrong
            
            # Continue the workflow
    ```
- ALWAYS prioritize early return;
- ALWAYS create function to represent nested loops:
    ```python
        def my_loop_2(self, i):
            for k in range(i):
                # DO something
            
            # DO Something more
        
        
        def my_loop_1():
            for x in range(0..10):
                result = my_loop_2(x)
                # DO SOMETHING

            # DO SOMETHING MORE
    ``` 
- USE PascalCase to write class name
- USE snake_case to write methods and variables.

#### Test guidelines

- write test names using SHOULD..WHEN.. pattern. Example: `def test_should_return_true_when_input_is_valid():`
- write tests following the pattern Arrange-Act-Assert

### DON'T

- DO NOT use ELSE statement;
- DO NOT write nested loops;
- NEVER run test in quiet mode;

## Memory instruction

- All changes result should be written in `agents/MEMORY.md` file
- The file is written in markdown
- ONLY add new description for the current prompt
- NEVER change the current data.
