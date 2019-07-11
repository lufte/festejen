CREATE TABLE "comment" (
    id INTEGER PRIMARY KEY,
    article_id INTEGER REFERENCES "article",
    reply_to INTEGER,
    number INTEGER,
    author TEXT,
    text_timestamp TEXT,
    parsed_timestamp INTEGER,
    is_spam BOOLEAN,
    content TEXT,
    FOREIGN KEY(reply_to) REFERENCES "comment"
);

CREATE TABLE "article" (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL
);

CREATE TABLE "tag" (
    slug TEXT PRIMARY KEY
);

CREATE TABLE "article_tag" (
    article_id INTEGER REFERENCES "article",
    tag_slug TEXT REFERENCES "tag",
    UNIQUE (article_id, tag_slug)
);
