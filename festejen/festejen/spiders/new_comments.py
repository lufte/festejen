import scrapy
from .comments import CommentsSpider


class NewCommentsSpider(CommentsSpider):

    name = 'newcomments'
    start_urls = ['http://www.elpais.com.uy/']

    def parse(self, response):
        for link in response.css('a.page-link::attr(href)'):
            yield scrapy.Request(url=response.urljoin(link.extract()), callback=self.parse_article)

    def parse_article(self, response):
        try:
            article_id = response.css(
                'div.social-media-button-article.mail::attr(data-id)'
            )[0].extract()
        except IndexError:
            pass
        else:
            return scrapy.Request(
                url=response.urljoin(self.comments_url.format(article_id=article_id, page=1)),
                callback=self.parse_comments,
                meta={'article_id': article_id, 'article_url': response.request.url}
            )
