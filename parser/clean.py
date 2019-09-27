# Copyright © 2019 Javier Ayres
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import re
from function_pipe import FunctionNode


VALID_NON_LETTER_SYMBOLS = ':¡!¿?.'


@FunctionNode
def clean_case(comment):
    return comment.lower()


@FunctionNode
def clean_invalid_diacritics(comment):
    comment = comment.replace('à', 'á')
    comment = comment.replace('è', 'é')
    comment = comment.replace('ì', 'í')
    comment = comment.replace('ò', 'ó')
    comment = comment.replace('ù', 'ú')
    return comment


@FunctionNode
def clean_symbols(comment):
    return re.sub(r'[^ 0-9a-zñäëïöüáéíóú{}]'.format(VALID_NON_LETTER_SYMBOLS), '', comment)


@FunctionNode
def break_symbols(comment):
    comment = re.sub(r'([{symbols}])(\w)'.format(symbols=VALID_NON_LETTER_SYMBOLS),
                     r'\1 \2',
                     comment)
    comment = re.sub(r'(\w)([{symbols}])'.format(symbols=VALID_NON_LETTER_SYMBOLS),
                     r'\1 \2',
                     comment)
    return comment


@FunctionNode
def clean_repetition(comment):
    return re.sub(r'([{symbols}])[{symbols} ]*[{symbols}]'.format(symbols=VALID_NON_LETTER_SYMBOLS),
                  r'\1',
                  comment)


@FunctionNode
def clean_symbols_prefix(comment):
    return re.sub(r'^[{symbols} ]*'.format(symbols=VALID_NON_LETTER_SYMBOLS),
                  '',
                  comment)


clean = (clean_case
         >> clean_invalid_diacritics
         >> clean_symbols
         >> break_symbols
         >> clean_repetition
         >> clean_symbols_prefix)
