# Coding Standards
- [Coding Standards](#coding-standards)
  - [General instructions](#general-instructions)
  - [Conditionals:](#conditionals)
  - [Loops:](#loops)
  - [Functions:](#functions)


## General instructions

- Use the python best practices
- Use pep8 definition
    - Use flake8 for linting
- Use functional paradigm
- Use `.venv/bin/python` file to run python commands
- Use `.venv/bin/pip3` file to run pip commands
- Use `.venv/bin/pytest` file to run pytest commands


## Conditionals:

Maximum of 1 level of indentation conditionals.  
Don’t Use The ELSE Keyword

**Correct code example:**

```python
if something_true:
    do_something()

def do_something():
    if check_something:
        print(true)

```

**Incorrect code example:**

```python
if something_true:
    if check_something:
        print(true)
```

## Loops:

Only One Level Of Indentation Per Loop.  
If is really necessary add a new one, create a new function to do that

**Correct code example;**

```python
for i in range(5):
    auxiliar_loop(i)

def auxiliar_loop(i):
    for j in range(i)
        pair = (i, j)
        print(pair)
```

**Incorrect code example:**

```python
for i in range(5):
    for j in range(i)
        pair = (i, j)
        print(pair)
```

## Functions:

Maximum of 3 levels of indentation per functions.  
Always do early return.

**Correct code example:**

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

**Incorrect code example:**

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
