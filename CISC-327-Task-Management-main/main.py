from taskManager import *
from datetime import datetime,date, timedelta
import re
import json
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://zachkizell87:f9gYzb7e5LKSkQJX@cluster0.eyssqkn.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["mydatabase"]

USER_DATA_FILE = "users.json"

#pull user info from JSON database
if os.path.exists(USER_DATA_FILE) and os.path.getsize(USER_DATA_FILE) > 0:
    with open(USER_DATA_FILE, "r") as file:
        user_data = json.load(file)
else: #if no file or empty file establish user database
    user_data = {}

#save info to user database
def save_user_data():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file)

#establish account
def create_account():
    username = input("Enter your username: ")
    if username in user_data:
        print("Username already exists. Please choose a different username.")
        create_account()
    else:
        password = input("Enter your password: ")
    #password strength checking
        if len(password) < 8 or \
            not any(char.isdigit() for char in password) or \
            not any(char.islower() for char in password) or \
            not any(char.isupper() for char in password) or \
            not any(char in "!@#$%^&*(),.?\":{}|<> " for char in password):
             print("Password must be at least 8 characters long and contain at least one each of:\nspecial character, capital letter, lowercase letter, and a number.")
             create_account()
        else:
            x = db.count.find({"_id": "UNIQUE COUNT DOCUMENT IDENTIFIER USERS"})
            db.users.insert_one({"_id": x[0]["COUNT"],"username":username, "password": password, "projects":[]})
            db.count.find_one_and_update(
                {"_id": "UNIQUE COUNT DOCUMENT IDENTIFIER USERS"},
                {"$inc": {'COUNT': 1}}
            )
            print("Account created successfully!")
            return [username, password]

#log-in function
def log_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user = db.users.find_one({"username": username, "password": password})
    
    if user:
        print("Login successful!")
        return user["projects"], [username, password]
    else:
        print("Invalid username or password. Please try again.")
        log_in()
        
def createTask(project):
    curr_project = db.projects.find_one({"_id": project})

    #creating a task by getting input of title, priority, status and deadline from user
    title = input("Enter a task name: ")

    desc = input("Add a task description: ")
    
    priority = input("Enter L for low priority, M for medium, H for high: ")
    
    status_choice = input("Choose a status:\na) not started\nb) in progress\nc) completed\n")
    if status_choice == "a":
        status = Status.NOT_STARTED
    elif status_choice == "b":
        status = Status.IN_PROGRESS
    else:
        status = Status.COMPLETED

    deadline = input("Enter due date in YYYY/MM/DD format: ")
    pattern = r'^\d{4}/\d{2}/\d{2}$'
    
    while ((re.match(pattern, deadline)) and (1 <= int(deadline[-2:]) <= 31) and (1 <= int(deadline[5:7]) <= 12)) != True:
        deadline = input("Enter due date in YYYY/MM/DD format: ")

    print("Would you like to add additional fields?")
    extra = input("Enter Y for yes, N for No: ")
    fields = {}
    while extra == "Y":
        fieldTitle = input("Enter the title of the new field: ")
        fieldDesc = input("Enter the description for the field: ")
        fields[fieldTitle] = fieldDesc
        print("Field has been added to task. Enter Y if you would like to add another")
        extra = input("")

    x = db.count.find({"_id": "UNIQUE COUNT DOCUMENT IDENTIFIER TASKS"})

    db.tasks.insert_many([{
        "title": title,
        "desc": desc,
        "status": status,
        "priority": priority,
        "project": curr_project["name"],
        "deadline": deadline,
        "fields": fields
    }])

    db.projects.find_one_and_update({"_id":curr_project["_id"]}, {"$push": {"tasks":x[0]["COUNT"]}})

    db.count.find_one_and_update(
        {"_id": "UNIQUE COUNT DOCUMENT IDENTIFIER TASKS"},
        {"$inc": {'COUNT': 1}}
    )

    task = Task(title, desc, status, priority, curr_project["name"], deadline, fields) #taking input from user and creating the object
    print("Succesfully Created!")

    
    
def changeStatus(project):
    # User can change task status
    task_name = input("Enter the task name: ")

    #finding task object
    task = db.tasks.find_one({"title": task_name})

    if task is not None:
        new_status = input("Enter new status:\n a) not started\n b) in progress\n c) completed\n")
        
        if new_status == "a":
            status = Status.NOT_STARTED
        elif new_status == "b":
            status = Status.IN_PROGRESS
        elif new_status == "c":
            status = Status.COMPLETED
        else:
            print("Invalid status choice.")
            return None

        #checking if new status is different than current status
        if task.status == status:
            print("Task is already in the selected status.")
        else:
            task.status = status
            print("Status changed.")
    else:
        print("Task not found.")
        
def viewStatus(project):
    # view status of a task
    task_name = input("Enter the task name: ")

    #finding task and outputting it for the user to see
    found_task = None
    for task in project.tasks:
        if task.title == task_name:
            print(task)
            return
    
    print("Task not found.")
    return
    
def createProject(user):
    project_name = input("Enter a project name: ")

    x = db.count.find_one_and_update(
        {"_id": "UNIQUE COUNT DOCUMENT IDENTIFIER PROJECTS"},
        {"$inc": {'COUNT': 1}},
        return_document=True
    )

    db.projects.insert_one({"_id": x["COUNT"], "name": project_name, "tasks": []})

    db.users.find_one_and_update(
        {"username": user[0], "password": user[1]},
        {"$push": {"projects": x["COUNT"]}}
    )

    project = Project(project_name)
    print(project)
    return project
def addTaskToProject():
    project_name = input("Enter the project name: ")

    #finding inputted project
    curr_project = db.projects.find_one({"name": project_name})
    if curr_project is not None:
        task_name = input("Enter the task name: ")

        curr_task = db.tasks.find_one({"title": task_name})
        if curr_task is not None:
            task_id = db.tasks.find_one({"title": task_name}, "_id")
            db.projects.find_one_and_update({"name": project_name, "tasks": curr_project["tasks"].append(task_id)})

        else:
            print("Task not found.")
    else:
        print("Project not found.")
    
def removeTaskFromProject():
    # User can remove task from project
    project_name = input("Enter the project name: ")

    # finding inputted project
    curr_project = db.projects.find_one({"name": project_name})
    if curr_project is not None:
        task_name = input("Enter the task name: ")

        curr_task = db.tasks.find_one({"name": task_name})
        if curr_task is not None:
            task_id = db.tasks.find_one({"title": task_name}, "_id")
            db.projects.find_one_and_update({"name": project_name, "tasks": curr_project["tasks"].remove(task_id)})

        else:
            print("Task not found.")
    else:
        print("Project not found.")
    
def viewProject():
    # Allows user to view project
    project_name = input("Enter the project name: ")

    # finding inputted project
    curr_project = db.projects.find_one({"name": project_name})
    if curr_project is not None:
        print(curr_project)
    else:
        print("Project not found.")

def sortByPriority(taskList):
    # Prints tasks sorted by priority
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
    # Prints tasks sorted by deadline
    taskList.sort(key=lambda date: datetime.strptime(date.deadline, "%Y/%m/%d"))
    taskList.reverse()
    for task in taskList:
        print(task)

def updatePriority(project):
    # User can update a priority deadline
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
    # User can update a task deadline
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
    


def chooseProj(projList,user):
    # Allows the user to create and manage projects
    check = True
    while check:
        if projList == []:
            print("You do not currently have any projects. Please create one.")
            project = createProject(user)
            projList.append(project)
        else:
            print("Enter the number associated with a project to access it. Enter P to create a new project ")
            print("Enter N to exit: ")
            x = 1
            projNames = db.projects.find({"_id": {"$in": projList}})
            for proj in projNames:
                print(str(x) + ". ", end="")
                print(proj["name"])
                x+=1
            custWant = input()
            if custWant == "P":
                project = createProject(user)
                projList.append(project)
                print("Do you want to access this project?")
                projCheck = input("Press Y to access, N to exit: ")
                if projCheck == "Y":
                    return project
                else:
                    print("Returning...")
            
            elif custWant == "N":
                return None

            elif custWant.isdigit() and int(custWant) > 0 and int(custWant) <= x:
                projToOpen = projList[int(custWant)-1]
                check = False
                return projToOpen
            else: 
                print("This is not a valid input, please try again")
    
def printTasks(project):
    # Prints all tasks in a project for user
    project.tasks.sort()
    if len(project.tasks) == 0:
        print("No tasks currently assigned to project")
    else:
        x = 1
        for task in project.tasks:
            print(str(x) + ". ", end="")
            print(task)
            x += 1

def notifyLate(projList):
    # Checks if any tasks are overdue and notifies user
    today = date.today()
    dates = today.strftime("%Y/%m/%d")
    times = dates.split("/")
    d1 = date(int(times[0]), int(times[1]), int(times[2]))
    for project in projList:
        lateTasks = []
        for task in project.tasks:
            deadline = task.deadline
            times2 = deadline.split("/")
            d2 = date(int(times2[0]), int(times2[1]), int(times2[2]))
            if d1 - d2 > timedelta(0):
                lateTasks.append(task)
        lateTasks.sort()
        if len(lateTasks) > 0:
            print("Late tasks in project ", end="")
            print(project)
            for task in lateTasks:
                print(task)

def projManage(project):
    # Function for interacting with tasks within a project
    check = True
    print("You have selected ", end="")
    print(project)
    while check:
        print("Press 1 to view tasks, 2 to create a task, 3 to update task details, 4 to exit")
        userInput = input()
        if userInput == "1":
            print("Press 1 to view sorted alphabetically, 2 to view sorted by priority, 3 to view sorted by deadline")
            view = input()
            if view == "1":
                printTasks(project)
            elif view == "2":
                sortByPriority(project.tasks)
            elif view == "3":
                sortDates(project.tasks)
            print("Enter the number associated with a task if you want to view more details")
            viewMore = input()
            if viewMore.isdigit():
                task = project.tasks[int(viewMore)-1]
                task.view_task()
        elif userInput == "2":
            createTask(project)
        elif userInput == "3":
            choice = input("Enter 1 to update a priority, 2 to update a deadline, 3 to update status: ")
            if choice == "1":
                updatePriority(project)
            elif choice == "2":
                updateDeadline(project)
            elif choice == "3":
                changeStatus(project)
        elif userInput == "4":
            check = False
        else: 
            print("Please enter a valid input")


def main():
    print("Welcome to our task management software!")
    print("Would you like to?")
    print("1. Create Account")
    print("2. Log In")
    choice = input("Enter your 1 or 2: ")
    projList = []
    if choice == "1":
        user = create_account()
    elif choice == "2":
        projList, user = log_in()
    
    check = True
    while check:
        #notifyLate(projList)
        proj = chooseProj(projList,user)
        if proj == None:
            check = False
            print("Thank you for using our program")
        else:
            projManage(proj)
    
    

 
    
if __name__ == "__main__":
    main()
