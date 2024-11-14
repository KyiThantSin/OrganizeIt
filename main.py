import customtkinter as ctk
from datetime import datetime, timedelta
from tasks_summary import TaskSummaryComponent
from tasks import Task, WorkTask, PersonalTask, UrgentTask
from tags_management import Tags
from zodb import ZODBConnection
from task_operations import TaskOperations
import uuid

ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

task_data = {
    "All Tasks": 100,
    "Doing": 30,
    "Completed": 50,
    "Processing": 20
}
class TaskManagementSystem:
    def __init__(self, root, zodb_connection):
        self.root = root
        self.zodb_connection = zodb_connection
        self.root.title("OrganizeIt")
        self.root.geometry("1450x900")
        self.task_ops = TaskOperations(zodb_connection)
        self.custom_tags = ["Work", "Personal", "Urgent"]
       
        # padding
        self.padx = 80

        # font 
        self.custom_title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
        self.custom_label_font = ctk.CTkFont(family="Arial", size=16, weight="bold")
        self.custom_task_label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")

        # app title 
        self.title_label = ctk.CTkLabel(self.root, text="OrganizeIt", font=self.custom_title_font)
        self.title_label.pack(side="top", anchor="w", padx=self.padx, pady=35)

        # variables
        self.filter_tag_var = ctk.StringVar()
        self.filter_status_var = ctk.StringVar()
        self.custom_tags = ["Work", "Personal", "Urgent"]  
        self.tasks = []  

        self.create_filter_section()

        # Add New Task button frame
        button_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")  
        button_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        self.pending_list_label = ctk.CTkLabel(button_frame, text="All Tasks", font=self.custom_label_font)
        self.pending_list_label.pack(side="left", padx=(5, 10))

        self.add_task_button = ctk.CTkButton(button_frame, text="Add New Task", command=self.open_task_creation_form)
        self.add_task_button.pack(side="right", padx=(10, 5))
        
        # Custom Tag button
        add_custom_tag_button = ctk.CTkButton(button_frame, text="Add Custom Tag", command=self.tags.open_custom_tag_creation_form)
        add_custom_tag_button.pack(side="right", padx=(5, 5))

        # task frame below "All Tasks"
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=self.padx, pady=10)

        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, pady=(0,5))
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(0, 0))

        self.create_task_list_area(self.left_frame)

        # Section to show top 3 deadline tasks
        self.deadline_tasks_label = ctk.CTkLabel(self.right_frame, text="Priority Tasks by Deadline", font=self.custom_label_font)
        self.deadline_tasks_label.pack(pady=(20, 5))

        self.deadline_tasks_frame = ctk.CTkFrame(self.right_frame,fg_color="transparent")
        self.deadline_tasks_frame.pack(pady=(0, 20))

        self.show_top_deadline_tasks()
        self.update_task_summary()

    def update_task_summary(self):
        tasks_list = self.task_ops.get_all_tasks()
        print("Tasks list:", tasks_list)  # Debug print
        if hasattr(self, 'task_summary'):
            self.task_summary.destroy()
        self.task_summary = TaskSummaryComponent(self.right_frame, tasks_list)
        self.task_summary.pack(padx=20, pady=5, anchor="w")
        self.task_summary.configure(fg_color="transparent")

    def apply_filter(self):
        selected_tag = self.filter_tag_var.get()
        selected_status = self.filter_status_var.get()
        
        filtered_tasks = self.task_ops.apply_filter(selected_tag, selected_status)
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for task_id, task in filtered_tasks.items():
            task_info = task.get_display_info()
            self.create_task_card(
                task_id=task_info["id"],
                task_name=task_info["name"],
                description=task_info["description"],
                tag=task_info["tag"],
                status=task_info["status"],
                deadline=task_info["deadline"]
            )

    def clear_filter(self):
        # Reset filter values
        self.filter_tag_var.set("")
        self.filter_status_var.set("")
        
        # Refresh task list to show all tasks
        self.refresh_task_list()

    def create_filter_section(self):
        filter_frame = ctk.CTkFrame(self.root, corner_radius=10)  
        filter_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        ctk.CTkLabel(filter_frame, text="Filter By Tags", font=self.custom_label_font).grid(row=0, column=0, padx=(10, 5), pady=(20, 5), sticky="w")
        ctk.CTkLabel(filter_frame, text="Filter By Status", font=self.custom_label_font).grid(row=0, column=1, padx=(10, 5), pady=(20, 5), sticky="w")

        tag_values = self.custom_tags
        status_values = ["On Progress", "Completed", "Not Started"]

        self.tag_entry = ctk.CTkComboBox(filter_frame, values=tag_values, variable=self.filter_tag_var, width=180)
        self.tag_entry.grid(row=1, column=0, padx=(10, 5), pady=(10, 40), sticky="ew")
        self.tag_entry.set("Not Started")  # Set default value
        self.tags = Tags(self.root, tag_entry=self.tag_entry) 

        self.status_entry = ctk.CTkComboBox(filter_frame, values=status_values, variable=self.filter_status_var, width=180)
        self.status_entry.grid(row=1, column=1, padx=(5, 10), pady=(10, 40), sticky="ew")
        self.status_entry.set("Not Started")  # Set default value

        button_frame = ctk.CTkFrame(filter_frame, fg_color="transparent") 
        button_frame.grid(row=1, column=2, columnspan=2, padx=(10, 10), pady=(10, 40), sticky="e")

        apply_button = ctk.CTkButton(button_frame, text="Apply Filter", width=15, command=self.apply_filter)
        apply_button.pack(side="left", padx=(5, 5))

        clear_button = ctk.CTkButton(button_frame, text="Clear", width=15, command=self.clear_filter)
        clear_button.pack(side="left", padx=(5, 5))
        self.tags.update_tag_values(self.tag_entry)

    def create_task_list_area(self, parent):
        self.canvas = ctk.CTkCanvas(parent, bg=self.root.cget("bg"), highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")

        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.no_tasks_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.load_tasks_from_zodb()

    def load_tasks_from_zodb(self):
        connection = self.zodb_connection.get_connection()
        root = connection.root()
        tasks_data = root.get("tasks", {})

        if not tasks_data:
            no_tasks_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            no_tasks_frame.pack(padx=5, pady=20, fill="x")
            
            no_tasks_label = ctk.CTkLabel(
                no_tasks_frame, 
                text="There are no tasks to show", 
                font=self.custom_label_font,
                text_color="gray"
            )
            no_tasks_label.pack(expand=True)
        else:
            for task_id, task in tasks_data.items():
                task_info = task.get_display_info()
                self.create_task_card(
                    task_id=task_info["id"],
                    task_name=task_info["name"],
                    description=task_info["description"],
                    tag=task_info["tag"],
                    status=task_info["status"],
                    deadline=task_info["deadline"]
                )
    
    def refresh_task_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.load_tasks_from_zodb()
    
    def validate_date(self, date_str):  
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def create_task_card(self, task_id, task_name="Task", description="Description", tag="Work", status="On Progress", deadline=None):
        card_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        card_frame.pack(padx=5, pady=(10,10), fill="x")

        ctk.CTkLabel(card_frame, text=f"{task_name}", font=self.custom_task_label_font).grid(row=0, column=0, sticky="w", padx=20, pady=(10,5))
        ctk.CTkLabel(card_frame, text=f"Description: {description}").grid(row=1, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Tag: {tag}").grid(row=2, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Status: {status}").grid(row=3, column=0, sticky="w", padx=20)
        if deadline:
            ctk.CTkLabel(card_frame, text=f"Deadline: {deadline.strftime('%Y-%m-%d')}").grid(row=4, column=0, sticky="w", padx=20)

        edit_button = ctk.CTkButton(card_frame, text="Edit", width=100, command=lambda: self.open_task_edit_form(task_id, task_name, description, tag, status, deadline))
        edit_button.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="e")

        delete_button = ctk.CTkButton(card_frame, text="Delete", width=100, command=lambda: self.task_ops.delete_task( task_id, self))
        delete_button.grid(row=5, column=1, padx=10, pady=(5, 10), sticky="e")

        # layout
        card_frame.grid_columnconfigure(0, weight=1)

        self.tasks.append({ "id": task_id, "name": task_name, "description": description, "tag": tag, "status": status, "deadline": deadline})

    def open_task_creation_form(self):
        self.task_creation_window = ctk.CTkToplevel(self.root)
        self.task_creation_window.title("Create New Task")
        self.task_creation_window.geometry("600x600")

        self.create_task_form(self.task_creation_window)

    def open_task_edit_form(self, task_id, task_name, description, tag, status, deadline):
        self.task_edit_window = ctk.CTkToplevel(self.root)
        self.task_edit_window.title(f"Edit Task: {task_name}")
        self.task_edit_window.geometry("600x600")

        self.create_task_form(
            parent=self.task_edit_window,
            task_id=task_id,
            task_name=task_name,
            description=description,
            tag=tag,
            status=status,
            deadline=deadline,
            isEdit = True
        )

    def create_task_form(self, parent, task_id=None, task_name=None, description=None, tag=None, status=None, deadline=None, isEdit = False):
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.place(relx=0.5, anchor="n")  # Centered horizontally

        # name
        task_name_label = ctk.CTkLabel(form_frame, text="Task Name")
        task_name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.task_name_entry = ctk.CTkEntry(form_frame, width=300)
        self.task_name_entry.grid(row=1, column=0, padx=10, pady=10)
        self.task_name_entry.insert(0, task_name if task_name else "Enter task name")
        # description
        task_description_label = ctk.CTkLabel(form_frame, text="Task Description")
        task_description_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.task_description_entry = ctk.CTkEntry(form_frame, width=300)
        self.task_description_entry.grid(row=3, column=0, padx=10, pady=10)
        self.task_description_entry.insert(0, description if description else "Enter task description")

        # tag 
        task_tag_label = ctk.CTkLabel(form_frame, text="Task Tag")
        task_tag_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.task_tag_entry = ctk.CTkComboBox(form_frame, values=self.custom_tags, width=300)
        self.task_tag_entry.grid(row=5, column=0, padx=10, pady=10)
        self.task_tag_entry.set(tag if tag else "Work")

        # status 
        task_status_label = ctk.CTkLabel(form_frame, text="Task Status")
        task_status_label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")
        self.task_status_entry = ctk.CTkComboBox(form_frame, values=["On Progress", "Completed", "Not Started"], width=300)
        self.task_status_entry.grid(row=7, column=0, padx=10, pady=10)
        self.task_status_entry.set(status if status else "Not Started")

        # deadline 
        task_deadline_label = ctk.CTkLabel(form_frame, text="Task Deadline")
        task_deadline_label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")
        self.task_deadline_entry = ctk.CTkEntry(form_frame, width=300)
        self.task_deadline_entry.grid(row=9, column=0, padx=10, pady=10)
        self.task_deadline_entry.insert(0, deadline.strftime("%Y-%m-%d") if deadline else "yyyy-mm-dd")

        self.error_label = ctk.CTkLabel(form_frame, text="", text_color="red", fg_color="transparent")
        self.error_label.grid(row=10, column=0, padx=10, pady=5)
        self.error_label.grid_forget()  # Initially hide the error label  
                  
        button_row = 11
        if isEdit:
            update_button = ctk.CTkButton(form_frame, text="Update", command=lambda: self.save_task(task_id, isEdit=True))
            update_button.grid(row=button_row, column=0, padx=10, pady=10)
        else:
            save_button = ctk.CTkButton(form_frame, text="Save", command=lambda: self.save_task(task_id, isEdit))
            save_button.grid(row=button_row, column=0, padx=10, pady=10)
        self.tags.update_tag_values(self.task_tag_entry)
                          
    def save_task(self, task_id=None, isEdit=False):
        task_name = self.task_name_entry.get()
        description = self.task_description_entry.get()
        tag = self.task_tag_entry.get()
        status = self.task_status_entry.get()
        deadline_str = self.task_deadline_entry.get()

        deadline = self.task_deadline_entry.get()

        if not self.validate_date(deadline):
            self.error_label.configure(text="Invalid date format! Please use YYYY-MM-DD.")
            self.error_label.grid(row=10, column=0, padx=10, pady=20)  
            return

        self.error_label.grid_forget()

        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d") if deadline_str else None
        except ValueError:
            return False

        if not isEdit:
            task_id = str(uuid.uuid4())
            if tag == "Work":
                new_task = WorkTask(task_id, task_name, description, deadline)
            elif tag == "Personal":
                new_task = PersonalTask(task_id, task_name, description, deadline)
            elif tag == "Urgent":
                new_task = UrgentTask(task_id, task_name, description, deadline)
            else:
                new_task = Task(task_id, task_name, description, tag, status, deadline)

            success = self.task_ops.save_task(task_id, new_task)
        else:
            success = self.task_ops.edit_task(task_id, task_name, description, tag, status, deadline)

        if success:
            self.refresh_task_list()
            self.update_task_summary()
            self.show_top_deadline_tasks()
            if isEdit:
                self.task_edit_window.destroy()
            else:
                self.task_creation_window.destroy()

    def show_top_deadline_tasks(self):
        for widget in self.deadline_tasks_frame.winfo_children():
            widget.destroy()

        deadline_tasks = self.task_ops.get_deadline_tasks(limit=3)
        
        if not deadline_tasks:
            no_tasks_label = ctk.CTkLabel(
                self.deadline_tasks_frame, 
                text="No upcoming deadline tasks",
                font=self.custom_task_label_font,
                text_color="gray"
            )
            no_tasks_label.pack(pady=20)
            return

        for index, task in enumerate(deadline_tasks):
            if task.deadline:  # only create cards for tasks with deadlines
                card_frame = ctk.CTkFrame(
                    self.deadline_tasks_frame, 
                    corner_radius=10, 
                    fg_color="#F5FFFA"
                )
                card_frame.grid(row=0, column=index, padx=10, pady=(5, 10), sticky="nsew")

                # Task name
                task_label = ctk.CTkLabel(
                    card_frame, 
                    text=f"{task.name}", 
                    font=self.custom_task_label_font
                )
                task_label.pack(pady=(5, 0), padx=10)

                # Deadline
                deadline_label = ctk.CTkLabel(
                    card_frame, 
                    text=f"Deadline: {task.deadline.strftime('%Y-%m-%d')}"
                )
                deadline_label.pack(pady=(0, 5), padx=10)

                # Calculate time remaining
                time_left = task.deadline - datetime.now()
                days_left = time_left.days
                hours_left = time_left.seconds // 3600

                # format time left text
                if days_left < 0:
                    time_left_text = "Deadline passed"
                elif days_left == 0:
                    time_left_text = f"{hours_left} hours left"
                else:
                    time_left_text = f"{days_left} days {hours_left} hours left"

                time_left_label = ctk.CTkLabel(card_frame, text=time_left_text)
                time_left_label.pack(pady=(0, 5), padx=10)

                status_label = ctk.CTkLabel(card_frame, text=f"Status: {task.status}")
                status_label.pack(pady=(0, 5), padx=10)

        for i in range(min(len(deadline_tasks), 3)):
            self.deadline_tasks_frame.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = ctk.CTk()
    db_file = "mydatabase.fs"
    zodb = ZODBConnection(db_file)

    try:
        zodb.open()
        app = TaskManagementSystem(root, zodb)
        root.mainloop()
    finally:
        zodb.close()

    root.mainloop()
