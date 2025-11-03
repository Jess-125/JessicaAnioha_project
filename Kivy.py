# memory_aid_kivy.py
"""
Cognitive Wellness & Memory Aid App (Kivy prototype)
- Single-file Kivy app.
- Storage: CSV file 'tasks.csv' with columns:
  id,user,title,description,reminder_time_iso,notified
- Date/time format for reminder entry: "YYYY-MM-DD HH:MM" (24-hour)
"""

import csv
import os
import uuid
from datetime import datetime
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

CSV_FILE = "tasks.csv"
USERS = ["Grace", "Samuel", "Linda"]  # default users; you can edit or extend


KV = r"""
<MainUI>:
    orientation: "vertical"
    padding: 12
    spacing: 10

    BoxLayout:
        size_hint_y: None
        height: "40dp"
        spacing: 8

        Label:
            text: "Selected user:"
            size_hint_x: None
            width: "110dp"
            halign: "left"
            valign: "middle"
            text_size: self.size

        Spinner:
            id: user_spinner
            text: root.current_user
            values: root.users
            size_hint_x: None
            width: "160dp"
            on_text: root.set_user(self.text)

        Button:
            text: "Refresh tasks"
            on_release: root.load_tasks()

        Button:
            text: "Add task"
            on_release: root.open_add_task()

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "34dp"
        spacing: 6

        Label:
            text: "Filter (search title):"
            size_hint_x: None
            width: "160dp"
            halign: "left"
            valign: "middle"
            text_size: self.size

        TextInput:
            id: filter_input
            multiline: False
            on_text: root.apply_filter(self.text)

        Button:
            text: "Clear filter"
            size_hint_x: None
            width: "100dp"
            on_release:
                filter_input.text = ""
                root.apply_filter("")

    Label:
        text: "Tasks (upcoming first). Click a task to delete it."
        size_hint_y: None
        height: "24dp"

    ScrollView:
        GridLayout:
            id: tasks_grid
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            row_default_height: "70dp"
            row_force_default: True
            spacing: 6
            padding: [0,6,0,6]

<TaskCard@Button>:
    task_id: ""
    orientation: "vertical"
    text_size: self.width - 20, None
    halign: "left"
    valign: "middle"
    size_hint_y: None
    height: "70dp"
    background_normal: ''
    background_color: (0.95,0.95,1,1) if not self.task_id else (1,1,1,1)

<AddTaskForm>:
    orientation: "vertical"
    padding: 12
    spacing: 8
    size_hint: None, None
    width: root.form_width
    height: "320dp"

    Label:
        text: "Add new task"
        size_hint_y: None
        height: "28dp"
        bold: True

    GridLayout:
        cols: 2
        row_force_default: True
        row_default_height: "36dp"
        spacing: 6

        Label:
            text: "User:"
            size_hint_x: None
            width: "90dp"
            halign: "left"
            valign: "middle"
            text_size: self.size
        Spinner:
            id: add_user
            text: root.default_user
            values: root.users

        Label:
            text: "Title:"
            halign: "left"
            valign: "middle"
            text_size: self.size
        TextInput:
            id: add_title
            multiline: False

        Label:
            text: "Reminder (YYYY-MM-DD HH:MM):"
            halign: "left"
            valign: "middle"
            text_size: self.size
        TextInput:
            id: add_time
            multiline: False

        Label:
            text: "Description:"
            halign: "left"
            valign: "top"
            text_size: self.size
        TextInput:
            id: add_desc
            multiline: True
            height: "80dp"

    BoxLayout:
        size_hint_y: None
        height: "42dp"
        spacing: 6

        Button:
            text: "Add"
            on_release: root.add_task()
        Button:
            text: "Cancel"
            on_release: root.cancel()
"""


class Task:
    def __init__(self, id_, user, title, description, reminder_time_iso, notified=False):
        self.id = id_
        self.user = user
        self.title = title
        self.description = description
        # store ISO: 'YYYY-MM-DD HH:MM' -> parse as datetime
        self.reminder_time_iso = reminder_time_iso
        self.notified = bool(int(notified)) if isinstance(notified, (str, int)) else bool(notified)

    def reminder_dt(self):
        try:
            return datetime.strptime(self.reminder_time_iso, "%Y-%m-%d %H:%M")
        except Exception:
            return None

    def to_csv_row(self):
        return [self.id, self.user, self.title, self.description, self.reminder_time_iso, "1" if self.notified else "0"]


def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "user", "title", "description", "reminder_time_iso", "notified"])


def load_tasks_from_csv():
    ensure_csv_exists()
    tasks = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # allow missing notified column
            notified = row.get("notified", "0")
            t = Task(
                id_=row.get("id") or str(uuid.uuid4()),
                user=row.get("user", ""),
                title=row.get("title", ""),
                description=row.get("description", ""),
                reminder_time_iso=row.get("reminder_time_iso", ""),
                notified=notified,
            )
            tasks.append(t)
    return tasks


def save_all_tasks_to_csv(tasks):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "user", "title", "description", "reminder_time_iso", "notified"])
        for t in tasks:
            writer.writerow(t.to_csv_row())


class AddTaskForm(BoxLayout):
    form_width = 460
    users = ListProperty(USERS)
    default_user = StringProperty(USERS[0])

    def __init__(self, submit_callback, cancel_callback, **kwargs):
        super().__init__(**kwargs)
        self.submit_callback = submit_callback
        self.cancel_callback = cancel_callback

    def add_task(self):
        user = self.ids.add_user.text.strip()
        title = self.ids.add_title.text.strip()
        reminder_time = self.ids.add_time.text.strip()
        desc = self.ids.add_desc.text.strip()

        if not user or not title or not reminder_time:
            Popup(title="Error", content=BoxLayout().add_widget(Label(text="User, title, and time are required.")), size_hint=(None, None), size=(400, 200))
            # avoid raising: instead show a simple popup
            p = Popup(title="Error", size_hint=(None, None), size=(380, 140))
            p.content = BoxLayout()
            p.content.add_widget(Label(text="Please fill User, Title, and Reminder time."))
            p.open()
            return

        # validate time format
        try:
            dt = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        except Exception:
            p = Popup(title="Invalid time", size_hint=(None, None), size=(420, 140))
            p.content = BoxLayout()
            p.content.add_widget(Label(text="Time must be YYYY-MM-DD HH:MM (24-hour)."))
            p.open()
            return

        new_task = Task(id_=str(uuid.uuid4()), user=user, title=title, description=desc, reminder_time_iso=reminder_time, notified=False)
        self.submit_callback(new_task)
        self.cancel_callback()

    def cancel(self):
        self.cancel_callback()


class MainUI(BoxLayout):
    current_user = StringProperty(USERS[0])
    users = ListProperty(USERS)
    tasks = ListProperty([])
    filter_text = StringProperty("")
    running = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_tasks()
        # check reminders every 20 seconds
        Clock.schedule_interval(self.check_reminders, 20)

    def set_user(self, user):
        self.current_user = user
        self.apply_filter(self.ids.filter_input.text)

    def load_tasks(self):
        all_tasks = load_tasks_from_csv()
        # sort upcoming first
        def keyfunc(t):
            dt = t.reminder_dt()
            return dt or datetime.max
        all_tasks.sort(key=keyfunc)
        self.tasks = all_tasks
        self.build_task_list()

    def build_task_list(self):
        grid = self.ids.tasks_grid
        grid.clear_widgets()
        for t in self.tasks:
            # filter by current user and filter_text
            if t.user != self.current_user:
                continue
            if self.filter_text and self.filter_text.lower() not in t.title.lower():
                continue
            dt = t.reminder_dt()
            dt_str = dt.strftime("%Y-%m-%d %H:%M") if dt else "Invalid time"
            notified_str = "[NOTIFIED]" if t.notified else ""
            btn_text = f"{t.title}  —  {dt_str} {notified_str}\n{t.description or ''}"
            btn = Builder.template("TaskCard", task_id=t.id)
            # can't use Builder.template to set text easily; fallback to Button
            from kivy.uix.button import Button
            b = Button(text=btn_text, halign="left", valign="middle", text_size=(self.width-40, None),
                       size_hint_y=None, height="70dp")
            b.bind(on_release=partial(self.confirm_delete_task, t.id))
            grid.add_widget(b)

    def apply_filter(self, text):
        self.filter_text = text.strip()
        self.build_task_list()

    def open_add_task(self):
        form = AddTaskForm(submit_callback=self.add_task, cancel_callback=self.dismiss_add_popup)
        popup = Popup(title="Add Task", content=form, size_hint=(None, None), size=(500, 380))
        # attach to instance so we can dismiss later
        self._add_popup = popup
        popup.open()

    def dismiss_add_popup(self):
        if hasattr(self, "_add_popup"):
            self._add_popup.dismiss()
            delattr(self, "_add_popup")
        self.load_tasks()

    def add_task(self, task: Task):
        # append to CSV (load all, append, save to keep format consistent)
        tasks = load_tasks_from_csv()
        tasks.append(task)
        save_all_tasks_to_csv(tasks)
        self.load_tasks()

    def confirm_delete_task(self, task_id, *args):
        content = BoxLayout(orientation="vertical", spacing=8)
        content.add_widget(Label(text="Delete this task? This is permanent."))
        btns = BoxLayout(size_hint_y=None, height="40dp", spacing=8)
        from kivy.uix.button import Button

        popup = Popup(title="Confirm delete", content=content, size_hint=(None, None), size=(380, 160))
        btn_yes = Button(text="Delete")
        btn_no = Button(text="Cancel")
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        content.add_widget(btns)

        btn_yes.bind(on_release=lambda *_: (self.delete_task(task_id), popup.dismiss()))
        btn_no.bind(on_release=popup.dismiss)
        popup.open()

    def delete_task(self, task_id):
        tasks = load_tasks_from_csv()
        tasks = [t for t in tasks if t.id != task_id]
        save_all_tasks_to_csv(tasks)
        self.load_tasks()

    def check_reminders(self, dt):
        now = datetime.now()
        tasks = load_tasks_from_csv()
        changed = False
        for t in tasks:
            if t.user != self.current_user:
                continue
            if t.notified:
                continue
            rdt = t.reminder_dt()
            if rdt and now >= rdt:
                # show popup
                title = f"Reminder for {t.user}: {t.title}"
                content = BoxLayout(orientation="vertical")
                content.add_widget(Label(text=f"{t.description or ''}\n\nScheduled: {t.reminder_time_iso}"))
                btn = BoxLayout(size_hint_y=None, height="40dp")
                from kivy.uix.button import Button
                ok = Button(text="OK")
                btn.add_widget(ok)
                content.add_widget(btn)
                popup = Popup(title=title, content=content, size_hint=(None, None), size=(420, 240))
                ok.bind(on_release=popup.dismiss)
                popup.open()
                # mark notified
                t.notified = True
                changed = True

        if changed:
            save_all_tasks_to_csv(tasks)
            self.load_tasks()


class MemoryAidApp(App):
    def build(self):
        ensure_csv_exists()
        Builder.load_string(KV)
        return MainUI()


if __name__ == "__main__":
    MemoryAidApp().run()
