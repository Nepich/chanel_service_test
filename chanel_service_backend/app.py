from datetime import date
import time

import cache_logic
import db_logic
import os
from gtable_logic import Table

import requests

LAST_UPDATE = date(2022, 7, 11)


def notifier():
    """Функция отправки уведомлений"""
    global LAST_UPDATE
    requests.post(f'https://api.telegram.org/bot{os.environ.get("TELEGRAM_TOKEN")}/sendMessage',
                  data={'chat_id': '153472688', 'text': db_logic.DB.get_deliver_info()})
    LAST_UPDATE = date.today()


def bd_updater():
    """Функция проверяющая наличие обновлений/изменений/удалений в гугл-таблице.
    Вносит изменения в БД в зависимости от наличия таковых"""
    Table.get_data_from_sheet()
    if cache_logic.CHANGES['new']:
        db_logic.DB.insert_data()
    if cache_logic.CHANGES['update']:
        db_logic.DB.update_data()
    if cache_logic.CHANGES['delete']:
        db_logic.DB.delete_data()


if __name__ == "__main__":
    while True:
        bd_updater()
        if LAST_UPDATE < date.today():
            notifier()
        time.sleep(60)
