# -*- coding: utf-8 -*-
import scrapy
from ..items import BetalistItem


class BetalistSpSpider(scrapy.Spider):
    name = 'betalist_sp'
    page_number = 2
    start_urls = ['https://betalist.com/']

    def parse(self, response):
        items = BetalistItem()

        all_data = response.css(".startupCard")

        for resp in all_data:
            product_name = resp.css(".startupCard__details__name::text").extract()
            description = resp.css(".startupCard__details__pitch::text").extract()
            urls = resp.css(".startupCard__visual__image::attr(src)").extract()
            votes = resp.css(".cuteButton__score::text").extract()

            items['product_name'] = product_name
            items['description'] = description
            items['urls'] = urls
            items['votes'] = votes

            yield items

            next_page = 'https://betalist.com/?page=' + str(BetalistSpSpider.page_number)
            if BetalistSpSpider.page_number <= 100:
                BetalistSpSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)
