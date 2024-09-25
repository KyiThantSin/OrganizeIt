import customtkinter as ctk
from tkinter import font

# theme
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue") 

class TaskManagementSystem:
    def __init__(self, root):
        self.root = root  # ctk 
        self.root.title("OrganizeIt")
        self.root.geometry("900x700")

        # padding
        self.padx = 80
        
        # font 
        self.custom_title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
        self.custom_label_font = ctk.CTkFont(family="Arial", size=16, weight="normal")

        # app title 
        self.title_label = ctk.CTkLabel(self.root, text="OrganizeIt", font=self.custom_title_font)
        self.title_label.pack(side="top", anchor="w", padx=self.padx, pady=40)

        # variables
        self.filter_tag_var = ctk.StringVar()
        self.filter_status_var = ctk.StringVar()

        self.create_filter_section()
    
    def create_filter_section(self):
        filter_frame = ctk.CTkFrame(self.root, corner_radius=10)  # Child of main window
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
        clear_button.pack(side="left",padx=(5, 5))

        #layout 
        filter_frame.grid_columnconfigure(0, weight=0)  
        filter_frame.grid_columnconfigure(1, weight=0)  
        filter_frame.grid_columnconfigure(2, weight=0)  
        filter_frame.grid_columnconfigure(3, weight=0) 


def main():
    root = ctk.CTk()
    task_manager = TaskManagementSystem(root)
    root.mainloop()

main()
