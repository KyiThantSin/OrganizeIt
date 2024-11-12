from ZODB import DB
from ZODB.FileStorage import FileStorage
import os
import transaction
class ZODBConnection:
    def __init__(self, db_file: str):
        """initialize """
        self.db_file = db_file
        self.db = None
        self.connection = None

    def open(self):
        if not os.path.exists(self.db_file):
            # create a new database if it doesn't exist
            storage = FileStorage(self.db_file)
            self.db = DB(storage)
            self.connection = self.db.open()
            print("Opened")
        else:
            storage = FileStorage(self.db_file)
            self.db = DB(storage)
            self.connection = self.db.open()
            print("Opened")


    def get_connection(self):
        print("Connected")
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
        if self.db:
            self.db.close()
    
    def get_task(self, task_id):
        root = self.get_connection().root()
        tasks = root.get("tasks", {}) 
        return tasks.get(task_id, None)