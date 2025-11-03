import csv
from datetime import datetime

# Data Structures
users = {
    "Grace": {"role": "elderly", "tasks": []},
    "Samuel": {"role": "caregiver", "tasks": []},
    "Linda": {"role": "elderly", "tasks": []}
}

CSV_FILE = "tasks.csv"


def save_tasks_to_csv():
    """Save all tasks to a CSV file"""
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Role", "Task", "Reminder", "Status"])
        for user, data in users.items():
            for t in data["tasks"]:
                writer.writerow([user, data["role"], t["task"], t["reminder"], t["status"]])
    print("Tasks saved to CSV.\n")


def load_tasks_from_csv():
    """Load tasks from the CSV file if it exists"""
    try:
        with open(CSV_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = row["User"].strip()  # use correct header
                if user in users:
                    task_info = {
                        "task": row["Task"].strip(),
                        "reminder": row["Reminder"].strip(),
                        "status": row["Status"].strip()
                    }
                    if task_info not in users[user]["tasks"]:
                        users[user]["tasks"].append(task_info)
        print("[Data loaded from tasks.csv]\n")
    except FileNotFoundError:
        print("No existing task file found, starting fresh.\n")


def add_task(user_name, task_name, reminder_time):
    task = {"task": task_name, "reminder": reminder_time, "status": "Pending"}
    users[user_name]["tasks"].append(task)
    print(f"Task '{task_name}' added for {user_name} at {reminder_time}.")
    save_tasks_to_csv()


def view_tasks(user_name):
    print(f"\n{user_name}'s Task List:")
    tasks = users[user_name]["tasks"]
    if not tasks:
        print("  No tasks available.")
        return
    for i, t in enumerate(tasks, 1):
        print(f"  {i}. {t['task']} - {t['status']} (Reminder: {t['reminder']})")


def mark_task(user_name, task_index, status):
    tasks = users[user_name]["tasks"]
    if 0 <= task_index < len(tasks):
        tasks[task_index]["status"] = status
        print(f"Task '{tasks[task_index]['task']}' marked as {status}.")
        save_tasks_to_csv()
    else:
        print("Invalid task index.")


def show_pending_reminders(current_time):
    print(f"\n[Checking reminders at {current_time}]")
    found = False
    for user, info in users.items():
        for task in info["tasks"]:
            if task["status"].lower() == "pending" and task["reminder"] == current_time:
                print(f"Reminder for {user} ({info['role']}): {task['task']}")
                found = True
    if not found:
        print("No reminders at this time.")


def caregiver_dashboard(caregiver_name):
    print(f"\n{caregiver_name}'s Caregiver Dashboard:")
    for user, data in users.items():
        if data["role"] == "elderly":
            view_tasks(user)


def simulate_reminder_check(times):
    for curr_time in times:
        show_pending_reminders(curr_time)


if __name__ == "__main__":
    print("Cognitive Wellness & Memory Aid App (Version 1.2)\n")

    load_tasks_from_csv()

    # Add sample tasks if CSV is empty
    if not any(u["tasks"] for u in users.values()):
        add_task("Grace", "Take morning medication", "09:00")
        add_task("Samuel", "Check on Grace's progress", "09:30")
        add_task("Linda", "Call doctor for appointment", "10:00")

    view_tasks("Grace")
    view_tasks("Linda")

    mark_task("Grace", 0, "Completed")

    caregiver_dashboard("Samuel")

    times_to_check = ["09:00", "09:30", "10:00"]
    simulate_reminder_check(times_to_check)

