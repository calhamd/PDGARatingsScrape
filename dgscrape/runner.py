import os
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from dgscrape.spiders.pdgarankings import PdgaRatingsSpider

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'DiscGolfRankings.csv',
    'LOG_ENABLED': False
})
c.crawl(PdgaRatingsSpider)
c.start()

# os.chdir(os.path.dirname(os.path.realpath(__file__)))

# try:
#     execute(
#         [
#             'scrapy',
#             'crawl',
#             'pdgaratings',
#             '-o',
#             'test.json'
#         ]
#     )
# except SystemExit:
#     pass