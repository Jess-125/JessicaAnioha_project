import pandas as pd
import os

def load_tasks(file='tasks.csv'):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=['User', 'Task', 'Status'])
        df.to_csv(file, index=False)
        return df

def save_tasks(df, file='tasks.csv'):
    df.to_csv(file, index=False)

def add_task(user, task, file='tasks.csv'):
    df = load_tasks(file)
    new_task = {'User': user, 'Task': task, 'Status': 'Pending'}
    df = df._append(new_task, ignore_index=True)
    save_tasks(df, file)
    print(f"Task added for {user}: {task}")

def view_tasks(user, file='tasks.csv'):
    df = load_tasks(file)
    print(df[df['User'] == user])

# Example test (hardcoded)
add_task('Grace', 'Take medication at 8 AM')
view_tasks('Grace')
