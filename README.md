# templatepython
A python project template

## Development

### Project and environment

Development is managed using hatch.

Development is managed using hatch. If you don't have it, it please go on
[the hatch installation web site](https://hatch.pypa.io/latest/install/).

Project is configured in pyproject.toml.

From the command line, inside the repository root directory:

- To start an environment with all the required dependencies: `hatch shell`

  - The script can be executed directly witing that shell (an executable is created)

- To create a build: hatch build

### Code quality control requirements

All those requirements are enforced by configuration in pyproject.toml at the
root of the repository.

The decision to change any item of this configuration is left to the main
author of the package.

#### Code linting

Code linting is performing using the ruff linter provided with hatch.

It has been configured so that all the non-experimental controls are enabled,
with some specific rules diabled with good reason.

It shall be checked using `hatch fmt`.

#### Typing

All the methods and functions shall be typed, mypy strict checking is enabled.
Exceptions shall be documented using `# type: ignore` comment.

Typing of variables is optional. It becomes mandatory if required by mypy to
verify typing of methods and functions.

This shall be checked using `hatch run types:check`.

#### Code documentation

All the public features in the code shall be documented. The numpy docstring
convention shall be used, wich the exception that, thanks to typing, type
documentation is not needed. Please refer to this example.

Documentation of private features is optional, and becomes required if
requested by (code linting)[#code-linting].

It shall be checked using `hatch fmt`.

#### Unit testing

We target full decision coverage on all the supported python versions.

Unit testing with statement and decision coverage is executed by
`hatch test --cover`.

Unit testing on supported python version is executed by `hatch test --all`.

#### Releases and changes

As soon as the version 0.1.0 is released, every development shall refer a
github issue. Upgrade to version minor or version major whall be made via a
change request.

Every release shall be developped in her own branch.

The main branch shall be updated, via a pull request, as the last step before
publication of the build.

The build shall be created on the upgraded main branch and published as a
github version. A corresponding tag shall be created.

#### Reporting issues

Issues shall be reported via the project GIT repository's issues

Apart of those issues, the following limitations are known:

## License and copyright

This is distributed under the terms of the BSD 3-Clause License.
See LICENSE.md.

Copyright (C) 2004-Today Michaël Hooreman
