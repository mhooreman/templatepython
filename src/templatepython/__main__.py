# Copyright (C) 2024-present Michaël Hooreman <mhooreman@icloud.com>
"""Run the package as a script.

It calls the cli.
"""

import sys

from templatepython.cli import templatepython

if __name__ == "__main__":
    sys.exit(templatepython())
