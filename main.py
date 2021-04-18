import telebot
import time
import funcs
from datetime import datetime
import json
from os import listdir

from assistant import Assistant
import recommend
import recommends_control

tomato_time = 1
filename = 'test_data.json'

if filename not in listdir():
    with open(filename, 'w') as file:
        json.dump({}, file)

assistant = Assistant()
assistant.load_from_json(filename)

bot = telebot.TeleBot('1583853458:AAGKFi8qgnmWNZYrnCBySoTVE51A5lB3KNU')
keyboard_start_tomat = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start_tomat.row('Начнем!')

personal_reccomendation = recommend.KNNRec()


def register_id(user_id):
    try:
        assistant.add_user(str(user_id))
    except ValueError:
        print('Пользователь уже существует')
    with open(filename, "r", encoding="UTF-8") as file:
        data = json.load(file)
    if user_id not in data.keys():
        data[user_id] = {"tasks": {}, "tomatoes": {}}
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(data, file)


@bot.message_handler(commands=['start'])
def start_message(message):
    register_id(str(message.from_user.id))
    bot.send_message(message.from_user.id, '''
    Привет! 
    Я бот, созданный помочь тебе устроить свое время так, чтобы ты смог работать максимально продуктивно. 
    Пока что я умею только запускать томаты. Попробуем?''', reply_markup=keyboard_start_tomat)


@bot.message_handler(commands=['start_tomato'])
def start_tomato_message(message):
    register_id(str(message.from_user.id))
    bot.send_message(message.from_user.id, 'Выбери задачу из списка:',
                     reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id)))


@bot.message_handler(commands=['remove_task'])
def remove_task_message(message):
    register_id(str(message.from_user.id))
    bot.send_message(message.from_user.id, 'Выбери задачу, которую хотите удалить:',
                     reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id), 'r'))


@bot.message_handler(commands=['register_task'])
def register_task_message(message):
    register_id(str(message.from_user.id))
    bot.send_message(message.from_user.id, 'Как называется задача?')
    bot.register_next_step_handler(message, register_task_name)


def register_task_name(message):
    name = message.text
    bot.send_message(message.from_user.id,
                     'Теперь описание. Напиши вопрос, который отражает твою продуктивность по данной задаче.')
    bot.register_next_step_handler(message, lambda message: register_task_description(message, name))


def register_task_description(message, name):
    description = message.text
    register_task(bot, message, name, description)


def register_task(bot, message, name, description):
    user_id = str(message.from_user.id)
    with open(filename, "r", encoding="UTF-8") as file:
        data = json.load(file)
    if data[user_id]["tasks"] == {}:
        task_id = "0"
    else:
        task_id = str(max(map(int, data[user_id]["tasks"].keys())) + 1)
    data[user_id]["tasks"][task_id] = {"name": name, "description": description, "status": 0}
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(data, file)
    assistant.users[str(message.from_user.id)].add_task(name, 6, description)
    bot.send_message(message.from_user.id, "Готово, задача в списке доступных томатов",
                     reply_markup=funcs.get_keyboard_default())


def get_time_tomato(bot, message, task_id, task, chat_id):
    if message.text.lower() == 'стандартный томат':
        current_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
        funcs.start_printed_timer(bot, message, tomato_time * 60, chat_id)
        bot.send_message(message.from_user.id, task['description'])
        bot.register_next_step_handler(message, lambda message: get_status_tomato(message, bot, task_id, current_time,
                                                                                  tomato_time))
    else:
        bot.send_message(message.from_user.id, 'Сколько минут длится томат?')
        bot.register_next_step_handler(message,
                                       lambda message: get_time_special_tomato(message, task_id, task, chat_id))


def start_personal_tomato(task, message, chat_id):
    funcs.start_printed_timer(bot, message, 60, chat_id)


def save_tomato(message, bot, task_id, time_start, status, time_tomato):
    answer = message.text
    user_id = str(message.from_user.id)
    with open(filename, "r", encoding="UTF-8") as file:
        data = json.load(file)
    if data[user_id]["tomatoes"] == {}:
        tomato_id = "0"
    else:
        tomato_id = str(max(map(int, data[user_id]["tomatoes"].keys())) + 1)
    data[user_id]["tomatoes"][tomato_id] = {'task_id': task_id, 'answer': answer, 'ts': time_start, 'status': status,
                                            'time_tomato': time_tomato}
    task_name = data[user_id]["tasks"][task_id]["name"]
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(data, file)
    assistant.users[str(message.from_user.id)].tasks[task_name].add_history(status, time_tomato, time_start, answer)
    bot.send_message(message.from_user.id, "Не мне тебя судить, но я записал",
                     reply_markup=funcs.get_keyboard_default())


def get_status_tomato(message, bot, task_id, time_start, time_tomato):
    status = message.text
    bot.send_message(message.from_user.id, "Теперь напиши комментарий")
    bot.register_next_step_handler(message,
                                   lambda message: save_tomato(message, bot, task_id, time_start, status, time_tomato))


def get_time_special_tomato(message, task_id, task, chat_id):
    time_tomato = int(message.text)
    current_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
    funcs.start_printed_timer(bot, message, time_tomato * 60, chat_id)
    bot.send_message(message.from_user.id, task['description'])
    bot.register_next_step_handler(message, lambda message: funcs.get_status_tomato(message, bot, task_id, current_time,
                                                                                    time_tomato))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    register_id(str(message.from_user.id))
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'запустить томат':
        bot.send_message(message.from_user.id, 'Выбери задачу из списка:',
                         reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id)))
    elif message.text.lower() == 'удалить задачу':
        bot.send_message(message.from_user.id, 'Выбери задачу, которую хотите удалить:',
                         reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id), 'r'))
    elif message.text.lower() == 'добавить задачу':
        bot.send_message(message.from_user.id, 'Как называется задача?')
        bot.register_next_step_handler(message, register_task_name)
    elif funcs.get_task_by_name(message.text, funcs.load_tasks(message.from_user.id)):
        task_id, task = funcs.get_task_by_name(message.text, funcs.load_tasks(message.from_user.id))
        bot.send_message(message.from_user.id, 'Какой томат?', reply_markup=funcs.get_keyboard_type_tomato())
        bot.register_next_step_handler(message, lambda message: get_time_tomato(bot, message, task_id, task, chat_id))
    elif message.text.startswith('r') and funcs.get_task_by_name(message.text[1:],
                                                                 funcs.load_tasks(message.from_user.id)):
        task_id, task = funcs.get_task_by_name(message.text[1:], funcs.load_tasks(message.from_user.id))
        funcs.to_black_list(str(message.from_user.id), task_id)
        bot.send_message(message.from_user.id, 'Удалил ' + task['name'], reply_markup=funcs.get_keyboard_default())
    elif recommends_control.is_refers_to_reccomendation(message):
        recommends_control.recomendation_command(bot, message, personal_reccomendation)
    else:
        bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=funcs.get_keyboard_default())


bot.polling(none_stop=True)
