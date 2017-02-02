from datetime import datetime
import re
import sqlite3
import os


class CleanWhitespace:

    def process_item(self, item, spider):
        for key in item.keys():
            if isinstance(item[key], str):
                item[key] = re.sub('\s{2,}', ' ', item[key]).strip()
        return item


class ParseNumber:

    def process_item(self, item, spider):
        item['number'] = int(item['number'][1:])
        return item


class ParseTimestamp:
    
    MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
              'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def process_item(self, item, spider):
        try:
            match = re.match('(\d+)/(\w+)/', item['text_timestamp'])
            month = str(self.MONTHS.index(match.group(2)) + 1)
            if len(month) < 2:
                month = '0' + month
            replaced = item['text_timestamp'].replace(match.group(2), month)
            if len(match.group(1)) < 2:
                replaced = '0' + replaced
            item['parsed_timestamp'] = datetime.strptime(replaced, '%d/%m/%Y %H:%M')
        except Exception as e:
            # Capture any exception and return the item anyway
            spider.logger.warning('Could not parse timestamp ' + item['text_timestamp'])
        return item


class SQLitePipeline:

    @staticmethod
    def get_connection():
        connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../../festejen.db'))
        connection.row_factory = sqlite3.Row
        connection.commit()
        return connection

    def process_item(self, item, spider):
        connection = SQLitePipeline.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO comment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                item['id'],
                item.get('article_id', None),
                item.get('article_url', None),
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
