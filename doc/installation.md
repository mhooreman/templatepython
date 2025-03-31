# Installation

## Production

### Standard python

Details of installation of python and management of virtual environments is out
of scope of the current documentation. If you are new to python and his
environment management and don't plan to dive into that language, please
consider the UV option shown below.

The tool can be installed using `pip` with the wheel package in argument. Since
we provide the package weel, no need to specify when this is an upgrade.

### Using UV

UV is supported. **This is considered as the best option for production usage,
as it does not needs installation of python.**

UV can be installed as described in the
[UV Website](https://docs.astral.sh/uv/getting-started/installation/).
Using UV will be described in the [usage](usage.md) section of this
documentation.

The tool installation will be managed automatically by uv. See
[usage](usage.md).

## Development

The project is managed using hatch, which can be downloaded as described in the
[hatch website](https://hatch.pypa.io/1.13/install/).

If missing, the required python version will be installed by hatch, locally.

To use the project, you simply have to clone the git repository from GitHub
(see [development](development.md)).

### Potential Windows issue with hatch

If your account contains special characters (accents, etc.),
issues might be encountered using hatch. In that case, move to a folder which
does not contains special characters (for example `c:\python\...`):

- the hatch directories (using environment variables, see hatch documentation)
- your clone of the git repository

## Documentation

The documentation package can simply be opened with a zip tool. The entry file
is `index.html`

**Attention:** opening the `index.html` file within the zip file without
"extracting" it won't work.
