import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

#database connection information
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "fireball123" 
DB_HOST = "localhost"
DB_PORT = "5432"

#predefined task names, 
#could also break tasks according to categories so that each catagory will have their own estimated time and total time. Makes it more specific and less generic possibly?
task_names = [
     ["Check Server Logs", 1],
     ["System Update", 2],
     ["Code Review", 3], 
     ["User Testing", 4],
     ["Debugging",5],
     ["Coding", 6],
     ["Software maintence",7]
]

bruh = random.choice(task_names)
print(bruh[0])
print(bruh[1])


#function to create synthetic data
def generate_synthetic_tasks (n = 100):
    tasks = []
    for i in range(n):
        task = random.choice(task_names)
        task_name = task[0]
        task_id = task[1]
        estimated_time = random.randint(1,50)
        assignee_id = random.randint(1,5) #five different employees
        var1 = random.randint(1,30)
        var2 = random.randint(1,5)
        var3 = random.randint(-10,10)
        time_total = random.randint(estimated_time - 10, estimated_time + 10) #sets time total +- 10 of estimated time 
        time_total = max (1, time_total) #makes sure its at least 1
        start_date = fake.date_between(start_date = '-3M', end_date = 'today')
        date_gap = random.randint(1, 9)
        end_date = start_date + timedelta(days = date_gap)
        tasks.append((task_id, task_name, estimated_time, time_total, assignee_id, var1, var2, var3, start_date, end_date))
        
        
    return tasks

try:
        #connect to PostgresSQL
        conn = psycopg2.connect (
             dbname = DB_NAME,
             user = DB_USER,
             password = DB_PASSWORD,
             host = DB_HOST,
             port = DB_PORT
        )
        cursor = conn.cursor()
        print ("Connected to database")

        #Create task table
       # Drop and recreate table
        cursor.execute("DROP TABLE IF EXISTS Tasks2")
        cursor.execute("""
        CREATE TABLE Tasks2(
            TaskId SERIAL PRIMARY KEY,
            task_id INTEGER NOT NULL,
            taskname TEXT NOT NULL,
            estimated_time INTEGER NOT NULL,
            total_time INTEGER NOT NULL,
            assignee_id INTEGER NOT NULL,
            var1 INTEGER NOT NULL,
            var2 INTEGER NOT NULL,
            var3 INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL
    )
""")

        #Removes rows from table so that you can update it if you have new values
        cursor.execute("TRUNCATE TABLE tasks2 RESTART IDENTITY")
        conn.commit()
        print("Table Tasks2 completed")

        #generate synthetic tasks
        synthetic_tasks = generate_synthetic_tasks(n = 2500)
        cursor.executemany(
        "INSERT INTO Tasks2 (task_id, taskname, estimated_time, total_time, assignee_id, var1, var2, var3, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        synthetic_tasks
    )

        conn.commit()
        print(f" Inserted {len(synthetic_tasks)} synthetic tasks")

except Exception as e:
        print("Error:", e)

finally:
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()
        print("Connection closed")

            
