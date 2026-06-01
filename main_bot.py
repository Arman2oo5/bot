# Тело бота
try:
    # Подключаем модуль для Телеграма
    import telebot
    print("import telebot")
    # import telegram
    # Подключаем файл с настройками (в нем хранитя токен бота)
    import config 
    print("import config")
    bot = telebot.TeleBot(config.TOKEN)
    print("bot = telebot.TeleBot(config.TOKEN)", bot.get_me())
except Exception as error:
    print(error)
