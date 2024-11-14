import customtkinter as ctk
import csv
from datetime import datetime

class TaskSummaryComponent(ctk.CTkFrame):
    def __init__(self, parent, tasks):
        super().__init__(parent)
        self.tasks = tasks
        self.setup_ui()
        self.update_task_counts()
        
    def setup_ui(self):
        # Font settings for labels
        self.custom_label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        
        # Progress section
        self.progress_label = ctk.CTkLabel(self, text="Progress", font=self.custom_label_font)
        self.progress_label.pack(pady=10, padx=10, anchor="w")
        
        self.progress_bar = ctk.CTkProgressBar(self, width=200)
        self.progress_bar.pack(pady=10, padx=10, anchor="w")
        
        # Task count labels
        self.total_label = ctk.CTkLabel(self, text="Total Tasks: 0", font=self.custom_label_font)
        self.total_label.pack(pady=10, padx=10, anchor="w")
        
        self.processing_label = ctk.CTkLabel(self, text="Processing Tasks: 0", font=self.custom_label_font)
        self.processing_label.pack(pady=10, padx=10, anchor="w")
        
        self.completed_label = ctk.CTkLabel(self, text="Completed Tasks: 0", font=self.custom_label_font)
        self.completed_label.pack(pady=10, padx=10, anchor="w")
        
        # Export button
        self.export_button = ctk.CTkButton(self, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(pady=10, padx=10)
    
    def update_task_counts(self):
        if not self.tasks:
            self.total_tasks = 0
            self.processing_tasks = 0
            self.completed_tasks = 0
            return
        
        self.total_tasks = len(self.tasks)
        
        # Count processing tasks (including "On Progress" and "Not Started")
        self.processing_tasks = sum(1 for task in self.tasks.values() 
                                  if isinstance(task, dict) and 
                                  task.get('status') in ["On Progress", "Not Started"])
        
        # Count completed tasks
        self.completed_tasks = sum(1 for task in self.tasks.values() 
                                 if isinstance(task, dict) and 
                                 task.get('status') == "Completed")
        
        # Update labels
        self.total_label.configure(text=f"Total Tasks: {self.total_tasks}")
        self.processing_label.configure(text=f"Processing Tasks: {self.processing_tasks}")
        self.completed_label.configure(text=f"Completed Tasks: {self.completed_tasks}")
        
        # Update progress bar
        self.update_progress_bar()
    
    def update_progress_bar(self):
        if self.total_tasks == 0:
            progress = 0
        else:
            progress = (self.completed_tasks / self.total_tasks)
        self.progress_bar.set(progress)
    
    def export_to_csv(self):
        try:
            with open("task_report.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Task ID", "Name", "Description", "Status", "Tag", "Deadline"])
                
                for task_id, task in self.tasks.items():
                    if isinstance(task, dict):
                        deadline = task.get('deadline', '')
                        deadline_str = deadline.strftime("%Y-%m-%d") if deadline else "N/A"
                        
                        writer.writerow([
                            task_id,
                            task.get('name', 'N/A'),
                            task.get('description', 'N/A'),
                            task.get('status', 'N/A'),
                            task.get('tag', 'N/A'),
                            deadline_str
                        ])
                    
            print("Task report exported successfully to task_report.csv")
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")