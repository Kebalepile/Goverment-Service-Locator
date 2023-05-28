import scrapy


class ContactsSpider(scrapy.Spider):
    name = "contacts"
    allowed_domains = ["www.saps.gov.za"]
    start_urls = ["https://www.saps.gov.za/contacts/index.php"]

    def parse(self, response):
        pass
