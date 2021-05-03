# pylint: disable=C0111,R0903
from enum import Enum
import json
import os


class Assistant:
    MaxScore = 10

    class User:
        class MostImportantQuestion(Enum):
            Experience = 0
            Growth = 1
            Contribution = 2

        class AreaOfBalance(Enum):
            # MostImportantQuestion = AreaOfBalance % 4
            LoveRelationship = 0
            Friendship = 1
            Adventures = 2
            Environment = 3
            Health = 4
            Intellectual = 5
            Skills = 6
            Spiritual = 7
            Career = 8
            Creative = 9
            Family = 10
            Community = 11

        class Task:
            def __init__(self, area, description=None):
                self.area = area
                self.description = description
                self.history = []

            def add_history(self, score, duration, ts, description):
                self.history.append((score, duration, ts, description))

        def __init__(self, areas=None):
            self.areas = areas
            self.tasks = {}

        def add_task(self, task_name, area: AreaOfBalance, description=None):
            self.tasks[task_name] = self.Task(area, description)
            return self.tasks[task_name]

    def __init__(self):
        self.users = {}

    def add_user(self, user, areas=None):
        if user in self.users:
            raise ValueError('already exists')
        self.users[user] = self.User(areas)
        return self.users[user]

    def load_from_json(self, path):
        files = os.listdir(path)
        data = {}
        for filename in files:
            with open(path + '/' + filename, 'r') as file:
                curr_data = json.load(file)
            data[filename.split('.')[0]] = curr_data
        # with open(filename, 'r') as file:
        #     data = json.load(file)
        users = data.keys()
        for user_id in users:
            user = self.User()
            for task_id, task_json in data[user_id]['tasks'].items():
                task = user.Task(6, task_json['description'])
                for tomato_id, tomato_json in data[user_id]['tomatoes'].items():
                    if tomato_json['task_id'] == task_id:
                        task.add_history(tomato_json['status'], tomato_json['time_tomato'], tomato_json['ts'], tomato_json['answer'])
                user.tasks[task_json['name']] = task
            self.users[user_id] = user

    def save_to_json(self, path):
        data = {}
        for user_id, user in self.users.items():
            data[user_id] = {'tasks': {}, 'tomatoes': {}}
            for task_name, task in user.tasks.items():
                data[user_id]['tasks'][task_name] = task.description
        # with open(filename, 'w') as file:
        #     json.dump(data, file)
        for key, value in data.items():
            with open(path + '/' + key + '.json', 'w') as file:
                json.dump(value, file)
