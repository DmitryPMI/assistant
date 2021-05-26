import telebot
import time
import funcs
import audio_recognition_funcs
from datetime import datetime
import json
from os import listdir
import requests

from assistant import Assistant
import recommend
import recommends_control
import config.config as conf
from threading import Thread

tomato_time = 1
tomato_processes = {}

assistant = Assistant()
assistant.load_from_json(conf.DATA_PATH)

bot = telebot.TeleBot(conf.TOKEN)
keyboard_start_tomat = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start_tomat.row('Начнем!')

personal_reccomendation = recommend.KNNRec()


def register_id(user_id):
    try:
        assistant.add_user(str(user_id))
    except ValueError:
        print('Пользователь уже существует')
    if str(user_id)  + '.json' not in listdir(conf.DATA_PATH):
        with open(conf.DATA_PATH + '/' + str(user_id)  + '.json', "w", encoding="UTF-8") as file:
            json.dump({"tasks": {}, "tomatoes": {}}, file)


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


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Спасибо, я запомнил :)')
    answer = ''
    if call.data == '1':
        answer = 'Досадно, но дальше задания будут только лучше!'
        personal_reccomendation.update_profiles(call.message.chat.id,
                                                personal_reccomendation.get_challenge_number(
                                                    personal_reccomendation.get_next_challenge(
                                                        call.message.chat.id)), 1)
    elif call.data == '2':
        answer = 'Окей, я запомнил...'
        personal_reccomendation.update_profiles(call.message.chat.id,
                                                personal_reccomendation.get_challenge_number(
                                                    personal_reccomendation.get_next_challenge(
                                                        call.message.chat.id)), 2)
    elif call.data == '3':
        answer = 'Нормально :)'
        personal_reccomendation.update_profiles(call.message.chat.id,
                                                personal_reccomendation.get_challenge_number(
                                                    personal_reccomendation.get_next_challenge(
                                                        call.message.chat.id)), 3)
    elif call.data == '4':
        answer = 'Здорово, я рад, что тебе понравилось!'
        personal_reccomendation.update_profiles(call.message.chat.id,
                                                personal_reccomendation.get_challenge_number(
                                                    personal_reccomendation.get_next_challenge(
                                                        call.message.chat.id)), 4)
    elif call.data == '5':
        answer = 'Отлично! :D'
        personal_reccomendation.update_profiles(call.message.chat.id,
                                                personal_reccomendation.get_challenge_number(
                                                    personal_reccomendation.get_next_challenge(
                                                        call.message.chat.id)), 5)

    bot.send_message(call.message.chat.id, text=answer, reply_markup=funcs.get_keyboard_default())
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.message_handler(content_types=['voice'])
def start_voice_message(message):
    register_id(str(message.from_user.id))
    file_info = bot.get_file(message.voice.file_id)
    audio = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(conf.TOKEN, file_info.file_path))
    res = audio_recognition_funcs.get_emotion_from_audio(audio.content)
    adv = audio_recognition_funcs.get_nearest(audio_recognition_funcs.get_vector_from_emotion(res))
    bot.send_message(message.from_user.id, f'Эмоция: {res}', reply_markup=keyboard_start_tomat)
    bot.send_message(message.from_user.id, f'Рекомендую: {adv}', reply_markup=keyboard_start_tomat)

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
    with open(conf.DATA_PATH + '/' + user_id + '.json', "r", encoding="UTF-8") as file:
        data = json.load(file)
    if data["tasks"] == {}:
        task_id = "0"
    else:
        task_id = str(max(map(int, data["tasks"].keys())) + 1)
    data["tasks"][task_id] = {"name": name, "description": description, "status": 0}
    with open(conf.DATA_PATH + '/' + user_id + '.json', "w", encoding="UTF-8") as file:
        json.dump(data, file)
    assistant.users[str(message.from_user.id)].add_task(name, 6, description)
    bot.send_message(message.from_user.id, "Готово, задача в списке доступных томатов",
                     reply_markup=funcs.get_keyboard_default())


def start_printed_timer(bot, message, time_in_seconds, chat_id):
    mes_id = bot.send_message(message.chat.id,
                              "Отсчет времени: {0}:{1}".format(time_in_seconds // 60 % 60,
                                                               time_in_seconds % 60)).message_id
    time_in_seconds -= 1
    while time_in_seconds >= 0:
        bot.edit_message_text("Отсчет времени: {0}:{1}".format(time_in_seconds // 60 % 60, time_in_seconds % 60),
                              message_id=mes_id, chat_id=chat_id)
        time_in_seconds -= 1
        try:
            with open('flag.json', 'r') as file:
                data = json.load(file)
            if data[str(message.from_user.id)]['flag'] == 1:
                data[str(message.from_user.id)]['flag'] = 0
                with open('flag.json', 'w') as file:
                    json.dump(data, file)
                break
            time.sleep(1)
        except:
            time.sleep(1)
    bot.send_message(message.from_user.id, "Оцени эффективность.")
    # bot.register_next_step_handler(message, lambda message: get_status_tomato(message, bot, task_id, current_time,
    #                                                                                   tomato_time))


def get_time_tomato(bot, message, task_id, task, chat_id):
    if message.text.lower() == 'стандартный томат':
        current_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
        t = Thread(target = lambda msg: start_printed_timer(bot, msg, tomato_time * 60, chat_id), args = (message,))
        t.start()
        
    else:
        bot.send_message(message.from_user.id, 'Сколько минут длится томат?')
        bot.register_next_step_handler(message,
                                       lambda message: get_time_special_tomato(message, task_id, task, chat_id))


def start_personal_tomato(task, message, chat_id):
    start_printed_timer(bot, message, 60, chat_id)


def save_tomato(message, bot, task_id, time_start, status, time_tomato):
    answer = message.text
    user_id = str(message.from_user.id)
    with open(conf.DATA_PATH + '/' + user_id + '.json', "r", encoding="UTF-8") as file:
        data = json.load(file)
    if data["tomatoes"] == {}:
        tomato_id = "0"
    else:
        tomato_id = str(max(map(int, data["tomatoes"].keys())) + 1)
    data["tomatoes"][tomato_id] = {'task_id': task_id, 'answer': answer, 'ts': time_start, 'status': status,
                                            'time_tomato': time_tomato}
    task_name = data["tasks"][task_id]["name"]
    with open(conf.DATA_PATH + '/' + user_id + '.json', "w", encoding="UTF-8") as file:
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
    start_printed_timer(bot, message, time_tomato * 60, chat_id)
    bot.send_message(message.from_user.id, task['description'])
    bot.register_next_step_handler(message, lambda message: get_status_tomato(message, bot, task_id, current_time,
                                                                                    time_tomato))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    register_id(str(message.from_user.id))
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'остановить томат':
        try:
            with open('flag.json', 'r') as file:
                data_flags = json.load(file)
        except:
            data_flags = {}
        data_flags[str(message.from_user.id)] = {}
        data_flags[str(message.from_user.id)]['flag'] = 1
        with open('flag.json', 'w') as file:
            json.dump(data_flags, file)
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
        recommends_control.recomendation_command(bot, message, personal_reccomendation, chat_id)
    else:
        bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=funcs.get_keyboard_default())


bot.polling(none_stop=True)
