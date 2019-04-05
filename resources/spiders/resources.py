import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../')

import re, scrapy 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from boilerpipe.extract import Extractor

from resources.items import ResourcesItem

class ResourcesSpider(CrawlSpider):
    name = "resources"
    allowed_domains = ["medium.com"]

    start_urls = ["https://medium.com/topic/mental-health"]
    deny_sites = ['.*medium.com\/.*\/followers', '.*medium.com\/.*\/following', 
             '.*medium.com/membership.*', '.*medium.com/topic.*', '.*medium.com/collections.*',
             '.*/latest.*', 'https://medium.com', '.*twitter.com.*', '.*source=footer_card.*']

    rules = [Rule( 
                LinkExtractor(allow=(), deny_domains=['twitter.com'], canonicalize=True),
                callback="parse_item",
                follow=True
            ),]

    def parse_item(self, response):
        item = ResourcesItem() 
        
        if not any(re.match(pattern, response.url) for pattern in self.deny_sites): 
            item['url'] = response.url

            extractor = Extractor(extractor='ArticleExtractor', html=response.text)
            item['text'] = extractor.getText()
            item['title'] = response.selector.xpath('//h1/text()').get()

            item['isArticle'] = (item['title'] != None and 
                            item['text'] != '' and 
                            (response.selector.xpath('//*[@id="feedLink"]') == [])
            )

            if item['isArticle']:
                yield item

            print('Processing -- {} -- {} -- {}'.format(item['isArticle'], item['title'], response.url[:50]))