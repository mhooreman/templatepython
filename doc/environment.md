# Environment requirements

## Operating system

In no case, operating systems not maintained by their suppliers are supposed to
support the tool.

This software has been developped on Windows and MacOS.

The following operating systems are supported:

- Microsoft Windows
- Apple MacOS

The following operating systems are most probably able to run the software:

- Linux, any flavour
- OpenBSD, FreeBSD, NetBSD
- AIX
- Solaris

Considering the availability of python, other operating systems are probably
able to run the tool.

## Python

A python version is supported if:

- It is supported by the python foundation in bugfix or security status (see
  [status of python versions](https://devguide.python.org/versions/#versions);
  this exludes pre releases and end-of-life releases)
- It passes the unit tests
- It is provided as CPython (other python implementations have not been tested)

If provided by the operating system, the python interpreter shall be at least
in the supported versions (at least python 3.10, see `pyproject.toml`), in the
[standard (CPython)](https://www.python.org) implementation.

Even if older releases are available, we recomment to use the latest minor
python release, exluding patch number 0 (semantic versioning, see also
[versioning](versioning.md)).

It is strongly encouraged to use the UV tool to run the software. This is
described in [installation](installation.md) and [usage](usage.md), and manages
his own python installation if needed.
