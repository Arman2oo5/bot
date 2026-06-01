# Подключаем модуль для создания поделючения к БД
import connector
# Подключаем модуль для SQLite
import sqlite3
# Подключаем модуль для работы с датой/веременем
from datetime import datetime

# Создание базы данных, заполнение ее данными 
def init_db():
    try:
        # Подключение к SQLite 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        print("База данных подключена")
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()

        ####################
        ##### customer #####
        ####################

        # Проверка наличия таблицы клиентов
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        #cursor.execute("SELECT 1 FROM pg_tables WHERE tablename = 'customer'")    # PostgreSQL
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customer'") # SQLite
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица customer уже существует")        
        else:
            create_table_query = '''CREATE TABLE "customer" (
                "id"	integer NOT NULL,
                "telegram_id"	integer NOT NULL,
                "phone_number"	varchar(20),
                "first_name"	varchar(64),
                "last_name"	varchar(64),
                PRIMARY KEY("id" AUTOINCREMENT) );'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица customer создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM customer"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее тестовой записью
        if row is None:
             # SQL-запрос новая запись
            sql = "INSERT INTO customer (telegram_id, phone_number, first_name, last_name) VALUES (?, ?, ?, ?)"
            print(sql)
            # Параметры запроса
            parameters = [1234567890, "+7-XXX-XXX-XXXX", "Not real user", None]
             # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
            cursor.execute(sql, parameters)
            # Применить изменения
            conn.commit()    
            print("Таблицы customer заполнена")   
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print("База данных отключена")        
    except Exception as error:
        print(error)

# Добавление пользователя
def insert_customer(telegram_id, phone_number, first_name, last_name):
    try:
        # SQL-запрос новая запись
        #sql = "INSERT INTO customer (telegram_id, phone_number, first_name, last_name, date_joined) VALUES (?, ?, ?, ?, ?)"
        sql = "INSERT INTO customer (telegram_id, phone_number, first_name, last_name, date_joined) VALUES (" + str(telegram_id) + ", '" + phone_number + "', '" + first_name + "', '" + last_name + "', '" + str(datetime.now()) + "')"
        print(sql)
        # Параметры запроса
        #parameters = [telegram_id, phone_number, first_name, last_name, datetime.now()]
        parameters = []
        print(parameters)
        # Выполнить запрос
        executeSQL(sql, parameters)
        print("Пользователь добавлен")        
    except Exception as error:
        print(error)

# Проверка наличия пользовтаеля Telegram (telegram_id) в базе данных пользователей
def check_telegram_id(telegram_id):
    try:
        # SQL-запрос
        sql = "SELECT id, telegram_id FROM customer WHERE telegram_id=" + str(telegram_id)
        print(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = fetchOne(sql)
        # Если такого пользователя нет то вернуть false если есть то true
        if row is None:
            exists = False
        else:
            exists = True
        print("exists ", exists)
        return exists
    except Exception as error:
        print(error)

# Выполнение параметрического запроса SQL (без возврата набора данных)
def executeSQL(sql, parameters):
    try:            
        # SQL-запрос 
        #print(sql)
        # Параметры запроса
        #print(parameters)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()            
        # Включить ограничения FOREIGN KEY 
        #cursor.execute("PRAGMA foreign_keys=ON")                  
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        cursor.execute(sql, parameters)
        # Применить изменения
        conn.commit()     
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print(sql)
        return 1
    except Exception as error:
        print(error)
        return -1
    
# Возврат данных из таблицы БД (множество записей)
def fetchAll(sql):
    try:
        # print(sql)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
        rows = cursor.fetchall()            
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        # Вернуть результат проверки
        return rows
    except Exception as error:
        print(error)

# Возврат данных из таблицы БД (одна запись)
def fetchOne(sql):
    try:
        #print(sql)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
        result = cursor.fetchone()
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        # Вернуть результат проверки
        return result
    except Exception as error:
        print(error)


