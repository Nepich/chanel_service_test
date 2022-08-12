import os
import cache_logic

import psycopg2


class DBConn:
    """Контекстный менеджер для БД"""
    def __init__(self, db_name='chanel_service', user='postgres',
                 password=os.environ.get('DB_PASS'), host='db', port='5432'):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.conn = psycopg2.connect(database=self.db_name,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host,
                                     port=self.port)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class DB:
    """Класс для работы с БД"""
    @staticmethod
    def insert_data():
        """Метод для занесения информации из таблицы в БД"""
        with DBConn() as connect:
            cursor = connect.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS orders'
                           '(order_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY, '
                           'order_number INTEGER UNIQUE NOT NULL, usd_price NUMERIC, '
                           'deliver_date DATE, rud_price NUMERIC);')
            for order_info in cache_logic.CHANGES['new']:
                cursor.execute('INSERT INTO orders (order_number, usd_price, deliver_date, rud_price) '
                               'VALUES (%s, %s, %s, %s) ON CONFLICT (order_number) DO NOTHING;',
                               (order_info[1], order_info[2], order_info[3], order_info[4]))
            connect.commit()

    @staticmethod
    def update_data():
        """Метод для обновления данных в БД при изменении строк в таблице"""
        with DBConn() as connect:
            cursor = connect.cursor()
            for order_info in cache_logic.CHANGES['update']:
                cursor.execute('UPDATE orders SET order_number = %s, usd_price = %s, deliver_date = %s, rud_price = %s '
                               'WHERE order_number = %s;',
                               (order_info[1], order_info[2], order_info[3], order_info[4], order_info[1]))
            connect.commit()

    @staticmethod
    def delete_data():
        """Метод для удаления данных из БД при удалении строк из таблицы"""
        with DBConn() as connect:
            cursor = connect.cursor()
            for order_info in cache_logic.CHANGES['delete']:
                cursor.execute('DELETE FROM orders WHERE order_number = %s;', (order_info[1], ))
            connect.commit()

    @staticmethod
    def get_deliver_info():
        """Метод получения данных о вышедшем сроке поставки из БД"""
        with DBConn() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT order_number FROM orders WHERE deliver_date < current_date')
            expired = cursor.fetchall()
            answer = ', '.join([str(order[0]) for order in expired])
            return f"Заказы №: {answer}, истекли"
