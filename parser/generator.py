from bisect import bisect_left as bisect
from random import random
from split import SENTENCE_END, SENTENCE_START


def build(index):
    return _build(index, '', SENTENCE_START, False, False)


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
            comment = comment + ' ' + '?'
            open_question = False
        elif open_exclamation:
            comment = comment + ' ' + '!'
            open_exclamation = False
        else:
            comment = comment + ' ' + '.'
        end_comment = random() > 0.5
    else:
        comment = comment + ' ' + next_word
    if not end_comment:
        return _build(index, comment, next_word, open_question, open_exclamation)
    else:
        return comment


