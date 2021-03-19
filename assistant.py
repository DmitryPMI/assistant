# pylint: disable=C0111,R0903
from enum import Enum
import json


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

    def load_from_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
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

    def save_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.users, file)


def test_create_user():
    assistant = Assistant()
    for score in range(Assistant.MaxScore):
        areas = {
            Assistant.User.AreaOfBalance(i): score
            for i in range(len(Assistant.User.AreaOfBalance))
        }
        user = f'user{score}'
        assistant.add_user(user, areas)
        assert (
            assistant.users[user].areas[Assistant.User.AreaOfBalance.Adventures]
            == score
        )


def test_add_task():
    assistant = Assistant()
    user = 'user with task'
    task_name = 'first task'
    area = Assistant.User.AreaOfBalance.Adventures
    description = 'some description'
    assistant.add_user(user).add_task(task_name, area, description)
    assert assistant.users[user].tasks[task_name].area == area
    assert assistant.users[user].tasks[task_name].description == description


def test_add_history():
    assistant = Assistant()
    user = 'user with history'
    task_name = 'first task'
    area = Assistant.User.AreaOfBalance.Adventures
    score = 3
    duration = 25
    ts = 1
    description = 'some description'

    assistant.add_user(user).add_task(task_name, area).add_history(
        score, duration, ts, description
    )
    assert assistant.users[user].tasks[task_name].history[0] == (
        score,
        duration,
        ts,
        description,
    )


test_create_user()
test_add_task()
test_add_history()