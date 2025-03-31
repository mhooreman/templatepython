"""Package information with semantic versioning features.

The __version__ constant is the traditional version string, while the
about.version value is a semantic version.

Semantic versions are provided as the SemanticVersion class.
"""

from __future__ import annotations

import dataclasses
import functools
import os
import pathlib
import re
import typing


class SegmentValueInvalidError(ValueError):
    """The segment value is incorrect."""

    def __init__(self, value: str, reason: str) -> None:
        """Construct an instance."""
        msg = f"{value=}, {reason=}"
        super().__init__(msg)


class SegmentKindSynonymUsedError(ValueError):
    """The segment kind is a synonym of acceptable value."""

    def __init__(self, value: str, expected: str) -> None:
        """Construct an instance."""
        msg = f"{value=}, {expected=}"
        super().__init__(msg)


class PositiveIntegerValueError(ValueError):
    """The proposed value cannot be converted to a positive integer."""

    def __init__(
        self, field: str, value: str | int | None, reason: str | Exception
    ) -> None:
        """Construct an instance."""
        msg = f"{field=}, {value=}, {reason=}"
        super().__init__(msg)


class SegmentKindUnknownError(ValueError):
    """The segment kind is unknown."""


def _verify_number(value: int | str, field_label: str) -> int:
    ret = value
    if isinstance(ret, str):
        try:
            ret = int(ret, base=10)
        except (ValueError, TypeError) as e:
            raise PositiveIntegerValueError(field_label, ret, e) from e
    if not isinstance(ret, int):
        raise PositiveIntegerValueError(
            field_label, ret, "Neither int nor str"
        )
    if ret < 0:
        raise PositiveIntegerValueError(field_label, ret, "Negative")
    return ret


@functools.total_ordering
class _Segment:
    _SEGMENT_SPLIT_RE = re.compile(r"^([^0-9]+)([0-9]+)$")

    def __init__(self, value: str | None) -> None:
        if value is None:
            self._kind = None
            self._number = None
            return

        if m := self._SEGMENT_SPLIT_RE.match(value):
            g = m.groups()
            self._kind = self._verify_kind(g[0])
            self._number = _verify_number(g[1], "segment.number")
        else:
            raise SegmentValueInvalidError(value, "Cannot extract parts")

    @property
    def kind(self) -> str | None:
        return self._kind

    @property
    def number(self) -> int | None:
        return self._number

    @classmethod
    def _verify_kind(cls, value: str) -> str:
        match value:
            case "dev" | "alpha" | "beta" | "rc" | "post":
                return value
            case "a":
                raise SegmentKindSynonymUsedError(value, "alpha")
            case "b":
                raise SegmentKindSynonymUsedError(value, "beta")
            case "c" | "pre" | "preview":
                raise SegmentKindSynonymUsedError(value, "rc")
            case "r" | "rev":
                raise SegmentKindSynonymUsedError(value, "post")
            case _:
                raise SegmentKindUnknownError(value)

    @property
    def sort_key(
        self,
    ) -> tuple[int | str | None, ...]:
        """Return a tuple used to sort self."""
        a = {
            "dev": 0,
            "alpha": 1,
            "beta": 2,
            "rc": 3,
            None: 4,
            "post": 5,
        }[self.kind]
        b = self.number
        return (a, b)

    def __eq__(self, other: object) -> bool:
        """Return True if other is the same version."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sort_key.__eq__(other.sort_key)

    def __lt__(self, other: object) -> bool:
        """Return True if other is a lower version."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sort_key.__lt__(other.sort_key)

    def __hash__(self) -> int:
        """Provide the hash of this version, based on his elements."""
        return (self.kind, self.number).__hash__()

    def __str__(self) -> str:
        """Return str(self).

        This is the intuitive string value for a version segment.
        """
        if self.isnone:
            return ""
        return f"{self.kind}{self.number}"

    def __repr__(self) -> str:
        """Return repr(self).

        This is super().__repr__() plus ': str(self)'.
        """
        return f"{super().__repr__()}: {self!s}"

    @property
    def isnone(self) -> bool:
        """Return True if self corresponds to no segment."""
        if (self.kind is None) != (self.number is None):
            msg = "Only one of kind and number is None"
            raise ValueError(msg)
        return self.kind is None


@functools.total_ordering
class SemanticVersion:
    """A semantic version handler, with sorting capacity."""

    def __init__(
        self, *, major: int, minor: int, patch: int, segment: str | None = None
    ) -> None:
        """Construct an instance."""
        self._major = _verify_number(major, "major")
        self._minor = _verify_number(minor, "minor")
        self._patch = _verify_number(patch, "patch")
        self._segment = _Segment(segment)

    @property
    def major(self) -> int:
        """Return the major version number."""
        return self._major

    @property
    def minor(self) -> int:
        """Return the minor version number."""
        return self._minor

    @property
    def patch(self) -> int:
        """Return the patch version number."""
        return self._patch

    @property
    def segment(self) -> _Segment:
        """Return the segment version number."""
        return self._segment

    @classmethod
    def from_string(cls, string: str) -> SemanticVersion:
        """Create the instance from the traditional string."""
        segment: str | None

        def _to_int(x: str) -> int:
            if x is None:
                raise ValueError(x)
            return int(x, base=10)

        s = string.split(".")
        if len(s) > 4:  # noqa: PLR2004
            msg = f"Cannot parse {string}: too much elements"
            raise ValueError(msg)
        while len(s) < 4:  # noqa: PLR2004
            s.append("")

        major, minor, patch = (_to_int(x) for x in s[:-1])
        segment = s[-1].strip()  # Still a string, as required by __init__
        if not segment:
            segment = None
        return cls(major=major, minor=minor, patch=patch, segment=segment)

    @classmethod
    def _segment_text_to_number(cls, txt: str | None) -> int:
        match txt:
            case "dev":
                return 1
            case "a" | "alpha":
                return 2
            case "b" | "beta":
                return 3
            case "c" | "rc" | "pre" | "preview":
                return 4
            case None:
                return 5
            case "r" | "rev" | "post":
                return 6
            case _:
                raise ValueError(txt)

    @property
    def sort_key(
        self,
    ) -> tuple[typing.Any, ...]:
        """Return a tuple used to sort self."""
        return (
            self.major,
            self.minor,
            self.patch,
            self.segment.sort_key,
        )

    def __eq__(self, other: object) -> bool:
        """Return True if other is the same version."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sort_key.__eq__(other.sort_key)

    def __lt__(self, other: object) -> bool:
        """Return True if other is a lower version."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sort_key.__lt__(other.sort_key)

    def __hash__(self) -> int:
        """Provide the hash of this version, based on his elements."""
        return (self.major, self.minor, self.patch, self.segment).__hash__()

    def __str__(self) -> str:
        """Return str(self).

        This is the intuitive string value for a version, meaning the
        traditional version string.
        """
        elts: list[int | _Segment]
        elts = [self.major, self.minor, self.patch]
        if not self.segment.isnone:
            elts.append(self.segment)
        return ".".join(map(str, elts))

    def __repr__(self) -> str:
        """Return repr(self).

        This is super().__repr__() plus ': str(self)'.
        """
        return f"{super().__repr__()}: {self!s}"


__version__ = "0.0.0"

_NAME = __name__.rsplit(".", 1)[0]
_DESCRIPTION = "Python template with flask"
_VERSION = SemanticVersion.from_string(__version__)
_LOCATION = pathlib.Path(__file__).parent.resolve()
_AUTHOR = "Michael Hooreman"
_AUTHOR_EMAIL = "mhooreman@icloud.com"


def _get_base_storage() -> pathlib.Path:
    """Return the base data directory.

    It is the {name}_data subdirectory of standard data directory, where
    {name} is the package name

    The standard data directory:
        - On windows, is %LOCALAPPDATA%
        - Otherwize, is $XDG_DATA_HOME or the standard equivalent if not
          defined ($HOME/.local/share, see
          https://specifications.freedesktop.org/basedir-spec/latest/)
    """
    if os.name == "nt":
        ret = pathlib.Path(os.environ["LOCALAPPDATA"])
    else:
        try:
            ret = pathlib.Path(os.environ["XDG_DATA_HOME"])
        except KeyError:
            try:
                ret = pathlib.Path(os.environ["HOME"])
            except KeyError:
                ret = pathlib.Path("~")
            ret = ret.joinpath(".local", "share")
    ret = ret.expanduser().resolve()
    ret /= f"{_NAME}_data"
    return ret


@dataclasses.dataclass(frozen=True)
class About:
    """Representation of information about the package.

    This data class is intended to be consturcted only using default values.
    This has to be considered as a factory, and the instance is about at the
    module level.
    """

    name: str = _NAME
    description: str = _DESCRIPTION
    version: SemanticVersion = _VERSION
    location: pathlib.Path = _LOCATION
    author: str = _AUTHOR
    author_email: str = _AUTHOR_EMAIL
    datadir: pathlib.Path = dataclasses.field(
        # Using this pattern as the _get_base_storage returns a mutable object,
        # which is a problem in linting (RUF009).
        # Note that the default factory shall be a calable...
        default_factory=_get_base_storage
    )


about = About()
