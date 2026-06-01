# Подключаем модуль для SQLite
import sqlite3
# Подключаем модуль для PostgreSQL 
import psycopg2

# Создание соединения с базой данных с указанием конкретной схемы
def get_connection():
    try:
        #conn = sqlite3.connect('db.sqlite3')
        conn = sqlite3.connect('C://django//2025-2026//shop.bot//db.sqlite3')
        # conn = psycopg2.connect("postgres://shop_admin:in6E36jBWmzdsLPgCzNFjjaXDJmWCCtd@dpg-cogjk3sf7o1s7380l2j0-a.frankfurt-postgres.render.com/shop_bot_pez3", sslmode="require")
        return conn  
    except Exception as error:
        print(error)
