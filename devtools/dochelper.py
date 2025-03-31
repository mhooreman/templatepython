"""Documentation building facilities.

This is intended to be used in the project development, in the doc hatch
environment.
"""

import functools
import importlib
import pathlib
import shutil
import subprocess  # noqa: S404
import sys
import tempfile
import typing

import click
import tomllib


class DocHelper:
    """Build the package documentation and make a zip in the dist folder."""

    @property
    def project_dir(self) -> pathlib.Path:
        """The directory of the project."""
        ret = pathlib.Path(sys.argv[0]).resolve()
        while not ret.joinpath("pyproject.toml").exists():
            ret = ret.parent
        return ret

    @property
    def doc_dir(self) -> pathlib.Path:
        """The directory of the documentation.

        This is the "root" of the mkdocs tool.
        """
        return self.project_dir.joinpath("doc")

    @property
    def _project_configuration(self) -> typing.Any:  # noqa: ANN401
        """The configuration of the project.

        It comes from pyproject.toml.
        """
        with self.project_dir.joinpath("pyproject.toml").open("rb") as fh:
            return tomllib.load(fh)

    @property
    def package_name(self) -> str:
        """The name of the package."""
        return str(self._project_configuration["project"]["name"])

    @property
    def package_version(self) -> str:
        """The version of the package."""
        return str(importlib.import_module(self.package_name).about.version)

    @functools.cached_property  # Need cache because is random
    def distributed_dir(self) -> pathlib.Path:
        """The directory of the distributed doc, before zip compression."""
        return self.project_dir.joinpath(
            "dist", f"doc-{self.package_name}-{self.package_version}"
        )

    @property
    def distributed_zip(self) -> pathlib.Path:
        """The zip file containing the distributed doc."""
        # Cannot use with_prefix as the version number contains dots, which
        # makes confusion.
        dd = self.distributed_dir
        return dd.parent.joinpath(dd.name + ".zip")

    @property
    def built_dir(self) -> pathlib.Path:
        """The directory containing the built documentation."""
        return pathlib.Path(
            tempfile.TemporaryDirectory(
                ignore_cleanup_errors=True, delete=False
            ).name
        )

    @property
    def source_dir(self) -> pathlib.Path:
        """The directory containing the documentation source."""
        return self.doc_dir

    @classmethod
    def _run_mkdocs(cls, *args: str, cwd: pathlib.Path | None = None) -> None:
        """Run mkdocs with the provided command line arguments.

        If cwd is provided, this is executed from within that directory.
        """
        subprocess.run(
            ["mkdocs", *args],  # noqa: S607 S603
            cwd=cwd,
            check=True,
        )

    def _build_mkdocs(self) -> None:
        click.echo("Building documentation using mkdocs")
        self._run_mkdocs(
            "build",
            "--no-directory-urls",
            "--site-dir",
            self.built_dir.as_posix(),
            "--verbose",
            cwd=self.project_dir,
        )

    def _build_copy_mkdocs_to_dist(self) -> None:
        click.echo("Copying documentation to a distribution directory")
        if self.distributed_dir.exists():
            # It cannot exists for shutil.copytree ... should not exists but
            # nobody knows in case of bug...
            shutil.rmtree(self.distributed_dir)
        if not self.distributed_dir.parent.exists():
            self.distributed_dir.parent.mkdir(parents=True)
        shutil.copytree(self.built_dir, self.distributed_dir)

    def _build_compress(self) -> None:
        click.echo("Compressing the distribution directory")
        shutil.make_archive(
            str(self.distributed_zip.with_suffix("")),
            "zip",
            self.distributed_dir.parent,
            self.distributed_dir.name,
        )

    def _build_cleanup(self) -> None:
        if self.built_dir.exists():
            click.echo("Removing the documentation as built with mkdocs")
            shutil.rmtree(
                # Even if created using tempfile.TemoraryDirectory, we use the
                # pathlib.Path conversion of his name, which is more
                # convenient. So, it means that there is no cleanup available.
                self.built_dir
            )
        if self.distributed_dir.exists():
            click.echo("Removing the distribution directory")
            shutil.rmtree(self.distributed_dir)

    def build(self) -> None:
        """Build the documentation and creates the distributable zip."""
        # Setting had_error to True initially and changing it to False at the
        # end. If we do this in the other way, e.g. using the except clause, we
        # will have a bare except, which is against E722.
        had_error = True
        try:
            self._build_mkdocs()
            self._build_copy_mkdocs_to_dist()
            self._build_compress()
            had_error = False
        finally:
            self._build_cleanup()
        if had_error:
            if self.distributed_zip.exists():
                self.distributed_zip.unlink()
        else:
            click.echo(f"Created {self.distributed_zip}")

    def serve(self, *, address: str, port: int, browse: bool) -> None:
        """Show the documentation in a web browser."""
        addr = f"{address}:{port}"
        args = [
            "serve",
            "--dev-addr",
            addr,
            "--verbose",
        ]
        if browse:
            args.append("--open")
        self._run_mkdocs(*args, cwd=self.project_dir)

    def show_deps(self) -> None:
        """Show the dependencies given the documentation configuration."""
        self._run_mkdocs("get-deps", cwd=self.project_dir)


@click.group()
@click.pass_context
def dochelper(ctx: click.Context) -> None:
    """Provide helping hand for managing documentation."""
    ctx.obj = DocHelper()


@dochelper.command
@click.pass_obj
@click.option(
    "--port",
    "-p",
    type=int,
    required=False,
    default=8000,
    show_default=True,
    help="HTTP server port",
)
@click.option(
    "--address",
    "-a",
    type=str,
    required=False,
    default="localhost",
    show_default=True,
    help="HTTP server address to listen to",
)
@click.option(
    "--browse/--no-browse",
    required=False,
    default=True,
    show_default=True,
    help="If possible, opens a browser with the documentation (OS dependent).",
)
def serve(
    dh: DocHelper,
    address: str,
    port: int,
    browse: bool,  # noqa: FBT001
) -> None:
    """Start a web server showing the documentation.

    When the documentation is modified, the changes are automatically
    displayed.
    """
    click.echo("Starting a web server to display the documentation")
    dh.serve(address=address, port=port, browse=browse)


@dochelper.command
@click.pass_obj
def build(dh: DocHelper) -> None:
    """Build the documentation.

    It first builds the documentation using mkdocs. Then, the generated
    documentation is copied in a zip file, based on the tool version, in the
    dist directory.
    """
    dh.build()


@dochelper.command
@click.pass_obj
def show_deps(dh: DocHelper) -> None:
    """Show the dependencies given the documentation configuration."""
    dh.show_deps()


if __name__ == "__main__":
    dochelper()
