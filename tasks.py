from persistent import Persistent

class Task(Persistent):
    def __init__(self, id, name, description, tag, status, deadline=None):
        self.id = id
        self.name = name
        self.description = description
        self.tag = tag
        self.status = status
        self.deadline = deadline

    def get_display_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tag": self.tag,
            "status": self.status,
            "deadline": self.deadline
        }

class WorkTask(Task):
    def __init__(self, id, name, description, deadline=None):
        super().__init__(id, name, description, tag="Work", status="Not Started", deadline=deadline)

    def get_display_info(self):
        task_info = super().get_display_info()
        task_info["priority"] = "High"  
        return task_info

class PersonalTask(Task):
    def __init__(self, id, name, description, deadline=None):
        super().__init__(id, name, description, tag="Personal", status="Not Started", deadline=deadline)

    def get_display_info(self):
        task_info = super().get_display_info()
        task_info["priority"] = "Low"
        return task_info

class UrgentTask(Task):
    def __init__(self, id, name, description, deadline=None):
        super().__init__(id, name, description, tag="Urgent", status="Not Started", deadline=deadline)

    def get_display_info(self):
        task_info = super().get_display_info()
        task_info["priority"] = "Critical"
        return task_info
