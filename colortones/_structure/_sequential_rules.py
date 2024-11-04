"""
Filename: _sequential_rules.py
Description: This file defines the function used to make inflections follow 
             the 2-2-3 rule in Chinese. Regional variance is bound to occur.

Author: TravisGK
Version: 1.0

License: GNU License
"""

from ._phonetics._inflections import *


def _prev_syllable(
    words: list,
    current_word_i: int,
    current_syllable_i: int,
    stepback: int = 1,
):
    """
    Finds the Syllable that occurs before the provided index.

    Parameters:
    words (list): a list of Word objects (the contents of a Sentence).
    current_word_i (int): the index of the current Word in words.
    current_syllable_i (int): the index of the current Syllable in the Word.
    stepback (int): the amount of indices to move back away
                    from the provided current syllable location.

    Returns:
    Syllable: the Syllable object that precedes the given syllable location.
    """

    current_word = words[current_word_i]
    index = current_syllable_i - stepback
    if index >= 0:
        return current_word[index]  # previous syllable is in same word.

    # steps backward until the desired Syllable is found.
    while stepback > 0:
        stepback -= 1
        current_syllable_i -= 1
        if current_syllable_i < 0:
            current_word_i -= 1
            if current_word_i < 0:
                return None  # no previous syllable exists
            current_word = words[current_word_i]
            current_syllable_i = len(current_word) - 1

    return current_word[current_syllable_i]


def _next_syllable(
    words: list,
    current_word_i: int,
    current_syllable_i: int,
    step: int = 1,
):
    """
    Finds the Syllable that occurs after the provided index.

    Parameters:
    words (list): a list of Word objects (the contents of a Sentence).
    current_word_i (int): the index of the current Word in words.
    current_syllable_i (int): the index of the current Syllable in the Word.
    stepback (int): the amount of indices to move forward
                    from the provided current syllable location.

    Returns:
    Syllable: the Syllable object that follows the given syllable location.
    """

    current_word = words[current_word_i]
    index = current_syllable_i + step
    if index < len(current_word):
        return current_word[index]  # next syllable is in same word.

    # steps forward until the desired Syllable is found.
    while step > 0:
        step -= 1
        current_syllable_i += 1
        if current_syllable_i >= len(current_word):
            current_word_i += 1
            current_syllable_i = 0

            if current_word_i >= len(words):
                return None  # no next syllable exists

            current_word = words[current_word_i]

    return current_word[current_syllable_i]


def _update_syllable(syllable, infl: int):
    """
    Updates the given Syllable provided its true inflection.
    """
    syllable["inflection-num"] = infl
    syllable["inflection-desc"] = TO_INFLECTION_LABEL[infl]
    spoken = TO_SPOKEN_TONE.get(infl, infl)
    syllable["spoken-tone-num"] = spoken
    syllable["spoken-tone-desc"] = TO_INFLECTION_LABEL[spoken]


def inflect_yi(words: list):
    """
    Edits the given Words list in-place,
    with any Syllable that is 一 being changed to be inflected accurately.

    When 一 (yī) is followed by a 4th tone, it changes to a 2nd tone.
    When followed by any other tone, it changes to the 4th tone.
    """
    for i, word in enumerate(words):
        for j, syllable in enumerate(word):
            if syllable["hanzi"] == "一":
                # this syllable is the word 一.
                # ---
                # gets the previous syllable.
                # if there is one and it's 第, 一 will retain its high tone.
                prev_syllable = _prev_syllable(words, i, j)
                if prev_syllable is not None and prev_syllable["hanzi"] in "第":
                    continue

                # gets the next syllable, skips if there is None.
                next_syllable = _next_syllable(words, i, j)
                if next_syllable is None or (
                    next_syllable["hanzi"] in "月号零一二三四五六七八九十年"
                ):
                    continue

                # gets the inflection of the next syllable.
                next_tone = next_syllable["spoken-tone-num"]

                # determines the new inflection for this syllable.
                if next_tone == FALLING_TONE_NUM:
                    _update_syllable(syllable, RISING_YI_INFLECTION)
                elif next_tone in PRIMARY_TONES:
                    _update_syllable(syllable, FALLING_YI_INFLECTION)


def inflect_bu(words: list):
    """
    Edits the given Words list in-place,
    with any Syllable that is 不 being changed to be inflected accurately.

    When 不 (bù) is followed by a 4th tone, it changes to a 2nd tone.
    """
    for i, word in enumerate(words):
        for j, syllable in enumerate(word):
            if syllable["hanzi"] == "不":
                # this syllable is the word 不.
                # ---
                # gets the next syllable, skips if there is None.
                next_syllable = _next_syllable(words, i, j)
                if next_syllable is None:
                    continue

                # changes the inflection to a rising tone
                # if the next tone is a falling tone.
                next_tone = next_syllable["spoken-tone-num"]
                if next_tone == FALLING_TONE_NUM:
                    _update_syllable(syllable, RISING_BU_INFLECTION)


def inflect_neutrals(words: list):
    """
    Edits the given Words list in-place,
    with its neutral inflections modified
    to accurately correspond to the tones that come before them.
    """
    for i, word in enumerate(words):
        for j, syllable in enumerate(word):
            if syllable["innate-tone-num"] == NEUTRAL_TONE_NUM:
                # this syllable has a neutral tone.
                # ---
                # gets the previous syllable, skips if there is None.
                prev_syllable = _prev_syllable(words, i, j)
                if prev_syllable is None:
                    continue

                # gets previous tone, which will inflect the current neutral.
                prev_tone = prev_syllable["innate-tone-num"]
                if prev_tone in PRIMARY_TONES + [NEUTRAL_TONE_NUM]:
                    # the previous syllable can inflect it.
                    infl = TO_INFLECTED_NEUTRAL[prev_tone]
                    _update_syllable(syllable, infl)

                elif prev_tone in TO_INFLECTED_NEUTRAL.items():
                    # the previous syllable is neutral but can still inflect.
                    infl = prev["inflection-num"]
                    _update_syllable(syllable, infl)


_PRINT_APPLY_RULE_DEBUG = False


def _print_markup_clause(rule_num, markup_clause, old_inflection, new_inflection):
    """Prints the current inflection markup clause."""
    if not _PRINT_APPLY_RULE_DEBUG:
        return

    MARK = {PUNCTUATION_TONE_NUM: "█", old_inflection: "•", new_inflection: "^"}
    print(f"rule #{rule_num:>2d}:   ", end="")
    for i, word in enumerate(markup_clause):
        for j, mark in enumerate(word):
            print(MARK.get(mark, "x"), end=" ", flush=True)
        if i + 1 < len(markup_clause):
            print("   ", end="")
    print("\n")


def _find_monosyllable_series(markup_clause, inflections):
    """
    Returns a list of groupings of tuples that indicate a series of
    monosyllables composed of the given <inflections>,
    with each tuple containing:
        - the index in the given <markup_clause> list.
        - the subindex in the given <markup_clause> list.
    """
    series = [[]]
    for i, word in enumerate(markup_clause):
        current_series = series[-1]

        """
        Step 1) Searches for pure monosyllables:
                    If the current series is empty or its last appended
                    tuple was a monosyllable that came directly before
                    the current one,
                    
                    then the current monosyllable is appended
                    to the current series. 
                    
                    Otherwise, the current monosyllable is used to start
                    a new series of monosyllables.
        """
        if len(word) == 1 and word[0] in inflections:
            # this is a monosyllable that has a relevant inflection.
            if len(current_series) == 0 or current_series[-1][0] == i - 1:
                series[-1].append((i, 0))  # part of the current series.
            else:
                series.append([(i, 0)])  # starts a new series.
            continue

        if len(word) <= 1:
            continue

        """
        Step 2) Searches for monosyllables isolated 
                at the beginning/end of a word.
        """
        if word[0] in inflections and word[1] not in inflections:
            # monosyllables are at the beginning of a word.
            if len(current_series) == 0 or current_series[-1][0] == i - 1:
                series[-1].append((i, 0))  # part of a series.
            else:
                series.append([(i, 0)])  # starts a new series.
        elif word[-1] in inflections and word[-2] not in inflections:
            # monosyllables are at the end of a word.
            if len(current_series) == 0 or current_series[-1][0] == i - 1:
                series[-1].append((i, len(word) - 1))  # part of a series.
            else:
                series.append([(i, len(word) - 1)])  # starts a new series.
    return series


def apply_sequential_rule(
    words: list,
    old_inflection: int,
    new_inflection: int,
):
    """
    This function applies the 2-2-3 rule to the given list of Words.

    Parameters:
    words (list): a list of Word objects.
    old_inflection (int): the inflection number to replace.
    new_inflection (int): the inflection number the old is replaced with.
    """

    CERTAIN = PUNCTUATION_TONE_NUM
    UNKNOWN = 99  # indicates a tone which will be determined

    markup_clause = [
        [
            UNKNOWN if syllable["inflection-num"] == old_inflection else CERTAIN
            for syllable in word
        ]
        for word in words
    ]

    if all(mark == CERTAIN for word in markup_clause for mark in word):
        return
    _print_markup_clause(0, markup_clause, old_inflection, new_inflection)

    """
    
    Step 1) If the inflection is the last occurrence in a row in the overall
            clause, then it remains <old_inflection>.
    """
    for i, word in enumerate(markup_clause):
        for j in range(len(word)):
            if word[j] == UNKNOWN and (
                (i == len(markup_clause) - 1 and j == len(word) - 1)
                or _next_syllable(markup_clause, i, j) not in [None, UNKNOWN]
            ):
                markup_clause[i][j] = old_inflection
    _print_markup_clause(1, markup_clause, old_inflection, new_inflection)

    """
    
    Step 2) In a series of UNKNOWN marks under one multisyllable word,
            every UNKNOWN tone in the series is marked as <new_inflection>.
    """
    for i, word in enumerate(markup_clause):
        if len(word) > 1:
            for j in range(len(word) - 1):
                if markup_clause[i][j] == UNKNOWN:
                    markup_clause[i][j] = new_inflection
    _print_markup_clause(2, markup_clause, old_inflection, new_inflection)

    """
    
    Step 3) A series of two or more UNKNOWN monosyllable words are filled,
            depending on the series' length being odd or even respectively:
                - <new> <old> <new> <new> <old>
                - <new> <old> <new> <old>
    """
    monosyllable_series = _find_monosyllable_series(
        markup_clause, [old_inflection, new_inflection, UNKNOWN]
    )
    for series in monosyllable_series:
        if len(series) > 1:
            changes = True
            for i, occurrence in enumerate(series):
                occurrences_left = len(series) - 1 - i
                if occurrences_left == 1 and not changes:
                    changes = True

                w, s = occurrence
                if markup_clause[w][s] == UNKNOWN:
                    if changes:
                        markup_clause[w][s] = new_inflection
                    else:
                        markup_clause[w][s] = old_inflection

                changes = not changes
    _print_markup_clause(3, markup_clause, old_inflection, new_inflection)

    """
    Step 4) An UNKNOWN mark will become <new_inflection> if
            one of its own neighboring inflections is <old_inflection>
            and both of these neighboring inflections are not UNKNOWN.
    """
    for i, word in enumerate(markup_clause):
        for j in range(len(word)):
            if word[j] != UNKNOWN:
                # skips any inflections that aren't unknown.
                continue

            # looks for the next neighboring inflection.
            next_inflection = _next_syllable(markup_clause, i, j)
            if next_inflection in [UNKNOWN, None]:
                # the current unknown inflection cannot be determined
                # because the next neighboring inflection
                # is either nonexistentor it itself is unknown.
                continue

            if i == 0 and j == 0:
                # if the current index is at the very start of the clause,
                # then the program doesn't need
                # to search for the previous inflection.
                if next_inflection == old_inflection:
                    markup_clause[i][j] = new_inflection
                else:
                    markup_clause[i][j] = old_inflection
            else:
                # looks for the previous neighboring inflection.
                prev_inflection = _prev_syllable(markup_clause, i, j)
                if prev_inflection in [UNKNOWN, None]:
                    # the current unknown inflection cannot be determined
                    # because the next neighboring inflection
                    # is either nonexistent or it itself is unknown.
                    continue

                # sets the inflection using its neighbors.
                if (
                    prev_inflection == old_inflection
                    or next_inflection == old_inflection
                ):
                    # both neighboring inflections are known
                    # and one of them is <old_inflection>.
                    markup_clause[i][j] = new_inflection
                else:
                    # neither of the neighboring
                    # inflections are <old_inflection>.
                    markup_clause[i][j] = old_inflection
    _print_markup_clause(4, markup_clause, old_inflection, new_inflection)

    """
    Step 5) Moving from right-to-left, 

            if the inflection that comes after
            the current UNKNOWN inflection is <old_inflection>,

            then the current UNKNOWN inflection becomes <new_inflection>.

            Otherwise, the UNKNOWN mark will become <old_inflection>.
    """
    for i in range(len(markup_clause) - 1, -1, -1):
        word = markup_clause[i]
        for j in range(len(word) - 1, -1, -1):
            if word[j] != UNKNOWN:
                # this inflection is already known.
                continue

            # searches rightward.
            next_inflection = _next_syllable(markup_clause, i, j)
            if next_inflection == old_inflection:
                markup_clause[i][j] = new_inflection
            else:
                markup_clause[i][j] = old_inflection
    _print_markup_clause(5, markup_clause, old_inflection, new_inflection)

    """
    Step 6) If a series of three monosyllables has a prior inflection
            that's nonexistent or CERTAIN, and the series itself is composed of
            a series of <old_inflection> and <new_inflection> such that:
                (CERTAIN), <new>, <new>, <old>
                (CERTAIN), <new>, <new>, <new>

            then the first occurrence of that monosyllable series
            will become <old_inflection>.
    """
    for series in monosyllable_series:
        if len(series) != 3:
            continue

        w_0, s_0 = series[0]
        w_1, s_1 = series[1]
        w_2, s_2 = series[2]

        syl_0 = markup_clause[w_0][s_0]
        syl_1 = markup_clause[w_1][s_1]
        syl_2 = markup_clause[w_2][s_2]

        if (
            all(s == new_inflection for s in [syl_0, syl_1])
            and syl_2 in [old_inflection, new_inflection]
            and (w_0 == 0 or markup_clause[w_0 - 1][-1] == CERTAIN)
        ):
            markup_clause[w_0][s_0] = new_inflection
    _print_markup_clause(6, markup_clause, old_inflection, new_inflection)

    """
    Step 7) If a series of four monosyllables has a prior inflection 
            that's nonexistent or CERTAIN, and the series itself is composed
            of a series of <old_inflection> or <new_inflection> such that:
                (CERTAIN), <new>, <old>, <new>, <old>

            then the first inflection will become <old_inflection>
            and the second inflection becomes <new_inflection>.
    """
    for series in monosyllable_series:
        if len(series) != 4:
            continue

        w_0, s_0 = series[0]
        w_1, s_1 = series[1]
        w_2, s_2 = series[2]
        w_3, s_3 = series[3]
        syl_0 = markup_clause[w_0][s_0]
        syl_1 = markup_clause[w_1][s_1]
        syl_2 = markup_clause[w_2][s_2]
        syl_3 = markup_clause[w_3][s_3]

        if (
            syl_0 == new_inflection
            and syl_1 == old_inflection
            and syl_2 == new_inflection
            and syl_3 == old_inflection
            and (w_0 == 0 or markup_clause[w_0 - 1][-1] == CERTAIN)
            and (
                w_3 + 1 >= len(markup_clause)
                or (
                    len(markup_clause[w_3 + 1]) == 1
                    and markup_clause[w_3 + 1][0] == CERTAIN
                )
                or (markup_clause[w_3 + 1][0] != new_inflection)
            )
        ):
            markup_clause[w_0][s_0] = old_inflection
            markup_clause[w_1][s_1] = new_inflection
    _print_markup_clause(7, markup_clause, old_inflection, new_inflection)

    """
    Result) Copies the inflections back.
    """
    for i, mark_word in enumerate(markup_clause):
        for j, inflection in enumerate(mark_word):
            if inflection not in [UNKNOWN, CERTAIN]:
                words[i][j].update_inflection(inflection)
