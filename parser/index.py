#!/usr/bin/env python3
import json
import re
import os
import sqlite3
from clean import VALID_NON_LETTER_SYMBOLS, clean


SENTENCE_START = '^'
SENTENCE_END = '$'


def _is_symbol(word):
    return (
        word not in (SENTENCE_START, SENTENCE_END)
        and re.match(r'[{symbols}]'.format(symbols=VALID_NON_LETTER_SYMBOLS),
                     word)
    )


def _gen_count_index(comments):
    index = {}
    for comment in comments:
        word_array = [w for w in comment.split(' ') if len(w) > 0]
        last_word = SENTENCE_START
        for current_word in word_array:
            if last_word not in index:
                index[last_word] = {}
            if not _is_symbol(current_word):
                index[last_word][current_word] = (index[last_word]
                                                  .get(current_word, 0) + 1)
                last_word = current_word
            elif last_word != SENTENCE_START:
                index[last_word][SENTENCE_END] = (index[last_word]
                                                  .get(SENTENCE_END, 0) + 1)
                last_word = SENTENCE_START

        if last_word not in (SENTENCE_START, SENTENCE_END):
            if last_word not in index:
                index[last_word] = {}
            index[last_word][SENTENCE_END] = (index[last_word]
                                              .get(SENTENCE_END, 0) + 1)

    return index


def _gen_probability_index(count_index):
    index ={}
    for first_word, next_words in count_index.items():
        total = sum(next_words.values())
        index[first_word] = {}
        for next_word in next_words:
            index[first_word][next_word] = next_words[next_word] / total
    return index


if __name__ == '__main__':
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__),
                                              '../festejen.db'))
    cursor = connection.cursor()
    count_index = _gen_count_index(
        clean(row[0]) for row  in cursor.execute(
            'select content from comment where content is not null',
        )
    )
    connection.commit()
    connection.close()
    probability_index = _gen_probability_index(count_index)
    with open(os.path.join(os.path.dirname(__file__),
                           '../index.json'), 'w') as f:
        json.dump(probability_index, f)
