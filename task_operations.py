from datetime import datetime
import transaction
class TaskOperations:
    def __init__(self, zodb_connection):
        self.zodb_connection = zodb_connection

    def apply_filter(self, selected_tag, selected_status):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
        tasks_data = root.get("tasks", {})
        
        filtered_tasks = {}
        for task_id, task in tasks_data.items():
            task_info = task.get_display_info()
            matches_tag = not selected_tag or selected_tag == "All" or task_info["tag"] == selected_tag
            matches_status = not selected_status or selected_status == "All" or task_info["status"] == selected_status
            
            if matches_tag and matches_status:
                filtered_tasks[task_id] = task
                
        return filtered_tasks

    def edit_task(self, task_id, task_name=None, description=None, tag=None, status=None, deadline=None):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
        
        if "tasks" in root and task_id in root["tasks"]:
            task = root["tasks"][task_id]
            
            if task_name is not None:
                task.name = task_name
            if description is not None:
                task.description = description
            if tag is not None:
                task.tag = tag
            if status is not None:
                task.status = status
            if deadline is not None:
                task.deadline = deadline
            
            transaction.commit()
            return True
        return False

    def delete_task(self, task_id, app):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
        
        if "tasks" in root and task_id in root["tasks"]:
            del root["tasks"][task_id]
            transaction.commit()
            app.refresh_task_list()
            app.update_task_summary()
            app.show_top_deadline_tasks()
            return True
        return False

    def get_all_tasks(self):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
    
        tasks = root.get("tasks", {})
    
        readable_tasks = {}
        for task_id, task in tasks.items():
            readable_tasks[task_id] = task.get_display_info()  
        
        return readable_tasks


    def save_task(self, task_id, task_obj):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
        
        if 'tasks' not in root:
            root['tasks'] = {}
            
        root['tasks'][task_id] = task_obj
        transaction.commit()
        return True

    def get_deadline_tasks(self, limit=3):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
        tasks = root.get("tasks", {})
        
        deadline_tasks = [
            task for task in tasks.values()
            if task.deadline is not None
        ]
        deadline_tasks.sort(key=lambda x: x.deadline)
        
        return deadline_tasks[:limit]