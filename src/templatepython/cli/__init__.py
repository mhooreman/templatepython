# Copyright (C) 2024-present Michaël Hooreman <mhooreman@icloud.com>

"""Command line interface."""

import click
from loguru import logger

from templatepython.__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(
    version=__version__,
)
def templatepython() -> None:
    """Do the same thing as any template project: say hello."""
    logger.info("Starting")
    click.echo("Hello world!")
    logger.info("Completed")
