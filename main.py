from taskManager import *
from datetime import datetime,date, timedelta
import re
from pymongo import MongoClient
import os

client = MongoClient("mongodb+srv://zachkizell87:f9gYzb7e5LKSkQJX@cluster0.eyssqkn.mongodb.net/?retryWrites=true&w=majority")  
db = client["mydatabase"]
USER = None

def create_account():
    global USER
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if db.users.find_one({"username": username}):
        print("Username already exists. Please choose a different username.")
        create_account()
    else:
        if len(password) < 8 or \
            not any(char.isdigit() for char in password) or \
            not any(char.islower() for char in password) or \
            not any(char.isupper() for char in password) or \
            not any(char in "!@#$%^&*(),.?\":{}|<> " for char in password):
            print("Password must be at least 8 characters long and contain at least one each of:\nspecial character, capital letter, lowercase letter, and a number.")
            create_account()
        else:
            db.users.insert_one({"username": username, "password": password})
            USER = username
            print("Account created successfully!")
            

def log_in():
    global USER
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    userCheck = db.users.find_one({"username": username, "password": password})

    if userCheck:
        USER = username
        print("Login successful!")
    else:
        print("Invalid username or password. Please try again.")
        log_in()
    
def createTask(project):
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
    assign = []
    print("Would you like to add additional fields?")
    extra = input("Enter Y for yes, N for No: ")
    fields = {}
    while extra == "Y":
        fieldTitle = input("Enter the title of the new field: ")
        fieldDesc = input("Enter the description for the field: ")
        fields[fieldTitle] = fieldDesc
        print("Field has been added to the task. Enter Y if you would like to add another")
        extra = input("Enter Y for yes, N for No: ")

    task_data = {
        "title": title,
        "description": desc,
        "status": status,
        "priority": priority,
        "deadline": deadline,
        "assigned": assign,
        "custom_fields": fields
    }
    
    members = db.users.find({"projects.name": project['name']})
    memberList = list(members)
    if memberList is []:
        db.users.update_one({"username": USER, "projects.name": project['name']},
                        {"$push": {"projects.$.tasks": task_data}})
    else:
        for i, member in enumerate(memberList, start=1):
            db.users.update_one({"username": member['username'], "projects.name": project['name']},
                        {"$push": {"projects.$.tasks": task_data}})
    
    print("Task created successfully")

    if extra == "N":
        print("Returning to project management...")
        return projManage(project)

def updateUsers(project):
    None
    
def changeStatus(project):
    # User can change task status
    task_name = input("Enter the task name: ")

    #finding task object
    found_task = None
    for task in project.tasks:
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

        #checking if new status is different than current status
        if found_task.status == status:
            print("Task is already in the selected status.")
        else:
            found_task.status = status
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
    
    
def addTaskToProject():
    project_name = input("Enter the project name: ")

    #finding inputted project
    found_project = None
    for project in Project().projects:
        if project.name == project_name:
            
            task_name = input("Enter the task name: ")

            #finding inputted task
            found_task = None
            for task in Task().tasks:
                if task.title == task_name:
                    project.add_task(task) #adding task to project
            
            print("Task not found.")            
    
    print("Project not found.")    
    
def removeTaskFromProject():
    # User can remove task from project
    project_name = input("Enter the project name: ")

    found_project = None
    for project in Project().projects:
        if project.name == project_name:
            
            task_name = input("Enter the task name: ")
        
            found_task = None
            for task in Task().tasks:
                if task.title == task_name:
                    project.remove_task(task) #removing task from project if both task and project are found
            
            print("Task not found.")            
    
    print("Project not found.")    
    
def viewProject():
    #allows user to view project
    project_name = input("Enter the project name: ")
    
    #finding inputted project and outputting it
    project = db.users.find_one({"username": USER, "projects.name": project_name})

    if project:
        printTasks(project)

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
    
def projectExistCheck():
    global USER
    if db.users.find_one({"username": USER, "projects": {"$exists": True, "$ne": []}}):
        return True
    else:
        return False

def createProject():
    global USER
    projectName = input("Enter a project name: ")
    newProject = {
        "name": projectName,
        "tasks": []
    }
    db.users.update_one({"username": USER}, {"$push": {"projects": newProject}})
    print(f"Project '{projectName}' added for user '{USER}'")

def chooseProj(projList):
    # Allows the user to create and manage projects
    global USER
    check = projectExistCheck()
    if not check:
            print("You do not currently have any projects. Please create one.")
            projectName = input("Enter a project name: ")
            newProject = {
                "name": projectName,
                "tasks": []
            }
            db.users.update_one({"username": USER}, {"$push": {"projects": newProject}})
            print(f"Project '{projectName}' added for user '{USER}'")
    projects = db.users.find_one({"username": USER}).get("projects", [])
    print(f"Projects for user '{USER}':")
    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project['name']}")
    select = int(input("Enter the number associated with the project to select it, or 0 to create another project: "))
    if 1 <= select <= len(projects):
        selectProject = projects[select - 1]
        print(f"You selected project: '{selectProject['name']}'")
        projManage(selectProject)
    elif select == 0:
        createProject()
        chooseProj(None)
    else:
        print("Invalid entry. Please try again.")
        
def printTasks(project):
    # Prints the names of all tasks in the project
    tasks = project['tasks']
    print(tasks)

    if not tasks:
        print("No tasks currently assigned to this project.")
    else:
        print("Tasks in project:", project['name'])
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task['title']}")

#add members to the current project
def addMembers(project):
    global USER
    print("Would you like to add team members to this project? Y or N")
    userInput = input()
    if userInput == "Y":
        memberName = input("Enter the username you would like to add:")
        userCheck = db.users.find_one({"username": memberName})
        if not userCheck:
            print("This user does not exist.")
            addMembers(project)
        else:
            project_data = {
                "name": project['name'],
            }
            db.users.update_one({"username": memberName}, {"$push": {"projects": project}})
            print(f"User {memberName} added to the project.")
    else:
        return None

#assign team members in project to certain tasks 
def assignTasks(project):
    members = db.users.find({"projects.name": project['name']})
    print(f"Members for project {project['name']}:")
    memberList = list(members)
    if memberList is []:
        print("There are no team members in your project.")
        return None
    else:
        for i, member in enumerate(memberList, start=1):
            print(f"User {i}: {member['username']}")
        selected = input("Enter the number corresponding to the user you want to assign: ")
        try:
            selected = int(selected)
            if 1 <= selected <= len(memberList):
                selectedUser = memberList[selected- 1]
                assign = selectedUser['username']
                task_data = {
                    "assigned": assign
                }
                print(f"{assign} has been assigned to the task.")
                if memberList is []:
                    db.users.update_one({"username": USER, "projects.name": project['name']},
                        {"$push": {"projects.$.tasks": task_data}})
                else:
                    for i, member in enumerate(memberList, start=1):
                        db.users.update_one({"username": member['username'], "projects.name": project['name']},
                            {"$push": {"projects.$.tasks": task_data}})
            else:
                print("Invalid input. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


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
    while check:
        print("Press 1 to view tasks, 2 to create a task, 3 to update task details, 4 to add team members, 5 to exit")
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
            choice = input("Enter 1 to update a priority, 2 to update a deadline, 3 to update status, 4 to assign members: ")
            if choice == "1":
                updatePriority(project)
            elif choice == "2":
                updateDeadline(project)
            elif choice == "3":
                changeStatus(project)
            elif choice == "4":
                assignTasks(project)
        elif userInput == "4":
            addMembers(project)
        elif userInput == "5":
            exit()
        else: 
            print("Please enter a valid input")


def main():
    print("Welcome to our task management software!")
    print("Would you like to?")
    print("1. Create Account")
    print("2. Log In")
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == "1":
            create_account()
            break
        elif choice == "2":
            log_in()
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

    projList = []
    check = True
    while check:
        notifyLate(projList)
        proj = chooseProj(projList)
        if proj == None:
            check = False
            print("Thank you for using our program")
        else:
            projManage(proj)
    
    

 
    
if __name__ == "__main__":
    main()
