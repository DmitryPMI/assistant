import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import collections
 
challenge_list = ['Примите душ (серотонин)',
                  'Примите контрастный душ (серотонин/эндорфин)',
                  'Прогуляйтесь (серотонин)',
                  'Спойте песню/наиграйте мелодию (дофамин',
                  'Нарисуйте картинку (дофамин)',
                  'Порисуйте двумя руками (дофамин)',
                  'Съешьте что-то новое (дофамин)',
                  'Посмотрите познавательное видео (дофамин)',
                  'Поиграйте в настольные/компьютерные игры (дофамин)',
                  'Сходите в кино (дофамин)',
                  'Сходите в театр (дофамин)',
                  'Купите необычную специю (дофамин)',
                  'Начните читать новую книгу (дофамин)',
                  'Послушайте аудиокнигу (дофамин)',
                  'Запишите пять своих желаний (дофамин)',
                  'Выберите подарок самому себе (серотонин)',
                  'Приготовьте в будний день праздничную еду (дофамин)',
                  'Нарисуйте свои эмоции красками (дофамин)',
                  'Примите горячую ванну (серотонин)',
                  'Сделайте маску для лица, дома или в салоне (дофамин)',
                  'Примите комплимент или сделайте себе сами комплимент (серотонин)',
                  'Посмотрите смешные видео (серотонин/эндорфин)',
                  'Украсьте свой дом или рабочее место свежими цветами (дофамин)',
                  'Сделайте однодневную поездку в интересное и веселое место в вашем районе, как аквариум, зоопарк или тематический парк (дофамин)',
                  'Поблуждайте в книжном магазине (дофамин)',
                  'Посетите магазин с модной одеждой и аксессуаров (дофамин)',
                  'Посмотрите пьесу, концерт или другое художественное исполнение (дофамин)',
                  'Присутствуйте на спортивном мероприятии (дофамин)',
                  'Посмотрите фильм (дофамин)',
                  'Наблюдайте восход солнца или закат (дофамин)',
                  'Слушайте аудио релаксации (дофамин)',
                  'Устройте пикник/термос с чаем в парке (дофамин)',
                  'Почитайте журнал (дофамин)',
                  'Сделайте себе маникюр и / или педикюр (дофамин)',
                  'Привлекайте немного к садоводству себя (дофамин)',
                  'Сходите в музей (дофамин)',
                  'Организуйте поездку, даже если это на весь выходной, в пункт назначения за несколько часов езды. Узнайте новое место (дофамин)',
                  'Сходите в парк (дофамин)',
                  'Купите себе хороший журнал, чтобы написать размышления, эмоции, цели, мечты (дофамин)',
                  'Это вещь, которую давно хотели сделать, но постоянно откладывали? Сделайте это (дофамин)',
                  'Не откладывайте достижение Ваших целей и мечтаний. Дайте себе в награду живую жизнь, в максимально возможной степени и в настоящее время. В настоящем это все есть. Не ждите, либо, пока не достигните своих целей, не сможете позволить себе одну из следующих наград (дофамин)',
                  'Сделайте кому-то неожиданный подарок - букет цветов, приготовленный в домашних условиях, еда, или что-то другое. Подлинная благодарность от любимого человека является большой наградой (окситоцин)',
                  'Возьмите мини-отпуск. Возьмите один или два дня от работы и сделайте все, что вам нужно и хотите с вашим временем (серотонин)',
                  'Практикуйте писательское творчество (дофамин/серотонин)',
                  'Работа над проектом ремесла, которое Вам нравится. Найдите веб-сайты, которые сосредоточены над проектами для идей «сделай сам» (серотонин)',
                  'Определите беззаботный день (дофамин)',
                  'Купите и соберите головоломку (дофамин/серотонин)',
                  'Посмотрите антикварный или благотворительный магазин (дофамин)',
                  'Зажгите свечи. Свечи-то делают необычным мир, он кажется волшебным (эндорфин)']

# В данном случае, influence = [серотонин, эндорфин, дофамин, окситоцин]

influence = [[1, 0, 0, 0],
             [1, 1, 0, 0],
             [2, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 2, 0],
             [0, 0, 3, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 2, 0],
             [0, 0, 1, 0],
             [0, 0, 2, 0],
             [0, 0, 4, 0],
             [0, 0, 5, 0],
             [0, 0, 3, 0],
             [0, 0, 1, 0],
             [1, 0, 0, 0],
             [0, 0, 4, 0],
             [0, 0, 2, 0],
             [4, 0, 0, 0],
             [0, 0, 1, 0],
             [2, 0, 0, 0],
             [1, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 2, 0],
             [0, 0, 4, 0],
             [0, 0, 2, 0],
             [0, 0, 3, 0],
             [0, 0, 1, 0],
             [0, 0, 5, 0],
             [0, 0, 2, 0],
             [0, 0, 3, 0],
             [0, 0, 1, 0],
             [0, 0, 6, 0],
             [0, 0, 1, 0],
             [0, 0, 3, 0],
             [0, 0, 4, 0],
             [0, 0, 6, 0],
             [0, 0, 2, 0],
             [0, 0, 7, 0],
             [0, 0, 3, 0],
             [0, 0, 0, 1],
             [5, 0, 0, 0],
             [2, 0, 3, 0],
             [2, 0, 0, 0],
             [0, 0, 4, 0],
             [2, 0, 1, 0],
             [0, 0, 2, 0],
             [0, 3, 0, 0]]


def create_data(datasize):
    challenges = np.array([random.randint(0, len(challenge_list) - 1) for _ in range(datasize)])
    data = {'personId': np.array([random.randint(10000, 11000) for _ in range(datasize)]),
            'time': np.array([random.randint(100000, 999999) for _ in range(datasize)]),
            'benefit': np.array([random.randint(1, 5) for _ in range(datasize)]),
            'challengenumber': challenges,
            'textmessage': np.array([challenge_list[i] for i in challenges])}
    df = pd.DataFrame(data=data)

    event_type_strength = {
        1: 0.2,
        2: 0.4,
        3: 0.6,
        4: 0.8,
        5: 1.0,
    }

    df['eventStrength'] = df['benefit'].apply(lambda x: event_type_strength[x])

    del df['benefit']
    del df['textmessage']

    profs = make_new_profiles(df)
    inters = make_new_interests(df)
    bans = make_new_bans(df)

    return profs, inters, bans


def make_new_profiles(df):
    profiles = {}
    df_matrix = np.array(df)
    for line in df_matrix:
        if line[0] not in profiles.keys():
            profiles[int(line[0])] = np.array(influence[int(line[2])]) * line[3]
        else:
            profiles[int(line[0])] += np.array(influence[int(line[2])]) * line[3]
    return profiles


def make_new_interests(df):
    interests = {}
    df_matrix = np.array(df)
    for line in df_matrix:
        if line[3] >= 0.8:
            if line[0] not in interests.keys():
                interests[int(line[0])] = [int(line[2])]
            else:
                interests[int(line[0])].append(int(line[2]))
    return interests


def make_new_bans(df):
    bans = {}
    df_matrix = np.array(df)
    for line in df_matrix:
        if line[3] < 0.5:
            if line[0] not in bans.keys():
                bans[int(line[0])] = [int(line[2])]
            else:
                bans[int(line[0])].append(int(line[2]))
    return bans


def euclidean(x, y):
    s = 0
    for i in range(len(x)):
        s += (x[i] - y[i]) ** 2
    return np.sqrt(s)


def uniq(arr):
    a = []
    for i in arr:
        if i not in a:
            a.append(i)
    return a


class KNNRec(object):
    def __init__(self):
        self.dic = None
        self.interests = {}
        self.dic = {}
        self.bans = {}

    def fit(self, dic, interests, bans):
        self.interests = interests
        self.dic = dic
        self.bans = bans

    def predict(self, key):
        ### Ищем ближайший профиль ###

        profile = self.dic[key]
        min_key = list(self.dic.keys())[0]
        min_dist = euclidean(profile, self.dic[min_key])
        for i in self.dic.keys():
            if not np.array_equal(profile, self.dic[i]):
                dist = euclidean(profile, self.dic[i])
                if dist < min_dist:
                    min_dist = dist
                    min_key = i

        # 1 подход. Оставим рекомендации, которые один сделал, а другой нет ###

        ints2 = self.interests[min_key]
        # ints1 = self.interests[key]
        # ints_final = [interest for interest in ints2 if interest not in ints1]

        # 2 подход. Используем баны ###

        bans1 = self.bans[key]
        ints_final = [interest for interest in ints2 if interest not in bans1]
        counts = collections.Counter(ints_final)
        new_ints_final = uniq(sorted(ints_final, key=lambda x: -counts[x]))[:3]

        return min_key, new_ints_final

    def update_profiles(self, id, challenge_number, benefit):
        self.dic[id] = self.dic[id] + np.array(influence[challenge_number]) * event_type_strength[benefit]
        if event_type_strength[benefit] >= 0.8:
            self.interests[id].append(challenge_number)
        if event_type_strength[benefit] < 0.5:
            self.bans[id].append(challenge_number)

    def get_rating(self, id):
        return (self.dic[id]).sum()

    def get_mean(self, id):
        return (self.dic[id]).mean()


# метод fit принимает 3 параметра: словарь профилей, словарь интересов, словарь банов
# метод predict принимает id пользователя, возвращает 3 лучших рекомендации
# метод update_profiles получает id человека, номер выполненного упражнения, и оценку.
# В соответствии с этим меняет профиль.
# метод get_rating возвращает суммарный скор (сумму профиля) для определенного id
# метод get_mean возвращает средний показатель профиля для определенного id

# Тут создается искусственный датасет, чтобы сеть как-то работала
profiles, interests, bans = create_data(30000)

rec_model = KNNRec()
rec_model.fit(profiles, interests, bans)
