# Agents definitions

- [Agents definitions](#agents-definitions)
  - [Files structure](#files-structure)
  - [Coding](#coding)
    - [General instructions](#general-instructions)
    - [Coding rules](#coding-rules)
      - [Conditionals:](#conditionals)
        - [Correct code example](#correct-code-example)
        - [Incorrect code example](#incorrect-code-example)
      - [Loops:](#loops)
        - [Correct code example](#correct-code-example-1)
        - [Incorrect code example](#incorrect-code-example-1)
      - [Functions:](#functions)
        - [Correct code example:](#correct-code-example-2)
        - [Incorrect code example:](#incorrect-code-example-2)

## Files structure

- `.` or `root`: contains scripts and documents for initialization.
  - `AGENT.md`:
    - Contains instructions that have be followed by the AI AGENTS.
  - `README.md`
    - Contain the definitions about the project.
- `./agents`: Contain files that should be used by AI agents
  - `features/`:
    - Folder that contains the features that should be implemented.
    - The features are enumerated sequentially, it represent the timestamp for implementation.
  - `MEMORY.md`: 
    - Memory bank for agents actions.
    - It contains all steps made by agents
    - Should be used as reference
- `./src/`: Source code

## Coding

### General instructions

- Use the python best practices
- Use pep8 definition
    - Use flake8 for linting
- Use functional paradigm

### Coding rules

#### Conditionals:

Maximum of 1 level of indentation conditionals.  
Don’t Use The ELSE Keyword

##### Correct code example

```python
if something_true:
    do_something()

def do_something():
    if check_something:
        print(true)

```

##### Incorrect code example

```python
if something_true:
    if check_something:
        print(true)
```

#### Loops:

Only One Level Of Indentation Per Loop.  
If is really necessary add a new one, create a new function to do that

##### Correct code example

```python
for i in range(5):
    auxiliar_loop(i)

def auxiliar_loop(i):
    for j in range(i)
        pair = (i, j)
        print(pair)
```

##### Incorrect code example

```python
for i in range(5):
    for j in range(i)
        pair = (i, j)
        print(pair)
```

#### Functions:

Maximum of 3 levels of indentation per functions.  
Always do early return.

##### Correct code example:

```python
def my_function():
    if something_wrong:
        return
    
    for i in range(5):
        if i % 2 == true:
            do_something_mod_2(i)

    do_something_else()

def do_something_mod_2(num):
    if i % 4 == true:
        print(num)

```

##### Incorrect code example:

```python
def my_function():
    if something_wrong:
        return
    
    for i in range(5):
        if i % 2 == true:
            if i % 4 == true:
                print('something')

    do_something_else()
```
