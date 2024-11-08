import customtkinter as ctk
from datetime import datetime, timedelta
from pie_chart import draw_pie_chart
from tasks_summary import TaskSummaryComponent

ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

task_data = {
    "All Tasks": 100,
    "Doing": 30,
    "Completed": 50,
    "Processing": 20
}

tasks = [
    {"name": "Task 1", "status": "processing"},
    {"name": "Task 2", "status": "completed"},
    {"name": "Task 3", "status": "processing"},
    {"name": "Task 4", "status": "completed"},
]
class Task:
    def __init__(self, name, description, tag, status, deadline=None):
        self.name = name
        self.description = description
        self.tag = tag
        self.status = status
        self.deadline = deadline

    def get_display_info(self):
        return {
            "name": self.name,
            "description": self.description,
            "tag": self.tag,
            "status": self.status,
            "deadline": self.deadline
        }

class WorkTask(Task):
    def __init__(self, name, description, deadline=None):
        super().__init__(name, description, tag="Work", status="Not Started", deadline=deadline)

    def get_display_info(self):
        task_info = super().get_display_info()
        task_info["priority"] = "High"  
        return task_info

class PersonalTask(Task):
    def __init__(self, name, description, deadline=None):
        super().__init__(name, description, tag="Personal", status="Not Started", deadline=deadline)

    def get_display_info(self):
        task_info = super().get_display_info()
        task_info["priority"] = "Low"  # Personal tasks have lower priority
        return task_info

class UrgentTask(Task):
    def __init__(self, name, description, deadline=None):
        super().__init__(name, description, tag="Urgent", status="Not Started", deadline=deadline)

    def get_display_info(self):
        task_info = super().get_display_info()
        task_info["priority"] = "Critical" 
        return task_info

class TaskManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("OrganizeIt")
        self.root.geometry("1450x900")
        
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
        self.tasks = []  # to hold all tasks with their deadlines

        self.create_filter_section()

        # Add New Task button frame
        button_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")  
        button_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        self.pending_list_label = ctk.CTkLabel(button_frame, text="All Tasks", font=self.custom_label_font)
        self.pending_list_label.pack(side="left", padx=(5, 10))

        self.add_task_button = ctk.CTkButton(button_frame, text="Add New Task", command=self.open_task_creation_form)
        self.add_task_button.pack(side="right", padx=(10, 5))
        
        # Custom Tag button
        add_custom_tag_button = ctk.CTkButton(button_frame, text="Add Custom Tag", command=self.open_custom_tag_creation_form)
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
        self.deadline_tasks_label = ctk.CTkLabel(self.right_frame, text="Top 3 Deadline Tasks", font=self.custom_label_font)
        self.deadline_tasks_label.pack(pady=(20, 5))

        self.deadline_tasks_frame = ctk.CTkFrame(self.right_frame,fg_color="transparent")
        self.deadline_tasks_frame.pack(pady=(0, 20))

        self.show_top_deadline_tasks()
        task_summary = TaskSummaryComponent(self.right_frame, tasks)
        task_summary.pack(padx=20, pady=5, anchor="w")
        task_summary.configure(fg_color="transparent")
        # pie chart
        self.pie_chart_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.pie_chart_frame.pack(pady=(20, 5), padx=20, anchor="w", fill="x")

        self.pie_chart_label = ctk.CTkLabel(self.pie_chart_frame, text="If you want to see data in a pie chart, click here:", fg_color="transparent")
        self.pie_chart_label.pack(side="left", padx=(0, 10))

        self.view_pie_chart_button = ctk.CTkButton(self.pie_chart_frame, text="View Pie Chart", command=lambda: draw_pie_chart(task_data))
        self.view_pie_chart_button.pack(side="left")

    def create_filter_section(self):
        filter_frame = ctk.CTkFrame(self.root, corner_radius=10)  
        filter_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        ctk.CTkLabel(filter_frame, text="Filter By Tags", font=self.custom_label_font).grid(row=0, column=0, padx=(10, 5), pady=(20, 5), sticky="w")
        ctk.CTkLabel(filter_frame, text="Filter By Status", font=self.custom_label_font).grid(row=0, column=1, padx=(10, 5), pady=(20, 5), sticky="w")

        self.tag_entry = ctk.CTkComboBox(filter_frame, values=self.custom_tags, variable=self.filter_tag_var, width=180)
        self.tag_entry.grid(row=1, column=0, padx=(10, 5), pady=(10, 40), sticky="ew")

        self.status_entry = ctk.CTkComboBox(filter_frame, values=["On Progress", "Completed", "Not Started"], variable=self.filter_status_var, width=180)
        self.status_entry.grid(row=1, column=1, padx=(5, 10), pady=(10, 40), sticky="ew")

        button_frame = ctk.CTkFrame(filter_frame, fg_color="transparent") 
        button_frame.grid(row=1, column=2, columnspan=2, padx=(10, 10), pady=(10, 40), sticky="e")

        apply_button = ctk.CTkButton(button_frame, text="Apply Filter", width=15)
        apply_button.pack(side="left", padx=(5, 5))

        clear_button = ctk.CTkButton(button_frame, text="Clear", width=15)
        clear_button.pack(side="left", padx=(5, 5))

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

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.create_task_card(task_name="Sample Task", description="This is a sample description", tag="Work", status="On Progress")

        for i in range(10):  
            self.create_task_card(task_name=f"Task {i+1}", description=f"This is the description for task {i+1}", tag="Work", status="On Progress")

    def create_task_card(self, task_name="Task", description="Description", tag="Work", status="On Progress", deadline=None):
        card_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        card_frame.pack(padx=5, pady=(10,10), fill="x")

        ctk.CTkLabel(card_frame, text=f"{task_name}", font=self.custom_task_label_font).grid(row=0, column=0, sticky="w", padx=20, pady=(10,5))
        ctk.CTkLabel(card_frame, text=f"Description: {description}").grid(row=1, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Tag: {tag}").grid(row=2, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Status: {status}").grid(row=3, column=0, sticky="w", padx=20)
        if deadline:
            ctk.CTkLabel(card_frame, text=f"Deadline: {deadline.strftime('%Y-%m-%d')}").grid(row=4, column=0, sticky="w", padx=20)

        edit_button = ctk.CTkButton(card_frame, text="Edit", width=100, command=lambda: self.open_task_edit_form(task_name, description, tag, status, deadline))
        edit_button.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="e")

        delete_button = ctk.CTkButton(card_frame, text="Delete", width=100)
        delete_button.grid(row=5, column=1, padx=10, pady=(5, 10), sticky="e")

        # layout
        card_frame.grid_columnconfigure(0, weight=1)

        # Store task details
        self.tasks.append({"name": task_name, "description": description, "tag": tag, "status": status, "deadline": deadline})

    def open_task_creation_form(self):
        self.task_creation_window = ctk.CTkToplevel(self.root)
        self.task_creation_window.title("Create New Task")
        self.task_creation_window.geometry("600x600")

        self.create_task_form(self.task_creation_window)

    def open_task_edit_form(self, task_name, description, tag, status, deadline):
        self.task_edit_window = ctk.CTkToplevel(self.root)
        self.task_edit_window.title(f"Edit Task: {task_name}")
        self.task_edit_window.geometry("600x600")

        self.create_task_form(self.task_edit_window, task_name, description, tag, status, deadline)

    def create_task_form(self, parent, task_name=None, description=None, tag=None, status=None, deadline=None):
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

        save_button = ctk.CTkButton(form_frame, text="Save", command=self.save_task)
        save_button.grid(row=10, column=0, padx=10, pady=10)

    def save_task(self):
        task_name = self.task_name_entry.get()
        description = self.task_description_entry.get()
        tag = self.task_tag_entry.get()
        status = self.task_status_entry.get()
        deadline_str = self.task_deadline_entry.get()

        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        else:
            deadline = None

        # Instantiate the appropriate task type based on the tag
        if tag == "Work":
            task = WorkTask(task_name, description, deadline)
        elif tag == "Personal":
            task = PersonalTask(task_name, description, deadline)
        elif tag == "Urgent":
            task = UrgentTask(task_name, description, deadline)
        else:
            task = Task(task_name, description, tag, status, deadline)

        self.create_task_card(task)
        self.task_creation_window.destroy()  # Close the creation window

    def open_custom_tag_creation_form(self):
        tag_creation_window = ctk.CTkToplevel(self.root)
        tag_creation_window.title("Create Custom Tag")
        tag_creation_window.geometry("600x600")

        label = ctk.CTkLabel(tag_creation_window, text="Enter custom tag name:", font=self.custom_label_font)
        label.pack(pady=10) 

        custom_tag_entry = ctk.CTkEntry(tag_creation_window)
        custom_tag_entry.pack(pady=10)

        def add_custom_tag():
            new_tag = custom_tag_entry.get()
            if new_tag and new_tag not in self.custom_tags:
                self.custom_tags.append(new_tag)
                refresh_tag_list()
                custom_tag_entry.delete(0, 'end')

        add_button = ctk.CTkButton(tag_creation_window, text="Add Tag", command=add_custom_tag)
        add_button.pack(pady=10)

        title_label = ctk.CTkLabel(tag_creation_window, text="Your Tags List", font=self.custom_label_font)
        title_label.pack(fill='x', padx=[self.padx], pady =10 )

        tag_list_frame = ctk.CTkFrame(tag_creation_window, fg_color="transparent")
        tag_list_frame.pack(fill='both', expand=True, pady=10)

        def delete_tag(tag):
            if tag in self.custom_tags:
                self.custom_tags.remove(tag)
                refresh_tag_list()

        def refresh_tag_list():
            for widget in tag_list_frame.winfo_children():
                widget.destroy()

            for tag in self.custom_tags:
                tag_frame = ctk.CTkFrame(tag_list_frame, fg_color="transparent", width=300)
                tag_frame.pack(fill='x', padx=[self.padx], pady=2)

                tag_label = ctk.CTkLabel(tag_frame, text=tag)
                tag_label.pack(side='left', padx=5)

                delete_button = ctk.CTkButton(tag_frame, text="Delete", command=lambda t=tag: delete_tag(t))
                delete_button.pack(side='right', padx=5)

        refresh_tag_list()

    def show_top_deadline_tasks(self):
        for widget in self.deadline_tasks_frame.winfo_children():
            widget.destroy()

        static_tasks = [
            {"name": "Task 1", "deadline": datetime.now() + timedelta(days=3, hours=3)},
            {"name": "Task 2", "deadline": datetime.now() + timedelta(days=2, hours=1)},
            {"name": "Task 3", "deadline": datetime.now() + timedelta(days=1, hours=12)},
        ]

        deadline_tasks = sorted(static_tasks, key=lambda x: x["deadline"])

        for index, task in enumerate(deadline_tasks):
            card_frame = ctk.CTkFrame(self.deadline_tasks_frame, corner_radius=10, fg_color="#F5FFFA")
            
            card_frame.grid(row=0, column=index, padx=10, pady=(5, 10), sticky="nsew")

            task_label = ctk.CTkLabel(card_frame, text=f"Task: {task['name']}", font=self.custom_task_label_font)
            task_label.pack(pady=(5, 0), padx=10)

            deadline_label = ctk.CTkLabel(card_frame, text=f"Deadline: {task['deadline'].strftime('%Y-%m-%d %H:%M')}")
            deadline_label.pack(pady=(0, 5), padx=10)

            # Calculate time left
            time_left = task['deadline'] - datetime.now()
            days_left = time_left.days
            hours_left = time_left.seconds // 3600
            minutes_left = (time_left.seconds % 3600) // 60

            # Display time left
            time_left_text = f"{days_left} days {hours_left} hours left" if days_left >= 0 else "Deadline passed"
            time_left_label = ctk.CTkLabel(card_frame, text=time_left_text)
            time_left_label.pack(pady=(5, 5), padx=10)

        for i in range(len(deadline_tasks)):
            self.deadline_tasks_frame.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TaskManagementSystem(root)
    root.mainloop()
