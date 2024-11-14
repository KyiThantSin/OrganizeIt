import customtkinter as ctk
import csv
from datetime import datetime

class TaskSummaryComponent(ctk.CTkFrame):
    def __init__(self, parent, tasks):
        super().__init__(parent)
        self.tasks = tasks 

        # Calculate task counts
        self.total_tasks = len(self.tasks)
        self.processing_tasks = sum(1 for task in tasks.values() if task['status'] == 'processing')
        self.completed_tasks = sum(1 for task in tasks.values() if task['status'] == 'completed')
        self.total_tasks = len(tasks)
        # Font settings for labels
        self.custom_label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self.progress_label = ctk.CTkLabel(self, text="Progress", font=self.custom_label_font)
        self.progress_label.pack(pady=10, padx=10, anchor="w")
        
        self.progress_bar = ctk.CTkProgressBar(self, width=200)
        self.progress_bar.set(self.calculate_task_progress(tasks))
        self.progress_bar.pack(pady=10, padx=10, anchor="w")

        # Display task counts
        self.total_label = ctk.CTkLabel(self, text=f"Total Tasks: {self.total_tasks}", font=self.custom_label_font)
        self.total_label.pack(pady=10, padx=10, anchor="w")
        
        self.processing_label = ctk.CTkLabel(self, text=f"Processing Tasks: {self.processing_tasks}", font=self.custom_label_font)
        self.processing_label.pack(pady=10, padx=10, anchor="w")
        
        self.completed_label = ctk.CTkLabel(self, text=f"Completed Tasks: {self.completed_tasks}", font=self.custom_label_font)
        self.completed_label.pack(pady=10, padx=10, anchor="w")

        # Export to CSV button
        self.export_button = ctk.CTkButton(self, text="Export to CSV", command=lambda: self.export_to_csv(tasks))
        self.export_button.pack(pady=10, padx=10)

        # Track historical data button
        self.track_button = ctk.CTkButton(self, text="Track Historical Data", command=lambda: self.track_historical_data(tasks))
        self.track_button.pack(pady=10, padx=10)
    
    def calculate_task_progress(self, tasks):
        total_progress = 0
        count = 0
        for task in tasks:
            if 'subtasks' in task: 
                subtasks_progress = sum(subtask['progress'] for subtask in task['subtasks']) / len(task['subtasks'])
                total_progress += subtasks_progress
                count += 1
        return total_progress / count if count > 0 else 0

    def export_to_csv(self, tasks):
        try:
            with open("task_report.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Task ID", "Name", "Status", "Priority", "Tag", "Date"])

                for task in tasks:
                    task_id = task.get('id', 'N/A')  
                    name = task.get('name', 'N/A')
                    status = task.get('status', 'N/A')
                    priority = task.get('priority', 'N/A')
                    tag = task.get('tag', 'N/A')
                    date = task.get('date', 'N/A')

                    writer.writerow([task_id, name, status, priority, tag, date])
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")

    def track_historical_data(self, tasks):
        date_trends = {}
        for task in tasks:
            task_date = task['date']
            date_trends[task_date] = date_trends.get(task_date, 0) + 1
        print(f"Task Trends by Date: {date_trends}")
