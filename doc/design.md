# Design

This section gives high level insights on design choices, to ease understanding
the structure of the source code and the resulting package.

## Programming languange and dependencies

The tool is developped using python 3.12 and 3.13. His supported python version
as well as the dependencies are documented into the project's `pyproject.toml`.

No other programming language interpreter or compiler is needed:

- Code itself is only in pure python, with some templating in the jinja
  language (and associated languages).
- Libraries relying on non-python code are available as binary wheels.

## Features and approach

...
