import pytest
from pathlib import Path
from main import *
import random

USER = "Testing"

def test_create_task(monkeypatch):
    global USER
    name = "create test" + str(random.random())
    inputs = iter([name, 'Test that task is created', 
                   'L','a','2025/12/12','N'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    createTask({"name": "Test"})
    x = db.users.find_one({"username":USER,"projects.tasks.title": name})
    assert x['projects'][0]['name'] == "Test"
    assert x['projects'][0]['tasks'][-1]['title'] == name
    assert x['projects'][0]['tasks'][-1]['description'] == "Test that task is created"
    assert x['projects'][0]['tasks'][-1]['status'] == "Not started"
    assert x['projects'][0]['tasks'][-1]['priority'] == "L"
    assert x['projects'][0]['tasks'][-1]['deadline'] == "2025/12/12"
    # db.users.find_one_and_update({"username":USER,"projects.tasks.title": name}, {"$pull": {"project.$.tasks.title": name}})

def test_no_title(monkeypatch,capsys):
    global USER
    name = "create test" + str(random.random())
    inputs = iter(["", name, 'Test that task is created', 
                   'L','a','2025/12/12','N'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    createTask({"name": "Test"})
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[0] == "Error: Task requires a name to create"
    x = db.users.find_one({"username":USER,"projects.tasks.title": name})
    assert x['projects'][0]['name'] == "Test"
    assert x['projects'][0]['tasks'][-1]['title'] == name
    


def test_add_field(monkeypatch,capsys):
    global USER
    name = "create test" + str(random.random())
    inputs = iter(["", name, 'Test that task is created', 
                   'L','a','2025/12/12','Y',"FieldTest","Field has been added","N"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    createTask({"name": "Test"})
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[0] == "Error: Task requires a name to create"
    x = db.users.find_one({"username":USER,"projects.tasks.title": name})
    assert x['projects'][0]['name'] == "Test"
    assert x['projects'][0]['tasks'][-1]['title'] == name
    assert x['projects'][0]['tasks'][-1]['custom_fields']["FieldTest"] == "Field has been added"

def test_sort_pri(capsys):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][1]
    sortByPriority(sortProj['tasks'])
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert "priority: H" in all_outputs[0]
    assert "priority: M" in all_outputs[1]
    assert "priority: L" in all_outputs[2]

def test_sort_deadline(capsys):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][1]
    sortDates(sortProj['tasks'])
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert "2023/12/12" in all_outputs[0]
    assert "2024/12/12" in all_outputs[1]
    assert "2025/12/12" in all_outputs[2]