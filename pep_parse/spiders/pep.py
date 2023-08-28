import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_hosts = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_pep = response.css(
            'section[id=numerical-index] tr a::attr(href)'
        ).getall()

        for pep_link in all_pep:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.css(
            'h1.page-title::text'
        ).get().strip().split('–')[0]

        name = response.css('h1.page-title::text').get().strip().split('–')[1]

        data = {
            'number': number.replace('PEP ', '').strip(),
            'name': name.strip(),
            'status': response.css('abbr::text').get(),
        }

        yield PepParseItem(data)
