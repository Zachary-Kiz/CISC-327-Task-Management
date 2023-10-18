from taskManager import *
from datetime import date
import re

def createTask():
    
    title = input("Enter a task name: ")
    
    priority = input("Enter L for low priority, M for medium, H for high: ")
    
    status_choice = input("Choose a status:\na) not started\nb) in progress\nc) completed\n")
    if status_choice == "a":
        status = Status.NOT_STARTED
    elif status_choice == "b":
        status = Status.IN_PROGRESS
    else:
        status = Status.COMPLETED
        
    
    project = None

    deadline = input("Enter due date in YYYY/MM/DD format: ")
    pattern = r'^\d{4}/\d{2}/\d{2}$'
    
    while ((re.match(pattern, deadline)) and (1 <= int(deadline[-2:]) <= 31) and (1 <= int(deadline[5:7]) <= 12)) != True:
        deadline = input("Enter due date in YYYY/MM/DD format: ")


    task = Task(title, status, priority, project, deadline)
    print(task)

    
    
def changeStatus():
    task_name = input("Enter the task name: ")

    found_task = None
    for task in Task().tasks:
        if task.title == task_name:
            found_task = task
            break

    if found_task is not None:
        new_status = input("Enter new status:\n a) not started\n b) in progress\n c) completed\n")
        
        if new_status == "a":
            status = Status.NOT_STARTED
        elif new_status == "b":
            status = Status.IN_PROGRESS
        elif new_status == "c":
            status = Status.COMPLETED
        else:
            print("Invalid status choice.")
            return

        if found_task.status == status:
            print("Task is already in the selected status.")
        else:
            found_task.status = status
            print("Status changed.")
    else:
        print("Task not found.")
        
def viewStatus():
    task_name = input("Enter the task name: ")

    found_task = None
    for task in Task().tasks:
        if task.title == task_name:
            print(task)
    
    print("Task not found.")
    
def createProject():
    project_name = input("Enter a project name: ")
    
    project = Project(project_name)
    print(project)
    
def addTaskToProject():
    project_name = input("Enter the project name: ")

    found_project = None
    for project in Project().projects:
        if project.name == project_name:
            
            task_name = input("Enter the task name: ")
        
            found_task = None
            for task in Task().tasks:
                if task.title == task_name:
                    project.add_task(task)
            
            print("Task not found.")            
    
    print("Project not found.")    
    
def removeTaskFromProject():
    project_name = input("Enter the project name: ")

    found_project = None
    for project in Project().projects:
        if project.name == project_name:
            
            task_name = input("Enter the task name: ")
        
            found_task = None
            for task in Task().tasks:
                if task.title == task_name:
                    project.remove_task(task)
            
            print("Task not found.")            
    
    print("Project not found.")    
    
def viewProject():
    
    found_project = None
    for project in Project().projects:
        if project.name == project_name:
            print(project)
            
    print("Project not found.")   




def main():

    createTask()
    
    changeStatus()
    
    viewStatus()
    
    createProject()
    
    addTaskToProject()
    
    removeTaskFromProject()
    
    viewProject()
    
    

 
    
if __name__ == "__main__":
    main()
