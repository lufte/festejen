BOT_NAME = 'festejen'

SPIDER_MODULES = ['festejen.spiders']
NEWSPIDER_MODULE = 'festejen.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
DOWNLOAD_DELAY = 3
ITEM_PIPELINES = {
    'festejen.pipelines.CleanWhitespace': 1,
    'festejen.pipelines.ParseNumber': 2,
}
