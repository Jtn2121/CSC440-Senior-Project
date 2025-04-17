import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

WORK_START_HOUR = 9
WORK_END_HOUR = 17
WORK_HOURS_PER_DAY = WORK_END_HOUR - WORK_START_HOUR

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        return None

def is_weekend(date_obj):
    return date_obj.weekday() >= 5  # 5 = Saturday, 6 = Sunday

def next_work_day(date_obj):
    next_day = date_obj + timedelta(days=1)
    while is_weekend(next_day):
        next_day += timedelta(days=1)
    return next_day

def calculate_estimated_completion(start_dt, total_hours):
    current = start_dt
    hours_left = total_hours

    while hours_left > 0:
        if is_weekend(current):
            current = datetime.combine(next_work_day(current.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)
            continue

        end_of_day = current.replace(hour=WORK_END_HOUR, minute=0, second=0, microsecond=0)
        start_of_day = current.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)

        if current < start_of_day:
            current = start_of_day

        hours_available_today = min((end_of_day - current).total_seconds() / 3600, WORK_HOURS_PER_DAY)
        if hours_left <= hours_available_today:
            return current + timedelta(hours=hours_left)
        else:
            hours_left -= hours_available_today
            current = datetime.combine(next_work_day(current.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)

    return current

def handle_input():
    current_date = datetime.now()

    start_date_str = start_date_entry.get()
    end_date_str = end_date_entry.get()
    length_of_task_str = length_of_task_entry.get()
    calculated_length_str = calculated_length_entry.get()

    # Validate dates
    start_date = validate_date(start_date_str)
    end_date = validate_date(end_date_str)

    if not start_date:
        messagebox.showerror("Input Error", "Invalid Start Date. Use MM-DD-YYYY.")
        return
    if not end_date:
        messagebox.showerror("Input Error", "Invalid End Date. Use MM-DD-YYYY.")
        return
    if end_date < start_date:
        messagebox.showerror("Input Error", "End Date must be after Start Date.")
        return

    # Validate number inputs
    try:
        length_of_task = float(length_of_task_str)
    except ValueError:
        messagebox.showerror("Input Error", "Length of Task must be a number.")
        return

    try:
        calculated_length = float(calculated_length_str)
    except ValueError:
        messagebox.showerror("Input Error", "Calculated Length of Task must be a number.")
        return

    # Weighted average
    average_task_length = 0.25 * length_of_task + 0.75 * calculated_length

    # Adjust current time to 9AM if it's before workday, or 9AM next workday if after 5PM
    use_date = current_date
    if start_date.date() > current_date.date():
        use_date = start_date
    elif current_date.hour >= WORK_END_HOUR:
        use_date = datetime.combine(next_work_day(current_date.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)
    elif current_date.hour < WORK_START_HOUR:
        use_date = current_date.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)

    # Calculate hours available between current/start date and end date (excluding weekends)
    temp = use_date
    total_hours_remaining = 0
    while temp.date() <= end_date.date():
        if not is_weekend(temp):
            if temp.date() == use_date.date():
                # Partial day today
                end_of_day = temp.replace(hour=WORK_END_HOUR, minute=0)
                hours_today = max(0, (end_of_day - temp).total_seconds() / 3600)
            else:
                hours_today = WORK_HOURS_PER_DAY
            total_hours_remaining += hours_today
        temp += timedelta(days=1)
        temp = temp.replace(hour=WORK_START_HOUR, minute=0)

    buffer_hours = total_hours_remaining - average_task_length
    buffer_ratio = buffer_hours / average_task_length if average_task_length > 0 else 0

    # Determine risk
    if buffer_ratio >= 0.25:
        risk_text = "Low Risk"
        risk_color = "gold"
    elif 0.05 <= buffer_ratio < 0.25:
        risk_text = "Medium Risk"
        risk_color = "orange"
    else:
        risk_text = "High Risk"
        risk_color = "red"

    # Determine overdue severity
    if buffer_ratio < 0:
        overrun_text = "Severe Overrun"
        overrun_color = "red"
    elif -0.1 <= buffer_ratio < 0:
        overrun_text = "Moderate Overrun"
        overrun_color = "orange"
    elif -0.25 <= buffer_ratio < -0.1:
        overrun_text = "Minor Overrun"
        overrun_color = "yellow"
    else:
        overrun_text = "No Overrun"
        overrun_color = "green"

    # Estimated completion time
    estimated_completion = calculate_estimated_completion(use_date, average_task_length)

    # Time left after completion (only on end date)
    remaining_hours_after_completion = 0
    temp = estimated_completion
    while temp.date() <= end_date.date():
        if not is_weekend(temp):
            if temp.date() == estimated_completion.date():
                end_of_day = temp.replace(hour=WORK_END_HOUR, minute=0)
                remaining = max(0, (end_of_day - temp).total_seconds() / 3600)
            else:
                remaining = WORK_HOURS_PER_DAY
            remaining_hours_after_completion += remaining
        temp += timedelta(days=1)
        temp = temp.replace(hour=WORK_START_HOUR, minute=0)

    # Update UI
    output_label.config(
        text=f"Task Length: {round(average_task_length, 2)} hrs",
        fg="white", bg="black"
    )
    estimate_label.config(
        text=f"Estimated Completion: {estimated_completion.strftime('%m-%d-%Y %I:%M %p')}\nTime Left After Completion: {int(remaining_hours_after_completion)} hrs",
        fg="white", bg="black"
    )
    risk_label.config(
        text=f"{risk_text} - {overrun_text}", fg=risk_color, bg="black"
    )

# GUI setup
root = tk.Tk()
root.title("Risk Assessment")

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

# Labels and Entry fields
labels = [
    ("Start Date (MM-DD-YYYY):", 0, 0),
    ("End Date (MM-DD-YYYY):", 0, 2),
    ("Length of Task (Hours):", 1, 0),
    ("Calculated Length (Hours):", 1, 2)
]
entries = {}

for text, row, col in labels:
    tk.Label(input_frame, text=text).grid(row=row, column=col, sticky="e", padx=5, pady=5)
    entry = tk.Entry(input_frame)
    entry.grid(row=row, column=col + 1, padx=5, pady=5)
    entries[text] = entry

start_date_entry = entries["Start Date (MM-DD-YYYY):"]
end_date_entry = entries["End Date (MM-DD-YYYY):"]
length_of_task_entry = entries["Length of Task (Hours):"]
calculated_length_entry = entries["Calculated Length (Hours):"]

# Submit button
tk.Button(root, text="Submit", command=handle_input).pack(pady=10)

# Output labels
output_label = tk.Label(root, text="", fg="white", bg="black", width=60, height=2)
output_label.pack(pady=5)

estimate_label = tk.Label(root, text="", fg="white", bg="black", width=60, height=3)
estimate_label.pack(pady=5)

risk_label = tk.Label(root, text="", fg="black", bg="black", width=60, height=2)
risk_label.pack(pady=5)

root.mainloop()
