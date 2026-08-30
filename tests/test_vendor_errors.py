"""The vendor fault texts and their provenance markers."""

from roombapy.const import ROOMBA_ERROR_MESSAGES
from roombapy.vendor_errors import (
    UNVERIFIED_OVERLAP,
    VENDOR_ERROR_TEXTS,
    vendor_error_text,
)

LANGUAGES = ("de", "en", "es", "fr", "it", "nl", "pl", "pt")


def test_every_code_has_every_language() -> None:
    """A missing language would surface as a silent English fallback."""
    for code, texts in VENDOR_ERROR_TEXTS.items():
        missing = set(LANGUAGES) - set(texts)
        assert not missing, f"code {code} missing {sorted(missing)}"


def test_overlap_set_matches_reality() -> None:
    """The unverified set must be exactly the codes we also label ourselves.

    If either table gains a code, this fails — which is the point: the
    provenance caveat has to stay accurate, not just accurate once.
    """
    actual = set(VENDOR_ERROR_TEXTS) & set(ROOMBA_ERROR_MESSAGES)
    assert actual == set(UNVERIFIED_OVERLAP)


def test_lookup_falls_back_to_english() -> None:
    """An unsupported language yields English rather than nothing."""
    result = vendor_error_text(6, "zz")
    assert result is not None
    assert result == VENDOR_ERROR_TEXTS[6]["en"]


def test_unknown_code_is_none_not_an_error() -> None:
    """Callers should not have to guard the lookup."""
    assert vendor_error_text(9999) is None
