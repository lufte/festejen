# Copyright © 2019 Javier Ayres
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
DOWNLOAD_DELAY = 0
ITEM_PIPELINES = {
    'scraper.pipelines.CleanWhitespace': 1,
    'scraper.pipelines.ParseNumber': 2,
    'scraper.pipelines.ParseTimestamp': 3,
    'scraper.pipelines.SQLiteCommentPipeline': 1000,
    'scraper.pipelines.SQLiteArticlePipeline': 1000,
}
LOG_LEVEL = 'INFO'
CONCURRENT_REQUESTS = 64
