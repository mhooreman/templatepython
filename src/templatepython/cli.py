"""Provide the command line interface."""

import pathlib
import secrets

import click
import flask.cli

from templatepython import about as _about
from templatepython import config as _config
from templatepython import wsgi as _wsgi


@click.group
@click.version_option(version=str(_about.version))
def templatepython() -> None:
    """Control the templatepython application."""


@templatepython.command
def run() -> None:
    """Run the application."""
    raise NotImplementedError


@templatepython.group
@click.option(
    "--configfile",
    "-c",
    help="Configuration file to use instead of the package provided one.",
    required=False,
    default=None,
    show_default=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--environment",
    "-e",
    help="The environment to use, as group of the config file, except default",
    required=True,
    type=str,
)
def wsgi(configfile: pathlib.Path | None, environment: str) -> None:
    """Manage the web application."""
    if configfile is not None:
        _config.set_path(configfile)
    _config.set_environment(environment)


@wsgi.group()
def config() -> None:
    """Manage the configuration."""


@wsgi.group(cls=flask.cli.FlaskGroup, create_app=_wsgi.create_app)
def app() -> None:
    """Control of the flask application."""


@config.command()
@click.option(
    "--nbytes",
    "-n",
    help="Number of bytes",
    type=click.IntRange(
        min=secrets.DEFAULT_ENTROPY  # type: ignore[attr-defined]
    ),
    required=False,
    default=secrets.DEFAULT_ENTROPY,  # type: ignore[attr-defined]
    show_default=True,
)
def seckey(nbytes: int | None) -> None:
    """Create a new secret key and show the value.

    That value can then be copy-pasted into the secret key values in the
    configuration file.

    The minimum accepted length if the "reasonable" value provided by the
    secrets module in the python standard library.
    """
    click.echo(secrets.token_hex(nbytes))
