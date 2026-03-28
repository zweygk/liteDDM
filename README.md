# liteDDM

## Introduction

liteDDM is a lightweight framework for testing data drift.

## Disclaimer 

Use at your own risk, I'm not responsible for failing to detect drift in your data. I literally shat this out in an afternoon so don't expect miracles.

## Motivation

I made this for myself because
1) I don't want the bloat that comes with supposedly "production-ready" solutions
2) I wanted to test both univariate and multivariate data drift

Most of the available solutions don't satisfy both these requirements so I created my own.

## Structure

```
liteDDM/
|
|-- src/
|   |-- __init__.py
|   |-- assertions.py
|   |-- helpers.py
|   |-- test_definitions.py
|
|-- examples/
|   |-- __init__.py
|   |-- test_example.py
|
|-- .gitignore
|-- LICENSE
|-- pyproject.toml
|-- README.md
|-- requirements.txt
```

## Requirements

Developed and tested on Python 3.12.2. 

Requirements.txt contains a list of required pip packages.

## Usage
```
0) Create your test directory and add it to pyproject.toml (as a list element to testpaths under [tool.pytest.ini_options])
1) Define your test in test_definitions.py 
2) Define your assertion in assertions.py
3) Create your .py-testfile in your newly created test directory
4) Run pytest from terminal
```

See /examples/test_example.py for an example
