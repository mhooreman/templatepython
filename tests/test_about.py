"""Unit tests about semantic version."""

# type: ignore
# ruff: noqa: PLC2801 SLF001 D103 ANN001 ANN201 PLC2701

import pytest

from templatepython import _about


def test_semver_correct():
    _about.SemanticVersion.from_string("1.2.3")


def test_semver_s_incomplete():
    with pytest.raises(ValueError, match="invalid literal .*"):
        _about.SemanticVersion.from_string("1.2")


@pytest.mark.parametrize("suffix", ["a", "b", "c", "r"])
def test_semver_s_segment_invalid(suffix):
    s = f"1.0.0.{suffix}"
    with pytest.raises(_about.SegmentValueInvalidError):
        _about.SemanticVersion.from_string(s)


@pytest.mark.parametrize("value", ["1.-1.0", "-1.1.1", "1.1.-1"])
def test_semver_s__nrpart_negative(value):
    with pytest.raises(_about.PositiveIntegerValueError):
        _about.SemanticVersion.from_string(value)


@pytest.mark.parametrize("value", ["un.0.0", "0.un.0", "0.0.un"])
def test_semver_s_nrpart_text(value):
    with pytest.raises(ValueError, match="invalid literal .*"):
        _about.SemanticVersion.from_string(value)


@pytest.mark.parametrize(
    "args",
    [
        {"major": -1, "minor": 0, "patch": 0, "segment": None},
        {"major": 0, "minor": -1, "patch": 0, "segment": None},
        {"major": 0, "minor": 0, "patch": -1, "segment": None},
        {"major": 1.1, "minor": 0, "patch": 0, "segment": None},
        {"major": 0, "minor": 1.1, "patch": 0, "segment": None},
        {"major": 0, "minor": 0, "patch": 1.1, "segment": None},
        {"major": "un", "minor": 0, "patch": 0, "segment": None},
        {"major": 0, "minor": "un", "patch": 0, "segment": None},
        {"major": 0, "minor": 0, "patch": "un", "segment": None},
    ],
)
def test_semver_init_negative(args):
    with pytest.raises(_about.PositiveIntegerValueError):
        _about.SemanticVersion(**args)


@pytest.mark.parametrize(
    "args",
    [
        {"major": 1, "minor": 0, "patch": 0, "segment": "dev1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "alpha1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "beta1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "rc1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "post1"},
    ],
)
def test_semver_segment_valid(args):
    _about.SemanticVersion(**args)


@pytest.mark.parametrize(
    "args",
    [
        {"major": 1, "minor": 0, "patch": 0, "segment": "dev"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "alpha"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "beta"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "rc"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "post"},
    ],
)
def test_semver_segment_invalid(args):
    with pytest.raises(_about.SegmentValueInvalidError):
        _about.SemanticVersion(**args)


@pytest.mark.parametrize(
    "args",
    [
        {"major": 1, "minor": 0, "patch": 0, "segment": "a1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "b1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "c1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "pre1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "preview1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "r1"},
        {"major": 1, "minor": 0, "patch": 0, "segment": "rev1"},
    ],
)
def test_semver_segment_synonym(args):
    with pytest.raises(_about.SegmentKindSynonymUsedError):
        _about.SemanticVersion(**args)


@pytest.mark.parametrize(
    "args",
    [
        {"major": 1, "minor": 0, "patch": 0, "segment": "p1"},
    ],
)
def test_semver_segment_unknown(args):
    with pytest.raises(_about.SegmentKindUnknownError):
        _about.SemanticVersion(**args)


def test_gt():
    assert _about.SemanticVersion.from_string(
        "10.0.0"
    ) > _about.SemanticVersion.from_string("9.0.0")


def test_eq():
    assert _about.SemanticVersion.from_string(
        "10.0.0"
    ) == _about.SemanticVersion.from_string("10.0.0")


def test_segment_eq():
    assert _about._Segment("dev1") == _about._Segment("dev1")


def test_segment_ne():
    assert _about._Segment("dev1") != _about._Segment("dev2")


def test_segment_lt():
    assert _about._Segment("dev1").__lt__(_about._Segment("dev2"))


def test_segment_gt():
    assert _about._Segment("dev2").__gt__(_about._Segment("dev1"))


def test_segment_vs_non_segment():
    assert _about._Segment("dev2").__eq__("dev2") == NotImplemented


def test_segment_hash():
    assert isinstance(_about._Segment("dev2").__hash__(), int)
