import pytest
from pathlib import Path
from main import *
import random

USER = "adamciszek"

def test_no_add_member(monkeypatch,capsys):
    global USER
    inputs = iter(["N"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))
    try:
        addMembers({"name": "Test"})
    except StopIteration:
        pass  # Handle StopIteration gracefully
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[1] == ""

def test_add_existing_member(monkeypatch,capsys):
    global USER
    inputs = iter(["Y", "a"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))
    addMembers({"name": "Test"})
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    x = db.users.find_one({"username":"a"})
    assert x['projects'][1]['name'] == "Test"

def test_add_nonexisting_member(monkeypatch,capsys):
    global USER
    inputs = iter(["Y", "NonExistent"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))
    try:
        addMembers({"name": "Test"})
    except StopIteration:
        pass  # Handle StopIteration gracefully
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    assert all_outputs[1] == "This user does not exist."

def test_add_nonexisting_recursive_member(monkeypatch,capsys):
    global USER
    inputs = iter(["Y", "NonExistent"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))
    try:
        addMembers({"name": "Test"})
    except StopIteration:
        inputs = iter(["Y", "a"])
    captured = capsys.readouterr()
    all_outputs = captured.out.split('\n')
    x = db.users.find_one({"username":"a"})
    assert x['projects'][1]['name'] == "Test"


def test_update_priority_valid(monkeypatch,capsys):
    global USER
    project = db.users.find_one({"username": USER}).get('projects', [])[0]
    inputs = iter(["1", "M"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))

    updatePriority(project)

    captured = capsys.readouterr()
    assert "Priority changed!" in captured.out

    updated_task = db.users.find_one({"username": USER, "projects.name": project['name']})['projects'][0]['tasks'][0]
    assert updated_task['priority'] == "M"


def test_update_priority_nonexisting_task(monkeypatch,capsys):
    global USER
    project = db.users.find_one({"username": USER}).get('projects', [])[0]
    inputs = iter(["5"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))

    try:
        updatePriority(project)
    except StopIteration:
        pass

    captured = capsys.readouterr().out.split('\n')
    assert "invalid input." in captured


def test_update_priority_invalid_priority(monkeypatch,capsys):
    global USER
    project = db.users.find_one({"username": USER}).get('projects', [])[0]
    inputs = iter(["1", "a"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))

    try:
        updatePriority(project)
    except StopIteration:
        pass

    captured = capsys.readouterr().out.split('\n')
    assert "Not a valid input, please try again" in captured


def test_update_priority_same_priority(monkeypatch,capsys):
    global USER
    project = db.users.find_one({"username": USER}).get('projects', [])[0]
    inputs = iter(["1", "M"])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: next(inputs))

    updatePriority(project)

    captured = capsys.readouterr().out.split('\n')
    assert "you have selected the same priority" in captured



