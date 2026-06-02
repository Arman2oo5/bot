# Хэндлеры бота
# Хендлеры это конечная точка в обработке событий. 
# Хендлеры могут быть блокирующими (если нашелся подходящий хендлер другие уже не проверяются и не выполняются) и не блокирующими (в таком случае количество выполняемых хендлеров не ограничено и зависит от того какие пройдут). 
# По умолчанию все хендлеры являются блокирующими
# Импортируем объект бота
from main_bot import bot 
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
from telegram import ParseMode
# Для определения имени пользователя
import getpass
# Инмпортируем все с файла сообщений
#from messages import msg
# Подключаем файл с настройками (в нем хранитя токен бота)
import config 
# Подключаем модуль для работы с БД
import db
# Подключаем модуль для работы с датой/веременем
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

import os

# Заявка 
class Application:
    def __init__(self, date_application, telegram_id, catalog_id):
        self.date_application = date_application
        self.telegram_id = telegram_id
        self.catalog_id = catalog_id

# Стартовое меню
def menu():
    print("menu")
    try:
        # Подключаем клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # Создать кнопки
        key_1 = types.InlineKeyboardButton(text=msg.menu_1, callback_data='menu_1')
        key_2 = types.InlineKeyboardButton(text=msg.menu_2, callback_data='menu_2')
        #key_3 = types.InlineKeyboardButton(text=msg.menu_3, callback_data='menu_3')
        # Добавить кнопки на экран
        keyboard.add(key_1).add(key_2)  #.add(key_3)
        ## Меню для администратора
        #if config.ADMIN_ID.count(chat_id):
        #    key_admin_menu = types.InlineKeyboardButton(text=msg.admin_menu, callback_data='admin_menu')
        #    keyboard.add(key_admin_menu)
        # Показать кнопки и написать сообщение о выборе
        bot.send_message(chat_id, text=msg.choose_an_action, reply_markup=keyboard)
    except Exception as error:
        print(error)

# Меню menu_1
def menu_1():
    print("menu_1")    
    try:
        # Получить список категорий товара
        sql = "SELECT id, category_title FROM category WHERE id IN (SELECT DISTINCT(category_id) FROM view_catalog) ORDER BY category_title"
        category = db.fetchAll(sql)
        # Подключаем клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # Создать кнопки
        # Указываем название кнопок, добавляем клавиатуру
        for row in category:
            keyboard.add(types.InlineKeyboardButton(row[1], callback_data="category" + "֍" + str(row[0])))
        key_home = types.InlineKeyboardButton(text=msg.home, callback_data='menu_home')
        # Добавить кнопки на экран
        keyboard.add(key_home)
        # Показать кнопки и написать сообщение о выборе
        bot.send_message(chat_id, text=msg.select_a_category, reply_markup=keyboard)
    except Exception as error:
        print(error)
        
# Меню menu_1_1
def menu_1_1(category_id):
    print("menu_1_1")    
    try:
        # Получить список товара
        sql = "SELECT id, catalog_title FROM view_catalog WHERE category_id=" + category_id  + " ORDER BY catalog_title"
        category = db.fetchAll(sql)
        # Подключаем клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # Создать кнопки
        # Указываем название кнопок, добавляем клавиатуру
        for row in category:
            keyboard.add(types.InlineKeyboardButton(row[1], callback_data="view_catalog" + "֍" + str(row[0])))
        key_home = types.InlineKeyboardButton(text=msg.home, callback_data='menu_home')
        # Добавить кнопки на экран
        keyboard.add(key_home)
        # Показать кнопки и написать сообщение о выборе
        bot.send_message(chat_id, text=msg.select_a_catalog, reply_markup=keyboard)
    except Exception as error:
        print(error)
        
# Меню menu_1_1_1
def menu_1_1_1(catalog_id):
    print("menu_1_1_1")    
    try:
        # Получить информацию о товаре (карточка)
        sql = "SELECT id, category, catalog_title, price, details, photo FROM view_catalog WHERE id=" + catalog_id 
        catalog = db.fetchOne(sql)
        # Заявка 
        global application  
        application = Application(None, chat_id, catalog[0])
        # Карточка товара
        #print(catalog[0])
        #print(catalog[1])
        #print(catalog[2])
        #print(catalog[3])
        #print(catalog[4])
        #print(catalog[5])
        bot.send_message(chat_id,  "<b>" + msg.category + ":</b> " + str(catalog[1]) + "\n" + 
                                   "<b>"+ msg.catalog_title + ":</b> " + str(catalog[2]) + "\n" + 
                                   "<b>" + msg.price + ":</b> " + str(catalog[3]) + " 〒\n" +
                                   "<b>" + msg.details + ":</b> " + str(catalog[4]), parse_mode=ParseMode.HTML )   
        # Картинка товара
        try:
            url="https://res.cloudinary.com/dwgreiscb/image/upload/v1/" + catalog[5]
            print(url)
            #url="https://res.cloudinary.com/dwgreiscb/image/upload/v1/media/images/catalog03_crsjmv"
            bot.send_photo(chat_id, photo=url)
        except Exception as error:
            print(error)
        # Подключаем клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # Создать кнопки
        key_additionally = types.InlineKeyboardButton(text=msg.additionally, callback_data='menu_additionally')
        key_home = types.InlineKeyboardButton(text=msg.home, callback_data='menu_home')
        # Добавить кнопки на экран
        keyboard.add(key_additionally).add(key_home)
        # Показать кнопки и написать сообщение о выборе
        bot.send_message(chat_id, text=msg.choose_an_action, reply_markup=keyboard)
    except Exception as error:
        print(error)
        
# Отправить заявку
def send_application():
    try:
        print("send_application")
        # Записать в БД
        application.date_application = datetime.now()
        print(str(application.date_application))
        print(str(application.telegram_id))
        print(str(application.catalog_id))
        # SQL-запрос новая запись
        #sql = "INSERT INTO application (date_application, telegram_id, catalog_id) VALUES (?, ?, ?)"
        sql = "INSERT INTO application (date_application, telegram_id,catalog_id) VALUES ('" + str(application.date_application) + "', " + str(application.telegram_id) + ", " +  str(application.catalog_id) + ")"
        # Параметры запроса
        #parameters = [str(application.date_application), application.telegram_id, application.catalog_id]
        parameters = []
        # Выполнить запрос
        db.executeSQL(sql, parameters)
        # Показать заявки
        view_application()
    except Exception as error:
        print(error)

# Посмотреть заявки
def view_application():
    print("view_application")
    try:
        # История заявок на ремонт устройств
        #sql = "SELECT id, strftime('%d.%m.%Y %H:%M:%S', date_application) AS data, telegram_id, category, catalog_title, price, final\n"
        sql = "SELECT id, TO_CHAR(date_application, 'DD.MM.YYYY HH24:MI') AS data, telegram_id, category, catalog_title, price, final\n"
        sql = sql + "FROM view_application\n"
        sql = sql + "WHERE telegram_id=" + str(chat_id) + "\n"
        sql = sql + "ORDER BY date_application"
        print(sql)
        result = db.fetchAll(sql)
        if len(result) > 0:
            bot.send_message(chat_id, "\n<b>" + msg.menu_1 + ":</b> ", parse_mode='HTML' )                
            for row in result:
                mes = "\n<b>" + msg.application_number + ":</b> " + str(row[0]) + "\n<b>" + msg.date_application + ":</b> " + str(row[1]) + "\n<b>" + msg.category + ":</b> " + str(row[3]) + "\n<b>" + msg.catalog_title + ":</b> " + str(row[4]) + "\n<b>" + msg.price + ":</b> " + str(row[5]) + "\n<b>" + msg.final + ":</b> " + str(row[6])
                bot.send_message(chat_id,  mes , parse_mode='HTML' )                
        # Возврат в стратовое меню
        menu()     
    except Exception as error:
        print(error)

# Меню menu_3
def menu_2():
    print("menu_2")    
    try:
        # Подключаем клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # Создать кнопки
        key_1 = types.InlineKeyboardButton(text=msg.menu_2_1, callback_data='menu_2_1')
        key_2 = types.InlineKeyboardButton(text=msg.menu_2_2, callback_data='menu_2_2')
        key_3 = types.InlineKeyboardButton(text=msg.menu_2_3, callback_data='menu_2_3')
        key_home = types.InlineKeyboardButton(text=msg.home, callback_data='menu_home')
        # Добавить кнопки на экран
        keyboard.add(key_1).add(key_2).add(key_3).add(key_home)
        # Показать кнопки и написать сообщение о выборе
        bot.send_message(chat_id, text=msg.choose_an_action, reply_markup=keyboard)
    except Exception as error:
        print(error)
        
# Меню menu_3
def menu_3():
    print("menu_3")    
    try:
        # Подключаем клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # Создать кнопки
        key_1 = types.InlineKeyboardButton(text=msg.menu_3_1, callback_data='menu_3_1')
        key_2 = types.InlineKeyboardButton(text=msg.menu_3_2, callback_data='menu_3_2')
        key_3 = types.InlineKeyboardButton(text=msg.menu_3_3, callback_data='menu_3_3')
        key_home = types.InlineKeyboardButton(text=msg.home, callback_data='menu_home')
        # Добавить кнопки на экран
        keyboard.add(key_1).add(key_2).add(key_3).add(key_home)
        # Показать кнопки и написать сообщение о выборе
        bot.send_message(chat_id, text=msg.choose_an_action, reply_markup=keyboard)
    except Exception as error:
        print(error)

# Меню администратора
def admin_menu():
    print("admin_menu")
    try:
        # Меню для администратора
        if config.ADMIN_ID.count(chat_id):
            # Подключаем клавиатуру
            keyboard = types.InlineKeyboardMarkup()
            # Создать кнопки
            key_1 = types.InlineKeyboardButton(text=msg.admin_menu_1, callback_data='admin_menu_1')
            key_2 = types.InlineKeyboardButton(text=msg.admin_menu_2, callback_data='admin_menu_2')
            key_3 = types.InlineKeyboardButton(text=msg.admin_menu_3, callback_data='admin_menu_3')
            key_home = types.InlineKeyboardButton(text=msg.home, callback_data='menu_home')
            # Добавить кнопки на экран
            keyboard.add(key_1).add(key_2).add(key_3).add(key_home)
            # Показать кнопки и написать сообщение о выборе
            bot.send_message(chat_id, text=msg.choose_an_action, reply_markup=keyboard)
        else:
            print("Нет доступа")
    except Exception as error:
        print(error)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print("callback_worker")
    choice = str(call.data).split("֍")
    print(choice[0])
    try:
        # Действие в зависимости от выбранной кнопки
        if call.data == "menu_1": 
            message = msg.category
            menu_1() 
        elif call.data == "menu_2": 
            message = "menu_2"
            view_application()
            #menu_2() 
        elif call.data == "menu_3": 
            message = "menu_3"
            menu_2() 
        elif call.data == "admin_menu": 
            message = "admin_menu"
            admin_menu() 
        elif call.data == "menu_home": 
            message = "menu_home"
            menu()
        elif call.data == "menu_additionally": 
            message = "menu_additionally"
            send_application()
        else: 
            if choice[0] == "category":            
                #print(choice[0], choice[1])
                message = msg.catalogs
                menu_1_1(choice[1])
            elif choice[0] == "view_catalog":
                #print(choice[0], choice[1])
                message = msg.catalog
                menu_1_1_1(choice[1])            
            else:
                message = "XZ"
        # Отправляем текст в Телеграм
        #bot.send_message(call.message.chat.id, message)
    except Exception as error:
        print(error)


@bot.message_handler(content_types=['contact']) 
# Запись/проверка контакта в БД
# Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def contact(message):
    try:
        print("contact")
        # Если присланный объект contact не равен нулю
        if message.contact is not None: 
            # Добавление контакта
            if message.contact.phone_number == None:
                message.contact.phone_number = ""
            if message.contact.first_name == None:
                message.contact.first_name = ""
            if message.contact.last_name == None:
                message.contact.last_name = ""
            db.insert_customer(message.chat.id, message.contact.phone_number, message.contact.first_name, message.contact.last_name)
            # Переход в главное меню
            menu()    
    except Exception as error:
        print(error)

# Обработчик команды /start (Выполняется, когда пользователь нажимает на start)
@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        bot.send_message(message.chat.id, msg.hello)
        # Чат id
        global chat_id
        chat_id = message.chat.id
        print(chat_id)
        # Если пользователя нет в базе
        if not db.check_telegram_id(message.chat.id):
            print("Пользователя нет в БД")
            # Подключаем клавиатуру
            keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
            # Указываем кнопки, которЫЕ появится у пользователя
            contact_button = types.KeyboardButton(text=msg.send_contact, request_contact=True)
            cancel_button = types.KeyboardButton(text=msg.continue_without_a_phone)
            # Добавляем эти кнопки
            keyboard.add(contact_button, cancel_button)
            # Отправка сообщения
            bot.send_message(message.chat.id, msg.send_your_phone_number, reply_markup=keyboard)
        # Если пользователь есть в базе
        else:
            print("Пользователь есть в БД")
            # Переход в главное меню
            menu()        
    except Exception as error:
        print(error)
 
# Обработчик команды /help
@bot.message_handler(commands=['help'])  
def help_command(message):  
    print("help")
    try:       
        print("help")
    except Exception as error:
        print(error)

# Любой текст
@bot.message_handler(content_types=["text"]) 
def text_messages(message):
    print("content_types=[\"text\"]")        
    try:    
        print(message.text)
        if(message.text == msg.continue_without_a_phone):
             # Если пользователя нет в базе добавить Telegram id
            if not db.check_telegram_id(message.chat.id):                
                db.insert_customer(message.chat.id, None, None, None)       
                # Переход в главное меню
                menu()        
        #elif(message.text==msg.menu_1):
        #    # Переход в меню 1
        #    menu_1(message) 
        #elif(message.text==msg.menu_2):
        #    # Переход в меню 2
        #    menu_2(message) 
        #elif(message.text==msg.menu_3):
        #    # Переход в меню 3
        #    menu_3(message) 
        #elif(message.text==msg.admin_menu):
        #    # Меню для администратора
        #    if config.ADMIN_ID.count(message.chat.id):
        #        admin_menu(message)
        #    else:
        #        print("Нет доступа")
        #elif(message.text==msg.home):
        #    menu() 
        else:
            bot.send_message(message.chat.id, message.text)   
            # Если выбор не понятен то возврат на главную
            menu() 
    except Exception as error:
        print(error)
 
USE_WEBHOOK = os.getenv("USE_WEBHOOK", "0") == "1"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)

import time

# Flask для Render Health Check
app = Flask(__name__)

@app.route("/")
def health_check():
    return "Bot is running"

def run_flask():
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000))
    )
    
if __name__ == '__main__':
    try:
        from messages_kz import msg
        print("from messages_kz import msg")

        db.init_db()
        print("db.init_db()")

        # Если приложение запущено на Render
        if os.getenv("RENDER"):
            print("RENDER DETECTED")

            flask_thread = Thread(target=run_flask)
            flask_thread.daemon = True
            flask_thread.start()

            print("HEALTH CHECK SERVER STARTED")

        else:
            print("LOCAL MODE")

        print("RUN MODE: POLLING (WITH AUTO-RESTART)")

        while True:
            try:
                bot.polling(
                    none_stop=True,
                    interval=0,
                    timeout=60
                )
            except Exception as polling_error:
                print(f"Бот упал из-за сетевой ошибки: {polling_error}")
                print("Перезапуск бота через 5 секунд...")
                bot.stop_polling()
                time.sleep(5)

    except Exception as exception:
        print("Критическая ошибка при инициализации приложения:", exception)
        
# if __name__ == '__main__':
#     try:
#         from messages_kz import msg
#         print("from messages_kz import msg")

#         db.init_db()
#         print("db.init_db()")

#         print("RUN MODE: RENDER / POLLING (WITH AUTO-RESTART)")

#         # Запускаем бесконечный цикл для защиты от сетевых сбоев
#         while True:
#             try:
#                 bot.polling(none_stop=True, interval=0, timeout=60)
#             except Exception as polling_error:
#                 # Сюда будут прилетать ошибки ReadTimeout, ConnectionError и т.д.
#                 print(f"Бот упал из-за сетевой ошибки: {polling_error}")
#                 print("Перезапуск бота через 5 секунд...")
#                 bot.stop_polling()  # Сбрасываем старый поток
#                 time.sleep(5)       # Небольшая пауза, чтобы не спамить серверам Telegram

#     except Exception as exception:
#         print("Критическая ошибка при инициализации приложения:", exception)

# if __name__ == '__main__':
#     try:
#         from messages_kz import msg
#         print("from messages_kz import msg")

#         db.init_db()
#         print("db.init_db()")

#         print("RUN MODE: RENDER / POLLING")

#         bot.polling(none_stop=True, interval=0)

#     except Exception as exception:
#         print(exception)
        
# if __name__ == '__main__':
#     try:
#         from messages_kz import msg
#         print("from messages_kz import msg")

#         db.init_db()
#         print("db.init_db()")

#         if USE_WEBHOOK and WEBHOOK_URL:
#             print("RUN MODE: WEBHOOK")

#             import flask
#             from flask import Flask, request

#             app = Flask(__name__)

#             @app.route(f"/{config.BOT_TOKEN}", methods=["POST"])
#             def webhook():
#                 json_str = request.get_data().decode("UTF-8")
#                 update = types.Update.de_json(json_str)
#                 bot.process_new_updates([update])
#                 return "OK"

#             @app.route("/")
#             def index():
#                 return "Bot is running"

#             bot.remove_webhook()
#             bot.set_webhook(url=f"{WEBHOOK_URL}/{config.BOT_TOKEN}")

#             app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

#         else:
#             print("RUN MODE: POLLING")
#             bot.polling(none_stop=True, interval=0)

#     except Exception as exception:
#         print(exception)
