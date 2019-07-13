import re
from clean import VALID_NON_LETTER_SYMBOLS

SENTENCE_START = '^'
SENTENCE_END = '$'


def is_symbol(word):
    return (
        word not in (SENTENCE_START, SENTENCE_END)
        and re.match(r'[{symbols}]'.format(symbols=VALID_NON_LETTER_SYMBOLS), word)
    )


def index_words(comment, index):
    word_array = [w for w in comment.split(' ') if len(w) > 0]
    last_word = SENTENCE_START
    for current_word in word_array:
        if last_word not in index:
            index[last_word] = {}
        if not is_symbol(current_word):
            index[last_word][current_word] = index.get(last_word, {}).get(current_word, 0) + 1
            last_word = current_word
        else:
            index[last_word][SENTENCE_END] = index.get(last_word, {}).get(SENTENCE_END, 0) + 1
            last_word = SENTENCE_START


def gen_probabilities(index):
    for word in index.values():
        total = sum(word.values())
        for next_word in word.keys():
            word[next_word] = word[next_word] / total
