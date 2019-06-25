from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'carcrawler',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass