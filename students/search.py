"""Typo-tolerant matching for the student search box (standard library only)."""
from difflib import SequenceMatcher


def _close(token, word):
    """A query token matches a word when it appears in it or is close to it."""
    if token in word:
        return True
    return len(token) >= 3 and SequenceMatcher(None, token, word).ratio() >= 0.65


def fuzzy_match(query, text):
    """True when every word of `query` loosely matches a word of `text`.

    Handles accents of normal typing: partial words ("mar"), skipped letters
    ("msria" -> Maria) and swapped endings ("reyz" -> Reyes).
    """
    query = " ".join(query.lower().split())
    if not query:
        return True
    text = text.lower()
    if query in text:
        return True
    words = text.replace(",", " ").split()
    return all(any(_close(token, word) for word in words) for token in query.split())
