import psycopg2
import random

#database connection information
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "fireball23" 
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
     ["Software maintenance",7]
]

bruh = random.choice(task_names)

#function to create synthetic data
def generate_synthetic_tasks (n = 100):
    tasks = []
    for i in range(n):
        task = random.choice(task_names)
        task_name = task[0]
        task_id = task[1]
        estimated_time = random.uniform(1,50)
        assignee_id = random.randint(1,5) #five different employees
        var1 = random.randint(1,30)
        var2 = random.randint(1,5)
        var3 = random.randint(-10,10)
        time_total = random.uniform(estimated_time - 10, estimated_time + 10) #sets time total +- 10 of estimated time 
        time_total = max (1, time_total) #makes sure its at least 1
        tasks.append((task_id, task_name, estimated_time, time_total, assignee_id, var1, var2, var3))
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks2(
                TaskId SERIAL PRIMARY KEY,
                task_id INTEGER NOT NULL,
                taskname TEXT NOT NULL,
                estimated_time DOUBLE PRECISION NOT NULL,
                total_time DOUBLE PRECISION NOT NULL,
                assignee_id INTEGER NOT NULL,
                var1 INTEGER NOT NULL,
                var2 INTEGER NOT NULL,
                var3 INTEGER NOT NULL
                       
            )
        """)
        #Removes rows from table so that you can update it if you have new values
        cursor.execute("TRUNCATE TABLE tasks2 RESTART IDENTITY")
        conn.commit()
        print("Table Tasks2 completed")

        #generate synthetic tasks
        synthetic_tasks = generate_synthetic_tasks(n = 2500)
        cursor.executemany(
             "INSERT INTO Tasks2 (task_id, taskname, estimated_time, total_time, assignee_id, var1, var2, var3) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", synthetic_tasks
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

            


