from datetime import datetime
import re


class CleanWhitespace:

    def process_item(self, item, spider):
        for key in item.keys():
            if isinstance(item[key], str):
                item[key] = re.sub('\s{2,}', ' ', item[key]).strip()


class ParseNumber:

    def process_item(self, item, spider):
        item['number'] = int(item['number'][1:])


class ParseTimestamp:
    
    MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
              'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def process_item(self, item, spider):
        try:
            match = re.match('(\d+)/(\w+)/', item['text_timestamp'])
            month = str(self.MONTHS.index(match.group(2)))
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
