from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
import psycopg2.extras
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")  # Allow frontend access

# Database info
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Jtn962540"
DB_HOST = "localhost"
DB_PORT = "5432"

psycopg2.extras.register_uuid()

# --- Constants for Risk Calculations ---
WORK_START_HOUR = 9
WORK_END_HOUR = 17
WORK_HOURS_PER_DAY = WORK_END_HOUR - WORK_START_HOUR

# --- Utility Functions for Risk Calculation ---
def is_weekend(date_obj):
    return date_obj.weekday() >= 5

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

        hours_left -= hours_available_today
        current = datetime.combine(next_work_day(current.date()), datetime.min.time()).replace(hour=WORK_START_HOUR)

    return current

def calculate_available_hours(start_dt, end_dt):
    total_hours = 0
    current_day = start_dt.date()
    end_day = end_dt.date()

    while current_day <= end_day:
        if not is_weekend(current_day):
            if current_day == start_dt.date():
                start_time = max(start_dt, start_dt.replace(hour=WORK_START_HOUR, minute=0, second=0))
                end_time = start_dt.replace(hour=WORK_END_HOUR, minute=0, second=0)
                if start_time < end_time:
                    total_hours += (end_time - start_time).total_seconds() / 3600
            else:
                total_hours += WORK_HOURS_PER_DAY
        current_day += timedelta(days=1)

    return total_hours

def determine_risk_and_overrun(task_hours, available_hours):
    if available_hours <= 0:
        percentage = float('inf')
    else:
        percentage = (task_hours / available_hours) * 100

    if available_hours <= 0:
        risk_text = "No Time Available"
    elif percentage <= 50:
        risk_text = f"Low Risk ({percentage:.1f}%)"
    elif percentage <= 75:
        risk_text = f"Medium Risk ({percentage:.1f}%)"
    else:
        risk_text = f"High Risk ({percentage:.1f}%)"

    if percentage <= 100:
        overrun_text = "On Time"
    elif percentage <= 110:
        overrun_text = f"Minor Overrun ({percentage - 100:.1f}%)"
    elif percentage <= 125:
        overrun_text = f"Medium Overrun ({percentage - 100:.1f}%)"
    else:
        overrun_text = f"Severe Overrun ({percentage - 100:.1f}%)"

    return risk_text, overrun_text

def train_model(template_choice_name):
    with psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as connection:
        with connection.cursor() as cursor:
            # Fetch all assignees from tasksuuid
            cursor.execute("SELECT DISTINCT assignee_id FROM tasksuuid")
            all_assignees = [str(row[0]) for row in cursor.fetchall()]

            # Fetch the template ID
            cursor.execute("SELECT template_id FROM templatesuuid WHERE template_name = %s", (template_choice_name,))
            result = cursor.fetchone()
            if not result:
                return None, None
            template_id = result[0]

            # Fetch the partial dataset (only for the template)
            cursor.execute("""
                SELECT assignee_id, total_time 
                FROM tasksuuid
                WHERE template_id = %s
            """, (template_id,))
            PartialArr = cursor.fetchall()

    if not PartialArr:
        return None, None

    # Build DataFrame
    df = pd.DataFrame(PartialArr, columns = ["Assignee_ID", "Total_time"])

    # Fit encoder on ALL assignees
    encoder = LabelEncoder()
    encoder.fit(all_assignees)

    # Now safely encode the subset
    df['Assignee_encoded'] = encoder.transform(df['Assignee_ID'])

    # Train the model
    X = df['Assignee_encoded'].values.reshape(-1, 1)
    y = df['Total_time'].values.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=4)

    lasso = Lasso()
    param_grid = {'alpha': [0.001, 0.01, 0.1, 1.0]}
    
    lasso_cv = GridSearchCV(lasso, param_grid, cv=3, n_jobs=-1)
    lasso_cv.fit(X_train, y_train)

    final_model = lasso_cv.best_estimator_

    return final_model, encoder



# Get Templates
@app.route('/templates', methods = ['GET'])
def get_templates():
    try:
        with psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT template_name FROM templatesuuid")
                template_rows = cursor.fetchall()
                templates = [row[0] for row in template_rows]

        return jsonify(templates)

    except Exception as e:
        print("Error fetching templates:", e)
        return jsonify([]), 500


# Get Assignees
@app.route('/assignees', methods = ['GET'])
def get_assignees():
    try:
        with psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT assignee_id FROM tasksuuid")
                assignee_rows = cursor.fetchall()
                assignees = [str(row[0]) for row in assignee_rows]

        # Map UUIDs to "Employee 1", "Employee 2", etc.
        mapped_assignees = []
        for idx, assignee_id in enumerate(assignees, start = 1):
            mapped_assignees.append({
                "id": assignee_id,
                "name": f"Employee {idx}"
            })

        return jsonify(mapped_assignees)

    except Exception as e:
        print("Error fetching assignees:", e)
        return jsonify([]), 500


# Predict Estimated Time
@app.route('/predict-time', methods=['POST'])
def predict_time():
    data = request.json
    assignee_id = data.get('userId')
    template_name = data.get('template')

    if not assignee_id or not template_name:
        return jsonify({"error": "Missing userId or template"}), 400

    model, encoder = train_model(template_name)
    if model is None:
        return jsonify({"error": "Template not found or no data available"}), 400

    try:
        assignee_encoded = encoder.transform([assignee_id])[0]
        predicted_time = model.predict(np.array([[assignee_encoded]]))
        return jsonify({"predictedTime": round(float(predicted_time[0]), 2)})

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 500

# Risk assessment calculation
@app.route('/assess-risk', methods=['POST'])
def assess_risk():
    data = request.json
    start_date_str = data.get('startDate')
    end_date_str = data.get('endDate')
    task_hours = data.get('taskHours')
    calculated_hours = data.get('calculatedLength')

    if not start_date_str or not task_hours or calculated_hours is None:
        return jsonify({"error": "Missing fields"}), 400

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        average_task_length = 0.25 * float(task_hours) + 0.75 * float(calculated_hours)
    except Exception as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    current_date = datetime.now()
    use_date = start_date if start_date.date() > current_date.date() else current_date

    if end_date_str and end_date_str.lower() != "n/a":
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        total_hours_available = calculate_available_hours(use_date, end_date)

        risk_text, overrun_text = determine_risk_and_overrun(average_task_length, total_hours_available)

        estimated_completion = calculate_estimated_completion(use_date, average_task_length)

        return jsonify({
            "estimatedCompletion": estimated_completion.strftime('%Y-%m-%dT%H:%M'),
            "risk": risk_text,
            "overrun": overrun_text,
            "availableHours": total_hours_available
        })

    else:
        estimated_completion = calculate_estimated_completion(use_date, average_task_length)
        return jsonify({
            "estimatedCompletion": estimated_completion.strftime('%Y-%m-%dT%H:%M'),
            "risk": "N/A",
            "overrun": "N/A",
            "availableHours": None
        })

if __name__ == "__main__":
    app.run(port=5000, debug=True)