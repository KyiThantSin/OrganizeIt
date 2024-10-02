import customtkinter as ctk

# theme
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue") 

class TaskManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("OrganizeIt")
        self.root.geometry("900x700")
         
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

        self.create_filter_section()
        self.create_task_card()
        
    def create_filter_section(self):
        filter_frame = ctk.CTkFrame(self.root, corner_radius=10)  
        filter_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        ctk.CTkLabel(filter_frame, text="Filter By Tags", font=self.custom_label_font).grid(row=0, column=0, padx=(10, 5), pady=(20, 5), sticky="w")
        ctk.CTkLabel(filter_frame, text="Filter By Status", font=self.custom_label_font).grid(row=0, column=1, padx=(10, 5), pady=(20, 5), sticky="w")

        self.tag_entry = ctk.CTkComboBox(filter_frame, values=["Work", "Personal", "Urgent"], variable=self.filter_tag_var, width=180)
        self.tag_entry.grid(row=1, column=0, padx=(10, 5), pady=(10, 40), sticky="ew")

        self.status_entry = ctk.CTkComboBox(filter_frame, values=["On Progress", "Completed", "Not Started"], variable=self.filter_status_var, width=180)
        self.status_entry.grid(row=1, column=1, padx=(5, 10), pady=(10, 40), sticky="ew")

        button_frame = ctk.CTkFrame(filter_frame, fg_color="transparent") 
        button_frame.grid(row=1, column=2, columnspan=2, padx=(10, 10), pady=(10, 40), sticky="e")

        apply_button = ctk.CTkButton(button_frame, text="Apply Filter", width=15)
        apply_button.pack(side="left", padx=(5, 5))

        clear_button = ctk.CTkButton(button_frame, text="Clear", width=15)
        clear_button.pack(side="left", padx=(5, 5))

        # layout 
        filter_frame.grid_columnconfigure(0, weight=0)  
        filter_frame.grid_columnconfigure(1, weight=0)  
        filter_frame.grid_columnconfigure(2, weight=0)  
        filter_frame.grid_columnconfigure(3, weight=0) 

        # Add New Task button frame
        button_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")  
        button_frame.pack(padx=self.padx, pady=(10, 10), fill="x")

        self.pending_list_label = ctk.CTkLabel(button_frame, text="Pending Lists", font=self.custom_label_font)
        self.pending_list_label.pack(side="left", padx=(5, 10))

        self.add_task_button = ctk.CTkButton(button_frame, text="Add New Task", command=self.open_task_creation_form)
        self.add_task_button.pack(side="right", padx=(10, 5))

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
        
        edit_button = ctk.CTkButton(card_frame, text="Edit", width=100)
        edit_button.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="e")

        delete_button = ctk.CTkButton(card_frame, text="Delete", width=100)
        delete_button.grid(row=5, column=1, padx=10, pady=(5, 10), sticky="e")

        # layout
        card_frame.grid_columnconfigure(0, weight=1)

    def open_task_creation_form(self):
        self.task_creation_window = ctk.CTkToplevel(self.root)
        self.task_creation_window.title("Create New Task")
        self.task_creation_window.geometry("400x400")

        ctk.CTkLabel(self.task_creation_window, text="Task Name", font=self.custom_label_font).pack(padx=10, pady=10)
        self.task_name_entry = ctk.CTkEntry(self.task_creation_window, width=300)
        self.task_name_entry.pack(padx=10, pady=10)

        ctk.CTkLabel(self.task_creation_window, text="Description", font=self.custom_label_font).pack(padx=10, pady=10)
        self.description_entry = ctk.CTkEntry(self.task_creation_window, width=300)
        self.description_entry.pack(padx=10, pady=10)

        ctk.CTkLabel(self.task_creation_window, text="Tag", font=self.custom_label_font).pack(padx=10, pady=10)
        self.new_tag_entry = ctk.CTkComboBox(self.task_creation_window, values=["Work", "Personal", "Urgent"], width=180)
        self.new_tag_entry.pack(padx=10, pady=10)

        ctk.CTkLabel(self.task_creation_window, text="Status", font=self.custom_label_font).pack(padx=10, pady=10)
        self.new_status_entry = ctk.CTkComboBox(self.task_creation_window, values=["On Progress", "Completed", "Not Started"], width=180)
        self.new_status_entry.pack(padx=10, pady=10)

        submit_button = ctk.CTkButton(self.task_creation_window, text="Add Task", command=self.add_task)
        submit_button.pack(padx=10, pady=(20, 10))

    def add_task(self):
        task_name = self.task_name_entry.get()
        description = self.description_entry.get()
        tag = self.new_tag_entry.get()
        status = self.new_status_entry.get()

        print(f"Task: {task_name}, Description: {description}, Tag: {tag}, Status: {status}")

        self.task_creation_window.destroy()  # close modal after adding

def main():
    root = ctk.CTk()
    task_manager = TaskManagementSystem(root)
    root.mainloop()

main()
