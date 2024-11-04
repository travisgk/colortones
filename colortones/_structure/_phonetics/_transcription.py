"""
Filename: _transcription.py
Description: This file contains functionality to transcribe pinyin into zhuyin 
             and the International Phonetic Alphabet.

Author: TravisGK
Version: 1.0

License: GNU License
"""

import json
import os
from ._tones import PUNCTUATION

_TO_EXCEPTIONS = {}
_TO_INITIALS = {}
_TO_FINALS = {}
_TO_SEGMENTS = {}


def _load_dicts():
    """Loads the necessary transcription dictionaries if not yet done."""
    global _TO_EXCEPTIONS, _TO_INITIALS, _TO_FINALS, _TO_SEGMENTS
    if len(_TO_EXCEPTIONS) > 0:
        return  # already loaded.

    local_dir = os.path.dirname(os.path.abspath(__file__))
    tr_path = os.path.join(local_dir, "res", "_transcription.json")
    with open(tr_path, "r", encoding="utf-8") as file:
        contents = json.load(file)
    _TO_EXCEPTIONS = contents["exceptions"]
    _TO_INITIALS = contents["initials"]
    _TO_FINALS = contents["finals"]
    _TO_SEGMENTS = contents["pinyin-segments"]


def to_zhuyin_and_ipa(pinyin_syllable: str):
    """Returns the root transcriptions for Zhuyin and IPA."""
    _load_dicts()
    p = pinyin_syllable

    if len(p) == 1 and p[0] in PUNCTUATION + " ":
        return "", ""

    result = _TO_EXCEPTIONS.get(p)
    if result is not None:
        return result

    start, end = None, None
    if len(p) > 1 and p[1] == "h" and p[0] in "zcs":  # zh, ch, sh
        start, end = p[:2], p[2:]
    elif len(p) > 0 and p[0] in "bpmfdtnlgkhjqxrzcs":  # single letter initial
        start, end = p[0], p[1:]

    if start is None:  # vowel initial
        initial = ("", "")
        segment = _TO_SEGMENTS.get(p)
        ending = _TO_FINALS[p] if segment is None else _TO_FINALS[segment]
    else:  # consonant initial
        initial = _TO_INITIALS[start]
        ending = _TO_FINALS[end]

    # constructs the results and returns them.
    zhuyin = initial[0] + ending[0]
    ipa = initial[1] + ending[1]

    return zhuyin, ipa
