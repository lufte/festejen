#!/usr/bin/env python3
import json
import os
import sys
from bisect import bisect_left as bisect
from random import random
from index import SENTENCE_END, SENTENCE_START


def build(index, start_word=None, all_caps=True):
    if start_word:
        comment = _build(index, start_word.title(), start_word, False, False)
    else:
        comment = _build(index, '', SENTENCE_START, False, False)
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


def _build(index, comment, last_word, open_question, open_exclamation):
    next_word = (_get_next(index[SENTENCE_START])
                 if last_word == SENTENCE_END
                 else _get_next(index[last_word]))
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
        end_comment = random() > 0.5
    else:
        next_word_to_print = (
            next_word
            if last_word not in (SENTENCE_END, SENTENCE_START)
            else next_word.title()
        )
        delimiter = ' ' if comment else ''
        comment = comment + delimiter + next_word_to_print
    if not end_comment:
        return _build(index, comment, next_word, open_question,
                      open_exclamation)
    else:
        return comment


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), '../index.json')) as f:
        index = json.load(f)

    start_word = None
    if len(sys.argv) > 1 and sys.argv[1] in index:
        start_word = sys.argv[1]

    print(build(index, start_word))
