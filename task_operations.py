from datetime import datetime
import transaction

def edit_task(task_name, description, tag, status, deadline, db_connection):
    task = db_connection.get_task(task_name)  
    if task:
        task.description = description
        task.tag = tag
        task.status = status
        task.deadline = deadline
        db_connection.update_task(task_name, task)  

def delete_task(task_id, db_connection, self):
    connection = db_connection.get_connection()
    root = connection.root()
    
    if "tasks" in root and task_id in root["tasks"]:
        del root["tasks"][task_id]
        print("Deleted")
        transaction.commit()
        self.refresh_task_list()
    else:
        print(f"Task '{task_id}' not found.")
