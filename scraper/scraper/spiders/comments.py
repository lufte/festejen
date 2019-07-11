import scrapy
import re
from ..items import Comment, Article


class CommentsSpider(scrapy.Spider):

    name = 'comments'
    allowed_domains = ['www.elpais.com.uy']
    start_urls = ['https://www.elpais.com.uy/sitemap-index.xml']
    comments_url = '/comment/threads/article-{article_id}/comments/page/{page}'

    def parse(self, response):
        matches = re.findall(
            'https://www.elpais.com.uy/sitemap-articles[^<]*',
            response.body.decode()
        )
        for match in matches:
            yield scrapy.Request(match, callback=self.parse_month)

    def parse_month(self, response):
        matches = re.findall('https://www.elpais.com.uy/[^<]*',
                             response.body.decode())
        for match in matches:
            yield scrapy.Request(match, callback=self.parse_article)

    def parse_article(self, response):
        try:
            article_id = response.css(
                'meta[name="cXenseParse:recs:articleid"]::attr(content)'
            )[0].extract()
        except IndexError:
            return
        else:
            article = Article(id=article_id, url=response.url)
            article['tags'] = [
                re.search('[^/]*$', tag)
                for tag
                in response.css('li.tag > a::attr(href)').extract()
            ]

            yield article

            yield scrapy.Request(
                url=response.urljoin(self.comments_url.format(
                    article_id=article_id,
                    page=1
                )),
                callback=self.parse_comments,
                meta={'article_id': article_id}
            )

    def parse_comments(self, response):
        for container in response.css(
                'body > div > div> .fos_comment_comment_show'
        ):
            comment = self.build_comment(
                container.css('.fos_comment_comment_depth_0')[0],
                response.meta['article_id'],
            )
            yield comment

            for reply in container.css('.fos_comment_comment_depth_1'):
                yield self.build_comment(
                    reply, response.meta['article_id'],
                    reply_to=comment['id']
                )
        try:
            next_url = response.css(
                'nav > *:last-child::attr(href)'
            )[0].extract()
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_comments,
                                 meta=response.meta)
        except IndexError:
            # No more pages
            pass

    def build_comment(self, container, article_id, reply_to=None):
        comment = Comment(article_id=article_id, reply_to=reply_to)
        comment['id'] = re.search(
            'fos_comment_(\d+)',
            container.css('div.comment-box')[0].extract()
        ).group(1)
        comment['number'] = container.css(
            'div.comment-info > ul > li:nth-child(1)::text'
        )[0].extract()
        comment['author'] = container.css(
            'div.comment-info > ul > li:nth-child(2) > a:nth-child(1)::text'
        )[0].extract()
        comment['text_timestamp'] = ''.join(container.css(
            'div.comment-info > ul > li:nth-child(3)::text, '
            'div.comment-info > ul > li:nth-child(4)::text'
        ).extract())
        comment['is_spam'] = len(
            container.css('div.comment-text.comment-spam')
        ) > 0
        if not comment['is_spam']:
            comment['content'] = container.css(
                'div.comment-text::text'
            )[0].extract()
        return comment
