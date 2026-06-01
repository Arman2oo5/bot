# Подключаем модуль для SQLite
import sqlite3
# Подключаем модуль для PostgreSQL 
import psycopg2

# Создание соединения с базой данных с указанием конкретной схемы
def get_connection():
    try:
        #conn = sqlite3.connect('db.sqlite3')
        # conn = sqlite3.connect('C://django//2025-2026//shop.bot//db.sqlite3')
        conn = psycopg2.connect("postgresql://shop_ifsl_user:BXAfX6IzDrACQPvHN63YJCWdL3CS16ke@dpg-d8elp1c2m8qs7392gdb0-a.frankfurt-postgres.render.com/shop_ifsl", sslmode="require")
        return conn  
    except Exception as error:
        print(error)
