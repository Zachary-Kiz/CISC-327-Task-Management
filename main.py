from taskManager import *

def main():
    #creating task
    task1 = Task("Task 1")
    print(task1)
    print("-----------------------")
    
    #creating project
    project1 = Project("Project 1")
    
    print(project1)
    print("-----------------------")
    
    #assigning status
    task1.assign_status("Completed")
    print("-----------------------")
    
    #verifying status change
    print(task1)
    print("-----------------------")
    
    #adding to project
    project1.add_task(task1)
    print("-----------------------")
    
    #viewing project
    print(project1)
    
    #removing from project
    project1.remove_task(task1)
    print("-----------------------")
    
    #viewing project
    print(project1)    
    
    
 
    
if __name__ == "__main__":
    main()
