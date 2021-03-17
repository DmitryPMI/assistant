import time
import telebot
import json


def start_printed_timer(bot, message, time_in_seconds, chat_id):
    mes_id = bot.send_message(message.chat.id,
                              "Отсчет времени: {0}:{1}".format(time_in_seconds // 60 % 60, time_in_seconds % 60)).message_id
    time_in_seconds -= 1
    while time_in_seconds >= 0:
        bot.edit_message_text("Отсчет времени: {0}:{1}".format(time_in_seconds // 60 % 60, time_in_seconds % 60),
                              message_id=mes_id, chat_id=chat_id)
        time_in_seconds -= 1
        time.sleep(1)

def load_tasks(user_id):
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	return data[str(user_id)]["tasks"]

def register_id(user_id):
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	if user_id not in data.keys():
		data[user_id] = {"tasks": {}, "tomatoes": {}}
	with open("test_data.json", "w", encoding="UTF-8") as file:
		json.dump(data, file)

def get_keyboard_tasks(tasks, prefix=""):
	keyboard = telebot.types.ReplyKeyboardMarkup()
	for task_id, task in tasks.items():
		if task['status'] != 1:
			keyboard.add(telebot.types.KeyboardButton(text = prefix + task["name"]))
	return keyboard

def get_keyboard_default():
	keyboard = telebot.types.ReplyKeyboardMarkup()
	keyboard.add(telebot.types.KeyboardButton(text = "Запустить томат"))
	keyboard.add(telebot.types.KeyboardButton(text = "Добавить задачу"))
	keyboard.add(telebot.types.KeyboardButton(text = "Удалить задачу"))
	return keyboard

def get_keyboard_type_tomato():
	keyboard = telebot.types.ReplyKeyboardMarkup()
	keyboard.add(telebot.types.KeyboardButton(text = "Стандартный томат"))
	keyboard.add(telebot.types.KeyboardButton(text = "Особый томат"))
	return keyboard

def get_task_by_name(name, tasks):
	for task_id, task in tasks.items():
		if task["name"] == name:
			return [task_id, task]
	return False

def to_black_list(user_id, task_id):
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	data[user_id]["tasks"][task_id]['status'] = 1
	with open("test_data.json", "w", encoding="UTF-8") as file:
		json.dump(data, file)