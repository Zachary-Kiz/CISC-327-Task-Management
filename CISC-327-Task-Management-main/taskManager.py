class Status:
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    
class Task:
    #Task class describing attributes of a task
    def __init__(self, title,desc, status=Status.NOT_STARTED, priority="L", project=None, deadline=None, extra = []):
        self.title = title
        self.desc = desc
        self.status = status
        self.priority = priority
        self.project = project
        self.deadline = deadline
        self.tasks = []
        self.extra = extra
          
        
    def assign_status(self, status):
        if self.status == status: #if task is assigned to the same status already we will return a statement
            print("Task is already in the", status, "state.")
        else:
            self.status = status
            print("Task has been assigned new state") #printing this statement to confirm the status change


    def view_status(self, task):
        #viewing task will print the description and status of it
        print(f"Task Description: {task.title}")
        print(f"Task Status: {task.status}") 

    def view_task(self):
        print(f"Task Description: {self.title}")
        print(f"Task Description: {self.desc}")
        print(f"Task Status: {self.status}") 
        print(f"Task Priority: {self.priority}")
        print(f"Task Deadline: {self.deadline}")
        for key in self.extra.keys():
            print(f"{key}: {self.extra[key]}")
    
    def update_pri(self, priority):
        self.priority = priority
        print(f"Task priority updated to {self.priority}")

    def update_date(self, deadline):
        self.deadline = deadline
        print(f"Task deadline updated to {self.deadline}")


    def __lt__(self, other):
        return self.title < other.title
        
    def __str__(self):
        task_info = f"{self.title}"
        return task_info    
    
        

class User:
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd      

#-------------------------------------------------------------------------       
class Project:
    def __init__(self, name):
        #a project has a name and a list of tasks associtated with it
        self.name = name
        self.tasks = []
        self.projects = []

    
    def add_task(self, task):
        self.tasks.append(task) #manually being able to add a task to a given project
        print("added successfully")
        
    def remove_task(self, task):
        self.tasks.remove(task) #manually being able to remove certain task from a project
        print("removed successfully")

    def get_tasks(self):
        return self.tasks

    def is_completed(self):
        #returns true if all tasks are stated as "Completed"
        return all(task.status == Status.COMPLETED for task in self.tasks)
    
    def __str__(self):
        #being able to view the prject will show the project name along with associated tasks
        project_info = f"Project Name: {self.name}\n"
        for task in self.tasks:
            project_info += str(task.title) + "\n"
        return project_info
   
#------------------------------------------------------------------

