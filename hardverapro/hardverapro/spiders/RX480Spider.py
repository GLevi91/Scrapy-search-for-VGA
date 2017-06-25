from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#Defining selector strings
select_hirdetes = '//div[@class="global_list_gray"] | //div[@class="global_list_def"]'
filter_iced = './/i[contains(@class,"iced")]'
filter_kereso = './/div[@class="left"]//a[contains(translate(.,"KERES","keres"),"keres")] | .//div[@class="left"]//a[contains(translate(.,"VENNÉK","vennék"),"vennék")]'
select_szoveg = './/div[@class="left"]//a/text()'
select_ar = 'span.price::text'
select_varos = './/*[contains(@class,"city")]/text()'
select_link = './/div[@class="left"]//a/@href'

class RX480Spider(CrawlSpider):
    name = "rx480"
    start_urls = ["http://hardverapro.hu/aprok/hardver/videokartya/pcie?kategoria_gyartokhoz=66&gyartokereses=-1&hirdetesVaros=-1&hirdetesTipusa=-1&GYORSKERESO_TOKEN=K5J2N58CKP77MB56MA8J&gyorskereses=rx+480&gyorskereses_hidden=Gyorskeres%C3%A9s+itt%3A+PCIe"]
    
    rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="tovabb"]',)), callback="parse_start_url", follow= True),)
                         
    def parse_start_url(self, response):
        for hirdetes in response.xpath(select_hirdetes):
            if hirdetes.xpath(filter_iced).extract_first() is None:
                if hirdetes.xpath(filter_kereso).extract():
                    pass
                else:
                    link = hirdetes.xpath(select_link).extract_first()
                    full_link = 'http://hardverapro.hu/'+ link
                    yield {
                        'szoveg': hirdetes.xpath(select_szoveg).extract_first(),
                        'ar': hirdetes.css(select_ar).extract_first(),
                        'varos': hirdetes.xpath(select_varos).extract_first(),
                        'fullLink': full_link
                    }