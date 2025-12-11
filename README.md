# Cognitive Wellness & Memory Aid App
**User Guide**
***Overview**
A browser-based cognitive wellness and memory support app built with Streamlit. The app lets older adults and caregivers manage daily tasks, receive reminders, track wellness, and record short audio notes. Users interact with the system through a clean, guided web interface that runs locally on streamlit.

**Features:**
*****Reminders (scheduled, with snooze & complete actions)*****
*****Task creation & tracking*****
*****Dashboard view of pending/completed tasks*****
*****Daily wellness logging (meal + mood)*****
*****Mood trends visualization*****
*****Built-in voice recording*****
*****Multi-user support (Grace, Samuel, Linda)*****

**Table of Contents**
-1.Requirements
-2. Installation
-3. How to Run the App
-4. First time setup
-5. Using the App — Step-by-step Guide
-6. Audio Recording Feature
-7. Common Errors & Fixes
-8. Known Limitations

***1. Requirements**
-Python 3.9 or later (developed and tested with Python 3.10).
-A modern web browser (Chrome, Edge, Firefox, Safari).
-Git (optional, only if you prefer cloning the repository).​
-pip (Python package installer)

-Streamlit
-Pandas
-Pydub
-audiorecorder Streamlit component
-FFmpeg installed on your machine (for audio processing)

**2. Installation**
****2.1 Get the Project****
Option A – Clone (recommended)
bash
git clone https://github.com/your-username/cognitive-wellness-app.git
cd cognitive-wellness-app

Option B – Download ZIP
On GitHub, click Code → Download ZIP.
Extract the ZIP.
Open the extracted folder in your terminal/command prompt.

****2.2 Create and Activate a Virtual Environment*****
bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

****2.3 Install Dependencies****
bash
pip install -r requirements.txt

If requirements.txt is not present, create one with at least:
-text
-streamlit
-pandas
-pydub
-streamlit-audiorecorder

****2.4 Install FFmpeg (Required for Audio)****
pydub relies on FFmpeg to handle audio files.​
Windows
Download FFmpeg (static build) from the official site.
Extract it (e.g., to C:\ffmpeg).
Add C:\ffmpeg\bin to your system PATH.
Open a new terminal and verify:
bash

ffmpeg -version
macOS (Homebrew)
bash

brew install ffmpeg
ffmpeg -version
Ubuntu/Debian
bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version


**3. Running the App**
From the project folder, with the virtual environment activated:
bash
streamlit run app.py

Your browser will open at http://localhost:8501.
If it does not open, copy the URL shown in the terminal and paste it into your browser.​
To stop the app, press Ctrl + C in the terminal.

**4. First-Time Setup**
No API keys, accounts, or external databases are required.
All data (tasks and wellness logs) is stored temporarily in memory using st.session_state.
Data resets when:
The browser is refreshed.
The app server is stopped and restarted.
If in a future version API keys or external services are added, instructions for creating a keys.py or .env file will be added here with a clear example.

**5. Using the App**
****5.1 Login / Select Profile****
On the start page, locate “Login / Select Profile”.
Use the Select profile dropdown to choose:
Grace (elderly)
Samuel (caregiver)
Linda (elderly)
Click “Sign In”.
The sidebar will show: Signed in as <Name> (elderly/caregiver).
To switch users:
Click “Sign Out” in the sidebar.
Choose a different profile and sign in again.

You cannot proceed without selecting a user.

<img width="1600" height="859" alt="Screenshot (832)" src="https://github.com/user-attachments/assets/a2aee619-6c36-4882-810c-8994df0769db" />

<img width="1600" height="856" alt="Screenshot (834)" src="https://github.com/user-attachments/assets/780f8316-54c6-439a-bf1e-a7b673fd78b3" />


<img width="1600" height="859" alt="Screenshot (844)" src="https://github.com/user-attachments/assets/12e621e7-3d73-436f-8da1-7abad57ffca3" />

****5.2 Sidebar Navigation****
After signing in, the left sidebar displays the main menu:
Dashboard
All Tasks
Add Task
Pending Tasks
Reminders
Wellness Tracker
Sign out
Click a menu item to move between pages.

<img width="581" height="853" alt="Screenshot (835)" src="https://github.com/user-attachments/assets/d2ea4604-1e1b-4915-98dc-9a36b22ffb42" />

****5.3 Dashboard****
The Dashboard page gives an overview of tasks:
At the top, three buttons:
Total Tasks
Pending Tasks
Completed Tasks
Clicking a button changes the filter:
Total Tasks: shows all tasks.
Pending Tasks: shows only tasks not yet completed.
Completed Tasks: shows tasks that have been finished.
The table below updates automatically when you click a button.

<img width="1600" height="859" alt="Screenshot (844)" src="https://github.com/user-attachments/assets/7893d497-7af5-4966-a2b9-0b551b949ddc" />

****5.4 All Tasks****
The All Tasks page shows every task in a single table:
Columns:
User (Grace, Samuel, Linda)
Role (elderly / caregiver)
Task
Reminder (HH:MM)
Status (Pending / Completed)
ID (internal unique identifier)
Use this page to review all tasks at once.

<img width="1600" height="850" alt="Screenshot (836)" src="https://github.com/user-attachments/assets/61bd538d-6621-4214-80c3-f5c8862bdfa9" />

****5.5 Add Task****
Use Add Task to create new reminders:
Open Add Task from the sidebar.
Fill in the form:
Assign To: select Grace, Samuel, or Linda.
Task Name: short description (e.g., “Take evening medicine”).
Reminder Time (HH:MM): time in 24-hour format, such as 09:30 or 18:45.
Click “Add Task”.

<img width="1600" height="853" alt="Screenshot (842)" src="https://github.com/user-attachments/assets/8a58c837-e7bf-4688-999b-30afd994abe4" />

Behavior:
If the time is not in HH:MM format, the app shows:
“Invalid time format. Use HH:MM”.
If valid, the task is saved, a success message appears, and the page refreshes so you see the new entry in task tables.

<img width="1600" height="868" alt="Screenshot (843)" src="https://github.com/user-attachments/assets/9d036624-36c9-450f-85e2-406537af8584" />


****5.6 Pending Tasks****
The Pending Tasks page shows only tasks whose status is Pending:
Use this page to see everything that is still outstanding.
Once a task is marked Completed, it disappears from this list.

<img width="1600" height="859" alt="Screenshot (841)" src="https://github.com/user-attachments/assets/efb547a6-2d56-42d0-8f50-339a2576b0ba" />

****5.7 Reminders Page****
The Reminders page checks for tasks scheduled at the current time:
The app reads the system time in HH:MM format.
Any tasks whose Reminder matches the current time appear in a table.
If nothing is scheduled for the current minute, the page displays:
“No reminders at this time.”
****5.8 Reminder Pop-ups (Modals)****
The app actively checks tasks and shows pop-up reminders:
When the current time matches a task’s Reminder and its Status is Pending, a modal window appears with:
The task name.
The reminder time.
Two buttons:
Mark Completed
Snooze 5 min
Actions:
Mark Completed
Changes the task’s status to Completed.
Closes the popup and updates the task list.
Snooze 5 min
Adds 5 minutes to the reminder time.
Saves the new time and closes the popup.
Each reminder is only shown once for that time, to avoid repeated pop-ups.

****5.9 Wellness Tracker****
*****5.9.1 Logging Today’s Wellness*****
Go to Wellness Tracker.
Under “Log Today’s Wellness”:
What did you eat today?: write a short description of your meals.
How was your mood today?: select from:
Excellent
Good
Okay
Bad
Very Bad
Click “Log Wellness”.
The app:
Saves the entry with:
Current user
Today’s date
Meal text
Selected mood
Shows a confirmation and refreshes the page.

<img width="1600" height="900" alt="Screenshot (839)" src="https://github.com/user-attachments/assets/9244bbd6-0b88-4d2c-9a6f-9fbc2463cd13" />

*****5.9.2 Viewing Past Data and Mood Chart*****
Below the form:
View Past Data: shows a table of all logged entries for the signed-in user.
Mood Over Time:
A line chart appears if there is any previous data.
The app converts moods to scores:
Very Bad = 1
Bad = 2
Okay = 3
Good = 4
Excellent = 5
The x-axis is date; the y-axis is mood score.

<img width="1600" height="853" alt="Screenshot (840)" src="https://github.com/user-attachments/assets/952089bb-97fd-4b71-9fe7-ee4cb1cca26b" />


****5.10 Voice Recorder****
The app includes a simple Voice Recorder built with a Streamlit audio recording component.​
5.10.1 Using the Recorder
Scroll to the Voice Recorder section.
Click “Start Recording”.
Speak into your microphone.
Click “Stop Recording”.
After stopping:
The recording is played back in the app.
A file named recorded_audio.wav is saved in the project folder.
A Download Recording button lets you save the audio locally.
5.10.2 Browser Permissions
If you see no audio or cannot record, check that:
The browser prompted for microphone access.
You clicked Allow.
Microphone is enabled in system and browser privacy settings.

**6. Common Issues & Fixes**
Problem / Message
Likely Cause
What to Do

****6.1. Invalid time format. Use HH:MM****
Reminder not written as HH:MM
Enter a valid 24-hour time, e.g., 09:30 or 18:45.
****6.2. No reminder pop-ups at the expected time****
Time does not exactly match reminder time
Check your system clock and ensure reminder times are correct to the minute.
****6.3. No audio recorded or played back****
Microphone access blocked or not granted
Allow microphone permissions in the browser and reload the page.
****6.4. Audio export or pydub errors****
FFmpeg missing or not in PATH
Install FFmpeg and confirm ffmpeg -version works in your terminal. ​
****6.5. Page or data resets unexpectedly****
App restarted or browser reloaded
Remember that data is stored only in memory and is not persisted yet.
****6.6. FFmpeg not found****
Fix: install FFmpeg
Mac:
brew install ffmpeg
Mac:
brew install ffmpeg
Windows:
Download from ffmpeg.org
Add /bin to PATH


**7. Current Limitations**
No persistent storage
Tasks and wellness logs are stored in memory only and are lost when the app/server restarts.
Fixed demo profiles
Only three predefined users: Grace, Samuel, and Linda; no custom account creation.
Reminder precision
Reminders trigger only when the current time equals the reminder time to the minute.
Single recording file
Each new recording overwrites recorded_audio.wav in the project folder.
More advanced technical details (file structure, component APIs, extension ideas, known bugs) should be documented separately in the developer documentation, not in this user guide.

**
