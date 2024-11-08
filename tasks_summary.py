import customtkinter as ctk

class TaskSummaryComponent(ctk.CTkFrame):
    def __init__(self, parent, tasks):
        super().__init__(parent)
        
        # calculate task counts
        self.total_tasks = len(tasks)
        self.processing_tasks = sum(1 for task in tasks if task['status'] == 'processing')
        self.completed_tasks = sum(1 for task in tasks if task['status'] == 'completed')

        # font settings for labels
        self.custom_label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")

        # display
        self.total_label = ctk.CTkLabel(self, text=f"Total Tasks: {self.total_tasks}", font=self.custom_label_font)
        self.total_label.pack(pady=10, padx=10, anchor="w")
        
        self.processing_label = ctk.CTkLabel(self, text=f"Processing Tasks: {self.processing_tasks}", font=self.custom_label_font)
        self.processing_label.pack(pady=10, padx=10, anchor="w")
        
        self.completed_label = ctk.CTkLabel(self, text=f"Completed Tasks: {self.completed_tasks}", font=self.custom_label_font)
        self.completed_label.pack(pady=10,  padx=10, anchor="w")
