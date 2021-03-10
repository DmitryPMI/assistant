import telebot
import time
import funcs
from datetime import datetime


tomato_time = 1
waiting_count = False
data_list = []

bot = telebot.TeleBot('1660376392:AAHqeib5RhnCGZPUl8p-c4Fi8Cc5iB381PM')
keyboard_start_tomat = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start_tomat.row('Начнем!')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, '''
    Привет! 
    Я бот, созданный помочь тебе устроить свое время так, чтобы ты смог работать максимально продуктивно. 
    Пока что я умею только запускать 10-минутные томаты. Попробуем?
    P.S. давай считать, что ты книжку читаешь :)
    ''', reply_markup=keyboard_start_tomat)


@bot.message_handler(commands=['start_tomato'])
def start_tomato_message(message):
    bot.send_message(message.from_user.id,'Выбери задачу из списка:', reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks()))

@bot.message_handler(commands=['remove_task'])
def remove_task_message(message):
    bot.send_message(message.from_user.id,'Выбери задачу, которую хотите удалить:', reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(), 'r'))

@bot.message_handler(commands=['register_task'])
def register_task_message(message):
    bot.send_message(message.from_user.id, 'Как называется задача?')
    bot.register_next_step_handler(message, register_task_name)

def register_task_name(message):
    name = message.text
    bot.send_message(message.from_user.id, '''Теперь описание. Напиши вопрос, который отражает 
        твою продуктивность по данной задаче.''')
    bot.register_next_step_handler(message, lambda message: register_task_description(message, name))

def register_task_description(message, name):
    description = message.text
    funcs.register_task(bot, message, name, description)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    if message.text.isdigit():
        data_list.append(int(message.text))
        bot.send_message(message.chat.id, 'Отлично! Пока что отдохни, а меня сделают чуть умнее, и я вернусь!')
    elif message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text == 'Начнем!':
        bot.send_message(message.from_user.id, 'Начали!')
        funcs.start_printed_timer(bot, message, tomato_time * 60, chat_id)
        bot.send_message(message.from_user.id, 'Сколько ты успел прочитать страниц?')
    elif funcs.get_task_by_name(message.text, funcs.load_tasks()):
        current_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
        task_id, task = funcs.get_task_by_name(message.text, funcs.load_tasks())
        funcs.start_printed_timer(bot, message, tomato_time * 60, chat_id)
        bot.send_message(message.from_user.id, task['description'])
        bot.register_next_step_handler(message, lambda message: funcs.save_tomato(message, bot, task_id, current_time))
    elif message.text.startswith('r') and funcs.get_task_by_name(message.text[1:], funcs.load_tasks()):
        task_id, task = funcs.get_task_by_name(message.text[1:], funcs.load_tasks())
        funcs.to_black_list(task_id)
        bot.send_message(message.from_user.id, 'Удалил ' + task['name'])
    else:
        bot.send_message(message.from_user.id, 'Че это?')


bot.polling(none_stop=True)
