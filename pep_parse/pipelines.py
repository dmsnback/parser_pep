from datetime import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parents[1]
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    counter_status = {}

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['status'] not in self.counter_status:
            PepParsePipeline.counter_status[item['status']] = 1
        else:
            PepParsePipeline.counter_status[item['status']] += 1

        return item

    def close_spider(self, spider):
        date_time = str(dt.now().strftime(DATE_FORMAT))
        filename = 'status_summary_' + date_time + '.csv'
        total = sum(self.counter_status.values())

        with open(
                BASE_DIR / 'results' / filename, 'w', encoding='utf-8'
        ) as file:
            file.write('Статус,Количество\n')

            for key, value in PepParsePipeline.counter_status.items():
                file.write(f'{key}, {value}\n')

            file.write(f'Total,{total}\n')
