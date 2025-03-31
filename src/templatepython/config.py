"""Management of the configuration file and configuration selection."""

import os
import pathlib
import platform
import shutil
import tomllib
import typing

from templatepython import about

_CONFIG_FILE_ENVVAR = f"{about.name.upper()}_CONFIG_FILE"
_ENVIRONMENT_ENVVAR = f"{about.name.upper()}_ENVIRONMENT"
_EXPECTED_CONFIG_FILE_SUFFIX = ".toml"
_CONFIG_FILE_DEFAULT = pathlib.Path(about.location).joinpath(
    "_data", "wsgi_config_default.toml"
)


def set_path(value: pathlib.Path | str) -> None:
    """Set the config file name.

    The value is the provided value with user ~ expanded and symbolic links
    resolved.
    """
    if not isinstance(value, pathlib.Path):
        value = pathlib.Path(value)
    value = value.expanduser().resolve()
    os.environ[_CONFIG_FILE_ENVVAR] = value.as_posix()


def get_path() -> pathlib.Path:
    """Return the config file path.

    It is extracted from an enviromnent variable depending on the package name.

    If the value is not set, it is the path of the default configuration file
    in the package in itself. See set_filename.

    Raise
    -----
    BadFileExtensionError
    """
    ret = pathlib.Path(
        os.environ.get(_CONFIG_FILE_ENVVAR, _CONFIG_FILE_DEFAULT)
    )
    _check_file_extension(ret)
    return ret


def _load_file() -> dict[str, typing.Any]:
    with get_path().open("rb") as fh:
        return tomllib.load(fh)


def get_available_environments() -> tuple[str, ...]:
    """Return the available environments provided in the configur file."""
    return tuple(sorted(x for x in list(_load_file()) if x != "default"))


class EnvironmentNotSetError(ValueError):
    """The environment has not be set yet."""

    def __init__(self) -> None:
        """Create an instance."""
        super().__init__(self.msg)

    @property
    def msg(self) -> str:
        """The error message."""
        return "The environment is not set yet. See set_environment."


def get_selected_environment() -> str:
    """Return the name of the selected environment.

    Raise
    -----
    EnvironmentNotSetError
    """
    try:
        return os.environ["_ENVIRONMENT_ENVVAR"]
    except KeyError as e:
        raise EnvironmentNotSetError from e


class UnknownEnvironmentError(KeyError):
    """The requested environment is not available."""

    def __init__(self, value: str) -> None:
        """Create an instance."""
        self._requested = value
        self._available = get_available_environments()
        super().__init__(self.msg)

    @property
    def requested(self) -> str:
        """Provide the requested value."""
        return self._requested

    @property
    def available(self) -> tuple[str, ...]:
        """Provide the available values."""
        return self._available

    @property
    def msg(self) -> str:
        """Provide the error message shown by the exception."""
        requested = self.requested
        available = self.available
        return f"{requested=}, {available=}"


def set_environment(value: str) -> None:
    """Set the environment.

    The environment must be one of the environments available in the
    configuration file (see get_available_environments()).

    Note
    ----
    The 'default' environment is not eligible: it is intended to provide
    common values for all environments, and shall not be used directly.

    Raise
    -----
    UnknownEnvironmentError

    """
    if value not in get_available_environments():
        raise UnknownEnvironmentError(value)
    os.environ["_ENVIRONMENT_ENVVAR"] = value


def get_storage() -> pathlib.Path:
    """Return the storage associated to the environment."""
    return about.get_env_datadir(get_selected_environment())


def get_config() -> typing.Any:  # noqa: ANN401 C901
    """Return the configuration of the selected environment."""
    storage = get_storage()

    def _replace_storage(x: str) -> str:
        if not isinstance(x, str):
            return x
        return x.replace("{{STORAGE}}", storage.as_posix())

    # Loading the file
    vals = _load_file()

    # Adding the default values if not yet there.
    # Attention: we only support scalars and lists.
    ret = vals[get_selected_environment()].copy()
    if "default" in vals:
        defs = vals["default"].copy()
        for k, v in defs.items():
            if k not in ret:
                ret[k] = v
            elif isinstance(ret[k], list):
                for v2 in v:
                    if v2 not in ret[k]:
                        ret[k].append(v2)

    # Replacing the {{STORAGE}} values if exists
    for k, v in ret.items():
        if isinstance(v, list):
            ret[k] = [_replace_storage(v_) for v_ in v]
        else:
            ret[k] = _replace_storage(ret[k])

    return ret


class LocationIsInMyPackageError(IOError):
    """The file to export the config is in the path of the package."""

    def __init__(self, location: pathlib.Path | str) -> None:
        """Create an instance."""
        if not isinstance(location, pathlib.Path):
            location = pathlib.Path(location)
        self._location = location.expanduser().resolve()
        super().__init__(self.msg)

    @property
    def location(self) -> pathlib.Path:
        """The erroneous location."""
        return self._location

    @property
    def package_location(self) -> pathlib.Path:
        """The location of the package."""
        return about.location

    @property
    def msg(self) -> str:
        """The error message."""
        location = self.location
        package = self.package_location
        return f"{location=}, {package=}"


class BadFileExtensionError(IOError):
    """The extension of a file is not as expected."""

    def __init__(self, path: pathlib.Path | str, expected: str) -> None:
        """Create an instance."""
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        self._path = path
        self._expected = expected
        super().__init__(self.msg)

    @property
    def path(self) -> pathlib.Path:
        """The erroneous file path."""
        return self._path

    @property
    def expected(self) -> str:
        """The expected suffix."""
        return self._expected

    @property
    def msg(self) -> str:
        """The error message."""
        path = self.path
        expected = self.expected
        return f"{path=}, {expected=}"


def _check_file_extension(path: pathlib.Path | str) -> None:
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    candidate = path
    if platform.system() == "Windows":
        candidate = pathlib.Path(candidate.as_posix().lower())
    if candidate.suffix != _EXPECTED_CONFIG_FILE_SUFFIX:
        raise BadFileExtensionError(path, _EXPECTED_CONFIG_FILE_SUFFIX)


def copy_configuration_file(location: pathlib.Path | str) -> None:
    """Copy the configuration file.

    If set_filename has not been called before, it will copy the default
    configuration file, provided in the package.

    Raise
    -----
    BadFileExtensionError
    """
    f = get_path()
    t = pathlib.Path(location).expanduser().resolve()
    _check_file_extension(location)
    if about.location in t.parents:
        raise LocationIsInMyPackageError(t)
    shutil.copy(f, t)
