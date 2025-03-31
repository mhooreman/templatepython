# Usage

## Starting the application

The application can be started by invoking the command line `templatepython`, with
different possibilities.

In the remaining parts of this documentation, all those possibilities
will be mentionned as `templatepython`.

### Using standard python or virtual environment

```text
templatepython
```

### Using UV

**As UV manages python installations and environment, this is the best option
if you don't use python and want to keep it simple**

```text
uv run --with templatepython-0.0.1.dev3-py3-none-any.whl templatepython
```

### In development

Go to the development project directory (the clone from GitHub, see
[development](development.md)). Then:

```text
hatch run templatepython
```

## The command line

### Preliminary notes

- The examples below are showing command line interaction. There is an
  alternance of blocks between the entered command line and the results.
- The examples are reflecting the status of the tool when the documentation was
  written. It is possible that the shown console results differs from what you
  have.

### Getting help

Invoking the command line without argument results in errors. The script stops
by explaining the first error, without any information on potental next errors.

Getting information on the command line tool invocation is possible using the
`--help` option:
```text
templatepython --help
```
```text
...
```

### Ensuring that you are using the right version

To show the version number, invoke the `--version` option:

```text
templatepython --version
```
```text
templatepython, version 0.0.1.dev3
```

### Running the tool

To run the tool, you need to provide the input and output files, respectively
as arguments to the `--input` and `--output` options:

```text
templatepython ...
```
```text
...
```

#### Practical tips and tricks

- On windows, to start the command line from within a directory of your choice,
  you can open that directory in the file explorer, and enter `cmd` in the
  address bar.
- To provide a file name location, you can:
  - Drag and drop the file from the file explorer to the command line console
  - Start typing the name or location of the file, then hit the [Tab] keywoard
    touch to provide completion.
- When spaces or special characters are on the file locations, the file
  location shall be surrounded by `"`.
