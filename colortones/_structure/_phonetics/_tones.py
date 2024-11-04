"""
Filename: _tones.py
Description: This file defines functionality
             to identify tone markers in pinyin.

Author: TravisGK
Version: 1.0

License: GNU License
"""

import json
import os

_APOSTROPHES = "'’"
CLAUSE_BREAKERS = "，；：（）,—;:～"
SENTENCE_ENDERS = "。！？、．.!?"
PUNCTUATION = _APOSTROPHES + CLAUSE_BREAKERS + SENTENCE_ENDERS

PUNCTUATION_TONE_NUM = -1
HIGH_TONE_NUM = 1
RISING_TONE_NUM = 2
LOW_TONE_NUM = 3
FALLING_TONE_NUM = 4
NEUTRAL_TONE_NUM = 5

PRIMARY_TONES = [
    HIGH_TONE_NUM,
    RISING_TONE_NUM,
    LOW_TONE_NUM,
    FALLING_TONE_NUM,
]

# this dictionary removes the tone marker from a char.
_TONE_TO_TONELESS = {}
_VOWEL_TO_TONE_NUM = {}


def _load_dicts():
    """Loads necessary dictionaries from .json files if not yet done."""
    global _TONE_TO_TONELESS, _VOWEL_TO_TONE_NUM
    if len(_TONE_TO_TONELESS) > 0:
        return  # already loaded.

    local_dir = os.path.dirname(os.path.abspath(__file__))
    tone_file_path = os.path.join(local_dir, "res", "_tones.json")
    with open(tone_file_path, "r", encoding="utf-8") as file:
        contents = json.load(file)
    _TONE_TO_TONELESS = contents["to-toneless"]
    _VOWEL_TO_TONE_NUM = contents["to-tone-num"]


def get_tone_num(syllable_str: str):
    """Returns a number indicating the pinyin syllable's tone."""
    if syllable_str[0] in PUNCTUATION:
        return PUNCTUATION_TONE_NUM

    _load_dicts()
    for char in syllable_str:
        tone_num = _VOWEL_TO_TONE_NUM.get(char)
        if tone_num is not None:
            return tone_num

    return NEUTRAL_TONE_NUM


def strip_tone_marker(syllable_str: str):
    """Returns the string with any tone markers removed."""
    _load_dicts()
    return "".join([_TONE_TO_TONELESS.get(c, c) for c in syllable_str])
