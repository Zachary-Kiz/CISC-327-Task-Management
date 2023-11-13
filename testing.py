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
    x['projects'][0]['tasks'] = []
    db.users.find_one_and_update({"username":USER,"projects.name":x['projects'][0]['name']},
                                    {"$set": {"projects.$.tasks": x['projects'][0]['tasks']}})
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
    
def test_create_due_task(capsys,monkeypatch):
     global USER
     name = "create test" + str(random.random())
     inputs = iter([name, 'Test that task is created', 
                   'L','a','2000/12/12','Y',"N"])
     monkeypatch.setattr('builtins.input', lambda _: next(inputs))
     createTask({"name": "Test"})
     captured = capsys.readouterr()
     all_outputs = captured.out.split('\n')
     assert all_outputs[0] == "Deadline is past due. Do you still want to create?"
     x = db.users.find_one({"username":USER,"projects.tasks.title": name})
     assert x['projects'][0]['tasks'][-1]['deadline'] == '2000/12/12'
     x['projects'][0]['tasks'] = []
     db.users.find_one_and_update({"username":USER,"projects.name":x['projects'][0]['name']},
                                    {"$set": {"projects.$.tasks": x['projects'][0]['tasks']}})
     
def test_opt_out_create_due_task(capsys,monkeypatch):
    global USER
    name = "create test" + str(random.random())
    inputs = iter([name, 'Test that task is created', 
                   'L','a','2000/12/12','N',"2200/12/12","N"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    createTask({"name": "Test"})
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[0] == "Deadline is past due. Do you still want to create?"
    x = db.users.find_one({"username":USER,"projects.tasks.title": name})
    assert x['projects'][0]['tasks'][-1]['deadline'] == '2200/12/12'
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

def test_pri_M(monkeypatch):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","M",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updatePriority(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['priority'] == "M"

def test_pri_H(monkeypatch):
    userStuff = db.users.find_one({"username": USER})
    sortProj = userStuff["projects"][2]
    inputs = iter(["1","H",])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    updatePriority(sortProj)
    userStuff = db.users.find_one({"username": USER})
    assert userStuff['projects'][2]['tasks'][0]['priority'] == "H"

def test_pri_L(monkeypatch):
    userStuff = db.users.find_one({"username": USER})
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
    assert all_outputs[0] == "Late tasks in project updateTests"
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

def test_change_task_status(monkeypatch):
    global USER
    name = "create test" + str(random.random())
    inputs = iter([name, 'Test that task is created',
                   'L', 'a', '2025/12/12', 'N'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    createTask({"name": "Test"})
    x = db.users.find_one({"username": USER, "projects.tasks.title": name})

    inputs_change_status = iter(["1", "c"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_change_status))
    changeStatus(x['projects'][0])

    updated_status = db.users.find_one({"username": USER, "projects.tasks.title": name})
    assert updated_status == "Completed"


def test_create_project(monkeypatch):
    global USER

    name = "Test"

    inputs_create_project = iter([name])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_create_project))
    createProject()

    userStuff = db.users.find_one({"username": USER})
    projects = userStuff.get("projects", [])
    project_names = [project['name'] for project in projects]

    assert name in project_names


def test_add_tasks_to_project(monkeypatch):
    global USER
    project_name = "Test"

    inputs_create_task = iter(["Testing Task", 'Task description', 'M', 'b', '2025/12/12', 'N'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_create_task))
    createTask({"name": project_name})

    project_data = db.users.find_one({"username": USER, "projects.name": project_name})
    project = project_data.get("projects", [])

    project_names = [project['name'] for project in project]

    assert project is not None
    assert "Testing Task" in project_names

