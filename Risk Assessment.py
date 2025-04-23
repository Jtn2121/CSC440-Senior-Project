import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Constants
WORK_START_HOUR = 9
WORK_END_HOUR = 17
WORK_HOURS_PER_DAY = WORK_END_HOUR - WORK_START_HOUR


def validate_date(date_str):
    """Validate date string in MM-DD-YYYY format."""
    try:
        return datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        return None


def is_weekend(date_obj):
    """Check if date falls on a weekend."""
    return date_obj.weekday() >= 5


def next_work_day(date_obj):
    """Get the next working day (skips weekends)."""
    next_day = date_obj + timedelta(days=1)
    while is_weekend(next_day):
        next_day += timedelta(days=1)
    return next_day


def calculate_estimated_completion(start_dt, total_hours):
    """Calculate when a task will be completed based on working hours."""
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

        hours_left -= hours_available_today
        current = datetime.combine(next_work_day(current.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)

    return current


def calculate_available_hours(start_dt, end_dt):
    """Calculate total available working hours between two dates."""
    total_hours = 0
    current_day = start_dt.date()
    end_day = end_dt.date()

    while current_day <= end_day:
        if not is_weekend(current_day):
            if current_day == start_dt.date():
                # First day - calculate remaining hours
                start_time = max(start_dt, start_dt.replace(hour=WORK_START_HOUR, minute=0, second=0))
                end_time = start_dt.replace(hour=WORK_END_HOUR, minute=0, second=0)
                if start_time < end_time:
                    total_hours += (end_time - start_time).total_seconds() / 3600
            else:
                # Full workday
                total_hours += WORK_HOURS_PER_DAY
        current_day += timedelta(days=1)

    return total_hours


def calculate_overrun_hours(completion_time, deadline):
    """Calculate how many working hours the task overruns the deadline."""
    if completion_time.date() <= deadline.date():
        return 0

    overrun_start = deadline.replace(hour=WORK_START_HOUR)
    overrun_end = completion_time

    # If completion is after work hours on deadline day, start counting from next day
    if completion_time.date() == deadline.date():
        if completion_time.hour >= WORK_END_HOUR:
            overrun_start = datetime.combine(next_work_day(deadline.date()), datetime.min.time()).replace(
                hour=WORK_START_HOUR)
        else:
            overrun_start = deadline  # If completing during work hours on deadline day

    return calculate_available_hours(overrun_start, overrun_end)


def determine_risk_and_overrun(task_hours, available_hours, overrun_hours):
    """
    Determine both risk and overrun levels:
    - Risk based on % of available time needed
    - Overrun based on hours past deadline
    """
    # Risk assessment
    if available_hours <= 0:
        risk_text = "No Time Available"
        risk_color = "red"
    else:
        percentage = (task_hours / available_hours) * 100
        if percentage <= 50:
            risk_text = f"Low Risk ({percentage:.1f}% of time needed)"
            risk_color = "green"
        elif percentage <= 75:
            risk_text = f"Medium Risk ({percentage:.1f}% of time needed)"
            risk_color = "orange"
        else:
            risk_text = f"High Risk ({percentage:.1f}% of time needed)"
            risk_color = "red"

    # Overrun assessment
    if overrun_hours <= 0:
        overrun_text = "No Overrun"
        overrun_color = "green"
    elif overrun_hours <= 2:
        overrun_text = f"Low Overrun (+{overrun_hours:.1f} hrs)"
        overrun_color = "gold"
    elif overrun_hours <= 4:
        overrun_text = f"Medium Overrun (+{overrun_hours:.1f} hrs)"
        overrun_color = "orange"
    else:
        overrun_text = f"High Overrun (+{overrun_hours:.1f} hrs)"
        overrun_color = "red"

    return risk_text, risk_color, overrun_text, overrun_color


def handle_input():
    """Handle user input and perform calculations."""
    try:
        current_date = datetime.now()
        start_date = validate_date(start_date_entry.get())
        end_date_str = end_date_entry.get().strip()
        length_of_task = float(length_of_task_entry.get())
        calculated_length = float(calculated_length_entry.get())

        if not start_date:
            raise ValueError("Invalid Start Date. Use MM-DD-YYYY.")

        na_mode = end_date_str.lower() == "n/a"

        if not na_mode:
            end_date = validate_date(end_date_str)
            if not end_date:
                raise ValueError("Invalid End Date. Use MM-DD-YYYY or 'N/A'.")
            if end_date < start_date:
                raise ValueError("End Date must be after Start Date.")

        average_task_length = 0.25 * length_of_task + 0.75 * calculated_length
        output_label.config(text=f"Task Length: {round(average_task_length, 2)} hrs", fg="white", bg="black")

        use_date = current_date
        if start_date.date() > current_date.date():
            use_date = start_date
        elif current_date.hour >= WORK_END_HOUR:
            use_date = datetime.combine(next_work_day(current_date.date()), datetime.min.time()).replace(
                hour=WORK_START_HOUR)
        elif current_date.hour < WORK_START_HOUR:
            use_date = current_date.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)

        estimated_completion = calculate_estimated_completion(use_date, average_task_length)

        if na_mode:
            estimate_label.config(
                text=f"Estimated Completion: {estimated_completion.strftime('%m-%d-%Y %I:%M %p')}\n"
                     f"End date is N/A — risk/overrun cannot be calculated.",
                fg="white", bg="black"
            )
            risk_label.config(text="N/A", fg="gray", bg="black")
            overrun_label.config(text="N/A", fg="gray", bg="black")
        else:
            total_hours_available = calculate_available_hours(use_date, end_date)
            remaining_hours_after_completion = calculate_available_hours(estimated_completion, end_date)
            overrun_hours = calculate_overrun_hours(estimated_completion, end_date)

            risk_text, risk_color, overrun_text, overrun_color = determine_risk_and_overrun(
                average_task_length, total_hours_available, overrun_hours
            )

            estimate_label.config(
                text=f"Estimated Completion: {estimated_completion.strftime('%m-%d-%Y %I:%M %p')}\n"
                     f"Total Available Hours: {total_hours_available:.1f} hrs\n"
                     f"Time Left After Completion: {remaining_hours_after_completion:.1f} hrs",
                fg="white", bg="black"
            )
            risk_label.config(text=risk_text, fg=risk_color, bg="black")
            overrun_label.config(text=overrun_text, fg=overrun_color, bg="black")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


# GUI setup
root = tk.Tk()
root.title("Risk Assessment")
root.configure(bg="black")

input_frame = tk.Frame(root, bg="black")
input_frame.pack(padx=10, pady=10)

fields = [
    ("Start Date (MM-DD-YYYY):", 0, 0),
    ("End Date (MM-DD-YYYY or N/A):", 0, 2),
    ("Length of Task (Hours):", 1, 0),
    ("Calculated Length (Hours):", 1, 2)
]

entries = {}
for text, row, col in fields:
    tk.Label(input_frame, text=text, bg="black", fg="white").grid(row=row, column=col, sticky="e", padx=5, pady=5)
    entry = tk.Entry(input_frame)
    entry.grid(row=row, column=col + 1, padx=5, pady=5)
    entries[text] = entry

start_date_entry = entries["Start Date (MM-DD-YYYY):"]
end_date_entry = entries["End Date (MM-DD-YYYY or N/A):"]
length_of_task_entry = entries["Length of Task (Hours):"]
calculated_length_entry = entries["Calculated Length (Hours):"]

tk.Button(root, text="Submit", command=handle_input, bg="gray", fg="white").pack(pady=10)

output_label = tk.Label(root, text="", fg="white", bg="black", width=60, height=2)
output_label.pack(pady=5)

estimate_label = tk.Label(root, text="", fg="white", bg="black", width=60, height=3)
estimate_label.pack(pady=5)

risk_label = tk.Label(root, text="", fg="white", bg="black", width=60, height=2, font=("Arial", 10, "bold"))
risk_label.pack(pady=5)

overrun_label = tk.Label(root, text="", fg="white", bg="black", width=60, height=2, font=("Arial", 10, "bold"))
overrun_label.pack(pady=5)

root.mainloop()