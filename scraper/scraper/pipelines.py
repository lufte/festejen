# Copyright © 2019 Javier Ayres
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import re
from datetime import datetime
from .dbutils import get_connection
from .items import Article, Comment


class Pipeline:

    class_ = None

    def process_item(self, item, spider):
        if isinstance(item, self.class_):
            return self.c_process_item(item, spider)
        else:
            return item

    def c_process_item(self, item, spider):
        raise NotImplementedError


class ArticlePipeline(Pipeline):

    class_ = Article


class CommentPipeline(Pipeline):

    class_ = Comment


class CleanWhitespace(CommentPipeline):

    def c_process_item(self, item, spider):
        for key in item.keys():
            if isinstance(item[key], str):
                item[key] = re.sub('\s{2,}|\r\n|\n', ' ', item[key]).strip()
        return item


class ParseNumber(CommentPipeline):

    def c_process_item(self, item, spider):
        item['number'] = int(item['number'][1:])
        return item


class ParseTimestamp(CommentPipeline):

    MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
              'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def c_process_item(self, item, spider):
        try:
            match = re.match('(\d+)/(\w+)/', item['text_timestamp'])
            month = str(self.MONTHS.index(match.group(2)) + 1)
            if len(month) < 2:
                month = '0' + month
            replaced = item['text_timestamp'].replace(match.group(2), month)
            if len(match.group(1)) < 2:
                replaced = '0' + replaced
            item['parsed_timestamp'] = datetime.strptime(replaced,
                                                         '%d/%m/%Y %H:%M')
        except Exception as e:
            # Capture any exception and return the item anyway
            spider.logger.warning('Could not parse timestamp '
                                  + item['text_timestamp'])
        return item


class SQLiteCommentPipeline(CommentPipeline):

    def c_process_item(self, item, spider):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO comment '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                item['id'],
                item.get('article_id', None),
                item.get('reply_to', None),
                item.get('number', None),
                item.get('author', None),
                item.get('text_timestamp', None),
                item.get('parsed_timestamp', None),
                item.get('is_spam', None),
                item.get('content', None),
            )
        )
        connection.commit()
        connection.close()
        return item


class SQLiteArticlePipeline(ArticlePipeline):

    def c_process_item(self, item, spider):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO article VALUES (?, ?)',
            (
                item['id'],
                item['url']
            )
        )
        for tag in item['tags']:
            clean_tag = tag[0].strip() if tag else ''
            if clean_tag:
                cursor.execute(
                    'INSERT OR IGNORE INTO tag VALUES (?)',
                    (clean_tag,)
                )
                cursor.execute(
                    'INSERT OR IGNORE INTO article_tag VALUES (?, ?)',
                    (item['id'], clean_tag)
                )
        connection.commit()
        connection.close()
        return item
