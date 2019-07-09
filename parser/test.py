from split import index_words, gen_probabilities
from generator import build
from clean import clean
import sqlite3

connection = sqlite3.connect('../festejen.db')
cursor = connection.cursor()
index = {}
for row in cursor.execute(
    'select content from comment where content is not null',
):
    comment = clean(row[0])
    index_words(comment, index)
connection.commit()
connection.close()
gen_probabilities(index)
print(build(index))
