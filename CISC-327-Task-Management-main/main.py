from taskManager import *
from datetime import datetime,date, timedelta
import re
import json
import os

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
            user_data[username] = password
            save_user_data()
            print("Account created successfully!")

#log-in function
def log_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in user_data and user_data[username] == password:
        print("Login successful!")
        return True
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

    print("Would you like to add additional fields?")
    extra = input("Enter Y for yes, N for No: ")
    fields = {}
    while extra == "Y":
        fieldTitle = input("Enter the title of the new field: ")
        fieldDesc = input("Enter the description for the field: ")
        fields[fieldTitle] = fieldDesc
        print("Field has been added to the task. Enter Y if you would like to add another")
        extra = input("Enter Y for yes, N for No: ")

    task = Task(title, desc, status, priority, project, deadline, **fields) 
    print(task)
    project.add_task(task)

    if extra == "N":
        print("Returning to project management...")
        return projManage(project)
    
    
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
    
def createProject():
    project_name = input("Enter a project name: ")

    #taking user input to create Project object
    project = Project(project_name)
    print(project)
    return project
    
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
    # Allows user to view project
    project_name = input("Enter the project name: ")
    
    #finding inputted project and outputting it
    found_project = None
    for project in Project().projects:
        if project.name == project_name:
            print(project)
            
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
    


def chooseProj(projList):
    # Allows the user to create and manage projects
    check = True
    while check:
        if projList == []:
            print("You do not currently have any projects. Please create one.")
            project = createProject()
            projList.append(project)
        else:
            print("Enter the number associated with a project to access it. Enter P to create a new project ")
            print("Enter N to exit: ")
            x = 1
            for proj in projList:
                print(str(x) + ". ", end="")
                print(proj)
                x+=1
            custWant = input()
            if custWant == "P":
                project = createProject()
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

#add members to the current project
def addMembers(project):
    print("Would you like to add team members to this project? Y or N")
    userInput = input()
    if userInput == "Y":
        memberName = input("Enter the usersname you would like to add:")
        #check user exists in JSON database
        if memberName not in user_data:
            print("This user does not exist.")
            addMembers(project)
        else:
            project.add_members(memberName)
            return project
    else:
        return None

#assign team members in project to certain tasks 
def assignTasks(project):
    print("Current members in this project: ")
    print(", ".join(project.members))  

    print("Would you like to assign members to this task? Y or N")
    userInput = input()
    if userInput == "Y":
        memberName = input("Enter the username you would like to add: ")
        #check if user exists
        if memberName in project.members:
            print(f"{memberName} has been assigned to the task.")
            return project
        else:
            print(f"{memberName} is not a member of the project. Please add them to the project first.")
            return None
    else:
        print("No members were assigned to the task.")
        return None

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
            if log_in():
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
