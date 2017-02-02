import scrapy
from .comments import CommentsSpider


class OldCommentsSpider(CommentsSpider):

    name = 'oldcomments'
    newest_article_id = 100000

    def start_requests(self):
        for article_id in range(self.newest_article_id, 0, -1):
            yield scrapy.Request(
                url='http://www.elpais.com.uy' + self.comments_url.format(article_id=article_id,
                                                                          page=1),
                callback=self.parse_comments,
                meta={'article_id': str(article_id), 'article_url': None}
            )
