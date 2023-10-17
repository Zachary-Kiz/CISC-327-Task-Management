class Status:
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    
class Task:
    #Task class describing attributes of a task
    def __init__(self, description, status=Status.NOT_STARTED, priority, project=None, deadline=None):
        self.description = description
        self.status = status
        self.priority = priority
        self.project = project
        self.deadline = deadline
        

class User:
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        
#-------------------------------------------------------------------------       
class ProgressManager: #this class tracks the progress of specific tasks
    def __init__(self):
        self.tasks = [] #only attribute is the list of tasks that have been created and stored

    def create_task(self, description, status=Status.NOT_STARTED, priority): #creating a task there is a description and  a status that is provided (if no status given, default of "not started" is given)
        task = Task(description, status, priority)
        self.tasks.append(task)

    def assign_task(self, task, status):
        if task.status == status: #if task is assigned to the same status already we will return a statement
            print("Task is already in the", status, "state.")
        else:
            task.status = status
            print("Task has been assigned new state") #printing this statement to confirm the status change


    def view_task(self, task):
        #viewing task will print the description and status of it
        print(f"Task Description: {task.description}")
        print(f"Task Status: {task.status}")
        
        
        
#-------------------------------------------------------------------------       
class Project:
    def __init__(self, name):
        #a project has a name and a list of tasks associtated with it
        self.name = name
        self.tasks = []
        self.projects = []
        
    def create_project(self, name, tasks=None):
        project = Project(name) #creating project
        
        if tasks:
            for task in tasks:
                project.add_task(task) #assigning all given tasks to it
    
        self.projects.append(project)

    
    def add_task(self, project, task):
        project.tasks.append(task) #manually being able to add a task to a given project
        
    def remove_task(self, project, task):
        project.tasks.remove(task) #manually being able to remove certain task from a project
    

    def is_completed(self):
        #returns true if all tasks are stated as "Completed"
        return all(task.status == Status.COMPLETED for task in self.tasks)
    
    def view_project(self, project):
        #being able to view the prject will show the project name along with associated tasks
        print(f"Project Name: {project.name}")
        for task in project.tasks:
            self.view_task(task)    
            
#------------------------------------------------------------------


