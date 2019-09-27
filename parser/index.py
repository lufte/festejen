# Copyright © 2019 Javier Ayres
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

#!/usr/bin/env python3
import pickle
import re
import os
import sqlite3
from .clean import VALID_NON_LETTER_SYMBOLS, clean


SENTENCE_START = '^'
SENTENCE_END = '$'


def _is_symbol(word):
    return (
        word not in (SENTENCE_START, SENTENCE_END)
        and re.match(r'[{symbols}]'.format(symbols=VALID_NON_LETTER_SYMBOLS),
                     word)
    )


def _gen_single_count_index(comments):
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


def _gen_double_count_index(comments):
    index = {}
    for comment in comments:
        word_array = [w for w in comment.split(' ') if len(w) > 0]
        last_2_words = (None, SENTENCE_START)
        for current_word in word_array:
            if last_2_words[1] == SENTENCE_START:
                last_2_words = (SENTENCE_START, current_word)
                continue

            if last_2_words not in index:
                index[last_2_words] = {}

            if not _is_symbol(current_word):
                index[last_2_words][current_word] = (index[last_2_words]
                                                     .get(current_word, 0) + 1)
                last_2_words = (last_2_words[1], current_word)
            elif last_2_words[1] != SENTENCE_START:
                index[last_2_words][SENTENCE_END] = (index[last_2_words]
                                                     .get(SENTENCE_END, 0) + 1)
                last_2_words = (None, SENTENCE_START)

        if last_2_words[1] != SENTENCE_START:
            if last_2_words not in index:
                index[last_2_words] = {}
            index[last_2_words][SENTENCE_END] = (index[last_2_words]
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
    query = """
        select content from comment
        join article on comment.article_id = article.id
        where content is not null
        and url like 'https://www.elpais.com.uy/informacion/%'
    """
    single_count_index = _gen_single_count_index(
        clean(row[0]) for row  in cursor.execute(query)
    )
    double_count_index = _gen_double_count_index(
        clean(row[0]) for row  in cursor.execute(query)
    )
    connection.commit()
    connection.close()
    final_index = {
        1: _gen_probability_index(single_count_index),
        2: _gen_probability_index(double_count_index),
    }
    with open(os.path.join(os.path.dirname(__file__),
                           '../index.pickle'), 'wb') as f:
        pickle.dump(final_index, f, protocol=pickle.HIGHEST_PROTOCOL)
