import pytest
from pathlib import Path
from main import *
import random

USER = "Testing"

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
