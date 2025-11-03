import streamlit as st
import pandas as pd
from datetime import datetime
import csv

CSV_FILE = "tasks.csv"


def load_tasks():
    """Load tasks from CSV"""
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["User", "Role", "Task", "Reminder", "Status"])
    return df

def save_tasks(df):
    """Save tasks to CSV"""
    df.to_csv(CSV_FILE, index=False)


st.title("Cognitive Wellness & Memory Aid App")

# Load CSV
df = load_tasks()

st.subheader("All Tasks")
st.dataframe(df)

st.subheader("Add New Task")
with st.form("add_task_form"):
    user = st.selectbox("User", ["Grace", "Samuel", "Linda"])
    role = "elderly" if user in ["Grace", "Linda"] else "caregiver"
    task_name = st.text_input("Task Name")
    reminder = st.text_input("Reminder Time (HH:MM)")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        new_task = {"User": user, "Role": role, "Task": task_name, "Reminder": reminder, "Status": "Pending"}
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
        save_tasks(df)
        st.success(f"Task '{task_name}' added for {user}")
        st.experimental_rerun()


st.subheader("Update Task Status")
if not df.empty:
    task_index = st.selectbox("Select Task", df.index, format_func=lambda i: f"{df.at[i,'User']} - {df.at[i,'Task']} ({df.at[i,'Status']})")
    if st.button("Mark as Completed"):
        df.at[task_index, "Status"] = "Completed"
        save_tasks(df)
        st.success(f"Task '{df.at[task_index,'Task']}' marked as Completed")
        st.experimental_rerun()


st.subheader("Pending Tasks")
st.dataframe(df[df["Status"]=="Pending"])


st.subheader("Reminders Now")
current_time = datetime.now().strftime("%H:%M")
reminders_now = df[df["Reminder"] == current_time]
if not reminders_now.empty:
    st.dataframe(reminders_now)
else:
    st.write("No reminders at this time.")


