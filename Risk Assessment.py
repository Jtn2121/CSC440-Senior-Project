import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        return None

def handle_input():
    current_date = datetime.today()

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

    # Validate integer inputs
    try:
        length_of_task = int(length_of_task_str)
    except ValueError:
        messagebox.showerror("Input Error", "Length of Task must be an integer.")
        return

    try:
        calculated_length = int(calculated_length_str)
    except ValueError:
        messagebox.showerror("Input Error", "Calculated Length of Task must be an integer.")
        return

    # Weighted average: 25% original, 75% calculated
    average_task_length = int(0.25 * length_of_task + 0.75 * calculated_length)

    current_date_only = current_date.date()
    start_date_only = start_date.date()
    end_date_only = end_date.date()

    output_text = ""
    risk_text = ""
    output_color = "black"

    if current_date_only < start_date_only:
        delta = (end_date_only - current_date_only).days
        hours_remaining = delta * 8
        buffer_hours = hours_remaining - average_task_length
        buffer_ratio = buffer_hours / average_task_length

        if buffer_ratio >= 0.25:
            risk_text = "Low Risk"
            output_color = "gold"
        elif 0.05 <= buffer_ratio < 0.25:
            risk_text = "Medium Risk"
            output_color = "orange"
        else:
            risk_text = "High Risk"
            output_color = "red"

        output_text = f"Hours Remaining: {hours_remaining}"

    elif start_date_only <= current_date_only < end_date_only:
        delta = (end_date_only - current_date_only).days
        hours_remaining = delta * 8 + 8
        buffer_hours = hours_remaining - average_task_length
        buffer_ratio = buffer_hours / average_task_length

        if buffer_ratio >= 0.25:
            risk_text = "Low Risk"
            output_color = "gold"
        elif 0.05 <= buffer_ratio < 0.25:
            risk_text = "Medium Risk"
            output_color = "orange"
        else:
            risk_text = "High Risk"
            output_color = "red"

        output_text = f"Hours Remaining: {hours_remaining}"

    elif current_date_only == end_date_only:
        output_text = "Due Today! (8 Hours!)"
        risk_text = "Due Today!"
        output_color = "blue"

    elif current_date_only > end_date_only:
        delta = (end_date_only - current_date_only).days
        hours_past_due = abs(delta * 8) + 8
        overrun_hours = calculated_length - average_task_length
        overrun_ratio = overrun_hours / average_task_length

        if overrun_ratio <= 0:
            severity = "No Overrun"
            output_color = "green"
        elif overrun_ratio <= 0.1:
            severity = "Minor Overrun"
            output_color = "gold"
        elif overrun_ratio <= 0.25:
            severity = "Moderate Overrun"
            output_color = "orange"
        else:
            severity = "Severe Overrun"
            output_color = "red"

        output_text = f"Hours Past Due: {hours_past_due}"
        risk_text = severity

    else:
        output_text = "Date comparison failed for some reason."
        risk_text = "Error"
        output_color = "gray"

    # Update output label with black background and color only the risk part
    output_label.config(text=output_text, fg="white", bg="black")
    risk_label.config(text=risk_text, fg=output_color, bg="black")


# GUI setup
root = tk.Tk()
root.title("Risk Assessment")

# Create a frame for the 2x2 grid of inputs
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

# Start Date
tk.Label(input_frame, text="Start Date (MM-DD-YYYY):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
start_date_entry = tk.Entry(input_frame)
start_date_entry.grid(row=0, column=1, padx=5, pady=5)

# End Date
tk.Label(input_frame, text="End Date (MM-DD-YYYY):").grid(row=0, column=2, sticky="e", padx=5, pady=5)
end_date_entry = tk.Entry(input_frame)
end_date_entry.grid(row=0, column=3, padx=5, pady=5)

# Length of Task
tk.Label(input_frame, text="Length of Task (Hours):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
length_of_task_entry = tk.Entry(input_frame)
length_of_task_entry.grid(row=1, column=1, padx=5, pady=5)

# Calculated Length of Task
tk.Label(input_frame, text="Calculated Length (Hours):").grid(row=1, column=2, sticky="e", padx=5, pady=5)
calculated_length_entry = tk.Entry(input_frame)
calculated_length_entry.grid(row=1, column=3, padx=5, pady=5)

# Submit Button
tk.Button(root, text="Submit", command=handle_input).pack(pady=10)

# Output Label
output_label = tk.Label(root, text="", fg="white", bg="black", width=40, height=2)
output_label.pack(pady=10)

# Risk Label (separate label for the risk part with its color)
risk_label = tk.Label(root, text="", fg="black", bg="black", width=40, height=2)
risk_label.pack(pady=5)

root.mainloop()