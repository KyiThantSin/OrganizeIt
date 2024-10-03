import customtkinter as ctk

# theme
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

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
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.create_task_list_area(self.left_frame)

        self.hello_world_label = ctk.CTkLabel(self.right_frame, text="Hello world", font=self.custom_label_font)
        self.hello_world_label.pack(pady=20)
        
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

        self.create_task_card()  # Create initial task card

        # Create additional task cards for demonstration
        for i in range(10):  # Add more tasks for scrolling
            self.create_task_card(f"Task {i+1}", f"This is the description for task {i+1}", "Work", "On Progress")

    def create_task_card(self, task_name="Task", description="Description", tag="Work", status="On Progress"):
        card_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        card_frame.pack(padx=5, pady=(10,10), fill="x")

        ctk.CTkLabel(card_frame, text=f"{task_name}", font=self.custom_task_label_font).grid(row=0, column=0, sticky="w", padx=20, pady=(10,5))
        ctk.CTkLabel(card_frame, text=f"Description: {description}").grid(row=1, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Tag: {tag}").grid(row=2, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Status: {status}").grid(row=3, column=0, sticky="w", padx=20)
        
        edit_button = ctk.CTkButton(card_frame, text="Edit", width=100, command=lambda: self.open_task_edit_form(task_name, description, tag, status))
        edit_button.grid(row=4, column=0, padx=10, pady=(5, 10), sticky="e")

        delete_button = ctk.CTkButton(card_frame, text="Delete", width=100)
        delete_button.grid(row=4, column=1, padx=10, pady=(5, 10), sticky="e")

        # layout
        card_frame.grid_columnconfigure(0, weight=1)

    def open_task_creation_form(self):
        self.task_creation_window = ctk.CTkToplevel(self.root)
        self.task_creation_window.title("Create New Task")
        self.task_creation_window.geometry("400x400")

        self.create_task_form(self.task_creation_window)

    def open_task_edit_form(self, task_name, description, tag, status):
        self.task_edit_window = ctk.CTkToplevel(self.root)
        self.task_edit_window.title("Edit Task")
        self.task_edit_window.geometry("400x400")

        form_frame = ctk.CTkFrame(self.task_edit_window, fg_color="transparent")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Pre-populating the form with task details
        ctk.CTkLabel(form_frame, text="Task Name", font=self.custom_label_font).grid(row=0, column=0, sticky="w", padx=5, pady=(10, 5))
        self.task_name_entry = ctk.CTkEntry(form_frame, width=300)
        self.task_name_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.task_name_entry.insert(0, task_name)

        # Description
        ctk.CTkLabel(form_frame, text="Description", font=self.custom_label_font).grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))
        self.description_entry = ctk.CTkEntry(form_frame, width=300)
        self.description_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.description_entry.insert(0, description)

        # Tag
        ctk.CTkLabel(form_frame, text="Tag", font=self.custom_label_font).grid(row=4, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_tag_entry = ctk.CTkComboBox(form_frame, values=self.custom_tags)
        self.new_tag_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.new_tag_entry.set(tag)

        # Status
        ctk.CTkLabel(form_frame, text="Status", font=self.custom_label_font).grid(row=6, column=0, sticky="w", padx=5, pady=(10, 5))
        self.status_entry = ctk.CTkComboBox(form_frame, values=["On Progress", "Completed", "Not Started"])
        self.status_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.status_entry.set(status)

        # Save and Cancel buttons
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=8, column=0, padx=5, pady=(10, 10), sticky="e")
        save_button = ctk.CTkButton(button_frame, text="Save", command=self.save_task_edit)
        save_button.pack(side="left", padx=(5, 5))
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.task_edit_window.destroy)
        cancel_button.pack(side="left", padx=(5, 5))

    def create_task_form(self, parent):
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Task Name", font=self.custom_label_font).grid(row=0, column=0, sticky="w", padx=5, pady=(10, 5))
        self.task_name_entry = ctk.CTkEntry(form_frame, width=300)
        self.task_name_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Description", font=self.custom_label_font).grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))
        self.description_entry = ctk.CTkEntry(form_frame, width=300)
        self.description_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Tag", font=self.custom_label_font).grid(row=4, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_tag_entry = ctk.CTkComboBox(form_frame, values=self.custom_tags)
        self.new_tag_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Status", font=self.custom_label_font).grid(row=6, column=0, sticky="w", padx=5, pady=(10, 5))
        self.status_entry = ctk.CTkComboBox(form_frame, values=["On Progress", "Completed", "Not Started"])
        self.status_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="ew")

        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=8, column=0, padx=5, pady=(10, 10), sticky="e")
        add_button = ctk.CTkButton(button_frame, text="Add Task", command=self.add_task)
        add_button.pack(side="left", padx=(5, 5))
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=parent.destroy)
        cancel_button.pack(side="left", padx=(5, 5))

    def add_task(self):
        task_name = self.task_name_entry.get()
        description = self.description_entry.get()
        tag = self.new_tag_entry.get()
        status = self.status_entry.get()
        self.create_task_card(task_name, description, tag, status)
        self.task_creation_window.destroy()

    def save_task_edit(self):
        # Logic for saving the edited task (not implemented in this example)
        self.task_edit_window.destroy()

    def open_custom_tag_creation_form(self):
        self.custom_tag_window = ctk.CTkToplevel(self.root)
        self.custom_tag_window.title("Add Custom Tag")
        self.custom_tag_window.geometry("400x400")

        form_frame = ctk.CTkFrame(self.custom_tag_window, fg_color="transparent")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Tag Name", font=self.custom_label_font).grid(row=0, column=0, sticky="w", padx=5, pady=(10, 5))
        self.custom_tag_entry = ctk.CTkEntry(form_frame, width=300)
        self.custom_tag_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=2, column=0, padx=5, pady=(10, 10), sticky="e")
        add_button = ctk.CTkButton(button_frame, text="Add Tag", command=self.add_custom_tag)
        add_button.pack(side="left", padx=(5, 5))
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.custom_tag_window.destroy)
        cancel_button.pack(side="left", padx=(5, 5))

    def add_custom_tag(self):
        custom_tag = self.custom_tag_entry.get()
        if custom_tag and custom_tag not in self.custom_tags:
            self.custom_tags.append(custom_tag)
            self.tag_entry.configure(values=self.custom_tags)  # Update the tag entry with new values
        self.custom_tag_window.destroy()

# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = TaskManagementSystem(root)
    root.mainloop()
