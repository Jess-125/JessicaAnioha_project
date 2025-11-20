import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

CSV_FILE = "tasks.csv"

# Helper Functions 
def load_tasks():
    try:
        df = pd.read_csv(CSV_FILE, dtype=str)
        for col in ["User", "Role", "Task", "Reminder", "Status", "ID"]:
            if col not in df.columns:
                df[col] = ""
        return df
    except FileNotFoundError:
        df = pd.DataFrame(columns=["User", "Role", "Task", "Reminder", "Status", "ID"])
        return df

def save_tasks(df):
    df.to_csv(CSV_FILE, index=False)

def make_new_task(user, role, task_name, reminder_time):
    task_id = str(int(datetime.now().timestamp()*1000))
    return {"User": user, "Role": role, "Task": task_name, "Reminder": reminder_time,
            "Status": "Pending", "ID": task_id}

# Session Defaults
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "reminders_shown" not in st.session_state:
    st.session_state.reminders_shown = set()

# Mobile-Friendly CSS 
st.markdown("""
<style>
.stButton>button {height:48px; font-size:16px;}
.stTextInput>div>div>input {height:40px; font-size:16px;}
.stSelectbox>div>div>div>button {height:44px; font-size:16px;}
.big-title {font-size:28px; font-weight:600; margin-bottom:15px;}
.section {padding: 10px 6px; border-radius:12px; margin-bottom:12px;}
</style>
""", unsafe_allow_html=True)

# Login 
st.title("Cognitive Wellness & Memory Aid App")
st.markdown("### Login / Select Profile")

if st.session_state.user is None:
    user_select = st.selectbox("Select profile", ["-- Select --", "Grace", "Samuel", "Linda"])
    if st.button("Sign In"):
        if user_select == "-- Select --":
            st.warning("Please select a profile to sign in.")
        else:
            st.session_state.user = user_select
            st.session_state.role = "elderly" if user_select in ["Grace", "Linda"] else "caregiver"
            st.success(f"Signed in as {st.session_state.user} ({st.session_state.role})")
            st.rerun()
else:
    st.sidebar.write(f"Signed in as **{st.session_state.user}** ({st.session_state.role})")
    if st.sidebar.button("Sign Out"):
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.reminders_shown = set()
        st.rerun()

if st.session_state.user is None:
    st.stop()

df = load_tasks()

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "All Tasks", "Add Task", "Pending Tasks", "Reminders"]
)

#  Reminder Modal
def check_reminders():
    current_time = datetime.now().strftime("%H:%M")
    user_tasks = df[(df["User"]==st.session_state.user) & (df["Status"]=="Pending") & (df["Reminder"]==current_time)]
    for _, row in user_tasks.iterrows():
        if row["ID"] not in st.session_state.reminders_shown:
            with st.modal(f"Reminder for {st.session_state.user}"):
                st.markdown(f"### {row['Task']}")
                st.write(f"Reminder time: **{row['Reminder']}**")
                if st.button("Mark Completed"):
                    idx = df.index[df["ID"]==row["ID"]][0]
                    df.at[idx, "Status"] = "Completed"
                    save_tasks(df)
                    st.success("Task marked completed.")
                    st.session_state.reminders_shown.add(row["ID"])
                    st.rerun()
                if st.button("Snooze 5 min"):
                    idx = df.index[df["ID"]==row["ID"]][0]
                    old_time = datetime.strptime(row["Reminder"], "%H:%M")
                    new_time = (old_time + timedelta(minutes=5)).strftime("%H:%M")
                    df.at[idx, "Reminder"] = new_time
                    save_tasks(df)
                    st.success(f"Snoozed to {new_time}")
                    st.session_state.reminders_shown.add(row["ID"])
                    st.rerun()

check_reminders()

# Pages
if page == "Dashboard":
    st.markdown('<div class="section"><h3>Dashboard</h3></div>', unsafe_allow_html=True)

    if "dashboard_filter" not in st.session_state:
        st.session_state.dashboard_filter = "All"

    col1, col2, col3 = st.columns(3)

    if col1.button("Total Tasks"):
        st.session_state.dashboard_filter = "All"
    if col2.button("Pending Tasks"):
        st.session_state.dashboard_filter = "Pending"
    if col3.button("Completed Tasks"):
        st.session_state.dashboard_filter = "Completed"

    if st.session_state.dashboard_filter == "All":
        filtered_df = df
        st.subheader("All Tasks")
    elif st.session_state.dashboard_filter == "Pending":
        filtered_df = df[df["Status"] == "Pending"]
        st.subheader("Pending Tasks")
    else:
        filtered_df = df[df["Status"] == "Completed"]
        st.subheader("Completed Tasks")

    st.dataframe(filtered_df)


elif page == "All Tasks":
    st.markdown('<div class="section"><h3>All Tasks</h3></div>', unsafe_allow_html=True)
    st.dataframe(df)

elif page == "Add Task":
    st.markdown('<div class="section"><h3>➕ Add Task</h3></div>', unsafe_allow_html=True)
    with st.form("add_task_form"):
        user = st.selectbox("Assign To", ["Grace", "Samuel", "Linda"])
        role = "elderly" if user in ["Grace","Linda"] else "caregiver"
        task_name = st.text_input("Task Name")
        reminder = st.text_input("Reminder Time (HH:MM)")
        submitted = st.form_submit_button("Add Task")
        if submitted:
            try:
                datetime.strptime(reminder, "%H:%M")
            except ValueError:
                st.error("Invalid time format. Use HH:MM")
                st.stop()
            new_task = make_new_task(user, role, task_name, reminder)
            df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
            save_tasks(df)
            st.success(f"Task '{task_name}' added for {user}")
            st.rerun()

elif page == "Pending Tasks":
    st.markdown('<div class="section"><h3>Pending Tasks</h3></div>', unsafe_allow_html=True)
    pending_df = df[df["Status"]=="Pending"]
    st.dataframe(pending_df)

elif page == "Reminders":
    st.markdown('<div class="section"><h3>Reminders Now</h3></div>', unsafe_allow_html=True)
    current_time = datetime.now().strftime("%H:%M")
    reminders_now = df[df["Reminder"]==current_time]
    if not reminders_now.empty:
        st.dataframe(reminders_now)
    else:
        st.write("No reminders at this time.")
