import sys

sys.path.append('../')

from assistant import Assistant
import json
import os


def test_init():
    ai = Assistant()
    assert ai.users == {}


def test_load_json():
    ai = Assistant()
    test_data = {"279501304": {"tasks": {
        "0": {"name": "\u0421\u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0438",
              "description": "\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0437\u0430\u0434\u0430\u0447 \u0441\u043e\u0441\u0442\u0430\u0432\u0438\u043b?",
              "status": 0}, "1": {"name": "\u041e\u0442\u043b\u0430\u0434\u0438\u0442\u044c \u043a\u043e\u0434",
                                  "description": "\u041a\u0430\u043a \u0442\u0430\u043c \u0441 \u043a\u043e\u0434\u043e\u043c?",
                                  "status": 1}, "2": {"name": "\u0421\u0434\u0435\u043b\u0430\u0442\u044c workflow",
                                                      "description": "\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0442\u0435\u0441\u0442\u043e\u0432 \u0434\u043e\u0431\u0430\u0432\u0438\u043b?",
                                                      "status": 0},
        "3": {"name": "123", "description": "123", "status": 1},
        "4": {"name": "123", "description": "123", "status": 0},
        "5": {"name": "1233123", "description": "123131231", "status": 0}}, "tomatoes": {
        "0": {"task_id": "0", "answer": "\u042f \u043f\u044b\u0442\u0430\u043b\u0441\u044f",
              "ts": "03/15/2021, 12:03:57", "status": "1", "time_tomato": 1}}}}
    with open('data/279501304.json', 'w') as file:
        json.dump(test_data['279501304'], file)
    ai.load_from_json('data')
    assert "279501304" in ai.users
    assert ai.users["279501304"].tasks[test_data["279501304"]["tasks"]["0"]["name"]].description == \
           test_data["279501304"]["tasks"]["0"]["description"]
    os.remove('data/279501304.json')


def test_save_json():
    ai = Assistant()
    test_data = {"279501304": {"tasks": {
        "0": {"name": "\u0421\u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0438",
              "description": "\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0437\u0430\u0434\u0430\u0447 \u0441\u043e\u0441\u0442\u0430\u0432\u0438\u043b?",
              "status": 0}, "1": {"name": "\u041e\u0442\u043b\u0430\u0434\u0438\u0442\u044c \u043a\u043e\u0434",
                                  "description": "\u041a\u0430\u043a \u0442\u0430\u043c \u0441 \u043a\u043e\u0434\u043e\u043c?",
                                  "status": 1}, "2": {"name": "\u0421\u0434\u0435\u043b\u0430\u0442\u044c workflow",
                                                      "description": "\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0442\u0435\u0441\u0442\u043e\u0432 \u0434\u043e\u0431\u0430\u0432\u0438\u043b?",
                                                      "status": 0},
        "3": {"name": "123", "description": "123", "status": 1},
        "4": {"name": "123", "description": "123", "status": 0},
        "5": {"name": "1233123", "description": "123131231", "status": 0}}, "tomatoes": {
        "0": {"task_id": "0", "answer": "\u042f \u043f\u044b\u0442\u0430\u043b\u0441\u044f",
              "ts": "03/15/2021, 12:03:57", "status": "1", "time_tomato": 1}}}}
    with open('data/279501304.json', 'w') as file:
        json.dump(test_data['279501304'], file)
    ai.load_from_json('data')
    ai.save_to_json('data')
    with open('data/279501304.json', 'r') as file:
        data = json.load(file)
    assert "279501304.json" in os.listdir('data')
    os.remove('data/279501304.json')


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
