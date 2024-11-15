import customtkinter as ctk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class TaskSummaryComponent(ctk.CTkFrame):
    def __init__(self, parent, tasks):
        super().__init__(parent)
        self.tasks = tasks
        self.setup_ui()
        self.update_task_counts()
        
    def setup_ui(self):
        # Font settings for labels
        self.custom_label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        
        # Create left and right frames for layout using grid
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        
        # Configure grid weights to make both frames equally wide
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Progress section (left frame)
        self.progress_label = ctk.CTkLabel(left_frame, text="Progress", font=self.custom_label_font)
        self.progress_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(left_frame, width=200)
        self.progress_bar.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        
        # Task count labels (left frame)
        self.total_label = ctk.CTkLabel(left_frame, text="Total Tasks: 0", font=self.custom_label_font)
        self.total_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        
        self.not_started_label = ctk.CTkLabel(left_frame, text="Not Started Tasks: 0", font=self.custom_label_font)
        self.not_started_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        
        self.processing_label = ctk.CTkLabel(left_frame, text="Processing Tasks: 0", font=self.custom_label_font)
        self.processing_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        
        self.completed_label = ctk.CTkLabel(left_frame, text="Completed Tasks: 0", font=self.custom_label_font)
        self.completed_label.grid(row=5, column=0, pady=10, padx=10, sticky="w")
        
        # Pie chart section (right frame)
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nswe")
        
    def update_task_counts(self):
        if not self.tasks:
            self.total_tasks = 0
            self.not_started_tasks = 0
            self.processing_tasks = 0
            self.completed_tasks = 0
            return
        
        self.total_tasks = len(self.tasks)
        
        self.not_started_tasks = sum(1 for task in self.tasks.values()
                                   if isinstance(task, dict) and
                                   task.get('status') == "Not Started")
        
        self.processing_tasks = sum(1 for task in self.tasks.values()
                                  if isinstance(task, dict) and
                                  task.get('status') == "On Progress")
        
        self.completed_tasks = sum(1 for task in self.tasks.values()
                                 if isinstance(task, dict) and
                                 task.get('status') == "Completed")
        
        # Update labels
        self.total_label.configure(text=f"Total Tasks: {self.total_tasks}")
        self.not_started_label.configure(text=f"Not Started Tasks: {self.not_started_tasks}")
        self.processing_label.configure(text=f"Processing Tasks: {self.processing_tasks}")
        self.completed_label.configure(text=f"Completed Tasks: {self.completed_tasks}")
        
        # Update progress bar and pie chart
        self.update_progress_bar()
        self.update_pie_chart()
    
    def update_progress_bar(self):
        if self.total_tasks == 0:
            progress = 0
        else:
            progress = (self.completed_tasks / self.total_tasks)
        self.progress_bar.set(progress)
    
    def update_pie_chart(self):
        self.ax.clear()

        self.figure.patch.set_alpha(0) 
        self.ax.set_facecolor('none') 

        labels = ['Not Started', 'Processing', 'Completed']
        sizes = [self.not_started_tasks, self.processing_tasks, self.completed_tasks]
        colors = ['#FF9999', '#66B2FF', '#99FF99']
        
        non_zero_sizes = []
        non_zero_labels = []
        non_zero_colors = []
        for size, label, color in zip(sizes, labels, colors):
            if size > 0:
                non_zero_sizes.append(size)
                non_zero_labels.append(f"{label}\n({size})")
                non_zero_colors.append(color)
        
        if sum(non_zero_sizes) > 0: 
            self.ax.pie(non_zero_sizes, labels=non_zero_labels, colors=non_zero_colors,
                        autopct='%1.1f%%', startangle=60, radius=0.7)  
        else:
            self.ax.text(0.5, 0.5, 'No Tasks', horizontalalignment='right',
                        verticalalignment='center', fontsize=10, color='gray')

        self.ax.axis('equal') 

        self.canvas.draw()
