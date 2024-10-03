import customtkinter as ctk

# theme
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

class TaskManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("OrganizeIt")
        self.root.geometry("990x800")
        
        # padding
        self.padx = 80
        
        # font 
        self.custom_title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
        self.custom_label_font = ctk.CTkFont(family="Arial", size=16, weight="bold")
        self.custom_task_label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")

        # app title 
        self.title_label = ctk.CTkLabel(self.root, text="OrganizeIt", font=self.custom_title_font)
        self.title_label.pack(side="top", anchor="w", padx=self.padx, pady=40)

        # variables
        self.filter_tag_var = ctk.StringVar()
        self.filter_status_var = ctk.StringVar()
        self.custom_tags = ["Work", "Personal", "Urgent"]  # default tags

        self.create_filter_section()
        self.create_task_card()
        
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

       
        # Add New Task button frame
        button_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")  
        button_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        self.pending_list_label = ctk.CTkLabel(button_frame, text="Pending Lists", font=self.custom_label_font)
        self.pending_list_label.pack(side="left", padx=(5, 10))

        self.add_task_button = ctk.CTkButton(button_frame, text="Add New Task", command=self.open_task_creation_form)
        self.add_task_button.pack(side="right", padx=(10, 5))
        
        # Custom Tag button
        add_custom_tag_button = ctk.CTkButton(button_frame, text="Add Custom Tag", command=self.open_custom_tag_creation_form)
        add_custom_tag_button.pack(side="right", padx=(5, 5))

        # task list frame
        self.tasks_list_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        self.tasks_list_frame.pack(padx=self.padx, pady=5, fill="both", expand=True)

    def create_task_card(self):
        card_frame = ctk.CTkFrame(self.tasks_list_frame, corner_radius=10)
        card_frame.pack(padx=0, pady=(10,10), fill="x")

        ctk.CTkLabel(card_frame, text=f"Task", font=self.custom_task_label_font).grid(row=0, column=0, sticky="w", padx=20, pady=(10,5))
        ctk.CTkLabel(card_frame, text=f"Description:").grid(row=1, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Tag: ").grid(row=2, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Status: ").grid(row=3, column=0, sticky="w", padx=20)
        ctk.CTkLabel(card_frame, text=f"Date: ").grid(row=4, column=0, sticky="w", padx=20, pady=(5,5))
        
        edit_button = ctk.CTkButton(card_frame, text="Edit", width=100, command=lambda: self.open_task_edit_form("Task", "Description", "Work", "On Progress"))
        edit_button.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="e")

        delete_button = ctk.CTkButton(card_frame, text="Delete", width=100)
        delete_button.grid(row=5, column=1, padx=10, pady=(5, 10), sticky="e")

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
        self.new_tag_entry = ctk.CTkComboBox(form_frame, values=self.custom_tags, width=180)
        self.new_tag_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.new_tag_entry.set(tag)

        # Status
        ctk.CTkLabel(form_frame, text="Status", font=self.custom_label_font).grid(row=6, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_status_entry = ctk.CTkComboBox(form_frame, values=["On Progress", "Completed", "Not Started"], width=180)
        self.new_status_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.new_status_entry.set(status)

        button_frame = ctk.CTkFrame(self.task_edit_window, fg_color="transparent")
        button_frame.pack(pady=(10, 10), anchor="center")

        save_button = ctk.CTkButton(button_frame, text="Save Changes", command=self.save_task_edits)
        save_button.pack(side="left", padx=(5, 5), pady=(0,10))  

        go_back_button = ctk.CTkButton(button_frame, text="Go Back", command=self.task_edit_window.destroy)
        go_back_button.pack(side="left", padx=(5, 0), pady=(0,10)) 

    def save_task_edits(self):
        task_name = self.task_name_entry.get()
        description = self.description_entry.get()
        tag = self.new_tag_entry.get()
        status = self.new_status_entry.get()

        print(f"Updated Task: {task_name}, Description: {description}, Tag: {tag}, Status: {status}")

        self.task_edit_window.destroy()  # close modal after saving

    def create_task_form(self, parent_window):
        # Task Name
        form_frame = ctk.CTkFrame(parent_window, fg_color="transparent")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Task Name", font=self.custom_label_font).grid(row=0, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_task_name_entry = ctk.CTkEntry(form_frame, width=300)
        self.new_task_name_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Description
        ctk.CTkLabel(form_frame, text="Description", font=self.custom_label_font).grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_description_entry = ctk.CTkEntry(form_frame, width=300)
        self.new_description_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Tag
        ctk.CTkLabel(form_frame, text="Tag", font=self.custom_label_font).grid(row=4, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_tag_entry = ctk.CTkComboBox(form_frame, values=self.custom_tags, width=180)
        self.new_tag_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Status
        ctk.CTkLabel(form_frame, text="Status", font=self.custom_label_font).grid(row=6, column=0, sticky="w", padx=5, pady=(10, 5))
        self.new_status_entry = ctk.CTkComboBox(form_frame, values=["On Progress", "Completed", "Not Started"], width=180)
        self.new_status_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="ew")

        button_frame = ctk.CTkFrame(parent_window, fg_color="transparent")
        button_frame.pack(pady=(10, 10), anchor="center")

        save_button = ctk.CTkButton(button_frame, text="Create Task", command=self.save_new_task)
        save_button.pack(side="left", padx=(5, 5), pady=(0,10))  

        go_back_button = ctk.CTkButton(button_frame, text="Go Back", command=parent_window.destroy)
        go_back_button.pack(side="left", padx=(5, 0), pady=(0,10)) 

    def save_new_task(self):
        task_name = self.new_task_name_entry.get()
        description = self.new_description_entry.get()
        tag = self.new_tag_entry.get()
        status = self.new_status_entry.get()

        print(f"New Task Created: {task_name}, Description: {description}, Tag: {tag}, Status: {status}")

        self.task_creation_window.destroy()  # close modal after saving

    def open_custom_tag_creation_form(self):
        self.custom_tag_window = ctk.CTkToplevel(self.root)
        self.custom_tag_window.title("Create Custom Tag")
        self.custom_tag_window.geometry("300x200")

        form_frame = ctk.CTkFrame(self.custom_tag_window, fg_color="transparent")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Custom Tag Name", font=self.custom_label_font).grid(row=0, column=0, sticky="w", padx=5, pady=(10, 5))
        self.custom_tag_entry = ctk.CTkEntry(form_frame, width=200)
        self.custom_tag_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        button_frame = ctk.CTkFrame(self.custom_tag_window, fg_color="transparent")
        button_frame.pack(pady=(10, 10), anchor="center")

        save_button = ctk.CTkButton(button_frame, text="Save Tag", command=self.save_custom_tag)
        save_button.pack(side="left", padx=(5, 5), pady=(0,10))  

        go_back_button = ctk.CTkButton(button_frame, text="Go Back", command=self.custom_tag_window.destroy)
        go_back_button.pack(side="left", padx=(5, 0), pady=(0,10)) 

    def save_custom_tag(self):
        custom_tag = self.custom_tag_entry.get()
        if custom_tag and custom_tag not in self.custom_tags:  # check if the tag is not empty and not already in the list
            self.custom_tags.append(custom_tag)
            self.tag_entry.configure(values=self.custom_tags)  # update the combo box values
            print(f"Custom Tag Added: {custom_tag}")
        else:
            print("Tag is either empty or already exists.")

        self.custom_tag_window.destroy()  # close modal after saving

def main():
    root = ctk.CTk()
    task_manager = TaskManagementSystem(root)
    root.mainloop()

main()
