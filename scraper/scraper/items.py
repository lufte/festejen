# Copyright © 2019 Javier Ayres
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import scrapy


class Comment(scrapy.Item):
    id = scrapy.Field()
    article_id = scrapy.Field()
    reply_to = scrapy.Field()
    number = scrapy.Field()
    author = scrapy.Field()
    text_timestamp = scrapy.Field()
    parsed_timestamp = scrapy.Field()
    is_spam = scrapy.Field()
    content = scrapy.Field()


class Article(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
