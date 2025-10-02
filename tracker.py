import json
import os
import sys
from datetime import datetime

#creates tasks.json
DATA_FILE = "tasks.json"

# helper functions

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def days_since(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (datetime.today().date() - date).days

# core features

def add_task(name, frequency_days):
    tasks = load_tasks()
    tasks[name] = {
        "last_done": None,
        "frequency_days": frequency_days
    }
    save_tasks(tasks)
    print(f"✅ Added task: {name} (every {frequency_days} days)")

def mark_done(name):
    tasks = load_tasks()
    if name in tasks:
        tasks[name]["last_done"] = str(datetime.today().date())
        save_tasks(tasks)
        print(f"✨ Marked '{name}' as done today")
    else:
        print(f"⚠️ Task '{name}' not found")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks yet.")
        return

    print("\n📋 Task List:")
    for name, info in tasks.items():
        last = info["last_done"]
        freq = info["frequency_days"]

        if last:
            days = days_since(last)
            overdue = days - freq
            status = f"last done {days} days ago"
            if overdue >= 0:
                status += f" ⚠️ overdue by {overdue} days!"
        else:
            status = "never done"

        print(f" - {name} → {status}")

# CLI interface

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tracker.py add \"Task name\" <frequency_days>")
        print("  python tracker.py done \"Task name\"")
        print("  python tracker.py list")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) != 4:
            print("Usage: python tracker.py add \"Task name\" <frequency_days>")
            return
        name = sys.argv[2]
        freq = int(sys.argv[3])
        add_task(name, freq)

    elif command == "done":
        if len(sys.argv) != 3:
            print("Usage: python tracker.py done \"Task name\"")
            return
        name = sys.argv[2]
        mark_done(name)

    elif command == "list":
        list_tasks()

    else:
        print(f"⚠️ Unknown command: {command}")

if __name__ == "__main__":
    main()
