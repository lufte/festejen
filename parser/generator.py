#!/usr/bin/env python3
import pickle
import os
import sys
import re
from bisect import bisect_left as bisect
from random import random
from .index import SENTENCE_END, SENTENCE_START


LENGTH_THRESHOLD = 200
prefix_pattern = re.compile('\w* ?\w+(?=\W*$)')


def build(index, seed=None, all_caps=True):
    try:
        seed_suffix = prefix_pattern.search(seed).group(0).lower()
        comment_prefix = seed_suffix.capitalize()
        last_2_words = tuple(seed_suffix.split())
        if len(last_2_words) == 1:
            comment = _build(index, comment_prefix, (None, last_2_words[0]),
                             False, False)
        else:
            try:
                comment = _build(index, comment_prefix, last_2_words,
                                 False, False)
            except KeyError:
                comment = _build(index, last_2_words[1].title(),
                                 (None, last_2_words[1]), False, False)
    except (TypeError, AttributeError, KeyError):
        comment = _build(index, '', (None, SENTENCE_START), False, False)

    if all_caps:
        return comment.upper()
    else:
        return comment


def _get_next(options):
    tuples = list(options.items())
    index = [0]
    for _, p in tuples:
        index.append(index[-1] + p)
    return tuples[bisect(index, random()) - 1][0]


def _build(index, comment, last_2_words, open_question, open_exclamation):
    if last_2_words[1] == SENTENCE_END:
        last_2_words = (None, SENTENCE_START)

    if not last_2_words[0]:
        next_word = _get_next(index[1][last_2_words[1]])
    else:
        next_word = _get_next(index[2][last_2_words])

    end_comment = False
    if next_word == SENTENCE_END:
        if open_question:
            comment = comment + '?'
            open_question = False
        elif open_exclamation:
            comment = comment + '!'
            open_exclamation = False
        else:
            comment = comment + '.'
        end_comment = (
            random() > LENGTH_THRESHOLD / (len(comment) + LENGTH_THRESHOLD)
        )
    else:
        next_word_to_print = (
            next_word
            if last_2_words[1] not in (SENTENCE_END, SENTENCE_START)
            else next_word.title()
        )
        delimiter = ' ' if comment else ''
        comment = comment + delimiter + next_word_to_print
    if not end_comment:
        return _build(index, comment, (last_2_words[1], next_word),
                      open_question, open_exclamation)
    else:
        return comment


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),
                           '../index.pickle'), 'rb') as f:
        index = pickle.load(f)

    start_word = None
    if len(sys.argv) > 1 and sys.argv[1] in index:
        start_word = sys.argv[1]

    print(build(index, start_word))
