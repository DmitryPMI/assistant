import funcs
import recommend
import json

reccomends_file = 'recs_file.json'

recs_commands = ['персональная подборка',
                 'узнать рейтинг',
                 'запустить следующую задачу',
                 'выбрать томат',
                 'запустить случайный томат',
                 'выбрать другой',
                 'запустить']

print(recs_commands)


def start_challenge(bot, message, chat_id, task):
    print('starting_challenge')
    funcs.start_printed_timer(bot, message, 3, chat_id)
    bot.send_message(message.from_user.id, text="Отлично! Оцени задание по 5-бальной шкале:",
                     reply_markup=funcs.get_task_evaluation())


def is_refers_to_reccomendation(message):
    print(message.text)
    if message.text.lower() in recs_commands or message.text in recommend.challenge_list:
        return 1
    else:
        return 0


def recomendation_command(bot, message, personal_reccomendation, chat_id):
    if message.text.lower() == 'персональная подборка':
        personal_reccomendation.add_new_user(message.from_user.id)
        if personal_reccomendation.get_count(message.from_user.id) == 0:
            bot.send_message(message.from_user.id,
                             "Добро пожаловать в систему индивидуальных рекомендаций. Здесь вы сможете получать "
                             "личные рекомендации на томаты, проходить их, набирать рейтинг, и соревноваться с "
                             "друзьями. Для начала вам необходимо выполнить 5 заданий, которые вы можете выбрать "
                             "сами, либо же получить рандомное задание. Пожалуйста, поставьте оценку выполненному "
                             "заданию, чтобы я быстрее смог начать подбирать для тебя задания.",
                             reply_markup=funcs.get_keyboard_personal())
        else:
            bot.send_message(message.from_user.id, 'Что дальше?',
                             reply_markup=funcs.get_keyboard_personal())
    elif message.text.lower() == 'узнать рейтинг':
        bot.send_message(message.from_user.id,
                         'Твой рейтинг - ' + str(personal_reccomendation.get_rating(message.from_user.id)))
    elif message.text.lower() == 'запустить следующую задачу':
        user_id = message.from_user.id
        personal_reccomendation.add_new_user(user_id)
        if personal_reccomendation.get_count(user_id) >= 5:
            nearest, reccomends = personal_reccomendation.predict(user_id)
            bot.send_message(user_id, 'Ваша персональная подборка томатов:',
                             reply_markup=funcs.get_personal_tasks(
                                 [recommend.challenge_list[ind] for ind in reccomends]
                             ))
        else:
            bot.send_message(user_id, 'Осталось выполнить ' + str(
                5 - personal_reccomendation.get_count(user_id)) + ' томатов до конца калибровки.',
                             reply_markup=funcs.get_personal_keyboard_task_type())

    elif message.text.lower() == 'выбрать томат':
        bot.send_message(message.from_user.id, 'Я этого пока не умею(((')
    elif message.text.lower() == 'запустить случайный томат' or message.text.lower() == 'выбрать другой':
        print('  pressed (Запустить случайный томат) or (Выбрать другой)')
        personal_reccomendation.add_random_next(message.from_user.id)
        bot.send_message(message.from_user.id,
                         'Твой томат: ' + personal_reccomendation.get_next_challenge(message.from_user.id),
                         reply_markup=funcs.get_personal_random_choice())
    elif message.text.lower() == 'запустить':
        print('  pressed (Запустить)')
        start_challenge(bot, message, chat_id, personal_reccomendation.get_next_challenge(message.from_user.id))
    elif message.text in recommend.challenge_list:
        print('  started recomended task')
        start_challenge(bot, message, chat_id, message.text)
    else:
        print(message.text)
        bot.send_message(message.from_user.id, text="А теперь?", reply_markup=funcs.get_keyboard_default())
