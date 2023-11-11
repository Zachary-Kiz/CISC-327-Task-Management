from datetime import datetime,date, timedelta
import re
from pymongo import MongoClient
import os

'''
CISC327 A3
Group 37 - Zachary Kizell, Aidan Wolf, and Adam Ciszek
Python + MongoDB
Our database establishes an individual query for each user that contains a nested project array
the project array contains the tasks array that holds the task data.
The choice of using a nested sturcture to embed data in a single query ensures performance
as it is one of the best practices within MongoDB.
Uses MongoDB's internal _id generation so each query as a unique ObjectID value for security.
0.0.0.0/0 has been added as an ip so the database should be accessible from anywhere.
'''


client = MongoClient("mongodb+srv://zachkizell87:f9gYzb7e5LKSkQJX@cluster0.eyssqkn.mongodb.net/?retryWrites=true&w=majority")  
db = client["mydatabase"]
USER = None

#function for establishing user account
def create_account():
    global USER
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    #username allocated already
    if db.users.find_one({"username": username}):
        print("Username already exists. Please choose a different username.")
        create_account()
    else:
        #password strength check
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
            
#verifies and log-in function
def log_in():
    global USER
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    userCheck = db.users.find_one({"username": username, "password": password})
    #ensures user exists 
    if userCheck:
        USER = username
        print("Login successful!")
    else:
        print("Invalid username or password. Please try again.")
        log_in()
    
def createTask(project):
    #creating a task by getting input of title, priority, status and deadline from user
    title = input("Enter a task name: ")
    while title == "":
        print("Error: Task requires a name to create")
        title = input("Enter a task name: ")

    desc = input("Add a task description: ")
    
    priority = input("Enter L for low priority, M for medium, H for high: ")
    
    status_choice = input("Choose a status:\na) not started\nb) in progress\nc) completed\n")
    if status_choice == "a":
        status = "Not started"
    elif status_choice == "b":
        status = "In progress"
    else:
        status = "Completed"
        
    
    check = True
    while check:
        deadline = input("Enter due date in YYYY/MM/DD format: ")

        pattern = r'^\d{4}/\d{2}/\d{2}$'
        
        while ((re.match(pattern, deadline)) and (1 <= int(deadline[-2:]) <= 31) and (1 <= int(deadline[5:7]) <= 12)) != True:
            deadline = input("Enter due date in YYYY/MM/DD format: ")

        today = date.today()
        dates = today.strftime("%Y/%m/%d")
        times = dates.split("/")
        d1 = date(int(times[0]), int(times[1]), int(times[2]))
        times2 = deadline.split("/")
        d2 = date(int(times2[0]), int(times2[1]), int(times2[2]))
        if d1 - d2 > timedelta(0):
            print("Deadline is past due. Do you still want to create?")
            getInput = input("Enter Y for yes, N for no: ")
            if getInput == "Y":
                check = False
        else:
            check = False
    


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
        

def changeStatus(project):
    #user can change task status
    task_name = input("Enter the task name: ")

    #find the task with the given title within the project's tasks
    task_data = None
    for task in project['tasks']:
        if task['title'] == task_name:
            task_data = task
            break

    if task_data:
        new_status = input("Enter new status:\n a) not started\n b) in progress\n c) completed\n")

        if new_status == "a":
            status = "Not started"
        elif new_status == "b":
            status = "In progress"
        elif new_status == "c":
            status = "Completed"
        else:
            print("Invalid Choice")

        task_data['status'] = status

        #update the project's tasks list in the database
        db.users.update_one({"username": USER, "projects.name": project['name']},
                            {"$set": {"projects.$.tasks": project['tasks']}})

        print("Task status updated successfully!")
    else:
        print("Task not found.")
        
def viewStatus(project):
    # view status of a task
    task_name = input("Enter the task name: ")

    # find the task with the given title within the project's tasks
    task_data = None
    for task in project['tasks']:
        if task['title'] == task_name:
            task_data = task
            break

    if task_data:
        print("Current status:", task_data['status'])
    else:
        print("Task not found.") 
    
def removeTaskFromProject(project):
    # user can remove task from project
    task_name = input("Enter the task name: ")

    # find the task with the given title within the project's tasks
    task_data = None
    for task in project['tasks']:
        if task['title'] == task_name:
            task_data = task
            break

    if task_data:
        #update the project's tasks list in the database
        db.users.update_one({"username": USER, "projects.name": project['name']},
                            {"$remove": {"projects.$.tasks": project['tasks']}})

        print("Task status updated successfully!")
    else:
        print("Task not found.")  
    
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
        if task["priority"] == "L":
            lowPri.append(task)
        if task["priority"] == "M":
            medPri.append(task)
        if task["priority"]== "H":
            highPri.append(task)
    lowPri = sorted(lowPri, key=lambda x : x['title'])
    medPri = sorted(medPri, key=lambda x : x['title'])
    highPri = sorted(highPri, key=lambda x : x['title'])
    highPri.extend(medPri)
    highPri.extend(lowPri)
    x = 1
    for title in highPri:
        print(str(x) + ". " + title["title"] + "\tpriority: " + title['priority'])
        x += 1
    return highPri


def sortDates(taskList):
    # Prints tasks sorted by deadline
    taskList.sort(key=lambda date: (datetime.strptime(date['deadline'], "%Y/%m/%d"),date['title']))
    #taskList.reverse()
    for i,task in enumerate(taskList,start=1):
        print(str(i) + ". " + task['title'] + '\tdeadline: ' + task['deadline'])
    return taskList

def updatePriority(project):
    # User can update a priority deadline
    printTasks(project)
    taskNum = input("Enter the number associated with the task whose priority you want to update: ")
    task = project['tasks'][int(taskNum) - 1]
    print("Task priority is: " + task['priority'])
    update = input("Enter the new priority of the task: ")
    priors = ["L","M","H"]
    while update not in priors:
        print("Not a valid input, please try again")
        update = input("Enter the new priority of the task: ")
    task['priority'] = update
    members = db.users.find({"projects.name": project['name']})
    memberList = list(members)
    for member in memberList:
        db.users.find_one_and_update(
            {"username":member['username'],"projects.name":project['name']},
            {"$set": {"projects.$.tasks": project['tasks']}}
            )
    print("Priority changed!")


def updateDeadline(project):
    # User can update a task deadline
    printTasks(project)
    taskNum = input("Enter the number associated with the task whose deadline you want to update: ")
    
    task = project['tasks'][int(taskNum) - 1]
    if task['deadline'] == None:
        print("Task does not currently have a deadline")
    else: 
        print("Task priority is: " + task['deadline'])
    deadline = input("Enter the new deadline of the task: ")
    pattern = r'^\d{4}/\d{2}/\d{2}$'
    
    while ((re.match(pattern, deadline)) and (1 <= int(deadline[-2:]) <= 31) and (1 <= int(deadline[5:7]) <= 12)) != True:
        deadline = input("Enter due date in YYYY/MM/DD format: ")
    task['deadline'] = deadline
    members = db.users.find({"projects.name": project['name']})
    memberList = list(members)
    for member in memberList:
        db.users.find_one_and_update({"username":member['username'],"projects.name":project['name']},
                                    {"$set": {"projects.$.tasks": project['tasks']}})
    print("Deadline updated!")
    
def projectExistCheck():
    #function to check project exists 
    global USER
    if db.users.find_one({"username": USER, "projects": {"$exists": True, "$ne": []}}):
        return True
    else:
        return False

def createProject():
    #function to quick create additional projects
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
    tasks = project["tasks"]
    if not tasks:
        print("No tasks currently assigned to this project.")
    else:
        print("Tasks in project:", project['name'])
        i = 1
        for task in project['tasks']:
                print(f"{i}. {task['title']}")
                i += 1


def addMembers(project):
    #add members to the current project
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

def assignTasks(project):
    #assign team members in project to certain tasks
    printTasks(project)
    taskNum = input("Enter the number associated with the task you would like to assign: ")
    task = project['tasks'][int(taskNum) - 1]
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
                task['assigned'] = assign
                print(f"{assign} has been assigned to the task.")
                if memberList is []:
                    db.users.find_one_and_update({"username": USER, "projects.name": project['name']},
                        {"$push": {"projects.$.tasks": project['tasks']}})
                else:
                    for i, member in enumerate(memberList, start=1):
                        db.users.find_one_and_update({"username": member['username'], "projects.name": project['name']},
                            {"$push": {"projects.$.tasks": project['tasks']}})
            else:
                print("Invalid input. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def projManage(project):
    # Function for interacting with tasks within a project
    check = True
    while check:
        print("Press 1 to view tasks, 2 to create a task, 3 to update task details, 4 to add team members, 5 to exit")
        userInput = input()
        if userInput == "1":
            proj = project['tasks']
            print("Press 1 to view sorted alphabetically, 2 to view sorted by priority, 3 to view sorted by deadline")
            view = input()
            if view == "1":
                printTasks(project)
            elif view == "2":
                proj = sortByPriority(project['tasks'])
            elif view == "3":
                proj = sortDates(project['tasks'])

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
        proj = chooseProj(projList)
        if proj == None:
            check = False
            print("Thank you for using our program")
        else:
            projManage(proj)
    
    

 
    
if __name__ == "__main__":
    main()
