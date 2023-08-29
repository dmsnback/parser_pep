from collections import defaultdict
import csv
from datetime import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parents[1]
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    def open_spider(self, spider):
        self.counter_status = defaultdict(int)

    def process_item(self, item, spider):
        if item['status'] not in self.counter_status:
            self.counter_status[item['status']] = 1
        else:
            self.counter_status[item['status']] += 1

        return item

    def close_spider(self, spider):
        date_time = dt.now().strftime(DATE_FORMAT)
        filename = 'status_summary_' + date_time + '.csv'
        status_quantity = self.counter_status.items()
        total = sum(self.counter_status.values())

        with open(
                BASE_DIR / 'results' / filename, 'w', encoding='utf-8'
        ) as file:
            write = csv.writer(file, dialect='unix')

            write.writerows(
                [
                    ['Статус', 'Количество'],
                    *status_quantity,
                    ['Total', total]
                ]
            )
