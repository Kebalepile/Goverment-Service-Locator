import scrapy
import re


class ContactsSpider(scrapy.Spider):
    name = "contacts"
    allowed_domains = ["www.saps.gov.za"]
    start_urls = ["https://www.saps.gov.za/contacts/index.php"]

    def parse(self, response):
        province_page_url_paths = response.xpath(
            '//area[starts-with(@href, "provdetails")]/@href').getall()

        for path in province_page_url_paths:
            absoluteURL = response.urljoin(path)
            yield response.follow(absoluteURL, callback=self.parse_province_info)

    def parse_province_info(self, response):
        details = {
            'province': "",
            "details": {}
        }
        province_name = response.css("div.panel-heading::text").get().strip()

        details["province"] = re.sub(r"(?i)province: ", "", province_name)

        contact_table_rows = response.xpath(
            '//table[@cellspacing="0" and @cellpadding="4" and @border="0"]//tr')

        for row in contact_table_rows:
            key = row.xpath('.//td[1]/b/text()').get()
            value = row.xpath(
                './/td[2]/text() | .//td[2]/a[starts-with(@href, "mailto:")]/@href').get()
            if key and value:
                details["details"][key.strip().rstrip(
                    ':')] = value.strip().replace('mailto:', '')

        address_table = response.xpath(
            '//table[@class="table table-bordered"]').get()

        # remove HTML Tags.
        address_string = re.sub(r'<[^>]+>', ' ', address_table)

        address_tuples = re.findall(
            r'(Street|Postal) Address:\s*(.*?)(?=(?:Street|Postal) Address:|$)', address_string, re.DOTALL)

        addresse_info = {key: value.strip()
                         for key, value in address_tuples if value.strip() != ''}
        details['details'].update(addresse_info)

        yield details

    def parse_police_station_info(self, response):
        # "police_stations"= [
        #         {"station_name": "",
        #          "contacts": {
        #              "email": "",
        #              "phone": "",
        #              "fax":""
        #          },
        #          "physical_address":"",
        #          "postal_address":"",
        #          "coordinates":{
        #              "latitude":"",
        #              "longitude":""
        #          }
        #          }
        #     ]
        police_stations = []
        pass
