"""Utilities for working with blog post tags."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

# Tags shown on the site must be part of this controlled vocabulary.
ALLOWED_TAGS: Sequence[str] = ("post", "wip", "talk", "notes")


def normalize_and_validate_tags(
    raw_tags: Iterable[object] | None,
    *,
    allowed: Sequence[str] = ALLOWED_TAGS,
) -> Tuple[List[str], List[str]]:
    """Normalise a collection of tag values and surface any invalid entries.

    Parameters
    ----------
    raw_tags:
        Any iterable collection that may contain tag-like objects. Strings will
        be stripped of leading/trailing whitespace and lower-cased. Non-string
        values are considered invalid and ignored in the normalised output.
    allowed:
        A collection of lowercase tag values that are considered valid.

    Returns
    -------
    tuple(list[str], list[str])
        A pair containing the list of unique, normalised tags that are valid
        and a list of invalid tag representations (as strings) encountered
        during processing.
    """

    if raw_tags is None:
        return [], []

    if isinstance(raw_tags, str):
        raw_iterable: Iterable[object] = [raw_tags]
    else:
        raw_iterable = raw_tags

    normalised: List[str] = []
    invalid: List[str] = []
    seen = set()

    for tag in raw_iterable:
        if isinstance(tag, str):
            cleaned = tag.strip().lower()
        else:
            cleaned = ""

        if not cleaned:
            if isinstance(tag, str) and tag.strip() == "":
                continue
            if tag not in (None, "", []):
                invalid.append(str(tag).strip())
            continue

        if cleaned in allowed:
            if cleaned not in seen:
                normalised.append(cleaned)
                seen.add(cleaned)
        else:
            invalid.append(cleaned if isinstance(tag, str) else str(tag).strip())

    return normalised, invalid

