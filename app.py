
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime
import csv
import os

# Daily Water Goal
daily_goal = 2000

total_water = 0

# History CSV File
history_file = "water_history.csv"

history = []


# Load Previous History
def load_history():
    global history, total_water

    if os.path.exists(history_file):

        with open(history_file, "r", newline="") as file:

            reader = csv.DictReader(file)

            for record in reader:

                # Support Old History Files
                if not record.get("Amount_ml"):
                    record["Amount_ml"] = str(
                        int(record.get("Glasses", 1)) * 200
                    )

                history.append({
                    "Date": record["Date"],
                    "Time": record["Time"],
                    "Day": record["Day"],
                    "Month": record["Month"],
                    "Year": record["Year"],
                    "Amount_ml": record["Amount_ml"]
                })

    # Calculate Today's Water Intake
    today = datetime.now().strftime("%Y-%m-%d")

    total_water = sum(
        int(record["Amount_ml"])
        for record in history
        if record["Date"] == today
    )


# Save History
def save_history():

    with open(history_file, "w", newline="") as file:

        fieldnames = [
            "Date",
            "Time",
            "Day",
            "Month",
            "Year",
            "Amount_ml"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(history)


# Hydration Greeting Function
def update_greeting():

    percentage = (total_water / daily_goal) * 100

    if total_water == 0:
        message = "Time to drink some water!"

    elif percentage < 25:
        message = "Keep drinking water!"

    elif percentage < 50:
        message = "Great start! Keep it up!"

    elif percentage < 75:
        message = "You're doing great! Stay hydrated!"

    elif percentage < 100:
        message = "Almost there! Keep going!"

    else:
        message = "Amazing! Daily goal completed!"

    greeting_label.config(text=message)


# Update Progress
def update_progress():

    remaining = max(daily_goal - total_water, 0)

    label.config(
        text=f"Total Water: {total_water} ml"
    )

    if remaining > 0:
        remaining_label.config(
            text=f"Remaining: {remaining} ml"
        )
    else:
        remaining_label.config(
            text="Daily Goal Completed!"
        )

    # Calculate Percentage
    percentage = min(
        (total_water / daily_goal) * 100, 100
    )

    # Update Circular Progress
    circle.delete("progress")

    circle.create_arc(
        20, 20, 180, 180,
        start=90,
        extent=-(percentage * 3.6),
        style="arc",
        outline="#2196F3",
        width=12,
        tags="progress"
    )

    # Update Percentage
    circle.itemconfig(
        percentage_text,
        text=f"{percentage:.0f}%"
    )

    circle.itemconfig(
        center_text,
        text=f"{total_water}/{daily_goal} ml"
    )

    # Update Greeting
    update_greeting()


# Add Water Function
def add_water():

    global total_water

    # Get Selected Water Size
    amount = int(
        size_var.get().replace(" ml", "")
    )

    total_water += amount

    # Get Current Date and Time
    now = datetime.now()

    # Create History Record
    record = {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%I:%M:%S %p"),
        "Day": now.strftime("%A"),
        "Month": now.strftime("%B"),
        "Year": now.strftime("%Y"),
        "Amount_ml": str(amount)
    }

    history.append(record)

    save_history()
    update_progress()


# Remove Latest Water Intake
def remove_water():

    global total_water

    today = datetime.now().strftime("%Y-%m-%d")

    # Find Latest Entry For Today
    for record in reversed(history):

        if record["Date"] == today:

            amount = int(record["Amount_ml"])

            total_water -= amount

            history.remove(record)

            save_history()
            break

    update_progress()


# Reset Today's Water Intake
def reset_water():

    global total_water, history

    today = datetime.now().strftime("%Y-%m-%d")

    # Preserve Previous Days' History
    history = [
        record for record in history
        if record["Date"] != today
    ]

    total_water = 0

    save_history()
    update_progress()


# Water Intake History Window
def show_history():

    history_window = tk.Toplevel(root)

    history_window.title("Water Intake History")
    history_window.geometry("900x450")
    history_window.config(bg="lightblue")

    # Heading
    history_heading = tk.Label(
        history_window,
        text="WATER INTAKE HISTORY",
        font=("Arial", 20, "bold"),
        bg="lightblue",
        fg="blue"
    )
    history_heading.pack(pady=15)

    # Table Frame
    table_frame = tk.Frame(history_window)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    scrollbar.pack(side="right", fill="y")

    # Table Columns
    columns = (
        "Date",
        "Time",
        "Day",
        "Month",
        "Year",
        "Amount"
    )

    history_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(
        command=history_table.yview
    )

    # Table Headings
    for column in columns:

        history_table.heading(
            column,
            text=column
        )

    # Column Widths
    history_table.column("Date", width=110)
    history_table.column("Time", width=120)
    history_table.column("Day", width=110)
    history_table.column("Month", width=110)
    history_table.column("Year", width=80)
    history_table.column("Amount", width=110)

    history_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Display Latest Records First
    for record in reversed(history):

        history_table.insert(
            "",
            "end",
            values=(
                record["Date"],
                record["Time"],
                record["Day"],
                record["Month"],
                record["Year"],
                record["Amount_ml"] + " ml"
            )
        )

    # Total History Entries
    total_label = tk.Label(
        history_window,
        text=f"Total Intake Entries: {len(history)}",
        font=("Arial", 13, "bold"),
        bg="lightblue",
        fg="blue"
    )

    total_label.pack(pady=10)


# Main Window
root = tk.Tk()

root.title("Water Intake Tracker")
root.geometry("500x850")
root.config(bg="lightblue")


# Heading
heading = tk.Label(
    root,
    text="WATER INTAKE TRACKER",
    font=("Arial", 20, "bold"),
    bg="lightblue",
    fg="blue"
)

heading.pack(pady=15)


# Water Counter
label = tk.Label(
    root,
    text="Total Water: 0 ml",
    font=("Arial", 16),
    bg="lightblue"
)

label.pack(pady=5)


# Remaining Water
remaining_label = tk.Label(
    root,
    text=f"Remaining: {daily_goal} ml",
    font=("Arial", 14),
    bg="lightblue"
)

remaining_label.pack(pady=5)


# Hydration Greeting Label
greeting_label = tk.Label(
    root,
    text="Time to drink some water!",
    font=("Arial", 13, "bold"),
    bg="lightblue",
    fg="#1565C0"
)

greeting_label.pack(pady=10)


# Circular Progress
circle = tk.Canvas(
    root,
    width=200,
    height=200,
    bg="lightblue",
    highlightthickness=0
)

circle.pack(pady=5)


# Background Circle
circle.create_oval(
    20, 20, 180, 180,
    outline="#D0E8F5",
    width=12
)


# Progress Circle
circle.create_arc(
    20, 20, 180, 180,
    start=90,
    extent=0,
    style="arc",
    outline="#2196F3",
    width=12,
    tags="progress"
)


# Percentage Text
percentage_text = circle.create_text(
    100, 85,
    text="0%",
    font=("Arial", 25, "bold"),
    fill="#1565C0"
)


# Center Text
center_text = circle.create_text(
    100, 120,
    text="0/2000 ml",
    font=("Arial", 11),
    fill="#455A64"
)


# Water Size Selection
size_label = tk.Label(
    root,
    text="Select Water Size:",
    font=("Arial", 13, "bold"),
    bg="lightblue",
    fg="#1565C0"
)

size_label.pack(pady=5)


# Dropdown Menu
size_var = tk.StringVar()

size_dropdown = ttk.Combobox(
    root,
    textvariable=size_var,
    values=[
        "150 ml",
        "200 ml",
        "250 ml",
        "300 ml",
        "500 ml"
    ],
    state="readonly",
    font=("Arial", 12),
    width=15
)

size_dropdown.set("200 ml")
size_dropdown.pack(pady=5)


# Add Water Button
button = tk.Button(
    root,
    text="Add Water",
    font=("Arial", 12, "bold"),
    command=add_water,
    bg="green",
    fg="white",
    width=15
)

button.pack(pady=6)


# Remove Water Button
remove_button = tk.Button(
    root,
    text="Remove Water",
    font=("Arial", 12, "bold"),
    command=remove_water,
    bg="orange",
    fg="white",
    width=15
)

remove_button.pack(pady=6)


# Reset Button
reset_button = tk.Button(
    root,
    text="Reset",
    font=("Arial", 12, "bold"),
    command=reset_water,
    bg="red",
    fg="white",
    width=15
)

reset_button.pack(pady=6)


# History Button
history_button = tk.Button(
    root,
    text="View Water History",
    font=("Arial", 12, "bold"),
    command=show_history,
    bg="#1565C0",
    fg="white",
    width=20
)

history_button.pack(pady=8)


# 3D Water Glass
glass = tk.Canvas(
    root,
    width=200,
    height=230,
    bg="lightblue",
    highlightthickness=0
)

glass.pack(pady=5)


# Glass Shadow
glass.create_oval(
    43, 185, 157, 205,
    fill="#9BB9C9",
    outline=""
)


# Glass Body
glass.create_polygon(
    40, 25,
    160, 25,
    140, 185,
    60, 185,
    fill="#EAF8FF",
    outline="#607D8B",
    width=3
)


# Water Inside Glass
glass.create_polygon(
    47, 100,
    153, 100,
    137, 180,
    63, 180,
    fill="#45BDEB",
    outline=""
)


# Water Surface
glass.create_oval(
    47, 91, 153, 109,
    fill="#70D5F5",
    outline="#249CCB",
    width=2
)


# Left Glass Reflection
glass.create_polygon(
    49, 32,
    60, 32,
    69, 177,
    62, 177,
    fill="#FFFFFF",
    outline=""
)


# Right Glass Shading
glass.create_polygon(
    139, 32,
    151, 32,
    134, 177,
    127, 177,
    fill="#A5D8EB",
    outline=""
)


# Glass Rim
glass.create_oval(
    39, 18, 161, 34,
    fill="#F8FDFF",
    outline="#607D8B",
    width=3
)


# Inner Rim
glass.create_oval(
    45, 22, 155, 31,
    outline="#B7DCEB",
    width=2
)


# Bottom Shine
glass.create_arc(
    59, 174, 141, 194,
    start=190,
    extent=160,
    style="arc",
    outline="white",
    width=3
)


# Load Previous History
load_history()

# Initialize Progress and Greeting
update_progress()


# Keep Application Running
root.mainloop()
