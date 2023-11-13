import pytest
from pathlib import Path
from main import *
import random

USER = "Testing"
def test_create_user(monkeypatch, capsys):
    name = "test user" + str(random.random())
    print(name)
    inputs = iter([name, 'passworD1@'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_account()
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[1] == "Account created successfully!"

    x = db.users.find_one({"username": name})
    assert x is not None
    assert x['username'] == name
    assert x['password'] == 'passworD1@'

def test_invalid_password(monkeypatch, capsys):
    name = "test user" + str(random.random())
    print(name)
    inputs = iter([name, 'invalid'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    try:
        create_account()
    except StopIteration:
        pass  # Handle StopIteration gracefully
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[1] == "Password must be at least 8 characters long and contain at least one each of:"

    x = db.users.find_one({"username": name})
    assert x is None

def test_preexisting_account(monkeypatch, capsys):
    name = "a"
    inputs = iter([name, 'a'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    try:
        create_account()
    except StopIteration:
        pass  # Handle StopIteration gracefully
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[0] == "Username already exists. Please choose a different username."

    x = db.users.find_one({"username": name})
    assert x is not None

def test_invalid_login(monkeypatch, capsys):
    name = "a"
    inputs = iter([name, 'invalid'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    try:
        log_in()
    except StopIteration:
        pass  # Handle StopIteration gracefully
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[0] == "Invalid username or password. Please try again."

    x = db.users.find_one({"username": name})
    assert x is not None

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
    x['projects'][0]['tasks'] = []
    db.users.find_one_and_update({"username":USER,"projects.name":x['projects'][0]['name']},
                                    {"$set": {"projects.$.tasks": x['projects'][0]['tasks']}})
    # db.users.find_one_and_update({"username":USER,"projects.tasks.title": name}, {"$pull": {"project.$.tasks.title": name}})

def test_add_member(monkeypatch,capsys):
    global USER
    inputs = iter(["Y", "a"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))
    addMembers({"name": "Test"})
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    x = db.users.find_one({"username":"a"})
    assert x['projects'][2]['name'] == "Test"

def test_add_nonexistent_member(monkeypatch,capsys):
    global USER
    name = "fake user" + str(random.random())
    inputs = iter(["Y", ""])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))
    try:
        addMembers({"name": "Test"})
    except StopIteration:
        pass  # Handle StopIteration gracefully
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[1] == "This user does not exist."

def test_assign_member(monkeypatch,capsys):
    userStuff = db.users.find_one({"username": USER})
    project = userStuff["projects"][1]
    inputs = iter(["1","1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assignTasks(project)
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert userStuff['projects'][1]['tasks'][-1]['assigned'] == []

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
    x['projects'][0]['tasks'] = []
    db.users.find_one_and_update({"username":USER,"projects.name":x['projects'][0]['name']},
                                    {"$set": {"projects.$.tasks": x['projects'][0]['tasks']}})


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
    x['projects'][0]['tasks'] = []
    db.users.find_one_and_update({"username":USER,"projects.name":x['projects'][0]['name']},
                                    {"$set": {"projects.$.tasks": x['projects'][0]['tasks']}})

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

def test_update_pri(monkeypatch):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","M",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updatePriority(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['priority'] == "M"
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","H",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updatePriority(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['priority'] == "H"
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","L",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updatePriority(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['priority'] == "L"

def test_update_deadline(monkeypatch):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","2027/12/12"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updateDeadline(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['deadline'] == "2027/12/12"
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","2025/12/12"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updateDeadline(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['deadline'] == "2025/12/12"

def test_not_dead(capsys):
    userStuff = db.users.find_one({"username": USER})
    notifyLate(userStuff['projects'])
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[0] == "Late tasks in project updateTest"
    assert all_outputs[1] == "lateTask"

def test_badInput_upPri(monkeypatch,capsys):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","fail","L"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updatePriority(sortProj)
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[4] == "Not a valid input, please try again"

def test_badIn_upDead(monkeypatch,capsys):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","fail","2025/12/12"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updateDeadline(sortProj)
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[4] == "Error: not a valid date"

    
