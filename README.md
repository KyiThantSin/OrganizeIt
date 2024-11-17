# OrganizeIt – Task Manager

### Project Description

**OrganizeIt** is a simple task management system built with Python, CustomTkinter, and ZODB. It allows users to easily create, edit, delete, and filter tasks, track their status, and organize them using custom tags, all through a user-friendly interface.

<img width="1451" alt="Screen Shot 2567-11-17 at 23 11 47" src="https://github.com/user-attachments/assets/93aedcb3-750e-404f-aa5e-74df76cf1d2c">

### Key Features

- **Task Management**: Create, edit, and delete tasks with fields for name, description, tag, and status. Every task has a unique ID for consistent lookup.
- **Filtering**: Filter tasks by tags and status using dropdowns.
- **Custom Tags**: Add and delete tags for personalized task organization.
- **Task Display**: A scrollable task list that dynamically loads tasks from ZODB, highlighting the top 3 tasks based on their approaching deadlines.
- **Progress Tracking**: Track the progress of tasks via a progress bar and a detailed task summary.
- **Data Visualization**: An interactive pie chart visualizes task distribution by status, dynamically updated in real-time.

### Use Cases

- **Personal Organization**: Plan and organize daily tasks with custom tags and progress tracking.
- **Work Management**: Filter and prioritize tasks by deadline and status.
- **Academic Planning**: Track homework, exams, and study schedules.

### Libraries Used

- **CustomTkinter**: A modern and easy-to-use library for creating graphical user interfaces in Python.
- **ZODB**: A lightweight object-oriented database used for task storage.
- **Matplotlib**: A library used for creating data visualizations, such as pie charts, to display task distributions.
- **datetime**: Python's standard library for handling date-related tasks, especially for deadline management.

