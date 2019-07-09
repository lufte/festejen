import scrapy


class Comment(scrapy.Item):
    id = scrapy.Field()
    article_id = scrapy.Field()
    article_url = scrapy.Field()
    reply_to = scrapy.Field()
    number = scrapy.Field()
    author = scrapy.Field()
    text_timestamp = scrapy.Field()
    parsed_timestamp = scrapy.Field()
    is_spam = scrapy.Field()
    content = scrapy.Field()
