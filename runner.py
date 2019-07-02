from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'autolistcrawler',
            '-o',
            'crawled.json',
        ]
    )
except SystemExit:
    pass