import time
import telebot
import json


def load_tasks(user_id):
    with open("data/" + str(user_id) + ".json" , "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data["tasks"]

def load_active_tomatoes(user_id):
    with open("data/" + str(user_id) + ".json" , "r", encoding="UTF-8") as file:
        data = json.load(file)
    print(data["tomatoes"].values())
    return list(filter(lambda x: x["status"] == 0, data["tomatoes"].values()))


def get_keyboard_tasks(tasks, prefix=""):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for task_id, task in tasks.items():
        if task['status'] != 1:
            keyboard.add(telebot.types.KeyboardButton(text=prefix + task["name"]))
    return keyboard


def get_keyboard_default():
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Персональная подборка"))
    keyboard.add(telebot.types.KeyboardButton(text="Запустить томат"))
    keyboard.add(telebot.types.KeyboardButton(text="Добавить задачу"))
    keyboard.add(telebot.types.KeyboardButton(text="Удалить задачу"))
    keyboard.add(telebot.types.KeyboardButton(text="Остановить томат"))
    return keyboard


def get_keyboard_personal():
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Запустить следующую задачу"))
    keyboard.add(telebot.types.KeyboardButton(text="Узнать рейтинг"))
    return keyboard


def get_keyboard_type_tomato():
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Стандартный томат"))
    return keyboard


def get_task_by_name(name, tasks):
    for task_id, task in tasks.items():
        if task["name"] == name:
            return [task_id, task]
    return False


def to_black_list(user_id, task_id):
    with open("data/" + str(user_id) + ".json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    data["tasks"][task_id]['status'] = 1
    with open("data/" + str(user_id) + ".json", "w", encoding="UTF-8") as file:
        json.dump(data, file)


def get_personal_tasks(tasks):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for task in tasks:
        keyboard.add(telebot.types.KeyboardButton(text=task))
    return keyboard


def get_personal_keyboard_task_type():
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.add(telebot.types.KeyboardButton(text="Запустить случайный томат"))
    keyboard.add(telebot.types.KeyboardButton(text="Выбрать томат"))
    return keyboard


def get_personal_random_choice():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text="Запустить"))
    keyboard.add(telebot.types.KeyboardButton(text="Выбрать другой"))
    return keyboard


def get_task_evaluation():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text='1', callback_data=1))
    keyboard.add(telebot.types.InlineKeyboardButton(text='2', callback_data=2))
    keyboard.add(telebot.types.InlineKeyboardButton(text='3', callback_data=3))
    keyboard.add(telebot.types.InlineKeyboardButton(text='4', callback_data=4))
    keyboard.add(telebot.types.InlineKeyboardButton(text='5', callback_data=5))
    return keyboard

def get_mark():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton(text="1"))
    keyboard.add(telebot.types.KeyboardButton(text="2"))
    keyboard.add(telebot.types.KeyboardButton(text="3"))
    keyboard.add(telebot.types.KeyboardButton(text="4"))
    keyboard.add(telebot.types.KeyboardButton(text="5"))
    return keyboard

def start_printed_timer(bot, message, time_in_seconds, chat_id):
    mes_id = bot.send_message(message.chat.id,
                              "Отсчет времени: {0}:{1}".format(time_in_seconds // 60 % 60,
                                                               time_in_seconds % 60)).message_id
    time_in_seconds -= 1
    while time_in_seconds >= 0:
        bot.edit_message_text("Отсчет времени: {0}:{1}".format(time_in_seconds // 60 % 60, time_in_seconds % 60),
                              message_id=mes_id, chat_id=chat_id)
        time_in_seconds -= 1
        time.sleep(1)

