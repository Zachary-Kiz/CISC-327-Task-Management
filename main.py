from taskManager import *
from datetime import datetime,date, timedelta
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
    return project
    
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

def sortByPriority(taskList):
    lowPri = []
    medPri = []
    highPri = []
    for task in taskList:
        if task.priority == "L":
            lowPri.append(task)
        if task.priority == "M":
            medPri.append(task)
        if task.priority == "H":
            highPri.append(task)
    lowPri.sort()
    medPri.sort()
    highPri.sort()
    highPri.extend(medPri)
    highPri.extend(lowPri)
    x = 1
    for title in highPri:
        print(str(x) + ". " + title.title)
        x += 1


def sortDates(taskList):
    taskList.sort(key=lambda date: datetime.strptime(date.deadline, "%Y/%m/%d"))
    taskList.reverse()
    for task in taskList:
        print(task)

def updatePriority(project):
    printTasks(project)
    taskNum = input("Enter the number associated with the task whose priority you want to update: ")
    task = project.tasks[int(taskNum) - 1]
    print("Task priority is: " + task.priority)
    update = input("Enter the new priority of the task: ")
    priors = ["L","M","H"]
    while update not in priors:
        print("Not a valid input, please try again")
        update = input("Enter the new priority of the task: ")
    task.update_pri(update)

def updateDeadline(project):
    printTasks(project)
    taskNum = input("Enter the number associated with the task whose deadline you want to update: ")
    task = project.tasks[int(taskNum) - 1]
    if task.deadline == None:
        print("Task does not currently have a deadline")
    else: 
        print("Task priority is: " + task.deadline)
    deadline = input("Enter the new deadline of the task: ")
    pattern = r'^\d{4}/\d{2}/\d{2}$'
    
    while ((re.match(pattern, deadline)) and (1 <= int(deadline[-2:]) <= 31) and (1 <= int(deadline[5:7]) <= 12)) != True:
        deadline = input("Enter due date in YYYY/MM/DD format: ")
    task.update_date(deadline)
    


def chooseProj(projList):
    check = True
    while check:
        if projList == []:
            print("You do not currently have any projects. Please create one.")
            project = createProject()
            projList.append(project)
        else:
            print("Enter the number associated with a project to access it. Enter P to create a new project: ")
            x = 1
            for proj in projList:
                print(str(x) + ". " + proj)
                x+=1
            custWant = input()
            if custWant == "P":
                project = createProject()
                projList.append(project)

            elif custWant.isdigit() and int(custWant) > 0 and int(custWant) <= x:
                projToOpen = projList[x-1]
                check = False
            else: 
                print("This is not a valid input, please try again")
    
def printTasks(project):
    project.tasks.sort()
    x = 1
    for task in project.tasks:
        print(str(x) + ". ", end="")
        print(task)
        x += 1

def notifyLate(projList):
    today = date.today()
    dates = today.strftime("%Y/%m/%d")
    times = dates.split("/")
    d1 = date(dates[0], dates[1], dates[2])
    for project in projList:
        lateTasks = []
        for task in project.tasks:
            deadline = task.deadline
            times2 = deadline.split("/")
            d2 = date(times2[0], times2[1], times2[2])
            if d1 - d2 > timedelta(0):
                lateTasks.append(task)
        lateTasks.sort()
        if len(lateTasks) > 0:
            print("Late tasks in project ", end="")
            print(project)
            for task in lateTasks:
                print(task)





def main():
    print("Welcome to our task management software!")
    projList = []
    x = Task("Hello")
    y = Task("Allo")
    proj = Project("Proj1")
    proj.tasks.append(x)
    proj.tasks.append(y)
    updateDeadline(proj)
    
    

 
    
if __name__ == "__main__":
    main()
