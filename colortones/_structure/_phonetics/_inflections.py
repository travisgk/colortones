"""
Filename: _inflections.py
Description: This file defines inflections, which are
             similar to tones, except that they represent
             the spoken tone in context and also contain
             other import contextual information.

Author: TravisGK
Version: 1.0

License: GNU License
"""

from ._transcription import to_zhuyin_and_ipa
from ._tones import *

# defines all the inflection values.
PUNCTUATION_INFLECTION = PUNCTUATION_TONE_NUM
HIGH_INFLECTION = HIGH_TONE_NUM
RISING_INFLECTION = RISING_TONE_NUM
LOW_INFLECTION = LOW_TONE_NUM
FALLING_INFLECTION = FALLING_TONE_NUM
NEUTRAL_INFLECTION = NEUTRAL_TONE_NUM
FULL_LOW_INFLECTION = 6
HALF_FALLING_INFLECTION = 7
NEUTRAL_HIGH_INFLECTION = 8
NEUTRAL_RISING_INFLECTION = 9
NEUTRAL_LOW_INFLECTION = 10
NEUTRAL_FALLING_INFLECTION = 11
RISING_LOW_INFLECTION = 12
RISING_YI_INFLECTION = 13
FALLING_YI_INFLECTION = 14
RISING_BU_INFLECTION = 15


# returns a string label identifying each inflection value.
TO_INFLECTION_LABEL = {
    PUNCTUATION_INFLECTION: "punctuation",
    HIGH_INFLECTION: "high",
    RISING_INFLECTION: "rising",
    LOW_INFLECTION: "low",
    FALLING_INFLECTION: "falling",
    NEUTRAL_INFLECTION: "neutral",
    FULL_LOW_INFLECTION: "full-low",
    HALF_FALLING_INFLECTION: "half-falling",
    NEUTRAL_HIGH_INFLECTION: "neutral-high",
    NEUTRAL_RISING_INFLECTION: "neutral-rising",
    NEUTRAL_LOW_INFLECTION: "neutral-low",
    NEUTRAL_FALLING_INFLECTION: "neutral-falling",
    RISING_LOW_INFLECTION: "rising-low",
    RISING_YI_INFLECTION: "rising-yi",
    FALLING_YI_INFLECTION: "falling-yi",
    RISING_BU_INFLECTION: "rising-bu",
}


# returns the inflection value for
# a specific neutral tone that follows a normal tone.
TO_INFLECTED_NEUTRAL = {
    HIGH_TONE_NUM: NEUTRAL_HIGH_INFLECTION,
    RISING_TONE_NUM: NEUTRAL_RISING_INFLECTION,
    LOW_TONE_NUM: NEUTRAL_LOW_INFLECTION,
    FALLING_TONE_NUM: NEUTRAL_FALLING_INFLECTION,
}


# returns the spoken tone. if the key isn't in here,
# then the key is already the spoken tone.
# spoken tones include the four traditional tones,
# a dummy punctuation tone (none), and the
# four possible ways the neutral tone can be inflected.
TO_SPOKEN_TONE = {
    NEUTRAL_INFLECTION: NEUTRAL_LOW_INFLECTION,  # defaults
    RISING_LOW_INFLECTION: RISING_TONE_NUM,
    RISING_YI_INFLECTION: RISING_TONE_NUM,
    FALLING_YI_INFLECTION: FALLING_TONE_NUM,
    RISING_BU_INFLECTION: RISING_TONE_NUM,
}


# returns the innate tone that syllable has in isolation.
# if the key isn't in here, then the key is already the tone value.
TO_INNATE_TONE = {
    FULL_LOW_INFLECTION: LOW_TONE_NUM,
    HALF_FALLING_INFLECTION: FALLING_TONE_NUM,
    NEUTRAL_HIGH_INFLECTION: NEUTRAL_TONE_NUM,
    NEUTRAL_RISING_INFLECTION: NEUTRAL_TONE_NUM,
    NEUTRAL_LOW_INFLECTION: NEUTRAL_TONE_NUM,
    NEUTRAL_FALLING_INFLECTION: NEUTRAL_TONE_NUM,
    RISING_LOW_INFLECTION: LOW_TONE_NUM,
    RISING_YI_INFLECTION: HIGH_TONE_NUM,
    FALLING_YI_INFLECTION: HIGH_TONE_NUM,
    RISING_BU_INFLECTION: FALLING_TONE_NUM,
}


# returns the spoken tone marker for the IPA.
TO_IPA_SUFFIX = {
    HIGH_INFLECTION: "˥",
    RISING_INFLECTION: "˧˥",
    LOW_INFLECTION: "˨˩",
    FALLING_INFLECTION: "˥˩",
    NEUTRAL_INFLECTION: "꜌",
    FULL_LOW_INFLECTION: "˨˩˦",
    HALF_FALLING_INFLECTION: "˥˧",
    NEUTRAL_HIGH_INFLECTION: "꜋",
    NEUTRAL_RISING_INFLECTION: "꜊",
    NEUTRAL_LOW_INFLECTION: "꜉",
    NEUTRAL_FALLING_INFLECTION: "꜌",
    RISING_LOW_INFLECTION: "˧˥",
    RISING_YI_INFLECTION: "˧˥",
    FALLING_YI_INFLECTION: "˥˩",
    RISING_BU_INFLECTION: "˧˥",
}


def inflection_is_neutral(inflection_num: int):
    """Returns True if the given inflection is some form of neutral tone."""
    return (
        inflection_num == NEUTRAL_TONE_NUM
        or inflection_num in TO_INFLECTED_NEUTRAL.values()
    )
