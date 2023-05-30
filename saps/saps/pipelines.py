# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from itertools import groupby


class SapsPipeline:
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        file_name = 'contacts_data.json'
        with open(file_name) as file:
            data_list = json.load(file)
        data_list.sort(key=lambda data: data["province"])
        refined_data = [
            max(g, key=lambda data: data["police_stations"]["total"]) for k, g in groupby(data_list, key=lambda data: data["province"])
        ]
        with open(file_name, 'w') as file:
            json.dump(refined_data, file, indent=4)

        print(
            f"*--------------*\n K e heditse ka go dirisa: {spider.name} \n*--------------*")
