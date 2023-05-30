import scrapy
import re
from saps.items import SapaContactsItem


class ContactsSpider(scrapy.Spider):
    name = "contacts_spider"
    allowed_domains = ["www.saps.gov.za"]
    start_urls = ["https://www.saps.gov.za/contacts/index.php"]

   
    def parse(self, response):
        province_page_url_paths = response.xpath(
            '//area[starts-with(@href, "provdetails")]/@href').getall()

        for path in province_page_url_paths:
            absoluteURL = response.urljoin(path)
            yield response.follow(absoluteURL, callback=self.parse_province_info)

    def parse_province_info(self, response):
        province_info = {
            'province': "",
            "commissioner_details": {},
            "police_stations": {
                "total": 0,
                "stations": []
            }
        }

        province_name = response.css("div.panel-heading::text").get().strip()
        province_info["province"] = re.sub(
            r"(?i)province: ", "", province_name)

        contact_table_rows = response.xpath(
            '//table[@cellspacing="0" and @cellpadding="4" and @border="0"]//tr')

        for row in contact_table_rows:
            key = row.xpath('.//td[1]/b/text()').get()
            value = row.xpath(
                './/td[2]/text() | .//td[2]/a[starts-with(@href, "mailto:")]/@href').get()
            if key and value:
                province_info["commissioner_details"][key.strip().rstrip(
                    ':')] = value.strip().replace('mailto:', '')

        address_table = response.xpath(
            '//table[@class="table table-bordered"]').get()

        # remove HTML Tags.
        address_string = re.sub(r'<[^>]+>', ' ', address_table)

        address_tuples = re.findall(
            r'(Street|Postal) Address:\s*(.*?)(?=(?:Street|Postal) Address:|$)', address_string, re.DOTALL)

        addresse_info = {key: value.strip()
                         for key, value in address_tuples if value.strip() != ''}
        province_info['commissioner_details'].update(
            addresse_info)

        station_details_paths = response.css(
            'a[href*="stationdetails"]::attr(href)').getall()

        for path in station_details_paths:
            absoluteURL = response.urljoin(path)
            yield scrapy.Request(
                absoluteURL,
                callback=self.parse_police_station_info,
                meta={"province_info": province_info}  # Pass province_info using meta
            )

    def parse_police_station_info(self, response):
        province_info = response.meta["province_info"]

        station_name = response.css("div.panel-heading::text").get().strip()

        station_details = {
            "name": re.sub(r"(?i)station: ", "", station_name),
            "contacts": {},
            "addresses": {},
        }

        contact_table_rows = response.xpath(
            '//table[@cellspacing="0" and @cellpadding="4" and @border="0"]//tr')

        for row in contact_table_rows:
            key = row.xpath('.//td[1]/b/text()').get()
            value = row.xpath(
                './/td[2]/text() | .//td[2]/a[starts-with(@href, "mailto:")]/@href').get()
            if key and value:
                station_details["contacts"][key.strip().rstrip(
                    ':')] = value.strip().replace('mailto:', '')

        address_table = response.xpath(
            '//table[@class="table table-bordered"]').get()

        # remove HTML Tags.
        address_string = re.sub(r'<[^>]+>', ' ', address_table)

        address_tuples = re.findall(
            r'(Street|Postal) Address:\s*(.*?)(?=(?:Street|Postal) Address:|$)', address_string, re.DOTALL)

        addresse_info = {key: value.strip()
                         for key, value in address_tuples if value.strip() != ''}
        station_details['addresses'].update(addresse_info)

        province_info["police_stations"]["stations"].append(station_details)
        province_info["police_stations"]["total"] = len(
            province_info["police_stations"]["stations"])

        saps_contact_item = SapaContactsItem()
        saps_contact_item["data"] = province_info
        yield saps_contact_item["data"] 
