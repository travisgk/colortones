"""
Filename: _structure._syllable.py
Description: This file contains a class definition for the Syllable object,
             as well as other functionality to create these objects.

Author: TravisGK
Version: 1.0

License: GNU License
"""

from ._phonetics._inflections import *
from ._phonetics._transcription import to_zhuyin_and_ipa


def _get_zhuyin_marker(spoken_tone_num):
    """Returns the prefix and suffix for zhuyin, given the spoken tone."""
    if spoken_tone_num == RISING_TONE_NUM:
        return ("", "ˊ")
    elif spoken_tone_num in [LOW_TONE_NUM, FULL_LOW_INFLECTION]:
        return ("", "ˇ")
    elif spoken_tone_num in [FALLING_TONE_NUM, HALF_FALLING_INFLECTION]:
        return ("", "ˋ")
    elif inflection_is_neutral(spoken_tone_num):
        return ("˙", "")
    return ("", "")


class Syllable:
    """
    A Syllable contains various pronunciation and transcription information.
    """

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def is_punct(self):
        return self.data["inflection-num"] == PUNCTUATION_INFLECTION

    def update_inflection(self, inflection_num: int):
        spoken_tone_num = TO_SPOKEN_TONE.get(inflection_num, inflection_num)
        zh = _get_zhuyin_marker(spoken_tone_num)
        self.data["zhuyin-prefix"], self.data["zhuyin-suffix"] = zh
        self.data["zhuyin"] = zh[0] + self.data["zhuyin-root"] + zh[1]
        self.data["ipa-suffix"] = TO_IPA_SUFFIX.get(inflection_num, "")
        self.data["ipa"] = self.data["ipa-root"] + self.data["ipa-suffix"]
        self.data["inflection-desc"] = TO_INFLECTION_LABEL[inflection_num]
        self.data["spoken-tone-desc"] = TO_INFLECTION_LABEL[spoken_tone_num]
        self.data["inflection-num"] = inflection_num
        self.data["spoken-tone-num"] = spoken_tone_num


def _make_syllable(hanzi: str, pinyin: str):
    """Returns a Syllable object of the syllable's information."""
    inflection_num = get_tone_num(pinyin)  # assuming 5 is neutral (? UNCERTAIN)
    spoken_tone_num = TO_SPOKEN_TONE.get(inflection_num, inflection_num)
    innate_tone_num = TO_INNATE_TONE.get(inflection_num, inflection_num)

    pinyin_no_marker = strip_tone_marker(pinyin)
    zhuyin_root, ipa_root = to_zhuyin_and_ipa(pinyin_no_marker)

    zhuyin_prefix, zhuyin_suffix = _get_zhuyin_marker(spoken_tone_num)
    ipa_suffix = TO_IPA_SUFFIX.get(inflection_num, "")

    return Syllable(
        {
            "hanzi": hanzi,
            "pinyin": pinyin,
            "pinyin-toneless": pinyin_no_marker,
            "zhuyin": zhuyin_prefix + zhuyin_root + zhuyin_suffix,
            "zhuyin-prefix": zhuyin_prefix,
            "zhuyin-root": zhuyin_root,
            "zhuyin-suffix": zhuyin_suffix,
            "ipa": ipa_root + ipa_suffix,
            "ipa-root": ipa_root,
            "ipa-suffix": ipa_suffix,
            "inflection-desc": TO_INFLECTION_LABEL[inflection_num],
            "spoken-tone-desc": TO_INFLECTION_LABEL[spoken_tone_num],
            "innate-tone-desc": TO_INFLECTION_LABEL[innate_tone_num],
            "inflection-num": inflection_num,
            "spoken-tone-num": spoken_tone_num,
            "innate-tone-num": innate_tone_num,
        }
    )
