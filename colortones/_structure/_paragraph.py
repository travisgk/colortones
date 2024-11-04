"""
Filename: _paragraph.py
Description: This file contains class definitions for language structure.
             This encompasses: Syllables, Words, Sentences and Paragraphs.

Author: TravisGK
Version: 1.0

License: GNU License
"""

import logging
import re
import jieba
import pypinyin
from ._phonetics._inflections import *
from ._syllable import _make_syllable
from ._sequential_rules import (
    inflect_yi,
    inflect_bu,
    inflect_neutrals,
    apply_sequential_rule,
)

jieba.setLogLevel(logging.ERROR)

# these will use spaces between words.
_SPACED_OUTPUTS = ["pinyin", "ipa-root", "ipa", "pinyin-toneless"]


class Word:
    """
    A Word holds a list of syllable dictionaries.
    """

    def __init__(self, word: str):
        p = pypinyin.pinyin(word, style=pypinyin.Style.TONE)
        self.syllables = [
            _make_syllable(word[i], p[i][0])
            for i in range(len(word))
            if len(p) > 1 or p[0][0] != " "
        ]

    def __getitem__(self, index):
        return self.syllables[index]

    def __setitem__(self, key, value):
        self.syllables[key] = value

    def __iter__(self):
        return iter(self.syllables)

    def __len__(self):
        return len(self.syllables)

    def is_punct(self):
        # print(str(self.syllables[0].data["pinyin"]) + "\t" + str(self.syllables[0].is_punct()))
        return self.syllables[0].is_punct()

    def to_color_str(self, key, color_scheme):
        result = ""
        last_content = None
        for syllable in self.syllables:
            result += color_scheme[syllable["inflection-num"]][2]

            if (
                not syllable.is_punct()
                and key in _SPACED_OUTPUTS
                and last_content is not None
                and strip_tone_marker(syllable[key][0]) in "aeiou"
            ):
                content = "'" + syllable[key]
            elif syllable.is_punct():
                content = syllable["hanzi"]
            else:
                content = syllable[key]

            result += content
            result += "\033[0m"
            last_content = content

        return result


class Clause:
    """
    A Clause holds a list of words.
    """

    def __init__(
        self,
        clause_str: str = None,
        clauses_to_unite: list = [],
    ):
        """The list of clauses are Sentences that will be combined."""
        self.words = []
        if clause_str is not None:
            words_list = jieba.lcut(clause_str)
            for word_str in words_list:
                word = Word(word_str)
                if len(word) > 0:
                    self.words.append(word)
            self._postprocess_inflections()
        else:
            for clause in clauses_to_unite:
                self.words.extend(clause.words)

    def __getitem__(self, index):
        return self.words[index]

    def __iter__(self):
        return iter(self.words)

    def __len__(self):
        return len(self.words)

    def _postprocess_inflections(self):
        """
        Modifies the inflections so that they reflect their context.
        """
        if len(self.words) > 1 or (len(self.words) == 1 and len(self.words[0]) > 1):
            inflect_yi(self.words)
            inflect_bu(self.words)
            inflect_neutrals(self.words)
            apply_sequential_rule(self.words, LOW_INFLECTION, RISING_LOW_INFLECTION)
            apply_sequential_rule(
                self.words, FALLING_INFLECTION, HALF_FALLING_INFLECTION
            )

    def to_color_str(self, key, color_scheme):
        result = ""
        for i, word in enumerate(self.words):
            result += word.to_color_str(key, color_scheme)
            if (
                i + 1 < len(self.words)
                and not self.words[i + 1].is_punct()
                and key in _SPACED_OUTPUTS
            ):
                result += " "
        return result


class Paragraph:
    """
    A Paragraph holds a list of words.
    """

    def __init__(self, text_str: str):
        clause_strings = re.split(f"([{CLAUSE_BREAKERS + SENTENCE_ENDERS}])", text_str)
        self.sentences = []
        for clause_str in clause_strings:
            if len(clause_str) == 0:
                continue

            clause = Clause(clause_str)
            if len(clause) > 0:
                self.sentences.append(clause)
        self.sentences = Paragraph._join_clauses(self.sentences)

    def __getitem__(self, index):
        return self.sentences[index]

    def __iter__(self):
        return iter(self.sentences)

    def _join_clauses(clauses):
        """Connects clauses together as one sentence."""
        ITERATIONS = 5
        for _ in range(ITERATIONS):
            new_sentences = []

            index = 0
            while index < len(clauses):
                s = clauses[index]
                if (
                    index + 1 < len(clauses)
                    and len(clauses[index + 1]) == 1
                    and clauses[index + 1][-1][-1]["hanzi"] in SENTENCE_ENDERS
                ):
                    # unites the sentence-ending punctuation
                    # to the end of the current sentence.
                    next_s_1 = clauses[index + 1]
                    new_sentence = Clause(clauses_to_unite=[s, next_s_1])
                    new_sentences.append(new_sentence)
                    index += 2
                elif (
                    index + 2 < len(clauses)
                    and clauses[index + 1][-1][-1]["hanzi"] in CLAUSE_BREAKERS
                ):
                    # a clause-breaker unites the text on both
                    # its left and right sides.
                    next_s_1 = clauses[index + 1]
                    next_s_2 = clauses[index + 2]
                    new_sentence = Clause(clauses_to_unite=[s, next_s_1, next_s_2])
                    new_sentences.append(new_sentence)
                    index += 3
                else:
                    new_sentences.append(s)
                    index += 1

            clauses = new_sentences
        return clauses

    def to_color_str(self, key="hanzi", color_scheme=None):
        return "".join(c.to_color_str(key, color_scheme) for c in self.sentences)
