# Development

## GitHub project

The repository is hosted on GitHub:
[mhooreman/templatepython](https://github.com/mhooreman/templatepython).

Tags and releases are managed as described in [versioning](versioning.md).

Most of the changes are described in the GitHub tickets, and commits are
containing the associated ticket number using `#n` notation in their titles.
This rule becomes mandatory from release `0.0.1.dev4` in case of impact to
existing features and from release `0.1.0` for any change.

Development is done in branches reflecting the version number (with suffix).
When the version is completed, a pull request it done, updating the main branch
with the version branch, and the version branch is deleted. The main branch is
then tagged after the version, and the version deliverables (packages and
documentation are built).

In case of risky/complex development, is is allowed to branch specifically the
version branch. In that case, the version branch will pull the changes from the
specific branch when the corresponding development is completed.

## Working with the package

The package is managed using `hatch`, as configured in `pyproject.toml`.

Table below shows the commands for various tasks. Please note that most of
those commands support additional arguments, including `--help`.

| Task | Command |
|------|---------|
| Run the tool | `hatch run templatepython` |
| Increasing the major version number | `hatch version major` |
| Increasing the minor version number | `hatch version minor` |
| Increasing the path version number | `hatch version patch` |
| Setting the version number, with suffix | `hatch version {value}` |
| Lint and format the code | `hatch fmt` |
| Validate type hints | `hatch run types:check` |
| Build the package | `hatch build` |
| Build the documentation | `hatch run doc:build` |
| Serve the documentation | `hatch run doc:serve` |
| Execute the unit tests | `hatch test` |
| Execute the unit tests on every supported python version | `hatch test --all` |
| Compute the unit tests code coverage | `hatch test --cover` |

*Notes:*

- Serving the documentation is showing the documentation built automatically
  every time a change happens. It is useful when writing the documentation.
- Changing version suffix can only be done by specifying the version to
  `hatch version`
- Changing version must be done together with the branch/tag strategy mentioned
  above
- It is not possible to decrease a version number using `hatch version`; manual
  edition of `_about.__version__` is required.

## Rules

In addition to versioning rules described in [versioning](versioning.md), the
following rule applies:

- All the code linting rules activated in `pyproject.toml` applies.
- All the type linting rules activated in `pyproject.toml` applies.
- Any exception to the two rules above must be non-avoidable (under decent
  efforts) and must be documented using the adequate exclusion rule, **always**
  with the ignored rule identifier
- No rule shoud be deactivated in `pyproject.toml` as of version `0.0.1.dev1`.
  Any exception should be documented in a GitHub ticket, for change control.
- Doscrtings shall follow a RST format (e.g. underlines, etc.); as soon as the
  parameters are obvously named and typed, docstrings are allowed to not
  described them
- It is at least required to have unit tests covering import of all the
  package's modules and submodules (including private ones)
- There is not yet any target rule on code coverage, but it is not allowed to
  remove existing unit tests, unless the corresponding feature is dropped
