import scrapy
from .comments import CommentsSpider
from ..dbutils import get_connection


class OldCommentsSpider(CommentsSpider):

    name = 'oldcomments'

    def start_requests(self):
        connection = get_connection()
        cursor = connection.cursor()
        oldest_article_id = next(
            cursor.execute('SELECT MIN(article_id) FROM comment')
        )[0]

        if oldest_article_id is None:
            raise ValueError('Unable to get MIN(article_id) from festejen.db')

        for article_id in range(oldest_article_id, 0, -1):
            yield scrapy.Request(
                url='http://www.elpais.com.uy'
                    + self.comments_url.format(article_id=article_id, page=1),
                callback=self.parse_comments,
                meta={'article_id': str(article_id), 'article_url': None}
            )
