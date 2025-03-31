"""Test import of all the modules."""

import importlib
import typing

import pytest  # type: ignore[import-not-found]

import templatepython


def _gen_modules() -> typing.Iterator[str]:
    pkg_loc = templatepython.about.location
    for f in pkg_loc.glob("**/*.py"):
        m: typing.Any
        m = f.relative_to(pkg_loc.parent).with_suffix("")
        m = m.parts
        if m[-1] == "__init__":
            m = m[:-1]
        m = ".".join(m)
        yield m


@pytest.mark.parametrize("module", list(_gen_modules()))  # type: ignore[misc]
def test_module(module: str) -> None:
    """Test import of a module.

    The module is described by his classpath (a.b.c....)
    """
    importlib.import_module(module)
    assert True
