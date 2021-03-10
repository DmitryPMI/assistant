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

def load_tasks():
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	return data["tasks"]

def get_keyboard_tasks(tasks, prefix=""):
	keyboard = telebot.types.ReplyKeyboardMarkup()
	for task_id, task in tasks.items():
		if task['status'] != 1:
			keyboard.add(telebot.types.KeyboardButton(text = prefix + task["name"]))
	return keyboard

def get_task_by_name(name, tasks):
	for task_id, task in tasks.items():
		if task["name"] == name:
			return [task_id, task]
	return False

def save_tomato(message, bot, task_id, time_start):
	answer = message.text
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	if data["tomatoes"] == {}:
		tomato_id = "0"
	else:
		tomato_id = str(max(map(int, data["tomatoes"].keys())) + 1)
	data["tomatoes"][tomato_id] = {'task_id': task_id, 'answer': answer, 'ts': time_start}
	with open("test_data.json", "w", encoding="UTF-8") as file:
		json.dump(data, file)
	bot.send_message(message.from_user.id, "Не мне тебя судить, но я записал")

def register_task(bot, message, name, description):
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	if data["tasks"] == {}:
		task_id = "0"
	else:
		task_id = str(max(map(int, data["tasks"].keys())) + 1)
	data["tasks"][task_id] = {"name": name, "description": description, "status": 0}
	with open("test_data.json", "w", encoding="UTF-8") as file:
		json.dump(data, file)
	bot.send_message(message.from_user.id, "Готово, задача в списке доступных томатов")

def to_black_list(task_id):
	with open("test_data.json", "r", encoding="UTF-8") as file:
		data = json.load(file)
	data["tasks"][task_id]['status'] = 1
	with open("test_data.json", "w", encoding="UTF-8") as file:
		json.dump(data, file)