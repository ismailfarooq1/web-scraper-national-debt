# -*- coding: utf-8 -*-
import scrapy
import logging


class GdbDebtSpider(scrapy.Spider):
    name = 'gdb_debt'
    allowed_domains = ['www.worldpopulationreview.com']
    start_urls = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        rows = response.xpath('//table/tbody/tr')
        for row in rows:
            name = row.xpath('.//td[position() = 1]/a/text()').get()
            url = row.xpath('.//td[position() = 1]/a/@href').get()
            national_debt = row.xpath('.//td[position() = 2]/text()').get()
            population = row.xpath('.//td[position() = 3]/text()').get()

            absolute_url = f"https://www.worldpopulationreview.com{url}"
            
            yield scrapy.Request(url=absolute_url, callback=self.parse_countries, meta={
                'name': name,
                'national_debt': national_debt,
                'population': population
            })


            # yield response.follow(
            #     url=url,
            #     callback=self.parse_countries, 
            #     meta={
            #     'name': name,
            #     'national_debt': national_debt,
            #     'population': population
            #     } 
            # )
            # yield {
            #     'name': name,
            #     'national_debt': national_debt,
            #     'population': population,
            #     'url': url
            # }

    def parse_countries(self, response):
        name = response.request.meta['name']
        rows = response.xpath("(//table[@class='datatableStyles__StyledTable-bwtkle-1 hOnuWY table table-striped'])[3]/tbody/tr")
        for row in rows:
            years = row.xpath('.//td[position() = 1]/text()').get()
            male_pc = row.xpath('.//td[position() = 3]/text()').get()
            female_pc = row.xpath('.//td[position() = 4]/text()').get()

            
            yield{
                "name": name,
                'year': years,
                'male_pc': male_pc,
                'female_pc': female_pc
            }


# (//table[@class='datatableStyles__StyledTable-bwtkle-1 hOnuWY table table-striped'])[3]