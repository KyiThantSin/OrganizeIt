from datetime import datetime
import transaction

def edit_task(task_id, task_name=None, description=None, tag=None, status=None, deadline=None, zodb_connection=None):
    connection = zodb_connection.get_connection()
    root = connection.root()

    if "tasks" in root and task_id in root["tasks"]:
        task = root["tasks"][task_id]
        
        # Update task attributes if provided
        if task_name is not None:
            task.task_name = task_name
        if description is not None:
            task.description = description
        if tag is not None:
            task.tag = tag
        if status is not None:
            task.status = status
        if deadline is not None:
            task.deadline = deadline
        
        transaction.commit()  # Save the changes
        print("updated")
    else:
        print(f"Task with ID {task_id} not found.")

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
