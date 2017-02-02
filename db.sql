CREATE TABLE "comment" (
    id INTEGER PRIMARY KEY,
    article_id INTEGER,
    article_url TEXT,
    reply_to INTEGER,
    number INTEGER,
    author TEXT,
    text_timestamp TEXT,
    parsed_timestamp INTEGER,
    is_spam BOOLEAN,
    content TEXT,
    FOREIGN KEY(reply_to) REFERENCES "comment"
);
