import telebot
import data
import game
import random
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

token = "6726977458:AAE8ROgDRDYz_UuhskOvWkX5phdFcSWXVBE"
bot = telebot.TeleBot(token)

num1 = random.randint(1, 10)
num2 = random.randint(1, 10)
answer = str(num1 + num2)
print(answer)


def create_markup(button_labels):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for label in button_labels:
        markup.add(KeyboardButton(label))
    markup.add(KeyboardButton("📢Помощь"))
    return markup


@bot.message_handler(commands=["start"])
def beginning(message):
    location = game.locations
    bot.send_photo(message.chat.id, location["Начало"]["рассказ"]["иллюстрация"],
                   location["Начало"]["рассказ"]["описание"],
                   reply_markup=create_markup(location["Кнопки_ввода"]["Начало"]["рассказ"]))


@bot.message_handler(content_types=["text"])
def checking_messages(message):
    location = game.locations
    text = message.text
    user_id = str(message.from_user.id)
    user_data = data.load_user_data()
    user_info = user_data.get(user_id, {})
    castle, password_input, help_kuru = (user_info.get("castle"), user_info.get("password_input"),
                                         user_info.get("help_kuru"))
    if text == "📢Помощь":
        bot.send_message(message.chat.id, "😲НАСТОЯТЕЛЬНО РЕКОМЕНДУЕМ не писать в чат, а использовать кнопки.")
    elif text == "что делает этот бот?🤖":
        bot.send_message(message.chat.id, "Это бот-квест с элементами RPG и Метроидвания, рассказывающий о жизни "
                                          "заботливого пенсионера.")
    elif castle and password_input:
        if text.isdigit() and len(text) == 4 or text in location["Кнопки_ввода"]["Вернуться_назад"]["назад"]:
            if text == location["Запертая_дверь"]["код"]:
                user_info["password_input"], user_info["castle"] = False, False
                data.save_user_data(user_data)
                bot.send_photo(message.chat.id,
                               location["Запертая_дверь"]["иллюстрация"],
                               location["Запертая_дверь"]["верный_пароль"],
                               reply_markup=create_markup(location["Кнопки_ввода"]["Кладовка"]["лопата"]))
                time.sleep(1)
                bot.send_message(message.chat.id,
                                 location["Запертая_дверь"]["фраза_рассказчика"])
            elif text == location["Рассказчик_и_мысли"]["Космический_корабль"]["запертая_дверь"]["код"]:
                phrases = location["Рассказчик_и_мысли"]["Космический_корабль"]["запертая_дверь"]
                for key in ["фраза_рассказчика", "мысли"]:
                    bot.send_message(message.chat.id, phrases[key])
                    time.sleep(2)
                return
            elif text in location["Кнопки_ввода"]["Вернуться_назад"]["назад"]:
                user_info["password_input"] = False
                user_info["castle"] = False
                data.save_user_data(user_data)
                bot.send_photo(message.chat.id,
                               location["Космический_корабль"]["рассказ"]["иллюстрация"],
                               location["Космический_корабль"]["рассказ"]["описание_1"],
                               reply_markup=create_markup(location
                                                          ["Кнопки_ввода"]["Космический_корабль"]["рассказ"]))
            else:
                bot.send_message(message.chat.id, location["Запертая_дверь"]["неверный_пароль"])
        else:
            bot.send_message(message.chat.id, location["Запертая_дверь"]["введите_пароль"])
    elif help_kuru:
        del_button = "Подслушивать разговор гигантского Кура"
        if text.isdigit():
            if text == answer:
                user_data[user_id]["help_kuru"] = False
                data.save_user_data(user_data)
                kur_replies = location["Реплики"]["Космический_корабль"]["Кур"]
                sasha_replies = location["Реплики"]["Космический_корабль"]["Cаша"]
                for reply in [kur_replies["реплика_1"], kur_replies["реплика_2"], sasha_replies["реплика_1"],
                              kur_replies["реплика_3"], sasha_replies["реплика_2"]]:
                    bot.send_message(message.chat.id, reply)
                    time.sleep(2)
                for phrase in [location["Рассказчик_и_мысли"]["Космический_корабль"]["подслушать_разговор"]
                               ["фраза_рассказчика_3"], location["Рассказчик_и_мысли"]["Космический_корабль"]
                               ["подслушать_разговор"]["мысли"]]:
                    bot.send_message(message.chat.id, phrase)
                    time.sleep(2)
                location["Кнопки_ввода"]["Космический_корабль"]["рассказ"].remove(del_button)
                data.save_user_data(user_data)
                bot.send_photo(message.chat.id,
                               location["Космический_корабль"]["рассказ"]["иллюстрация"],
                               location["Космический_корабль"]["рассказ"]["описание_1"],
                               reply_markup=create_markup(
                                   location["Кнопки_ввода"]["Космический_корабль"]["рассказ"]))
            else:
                bot.send_message(message.chat.id, "Неверно. Попробуйте снова.")
        else:
            bot.send_message(message.chat.id, "Введите числовой ответ.")
    elif text == "Да!":  # Начало
        if user_id not in user_data:
            user_data[user_id] = {"name": message.from_user.first_name, "levels": -1, "castle": False,
                                  "shovel": False, "password_input": False, "help_kuru": False, "trust_kura": False}
            data.save_user_data(user_data)
        bot.send_message(message.chat.id, "Супер!", reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
        bot.send_photo(message.chat.id,
                       location["Начало"]["рассказ1"]["иллюстрация"],
                       location["Начало"]["рассказ1"]["описание"])
        time.sleep(5)
        bot.send_photo(message.chat.id,
                       location["Начало"]["рассказ2"]["иллюстрация"],
                       location["Начало"]["рассказ2"]["описание"])
        time.sleep(4)
        bot.send_photo(message.chat.id,
                       location["Начало"]["рассказ3"]["иллюстрация"],
                       location["Начало"]["рассказ3"]["описание"])
        time.sleep(3)
        bot.send_message(message.chat.id,
                         location["Реплики"]["Начало"]["Саша"]["реплика"])
        time.sleep(4)
        bot.send_message(message.chat.id,
                         location["Реплики"]["Начало"]["Кур"]["реплика"],
                         reply_markup=create_markup(location["Кнопки_ввода"]["Реплики"]["диалог"]))
    elif text == "Иначе?":
        bot.send_message(message.chat.id,
                         location["Реплики"]["Начало"]["Кур"]["реплика_1"],
                         reply_markup=create_markup(location["Кнопки_ввода"]["Реплики"]["диалог_1"]))
    elif text == "Отказаться от путешествия":
        bot.send_message(message.chat.id, location["Реплики"]["Начало"]["Саша"]["реплика_1"])
        time.sleep(2)
        bot.send_photo(message.chat.id,
                       location["Начало"]["финал"]["иллюстрация"],
                       location["Начало"]["финал"]["описание"],
                       reply_markup=ReplyKeyboardRemove())
        del user_data[user_id]
        data.save_user_data(user_data)
        return
    elif text == ". . ." or text == "Принять путешествия":
        bot.send_photo(message.chat.id,
                       location["Начало"]["рассказ4"]["иллюстрация"],
                       location["Начало"]["рассказ4"]["описание"],
                       reply_markup=ReplyKeyboardRemove())
        time.sleep(2)
        bot.send_photo(message.chat.id,
                       location["Начало"]["рассказ5"]["иллюстрация"],
                       location["Начало"]["рассказ5"]["описание"])
        time.sleep(3)
        bot.send_message(message.chat.id,
                         location["Рассказчик_и_мысли"]["Начало"]["фраза_рассказчика"])
        time.sleep(4)
        bot.send_photo(message.chat.id,
                       location["Космический_корабль"]["рассказ"]["иллюстрация"],
                       location["Космический_корабль"]["рассказ"]["описание"],
                       reply_markup=create_markup(location["Кнопки_ввода"]["Космический_корабль"]["рассказ"]))
        user_data[user_id]["levels"] = 1
        data.save_user_data(user_data)  # локация 1
    elif text in location["Кнопки_ввода"]["Космический_корабль"]["рассказ"]:
        if text == "Идти в комнату и ложится спать":
            phrases = location["Рассказчик_и_мысли"]["Космический_корабль"]["идет_спать"]
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Космический_корабль"]["идет_спать"]
                             ["фраза_рассказчика"],
                             reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            for key in ["мысли", "фраза_рассказчика_1"]:
                bot.send_message(message.chat.id, phrases[key])
                time.sleep(2)
            user_data[user_id]["levels"] = 2
            data.save_user_data(user_data)
        elif text == "Подойти к двери с кодовым замком":
            user_data[user_id]["castle"] = True
            user_data[user_id]["password_input"] = True
            data.save_user_data(user_data)
            bot.send_photo(message.chat.id,
                           location["Космический_корабль"]["рассказ1"]["иллюстрация"],
                           location["Космический_корабль"]["рассказ1"]["описание"],
                           reply_markup=create_markup(location["Кнопки_ввода"]["Вернуться_назад"]["назад"]))
        elif text == "Подойти к тумбочке и посмотреть семейную фотографию":
            phrases = location["Рассказчик_и_мысли"]["Космический_корабль"]["идет_тумбочке"]
            del_button = "Подойти к тумбочке и посмотреть семейную фотографию"
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Космический_корабль"]["идет_тумбочке"]
                             ["фраза_рассказчика"],
                             reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            for key in ["мысли", "мысли_1", "мысли_2", "фраза_рассказчика_1", "мысли_3"]:
                bot.send_message(message.chat.id, phrases[key])
                time.sleep(3)
            location["Кнопки_ввода"]["Космический_корабль"]["рассказ"].remove(del_button)
            bot.send_photo(message.chat.id,
                           location["Космический_корабль"]["рассказ"]["иллюстрация"],
                           location["Космический_корабль"]["рассказ"]["описание_1"],
                           reply_markup=create_markup(location["Кнопки_ввода"]["Космический_корабль"]["рассказ"]))
        else:
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Космический_корабль"]["подслушать_разговор"]
                             ["фраза_рассказчика"],
                             reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Космический_корабль"]["подслушать_разговор"]
                             ["фраза_рассказчика_1"],
                             reply_markup=create_markup(
                                 location["Кнопки_ввода"]["Космический_корабль"]["подслушать_разговор"]))
    elif text in location["Кнопки_ввода"]["Кладовка"]["лопата"]:
        if text == "Взять":
            user_data[user_id]["shovel"] = True
            bot.send_message(message.chat.id, location["Рассказчик_и_мысли"]["Космический_корабль"]["кладовка"]
                             ["взять"])
        else:
            bot.send_message(message.chat.id, location["Рассказчик_и_мысли"]["Космический_корабль"]["кладовка"]
                             ["не_взять"])
        location["Кнопки_ввода"]["Космический_корабль"]["рассказ"].remove("Подойти к двери с кодовым замком")
        data.save_user_data(user_data)
        bot.send_photo(message.chat.id,
                       location["Космический_корабль"]["рассказ"]["иллюстрация"],
                       location["Космический_корабль"]["рассказ"]["описание_1"],
                       reply_markup=create_markup(location["Кнопки_ввода"]["Космический_корабль"]["рассказ"]))
    elif text in location["Кнопки_ввода"]["Космический_корабль"]["подслушать_разговор"]:
        del_button = "Подслушивать разговор гигантского Кура"
        if text == "Вмешаться":
            time.sleep(1)
            bot.send_photo(message.chat.id,
                           location["Космический_корабль"]["рассказ2"]["иллюстрация"],
                           location["Космический_корабль"]["рассказ2"]["описание"],
                           reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Реплики"]["Космический_корабль"]["Cаша"]["реплика"])
            time.sleep(3)
            bot.send_message(message.chat.id,
                             location["Реплики"]["Космический_корабль"]["Кур"]["реплика"])
            time.sleep(3)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Космический_корабль"]["подслушать_разговор"]
                             ["фраза_рассказчика_2"])
            time.sleep(3)
            bot.send_message(message.chat.id, f"Вам нужно решить математическое уравнение:\n {num1} + {num2}\n"
                                              f"Напишите ответ математическое уравнение в чат: ")
            user_data[user_id].update({"levels": 2, "help_kuru": True, "trust_kura": True})
            data.save_user_data(user_data)
        else:
            location["Кнопки_ввода"]["Космический_корабль"]["рассказ"].remove(del_button)
            data.save_user_data(user_data)
            bot.send_photo(message.chat.id,
                           location["Космический_корабль"]["рассказ"]["иллюстрация"],
                           location["Космический_корабль"]["рассказ"]["описание_1"],
                           reply_markup=create_markup(location["Кнопки_ввода"]["Космический_корабль"]["рассказ"]))
    elif text in location["Кнопки_ввода"]["Тревожная_ситуация"]["тревога_началась"]:
        if text == "Проигнорировать":
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["проигнорировать"]
                             ["фраза_рассказчика"], reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["проигнорировать"]
                             ["мысли"])
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["проигнорировать"]
                             ["фраза_рассказчика_1"])
            time.sleep(5)
            bot.send_photo(message.chat.id,
                           location["Тревожная_ситуация"]["кк_взорвался"]["иллюстрация"],
                           location["Тревожная_ситуация"]["кк_взорвался"]["описание"])
            del user_data[user_id]
            data.save_user_data(user_data)
        else:
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["пойти_проверить"]
                             ["фраза_рассказчика"], reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["пойти_проверить"]
                             ["фраза_рассказчика_1"])
            time.sleep(2)
            bot.send_message(message.chat.id, location["Реплики"]["Тревожная_ситуация"]["Cаша"]["реплика"])
            time.sleep(2)
            bot.send_message(message.chat.id, location["Реплики"]["Тревожная_ситуация"]["Кур"]["реплика"])
            time.sleep(2)
            bot.send_message(message.chat.id, location["Реплики"]["Тревожная_ситуация"]["Cаша"]["реплика_1"])
            time.sleep(2)
            bot.send_message(message.chat.id, location["Реплики"]["Тревожная_ситуация"]["Кур"]["реплика_1"])
            time.sleep(2)
            bot.send_photo(message.chat.id,
                           location["Тревожная_ситуация"]["пойти_проверить"]["иллюстрация"],
                           location["Тревожная_ситуация"]["пойти_проверить"]["описание"],
                           reply_markup=create_markup(location["Кнопки_ввода"]["Тревожная_ситуация"]["решение"]))
    elif text in location["Кнопки_ввода"]["Тревожная_ситуация"]["решение"]:
        if text == "Спрыгнуть с парашютом":
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["cпрыгнуть"]["фраза_рассказчика"],
                             reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["cпрыгнуть"]["фраза_рассказчика_1"])
            time.sleep(2)
            bot.send_message(message.chat.id, location["Реплики"]["Тревожная_ситуация"]["Cаша"]["реплика_4"])
            time.sleep(2)
            bot.send_message(message.chat.id, location["Реплики"]["Тревожная_ситуация"]["Кур"]["реплика_2"])
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["cпрыгнуть"]["фраза_рассказчика_2"])
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["cпрыгнуть"]["фраза_рассказчика_3"])
            time.sleep(5)
            bot.send_photo(message.chat.id,
                           location["Тревожная_ситуация"]["хороший_финал"]["иллюстрация"],
                           location["Тревожная_ситуация"]["хороший_финал"]["описание"])
            del user_data[user_id]
            data.save_user_data(user_data)
        else:
            bot.send_photo(message.chat.id,
                           location["Тревожная_ситуация"]["удалить_вирус"]["иллюстрация"],
                           location["Тревожная_ситуация"]["удалить_вирус"]["описание"],
                           reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["удалить_вирус"]["фраза_рассказчика"])
            time.sleep(5)
            bot.send_message(message.chat.id,
                             location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["удалить_вирус"]
                             ["фраза_рассказчика_1"])
            time.sleep(5)
            bot.send_photo(message.chat.id,
                           location["Тревожная_ситуация"]["кк_взорвался"]["иллюстрация"],
                           location["Тревожная_ситуация"]["кк_взорвался"]["описание"])
            del user_data[user_id]
            data.save_user_data(user_data)
    else:
        bot.send_message(message.chat.id, "Пожалуйста не пишите в чат, а используйте кнопки.")  # локация 2
    if user_id in user_data and not user_data[user_id]["trust_kura"] and text == "Идти в комнату и ложится спать":
        time.sleep(3)
        bot.send_message(message.chat.id,
                         location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["начало_эпизода"]["фраза_рассказчика"])
        time.sleep(2)
        bot.send_message(message.chat.id,
                         location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["начало_эпизода"]["фраза_рассказчика_1"])
        time.sleep(2)
        bot.send_message(message.chat.id,
                         location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["начало_эпизода"]["фраза_рассказчика_2"],
                         reply_markup=create_markup(location["Кнопки_ввода"]["Тревожная_ситуация"]["тревога_началась"]))
    elif user_id in user_data and user_data[user_id]["trust_kura"] and text == "Идти в комнату и ложится спать":
        bot.send_message(message.chat.id,
                         location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["альтернативный_финал"]
                         ["фраза_рассказчика"])
        time.sleep(2)
        bot.send_message(message.chat.id,
                         location["Рассказчик_и_мысли"]["Тревожная_ситуация"]["альтернативный_финал"]
                         ["фраза_рассказчика_1"])
        time.sleep(5)
        bot.send_photo(message.chat.id,
                       location["Тревожная_ситуация"]["хороший_финал"]["иллюстрация"],
                       location["Тревожная_ситуация"]["хороший_финал"]["описание"])
        del user_data[user_id]
        data.save_user_data(user_data)


bot.polling()
