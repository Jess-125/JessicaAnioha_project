'''
The update for the Version 1 Python prototype of the Cognitive Wellness & Memory Aid App.
Core features implemented so far: elderly users can add, view, and mark tasks as Completed, Skipped, or 
Deferred, while caregivers can monitor all elderly users’ tasks through a dashboard. The app includes 
a simple text-based interface and time-based reminder checking. Additionally, basic data structures 
were created to store user information and tasks, ensuring the system can track multiple users and 
their task statuses. This version lays the foundation for future improvements such as audio/text notifications, 
a graphical user interface, persistent storage, and enhanced accessibility features. 
'''

import time
from datetime import datetime

# Data Structures
users = {
    "Grace": {"role": "elderly", "tasks": []},
    "Samuel": {"role": "caregiver", "tasks": []},
    "Linda": {"role": "elderly", "tasks": []}
}

# Helper Functions

def add_task(user_name, task_name, reminder_time):
    """Add a new task for a specific user"""
    task = {
        "task": task_name,
        "reminder": reminder_time,
        "status": "Pending"
    }
    users[user_name]["tasks"].append(task)
    print(f"Task '{task_name}' added for {user_name} at {reminder_time}.")

def view_tasks(user_name):
    """View all tasks for a specific user"""
    print(f"\n {user_name}'s Task List:")
    for i, t in enumerate(users[user_name]["tasks"], 1):
        print(f"{i}. {t['task']} - {t['status']} (Reminder: {t['reminder']})")

def mark_task(user_name, task_index, status):
    """Mark a task as Completed, Skipped, or Deferred"""
    tasks = users[user_name]["tasks"]
    if 0 <= task_index < len(tasks):
        tasks[task_index]["status"] = status
        print(f" Task '{tasks[task_index]['task']}' marked as {status}.")
    else:
        print("Invalid task index.")

def show_pending_reminders(now):
    """Check for any reminders due in the next minute"""
    #now = datetime.now().strftime("%H:%M")
    print("\n Checking for upcoming reminders...")
    for user, data in users.items():
        for t in data["tasks"]:
            #print(t["status"], t["reminder"])
            if t["status"] == "Pending" and t["reminder"] == now:
                print(f" Reminder for {user}: {t['task']} (Time: {t['reminder']})")

def caregiver_dashboard(caregiver_name):
    """Show all elderly users’ tasks and statuses for a caregiver"""
    print(f"\n {caregiver_name}'s Caregiver Dashboard")
    for user, data in users.items():
        if data["role"] == "elderly":
            view_tasks(user)

# Example Usage (Simulated Flow)
if __name__ == "__main__":
    print(" Cognitive Wellness & Memory Aid App (Version 1)\n")

    # Add sample tasks
    add_task("Grace", "Take morning medication", "09:00")
    add_task("Samuel", "Check on Grace's progress", "09:30")  # caregiver can have tasks too
    add_task("Linda", "Call doctor for appointment", "10:00")

    # Elderly users view their tasks
    view_tasks("Grace")
    view_tasks("Linda")

    # Mark a task as completed
    mark_task("Grace", 0, "Completed")

    # Show caregiver dashboard
    caregiver_dashboard("Samuel")

    # CH save to CSV file (not implemented yet)
    # this should actually be done after each add/mark action to ensure persistence

    # Simulate

    # read in tasks from CSV (not implemented yet)

    # Simulate time-based reminder checking
    #current_time = datetime.now().strftime("%H:%M")
    current_time = "09:30"  # For demonstration, set to a specific time
    print(f"\n Current time: {current_time}")
    show_pending_reminders(current_time)

    for curr_time in ["09:00", "09:30", "10:00"]:
        print(f"\n Current time: {curr_time}")
        show_pending_reminders(curr_time)
        
    # CH Better: write a function that takes a list of times and simulates the checking
