# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from WikipediaEvent.items import WikipediaEventItem
from scrapy.http    import Request
from unicodedata import normalize
from datetime import datetime

class WikieventSpider(scrapy.Spider):
    name = 'WikiEvent'
    allowed_domains = ['en.wikipedia.org']
    start_urls      = ["https://en.wikipedia.org/wiki/Portal:Current_events/January_1995"]
    #["https://en.wikipedia.org/wiki/Portal:Current_events/January_2011"]
 
    def parse(self, response):
        event_tables = response.css('.vevent')
        for table in event_tables:
            item = WikipediaEventItem()
            date_obj = table.css('.summary::text').extract()
            date_string = normalize("NFKD", date_obj[0].strip())
            item["date"] = datetime.strptime(date_string, '%B %d, %Y')
            item["day_of_week"] = date_obj[1].strip().strip('()')
            descriptions = table.xpath('*/td[contains(@class, "description")]/dl/dt|*/td[contains(@class, "description")]/ul/li')
            for description in descriptions:
                # For category
                if description.xpath('name()').extract_first() == 'dt':
                    item["category"] = description.xpath('text()').extract_first()
                else:
                    subCat = False
                    # For sub-category
                    if float(description.xpath('count(ul)').extract_first()) >= 1:
                        text = description.xpath('a/text()|text()')
                        item["sub_category"] = (text or "").extract_first().encode("ascii", errors="replace").decode("utf-8")
                        subCat = True
                    else:
                        item["sub_category"] = ""
                    texts = description.xpath('{0}a[not(contains(@class, "external"))]/text()|{0}a[not(contains(@class, "external"))]/*/text()|{0}text()|{0}*/text()' \
                            .format(('ul/li/' if subCat else ''))).extract()
                    item["news_header"] =  normalize("NFKD", "".join(texts) if len(texts) > 0 else "").encode("ascii", errors="replace").decode("utf-8")
                    #normalize("NFKD", "".join(texts) if len(texts) > 0 else "").encode("ascii", errors="replace")
                    references = description.xpath('(a[contains(@class, "external")])')
                    source_list = []
                    for ref in references:
                        url = ref.xpath('@href').extract_first()
                        source = ref.xpath('text()').extract_first()
                        if source is not None:
                            source = source.strip("()")
                        source_list.append((source, url))
                    item['source'] = source_list
                    yield item
    
        next_page = response.xpath('//span[@class="noprint"]/a[text()="▶"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
