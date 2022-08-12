from datetime import date

import os
import cache_logic

import gspread as gspread
from pycbrf.toolbox import ExchangeRates


class Table:
    """Класс для работы с гугл-таблицей"""
    @staticmethod
    @cache_logic.table_cacher
    def get_data_from_sheet():
        """Метод получения данных из гугл-таблицы"""
        gc = gspread.service_account(filename=os.environ.get('FILE_NAME'))
        table = gc.open_by_key('1UfcLP36X-Oe3mgjHJOQUU3nvJMLlKWJQwuLjKmlxMJg')
        data = table.sheet1.get_all_values()
        rates = ExchangeRates(date.today())
        for row in data[1:]:
            row[3] = '-'.join(row[3].split('.')[::-1])
            rub_col = int(row[2]) * rates['USD'].value
            row.append(round(rub_col, 2))
        return data
