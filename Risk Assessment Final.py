import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Constants for workday hours
WORK_START_HOUR = 9
WORK_END_HOUR = 17
WORK_HOURS_PER_DAY = WORK_END_HOUR - WORK_START_HOUR


def validate_date(date_str):
    """Convert a string in MM-DD-YYYY format to a datetime object, or return None if invalid."""
    try:
        return datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        return None


def is_weekend(date_obj):
    """Return True if the given date is Saturday or Sunday."""
    return date_obj.weekday() >= 5


def next_work_day(date_obj):
    """Return the next weekday (skipping Saturday and Sunday)."""
    next_day = date_obj + timedelta(days=1)
    while is_weekend(next_day):
        next_day += timedelta(days=1)
    return next_day


def calculate_estimated_completion(start_dt, total_hours):
    """Estimate task completion datetime given a start datetime and total hours required."""
    current = start_dt
    hours_remaining = total_hours

    while hours_remaining > 0:
        if is_weekend(current):
            current = datetime.combine(next_work_day(current.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)
            continue

        end_of_day = current.replace(hour=WORK_END_HOUR, minute=0, second=0, microsecond=0)
        start_of_day = current.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)

        if current < start_of_day:
            current = start_of_day

        hours_available_today = min((end_of_day - current).total_seconds() / 3600, WORK_HOURS_PER_DAY)

        if hours_remaining <= hours_available_today:
            return current + timedelta(hours=hours_remaining)

        hours_remaining -= hours_available_today
        current = datetime.combine(next_work_day(current.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)

    return current


def calculate_available_hours(start_dt, end_dt):
    """Return total working hours between two date times, excluding weekends and outside work hours."""
    total = 0
    current_day = start_dt.date()
    final_day = end_dt.date()

    while current_day <= final_day:
        if not is_weekend(current_day):
            if current_day == start_dt.date():
                work_start = max(start_dt, start_dt.replace(hour=WORK_START_HOUR, minute=0, second=0))
                work_end = start_dt.replace(hour=WORK_END_HOUR, minute=0, second=0)
                if work_start < work_end:
                    total += (work_end - work_start).total_seconds() / 3600
            else:
                total += WORK_HOURS_PER_DAY
        current_day += timedelta(days=1)

    return total


def determine_risk_and_overrun(task_hours, available_hours):
    """
    Assess risk and overrun severity based on task time vs available work time.
    """
    if available_hours <= 0:
        percentage_used = float('inf')
    else:
        percentage_used = (task_hours / available_hours) * 100

    # Risk evaluation
    if available_hours <= 0:
        risk = "No Time Available"
        risk_color = "red"
    elif percentage_used <= 50:
        risk = f"Low Risk ({percentage_used:.1f}%)"
        risk_color = "green"
    elif percentage_used <= 75:
        risk = f"Medium Risk ({percentage_used:.1f}%)"
        risk_color = "orange"
    else:
        risk = f"High Risk ({percentage_used:.1f}%)"
        risk_color = "red"

    # Overrun evaluation
    if percentage_used <= 100:
        overrun = "On Time"
        overrun_color = "green"
    elif percentage_used <= 110:
        overrun = f"Minor Overrun ({percentage_used - 100:.1f}%)"
        overrun_color = "gold"
    elif percentage_used <= 125:
        overrun = f"Medium Overrun ({percentage_used - 100:.1f}%)"
        overrun_color = "orange"
    else:
        overrun = f"Severe Overrun ({percentage_used - 100:.1f}%)"
        overrun_color = "red"

    return risk, risk_color, overrun, overrun_color


def handle_input():
    """Read user inputs, run calculations, and update GUI labels."""
    try:
        now = datetime.now()
        start_date = validate_date(start_date_entry.get())
        end_date_input = end_date_entry.get().strip()
        entered_task_length = float(length_of_task_entry.get())
        calculated_task_length = float(calculated_length_entry.get())

        if not start_date:
            raise ValueError("Invalid Start Date. Use MM-DD-YYYY.")

        no_deadline = end_date_input.lower() == "n/a"

        if not no_deadline:
            end_date = validate_date(end_date_input)
            if not end_date:
                raise ValueError("Invalid End Date. Use MM-DD-YYYY or 'N/A'.")
            if end_date < start_date:
                raise ValueError("End Date must be after Start Date.")

        weighted_task_length = 0.25 * entered_task_length + 0.75 * calculated_task_length
        output_label.config(text=f"Task Length: {round(weighted_task_length, 2)} hrs", fg="white", bg="black")

        # Use start date if in the future, otherwise adjust based on work hours
        active_start = now
        if start_date.date() > now.date():
            active_start = start_date
        elif now.hour >= WORK_END_HOUR:
            active_start = datetime.combine(next_work_day(now.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)
        elif now.hour < WORK_START_HOUR:
            active_start = now.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)

        completion_estimate = calculate_estimated_completion(active_start, weighted_task_length)

        if no_deadline:
            estimate_label.config(
                text=f"Estimated Completion: {completion_estimate.strftime('%m-%d-%Y %I:%M %p')}\n"
                     f"End date is N/A — risk/overrun cannot be calculated.",
                fg="white", bg="black"
            )
            risk_label.config(text="N/A", fg="gray", bg="black")
            overrun_label.config(text="N/A", fg="gray", bg="black")
        else:
            total_work_hours = calculate_available_hours(active_start, end_date)
            remaining_hours = calculate_available_hours(completion_estimate, end_date)

            risk, risk_color, overrun, overrun_color = determine_risk_and_overrun(
                weighted_task_length, total_work_hours
            )

            estimate_label.config(
                text=f"Estimated Completion: {completion_estimate.strftime('%m-%d-%Y %I:%M %p')}\n"
                     f"Total Available Hours: {total_work_hours:.1f} hrs\n"
                     f"Time Left After Completion: {remaining_hours:.1f} hrs",
                fg="white", bg="black"
            )
            risk_label.config(text=risk, fg=risk_color, bg="black")
            overrun_label.config(text=overrun, fg=overrun_color, bg="black")

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
for label_text, row, col in fields:
    tk.Label(input_frame, text=label_text, bg="black", fg="white").grid(row=row, column=col, sticky="e", padx=5, pady=5)
    entry_widget = tk.Entry(input_frame)
    entry_widget.grid(row=row, column=col + 1, padx=5, pady=5)
    entries[label_text] = entry_widget

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
