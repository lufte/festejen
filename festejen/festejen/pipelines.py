import re


class CleanWhitespace(object):

    def process_item(self, item, spider):
        for key in item.keys():
            item[key] = re.sub('\s{2,}', ' ', item[key]).strip()


class ParseNumber(object):

    def process_item(self, item, spider):
        item['number'] = item['number'][1:]