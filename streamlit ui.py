import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pydub import AudioSegment
from pydub.utils import which
from pydub import AudioSegment


if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=["User","Role","Task","Reminder","Status","ID"])
if "wellness_df" not in st.session_state:
    st.session_state.wellness_df = pd.DataFrame(columns=["User","Date","Meal","Mood"])


def make_new_task(user, role, task_name, reminder_time):
    task_id = str(int(datetime.now().timestamp()*1000))
    return {"User": user, "Role": role, "Task": task_name, "Reminder": reminder_time,
            "Status": "Pending", "ID": task_id}


if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "reminders_shown" not in st.session_state:
    st.session_state.reminders_shown = set()
if "dashboard_filter" not in st.session_state:
    st.session_state.dashboard_filter = "All"


st.markdown("""
<style>
.stButton>button {height:48px; font-size:16px;}
.stTextInput>div>div>input {height:40px; font-size:16px;}
.stSelectbox>div>div>div>button {height:44px; font-size:16px;}
.big-title {font-size:28px; font-weight:600; margin-bottom:15px;}
.section {padding: 10px 6px; border-radius:12px; margin-bottom:12px;}
</style>
""", unsafe_allow_html=True)


st.title("Cognitive Wellness & Memory Aid App")
st.markdown("### Login / Select Profile")

if st.session_state.user is None:
    user_select = st.selectbox("Select profile", ["-- Select --", "Grace", "Samuel", "Linda"])
    if st.button("Sign In"):
        if user_select != "-- Select --":
            st.session_state.user = user_select
            st.session_state.role = "elderly" if user_select in ["Grace", "Linda"] else "caregiver"
            st.success(f"Signed in as {st.session_state.user} ({st.session_state.role})")
            st.rerun()
        else:
            st.warning("Please select a profile.")
else:
    st.sidebar.write(f"Signed in as **{st.session_state.user}** ({st.session_state.role})")
    if st.sidebar.button("Sign Out"):
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.reminders_shown = set()
        st.rerun()

if st.session_state.user is None:
    st.stop()

tasks_df = st.session_state.tasks_df
wellness_df = st.session_state.wellness_df


page = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "All Tasks", "Add Task", "Pending Tasks", "Reminders", "Wellness Tracker"]
)


def check_reminders():
    current_time = datetime.now().strftime("%H:%M")
    user_tasks = tasks_df[(tasks_df["User"]==st.session_state.user) & (tasks_df["Status"]=="Pending") & (tasks_df["Reminder"]==current_time)]
    for _, row in user_tasks.iterrows():
        if row["ID"] not in st.session_state.reminders_shown:
            with st.modal(f"🔔 Reminder for {st.session_state.user}"):
                st.markdown(f"### {row['Task']}")
                st.write(f"Reminder time: **{row['Reminder']}**")
                if st.button("Mark Completed"):
                    idx = tasks_df.index[tasks_df["ID"]==row["ID"]][0]
                    tasks_df.at[idx, "Status"] = "Completed"
                    st.session_state.tasks_df = tasks_df
                    st.success("Task marked completed.")
                    st.session_state.reminders_shown.add(row["ID"])
                    st.rerun()
                if st.button("Snooze 5 min"):
                    idx = tasks_df.index[tasks_df["ID"]==row["ID"]][0]
                    old_time = datetime.strptime(row["Reminder"], "%H:%M")
                    new_time = (old_time + timedelta(minutes=5)).strftime("%H:%M")
                    tasks_df.at[idx, "Reminder"] = new_time
                    st.session_state.tasks_df = tasks_df
                    st.success(f"Snoozed to {new_time}")
                    st.session_state.reminders_shown.add(row["ID"])
                    st.rerun()

check_reminders()


if page == "Dashboard":
    st.markdown('<div class="section"><h3>Dashboard</h3></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    if col1.button("Total Tasks"):
        st.session_state.dashboard_filter = "All"
    if col2.button("Pending Tasks"):
        st.session_state.dashboard_filter = "Pending"
    if col3.button("Completed Tasks"):
        st.session_state.dashboard_filter = "Completed"

    if st.session_state.dashboard_filter == "All":
        filtered_df = tasks_df
        st.subheader("All Tasks")
    elif st.session_state.dashboard_filter == "Pending":
        filtered_df = tasks_df[tasks_df["Status"]=="Pending"]
        st.subheader("Pending Tasks")
    else:
        filtered_df = tasks_df[tasks_df["Status"]=="Completed"]
        st.subheader("Completed Tasks")
    st.dataframe(filtered_df)

elif page == "All Tasks":
    st.markdown('<div class="section"><h3>All Tasks</h3></div>', unsafe_allow_html=True)
    st.dataframe(tasks_df)

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
            st.session_state.tasks_df = pd.concat([tasks_df, pd.DataFrame([new_task])], ignore_index=True)
            st.success(f"Task '{task_name}' added for {user}")
            st.rerun()

elif page == "Pending Tasks":
    st.markdown('<div class="section"><h3>Pending Tasks</h3></div>', unsafe_allow_html=True)
    pending_df = tasks_df[tasks_df["Status"]=="Pending"]
    st.dataframe(pending_df)

elif page == "Reminders":
    st.markdown('<div class="section"><h3>Reminders Now</h3></div>', unsafe_allow_html=True)
    current_time = datetime.now().strftime("%H:%M")
    reminders_now = tasks_df[tasks_df["Reminder"]==current_time]
    if not reminders_now.empty:
        st.dataframe(reminders_now)
    else:
        st.write("No reminders at this time.")

elif page == "Wellness Tracker":
    st.markdown('<div class="section"><h3> Wellness Tracker</h3></div>', unsafe_allow_html=True)

    st.subheader("Log Today’s Wellness")
    with st.form("wellness_form"):
        today = datetime.now().strftime("%Y-%m-%d")
        meal = st.text_input("What did you eat today?")
        mood = st.selectbox("How was your mood today?", ["Excellent", "Good", "Okay", "Bad", "Very Bad"])
        submitted = st.form_submit_button("Log Wellness")
        if submitted:
            new_entry = {"User": st.session_state.user, "Date": today, "Meal": meal, "Mood": mood}
            st.session_state.wellness_df = pd.concat([wellness_df, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Wellness data saved!")
            st.rerun()

    st.subheader("View Past Data")
    user_data = wellness_df[wellness_df["User"]==st.session_state.user]
    st.dataframe(user_data)

    if not user_data.empty:
        st.subheader("Mood Over Time")
        mood_mapping = {"Very Bad":1, "Bad":2, "Okay":3, "Good":4, "Excellent":5}
        user_data["Mood_Score"] = user_data["Mood"].map(mood_mapping)
        user_data["Date"] = pd.to_datetime(user_data["Date"])
        st.line_chart(user_data.set_index("Date")["Mood_Score"])

        import streamlit as st
from audiorecorder import audiorecorder


st.set_page_config(page_title="My Streamlit App", layout="wide")


st.write("Welcome! Use the voice recorder below to capture audio.")


st.subheader("Voice Recorder")

audio = audiorecorder("Start Recording", "Stop Recording")

# When recording is done
if len(audio) > 0:
    st.audio(audio.tobytes(), format="audio/wav")

    st.success("Recording captured!")

    # Save recording
    save_path = "recorded_audio.wav"
    with open(save_path, "wb") as f:
        f.write(audio.tobytes())

    st.info(f"Audio saved as **{save_path}**")

    # Add download button
    st.download_button(
        label="Download Recording",
        data=audio.tobytes(),
        file_name="recorded_audio.wav",
        mime="audio/wav"
    )



