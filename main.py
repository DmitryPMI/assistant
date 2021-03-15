import telebot
import time
import funcs
from datetime import datetime


tomato_time = 1

bot = telebot.TeleBot('1660376392:AAHqeib5RhnCGZPUl8p-c4Fi8Cc5iB381PM')
keyboard_start_tomat = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start_tomat.row('Начнем!')


@bot.message_handler(commands=['start'])
def start_message(message):
    funcs.register_id(str(message.from_user.id))
    bot.send_message(message.from_user.id, '''
    Привет! 
    Я бот, созданный помочь тебе устроить свое время так, чтобы ты смог работать максимально продуктивно. 
    Пока что я умею только запускать 10-минутные томаты. Попробуем?
    P.S. давай считать, что ты книжку читаешь :)
    ''', reply_markup=keyboard_start_tomat)


@bot.message_handler(commands=['start_tomato'])
def start_tomato_message(message):
    bot.send_message(message.from_user.id,'Выбери задачу из списка:', reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id)))

@bot.message_handler(commands=['remove_task'])
def remove_task_message(message):
    bot.send_message(message.from_user.id,'Выбери задачу, которую хотите удалить:', reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id), 'r'))

@bot.message_handler(commands=['register_task'])
def register_task_message(message):
    bot.send_message(message.from_user.id, 'Как называется задача?')
    bot.register_next_step_handler(message, register_task_name)

def register_task_name(message):
    name = message.text
    bot.send_message(message.from_user.id, 'Теперь описание. Напиши вопрос, который отражает твою продуктивность по данной задаче.')
    bot.register_next_step_handler(message, lambda message: register_task_description(message, name))

def register_task_description(message, name):
    description = message.text
    funcs.register_task(bot, message, name, description)

def get_time_tomato(bot, message, task_id, task, chat_id):
    if message.text.lower() == 'стандартный томат':
        current_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
        funcs.start_printed_timer(bot, message, tomato_time * 60, chat_id)
        bot.send_message(message.from_user.id, task['description'])
        bot.register_next_step_handler(message, lambda message: funcs.get_status_tomato(message, bot, task_id, current_time, tomato_time))
    else:
        bot.send_message(message.from_user.id, 'Сколько минут длится томат?')
        bot.register_next_step_handler(message, lambda message: get_time_special_tomato(message, task_id, task, chat_id))

def get_time_special_tomato(message, task_id, task, chat_id):
    time_tomato = int(message.text)
    current_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
    funcs.start_printed_timer(bot, message, time_tomato * 60, chat_id)
    bot.send_message(message.from_user.id, task['description'])
    bot.register_next_step_handler(message, lambda message: funcs.get_status_tomato(message, bot, task_id, current_time, time_tomato))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'запустить томат':
        bot.send_message(message.from_user.id,'Выбери задачу из списка:', reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id)))
    elif message.text.lower() == 'удалить задачу':
        bot.send_message(message.from_user.id,'Выбери задачу, которую хотите удалить:', reply_markup=funcs.get_keyboard_tasks(funcs.load_tasks(message.from_user.id), 'r'))
    elif message.text.lower() == 'добавить задачу':
        bot.send_message(message.from_user.id, 'Как называется задача?')
        bot.register_next_step_handler(message, register_task_name)
    elif funcs.get_task_by_name(message.text, funcs.load_tasks(message.from_user.id)):
        task_id, task = funcs.get_task_by_name(message.text, funcs.load_tasks(message.from_user.id))
        bot.send_message(message.from_user.id, 'Какой томат?', reply_markup=funcs.get_keyboard_type_tomato())
        bot.register_next_step_handler(message, lambda message: get_time_tomato(bot, message, task_id, task, chat_id))
    elif message.text.startswith('r') and funcs.get_task_by_name(message.text[1:], funcs.load_tasks(message.from_user.id)):
        task_id, task = funcs.get_task_by_name(message.text[1:], funcs.load_tasks(message.from_user.id))
        funcs.to_black_list(str(message.from_user.id), task_id)
        bot.send_message(message.from_user.id, 'Удалил ' + task['name'], reply_markup=funcs.get_keyboard_default())
    else:
        bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=funcs.get_keyboard_default())


bot.polling(none_stop=True)
