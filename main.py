from datetime import datetime
import re

class Task:
    def __init__(self, title, desc, priority, proj, deadline, extra ):
        self.title = title
        self.desc = desc
        self.priority = priority
        self.proj = proj
        self.extra = extra
        self.deadline = deadline

    def __lt__(self, other):
        return self.title < other.title
    
    def __str__(self):
        return self.title
    



class User:
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

def createTask():
    title = input("Input Task Title: ")
    while title == "":
        print("Please enter a title")
        title = input("Input Task Title: ")
    print("Leave the following inputs blank if you don't want them to be included")
    desc = input("Enter a description for the task: ")
    print("Enter L for low priority, M for medium, H for high")
    priority = input()
    validPri = ["", "L", "M", "H"]
    while priority not in validPri:
        print("Not a valid priority")
        print("Enter L for low priority, M for medium, H for high")
        priority = input()
    deadline = input("Enter due date in YYYY/MM/DD format: ")
    pattern = r'^\d{4}/\d{2}/\d{2}$'
    check = False
    if re.match(pattern, deadline):
        check = True
    print(deadline[-2:])
    print(deadline[5:7])
    while not check or int(deadline[-2:]) > 31 or int(deadline[5:7]) > 12 or int(deadline[5:7]) <= 0 or int(deadline[-2:]) <= 0:
        print("Not a valid date, please try again")
        deadline = input("Enter due date in YYYY/MM/DD format: ")
        if re.match(pattern, deadline):
            check = True

    task = Task(title, desc, priority,"", deadline, [])
    return task

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


def main():
    taskList = []
    check = input("Enter Y to create a new task: ")
    while check == "Y":
        task = createTask()
        taskList.append(task)
        print(task.title)
        check = input("Enter Y to create a new task: ")
    sortDates(taskList)

main()