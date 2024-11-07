import customtkinter as ctk
from datetime import datetime, timedelta

# theme
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

class Task:
    def __init__(self, name, description, tag, status, deadline=None):
        self.name = name
        self.description = description
        self.tag = tag
        self.status = status
        self.deadline = deadline

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
        self.custom_tags = ["Work", "Personal", "Urgent"]  # default tags
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
        # Create a canvas and a vertical scrollbar
        self.canvas = ctk.CTkCanvas(parent, bg=self.root.cget("bg"), highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")

        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack the canvas and scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create initial task card
        self.create_task_card()  

        # Create additional task cards for demonstration
        for i in range(10):  # Add more tasks for scrolling
            self.create_task_card(f"Task {i+1}", f"This is the description for task {i+1}", "Work", "On Progress")

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
        self.task_creation_window.geometry("400x400")

        self.create_task_form(self.task_creation_window)

    def open_task_edit_form(self, task_name, description, tag, status, deadline):
        self.task_edit_window = ctk.CTkToplevel(self.root)
        self.task_edit_window.title(f"Edit Task: {task_name}")
        self.task_edit_window.geometry("400x400")

        self.create_task_form(self.task_edit_window, task_name, description, tag, status, deadline)

    def create_task_form(self, parent, task_name=None, description=None, tag=None, status=None, deadline=None):
        self.task_name_entry = ctk.CTkEntry(parent)
        self.task_name_entry.grid(row=0, column=0, padx=10, pady=10)
        self.task_name_entry.insert(0, task_name if task_name else "Task Name")

        self.task_description_entry = ctk.CTkEntry(parent)
        self.task_description_entry.grid(row=1, column=0, padx=10, pady=10)
        self.task_description_entry.insert(0, description if description else "Task Description")

        self.task_tag_entry = ctk.CTkComboBox(parent, values=self.custom_tags)
        self.task_tag_entry.grid(row=2, column=0, padx=10, pady=10)
        self.task_tag_entry.set(tag if tag else "Work")

        self.task_status_entry = ctk.CTkComboBox(parent, values=["On Progress", "Completed", "Not Started"])
        self.task_status_entry.grid(row=3, column=0, padx=10, pady=10)
        self.task_status_entry.set(status if status else "Not Started")

        self.task_deadline_entry = ctk.CTkEntry(parent)
        self.task_deadline_entry.grid(row=4, column=0, padx=10, pady=10)
        self.task_deadline_entry.insert(0, deadline.strftime("%Y-%m-%d") if deadline else "yyyy-mm-dd")

        save_button = ctk.CTkButton(parent, text="Save", command=self.save_task)
        save_button.grid(row=5, column=0, padx=10, pady=10)

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

        self.create_task_card(task_name, description, tag, status, deadline)

        self.task_creation_window.destroy()  # Close the creation window

    def open_custom_tag_creation_form(self):
        # You can implement this form to add custom tags here
        tag_creation_window = ctk.CTkToplevel(self.root)
        tag_creation_window.title("Create Custom Tag")
        tag_creation_window.geometry("300x200")

        label = ctk.CTkLabel(tag_creation_window, text="Enter custom tag name:", font=self.custom_label_font)
        label.pack(pady=10)

        custom_tag_entry = ctk.CTkEntry(tag_creation_window)
        custom_tag_entry.pack(pady=10)

        def add_custom_tag():
            new_tag = custom_tag_entry.get()
            if new_tag and new_tag not in self.custom_tags:
                self.custom_tags.append(new_tag)
                tag_creation_window.destroy()

        add_button = ctk.CTkButton(tag_creation_window, text="Add Tag", command=add_custom_tag)
        add_button.pack(pady=10)

    def show_top_deadline_tasks(self):
         # Clear previous deadline tasks
        for widget in self.deadline_tasks_frame.winfo_children():
            widget.destroy()

        # Static data for testing purposes
        static_tasks = [
            {"name": "Task 1", "deadline": datetime.now() + timedelta(days=3, hours=3)},
            {"name": "Task 2", "deadline": datetime.now() + timedelta(days=2, hours=1)},
            {"name": "Task 3", "deadline": datetime.now() + timedelta(days=1, hours=12)},
        ]

        deadline_tasks = sorted(static_tasks, key=lambda x: x["deadline"])

        # Create task cards in a grid layout
        for index, task in enumerate(deadline_tasks):
            # Create a card frame for each task
            card_frame = ctk.CTkFrame(self.deadline_tasks_frame, corner_radius=10, fg_color="#F5FFFA")
            
            # Pack the card frame into the grid
            card_frame.grid(row=0, column=index, padx=10, pady=(5, 10), sticky="nsew")

            # Task name and deadline
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
        # Adjust grid weights for equal spacing
        for i in range(len(deadline_tasks)):
            self.deadline_tasks_frame.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TaskManagementSystem(root)
    root.mainloop()
