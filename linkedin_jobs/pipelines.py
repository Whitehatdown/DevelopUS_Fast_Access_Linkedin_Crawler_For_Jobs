# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from datetime import datetime
from scrapy.exporters import CsvItemExporter, JsonItemExporter

class LinkedinJobsPipeline:
    def process_item(self, item, spider):
        return item

class CustomExportPipeline:
    def open_spider(self, spider):
        run_date = spider.run_date
        file_number = spider.file_number
        # Create output directory if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')
        # Open CSV and JSON files for writing
        self.csv_file = open(f'output/jobs_{file_number}_{run_date}.csv', 'wb')
        self.json_file = open(f'output/jobs_{file_number}_{run_date}.json', 'wb')
        # Initialize exporters
        self.csv_exporter = CsvItemExporter(self.csv_file, encoding='utf-8')
        self.json_exporter = JsonItemExporter(self.json_file, encoding='utf-8')
        self.csv_exporter.start_exporting()
        self.json_exporter.start_exporting()

    def close_spider(self, spider):
        # Finish exporting and close files
        self.csv_exporter.finish_exporting()
        self.json_exporter.finish_exporting()
        self.csv_file.close()
        self.json_file.close()

    def process_item(self, item, spider):
        # Export item to both CSV and JSON
        self.csv_exporter.export_item(item)
        self.json_exporter.export_item(item)
        return item
