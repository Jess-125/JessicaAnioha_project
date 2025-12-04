import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import base64
import os
 

# Create audio folder if it doesn't exist
AUDIO_FOLDER = "audio"
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# Create data folder if it doesn't exist
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

TASKS_FILE = os.path.join(DATA_FOLDER, "tasks.csv")
WELLNESS_FILE = os.path.join(DATA_FOLDER, "wellness.csv")

if "tasks_df" not in st.session_state:
    # Load from CSV if exists, otherwise create empty dataframe
    if os.path.exists(TASKS_FILE):
        st.session_state.tasks_df = pd.read_csv(TASKS_FILE)
    else:
        st.session_state.tasks_df = pd.DataFrame(columns=["User","Role","Task","Reminder","Status","ID"])
if "wellness_df" not in st.session_state:
    # Load from CSV if exists, otherwise create empty dataframe
    if os.path.exists(WELLNESS_FILE):
        st.session_state.wellness_df = pd.read_csv(WELLNESS_FILE)
    else:
        st.session_state.wellness_df = pd.DataFrame(columns=["User","Date","Meal","Mood","AudioNote"])
if "audio_recordings" not in st.session_state:
    st.session_state.audio_recordings = {}
if "current_audio_id" not in st.session_state:
    st.session_state.current_audio_id = None
if "latest_audio_data" not in st.session_state:
    st.session_state.latest_audio_data = None


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
            # Save to CSV
            st.session_state.tasks_df.to_csv(TASKS_FILE, index=False)
            st.success(f"Task '{task_name}' added for {user}")
            st.rerun()

elif page == "Pending Tasks":
    st.markdown('<div class="section"><h3>Pending Tasks</h3></div>', unsafe_allow_html=True)
    pending_df = tasks_df[tasks_df["Status"]=="Pending"]
    
    if not pending_df.empty:
        for idx, row in pending_df.iterrows():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"**{row['Task']}**")
            with col2:
                st.write(f"👤 {row['User']}")
            with col3:
                st.write(f"⏰ {row['Reminder']}")
            with col4:
                if st.button("✅", key=f"complete_{row['ID']}", help="Mark as completed"):
                    tasks_df.at[idx, "Status"] = "Completed"
                    st.session_state.tasks_df = tasks_df
                    # Save to CSV
                    st.session_state.tasks_df.to_csv(TASKS_FILE, index=False)
                    st.success("Task completed!")
                    st.rerun()
            st.divider()
    else:
        st.info("No pending tasks.")

elif page == "Reminders":
    st.markdown('<div class="section"><h3>Reminders</h3></div>', unsafe_allow_html=True)
    st.dataframe(tasks_df[["User", "Task", "Reminder", "Status"]])

elif page == "Wellness Tracker":
    st.markdown('<div class="section"><h3> Wellness Tracker</h3></div>', unsafe_allow_html=True)

    st.subheader("Log Today's Wellness")
    st.write("Record your daily wellness information including meals, mood, and optional audio notes.")
    
    # Use a unique key that includes a counter to force widget reset
    if 'audio_widget_key' not in st.session_state:
        st.session_state.audio_widget_key = 0
    
    # Store form inputs in session state
    if 'form_meal' not in st.session_state:
        st.session_state.form_meal = ""
    if 'form_mood' not in st.session_state:
        st.session_state.form_mood = "Excellent"
    
    # Form inputs
    meal = st.text_input("What did you eat today?", value=st.session_state.form_meal, key="meal_input")
    mood = st.selectbox("How was your mood today?", ["Excellent", "Good", "Okay", "Bad", "Very Bad"], 
                        index=["Excellent", "Good", "Okay", "Bad", "Very Bad"].index(st.session_state.form_mood), key="mood_input")
    
    # Audio recorder positioned after mood input
    audio_bytes = st.audio_input("Record your wellness audio note (optional)", key=f"wellness_audio_recorder_{st.session_state.audio_widget_key}")
    
    # Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📎 Log Wellness"):
            today = datetime.now().strftime("%Y-%m-%d")
            # Save wellness entry
            if audio_bytes is not None:
                # Save audio file
                timestamp = int(datetime.now().timestamp() * 1000)
                filename = f"wellness_{st.session_state.user}_{today}_{timestamp}.wav"
                filepath = os.path.join(AUDIO_FOLDER, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(audio_bytes.getvalue())
                
                new_entry = {"User": st.session_state.user, "Date": today, "Meal": meal, "Mood": mood, "AudioNote": filename}
                st.session_state.wellness_df = pd.concat([wellness_df, pd.DataFrame([new_entry])], ignore_index=True)
                # Save to CSV
                st.session_state.wellness_df.to_csv(WELLNESS_FILE, index=False)
                st.success(f"✅ Wellness data and audio saved!")
                # Increment key to reset the audio widget
                st.session_state.audio_widget_key += 1
            else:
                # Save without audio
                new_entry = {"User": st.session_state.user, "Date": today, "Meal": meal, "Mood": mood, "AudioNote": ""}
                st.session_state.wellness_df = pd.concat([wellness_df, pd.DataFrame([new_entry])], ignore_index=True)
                # Save to CSV
                st.session_state.wellness_df.to_csv(WELLNESS_FILE, index=False)
                st.success("Wellness data saved!")
            
            # Clear form
            st.session_state.form_meal = ""
            st.session_state.form_mood = "Excellent"
            st.session_state.current_audio_id = None
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Recording"):
            st.session_state.current_audio_id = None
            st.session_state.latest_audio_data = None
            # Increment key to reset the audio widget
            st.session_state.audio_widget_key += 1
            st.rerun()

    st.subheader("View Past Data")
    user_data = wellness_df[wellness_df["User"]==st.session_state.user]
    if not user_data.empty:
        # Header row with 4 columns
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
        with col1:
            st.write("**Date**")
        with col2:
            st.write("**Meal**")
        with col3:
            st.write("**Mood**")
        with col4:
            st.write("**Play**")
        st.divider()
        
        # Display each entry
        for idx, row in user_data.iterrows():
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
            
            with col1:
                st.write(row['Date'])
            with col2:
                st.write(row['Meal'])
            with col3:
                st.write(row['Mood'])
            with col4:
                if row['AudioNote']:
                    audio_file = row['AudioNote']
                    audio_path = os.path.join(AUDIO_FOLDER, audio_file)
                    
                    if os.path.exists(audio_path):
                        # Create play button that plays audio inline
                        play_button_key = f"play_{idx}"
                        if st.button("▶️", key=play_button_key, help="Play audio"):
                            # Load and play audio
                            with open(audio_path, 'rb') as f:
                                audio_bytes_data = f.read()
                            audio_base64 = base64.b64encode(audio_bytes_data).decode()
                            
                            # Auto-playing audio without controls
                            play_html = f"""
                            <audio id="audio_{idx}" autoplay>
                                <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                            </audio>
                            """
                            st.markdown(play_html, unsafe_allow_html=True)
                    else:
                        st.caption("⚠️")
                else:
                    st.write("")
            
            st.divider()
    else:
        st.info("No wellness data recorded yet.")

    if not user_data.empty:
        st.subheader("Mood Over Time")
        mood_mapping = {"Very Bad":1, "Bad":2, "Okay":3, "Good":4, "Excellent":5}
        user_data["Mood_Score"] = user_data["Mood"].map(mood_mapping)
        user_data["Date"] = pd.to_datetime(user_data["Date"])
        st.line_chart(user_data.set_index("Date")["Mood_Score"])

