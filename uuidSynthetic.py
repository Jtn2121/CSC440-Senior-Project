import psycopg2
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

#database connection information
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "password" 
DB_HOST = "localhost"
DB_PORT = "5432"

#predefined task names, 
#could also break tasks according to categories so that each catagory will have their own estimated time and total time. Makes it more specific and less generic possibly?

uuid1 = uuid.uuid4()  
uuid2 = uuid.uuid4()    
uuid3 = uuid.uuid4() 
uuid4 = uuid.uuid4() 
uuid5 = uuid.uuid4() 
uuid6 = uuid.uuid4()  
uuid7 = uuid.uuid4()    
uuid8 = uuid.uuid4() 
uuid9 = uuid.uuid4() 
uuid10 = uuid.uuid4()
uuid11 = uuid.uuid4()  
uuid12 = uuid.uuid4()    
uuid13 = uuid.uuid4() 
uuid14 = uuid.uuid4() 
uuid15 = uuid.uuid4()  

task_names = [
     ["Check Server Logs", uuid1],
     ["System Update", uuid2],
     ["Code Review", uuid3],
     ["User Testing", uuid4],
     ["Debugging", uuid5],
     ["Coding", uuid6],
     ["Software maintenance", uuid7],
     ["Data Scrubbing", uuid8],
     ["Analytics Monitoring", uuid9],
     ["Meeting Planning", uuid10],
     ["Documentation", uuid11],
     ["Database Management", uuid12],
     ["Database Auditing", uuid13],
     ["Aircraft Induction", uuid14],
     ["Deployment", uuid15],
]

assignee1 = uuid.uuid4()  
assignee2 = uuid.uuid4()    
assignee3 = uuid.uuid4() 
assignee4 = uuid.uuid4() 
assignee5 = uuid.uuid4() 
assignee6 = uuid.uuid4()  
assignee7 = uuid.uuid4()    
assignee8 = uuid.uuid4() 
assignee9 = uuid.uuid4() 
assignee10 = uuid.uuid4()
assignee11 = uuid.uuid4() 
assignee12 = uuid.uuid4() 
assignee13 = uuid.uuid4()

assignee_ids = [assignee1, assignee2, assignee3, assignee4, assignee5, assignee6, assignee7, assignee8, assignee9, assignee10, assignee11, assignee12, assignee13]

template1 = uuid.uuid4()
template2 = uuid.uuid4()
template3 = uuid.uuid4()
template4 = uuid.uuid4()

template_names = [
     [None, 32*"0"], # The 'null' version of a UUID is 32*"0", hence needed
     ["Sprints", template1],
     ["Orders", template2],
     ["Reports", template3],
     ["Marketing", template4],
]

mini = 1
maxi = 10
assigneeWeight = 1.0

#function to create synthetic data
def generate_synthetic_tasks (n = 100):
    tasks = []
    for i in range(n):
        task = random.choice(task_names)
        task_name = task[0]
        task_id = task[1]

        #task id 
        if task_id == uuid1:
             mini = 1
             maxi = 8
        elif task_id == uuid2:
             mini = 1
             maxi = 12
        elif task_id == uuid3:
             mini = 3
             maxi = 20
        elif task_id == uuid4:
             mini = 3
             maxi = 10
        elif task_id == uuid5:
             mini = 5
             maxi = 35
        elif task_id == uuid6:
             mini = 1
             maxi = 25
        elif task_id == uuid7:
             mini = 3
             maxi = 30
        elif task_id == uuid8:
             mini = 1
             maxi = 12
        elif task_id == uuid9:
             mini = 2
             maxi = 8
        elif task_id == uuid10:
             mini = 5
             maxi = 56
        elif task_id == uuid11:
             mini = 5
             maxi = 56
        elif task_id == uuid12:
             mini = 5
             maxi = 56
        elif task_id == uuid13:
             mini = 5
             maxi = 56
        elif task_id == uuid14:
             mini = 5
             maxi = 56
        elif task_id == uuid15:
             mini = 5
             maxi = 56
        else:
             mini = 1
             maxi = 10
     
        task_id = uuid.uuid4()  # Changed so that every task entry is different

        assignee_id = random.choice(assignee_ids) #13 different employees

        # Adds weight to each employee for more diverse results
        if assignee_id == assignee1:
            assigneeWeight = 0.65
        elif assignee_id == assignee2:
            assigneeWeight = 1.25
        elif assignee_id == assignee3:
            assigneeWeight = 1.0
        elif assignee_id == assignee4:
            assigneeWeight = 0.85
        elif assignee_id == assignee5:
            assigneeWeight = 1.4
        elif assignee_id == assignee6:
            assigneeWeight = 1.3
        elif assignee_id == assignee7:
            assigneeWeight = 1.9
        elif assignee_id == assignee8:
            assigneeWeight = 1.85
        elif assignee_id == assignee9:
            assigneeWeight = 2.0
        elif assignee_id == assignee10:
            assigneeWeight = 0.55
        elif assignee_id == assignee11:
            assigneeWeight = 1.67
        elif assignee_id == assignee12:
            assigneeWeight = 1.4
        elif assignee_id == assignee13:
            assigneeWeight = 1.4

        mini *= assigneeWeight
        maxi *= assigneeWeight


        templateChoice = random.choice(template_names)
        template_name = templateChoice[0]
        template_id = templateChoice[1]


        estimated_time = random.uniform(mini,maxi)
        time_total = random.uniform(estimated_time - 10, estimated_time + 10) #sets time total +- 10 of estimated time 
        time_total = max (1, time_total) #makes sure its at least 1
        start_date = fake.date_between(start_date = '-3M', end_date = 'today')
        date_gap = random.randint(1, 9)
        end_date = start_date + timedelta(days = date_gap)
        tasks.append((str(task_id), task_name, time_total, estimated_time, str(assignee_id), template_name, str(template_id), start_date, end_date))
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
            CREATE TABLE IF NOT EXISTS TasksUUID(
                TaskId SERIAL PRIMARY KEY,
                task_id uuid NOT NULL,
                taskname TEXT NOT NULL,
                estimated_time DOUBLE PRECISION NOT NULL,
                total_time DOUBLE PRECISION NOT NULL,
                assignee_id uuid NOT NULL,
                templatename TEXT,
                template_id uuid,
                start_date DATE,
                end_date DATE                                
            )
        """)
        #Removes rows from table so that you can update it if you have new values
        cursor.execute("TRUNCATE TABLE tasksUUID RESTART IDENTITY")
        conn.commit()
        print("Table TasksUUID completed")

        #creates templatesuuid table
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS templatesuuid
          (
               template_id uuid,
               template_name text,
               list_id uuid,
               templateNum int GENERATED ALWAYS AS IDENTITY
          )
        """)
        cursor.execute("TRUNCATE TABLE templatesuuid RESTART IDENTITY")
        conn.commit()
        print("templatesuuid table created!")


        #creates listsuuid table
        cursor.execute("""
             CREATE TABLE IF NOT EXISTS listsuuid
               (
                    list_id uuid NOT NULL DEFAULT gen_random_uuid(),
                    tasks_ids uuid[],
                    listNum int GENERATED ALWAYS AS IDENTITY,
                    CONSTRAINT listsuuid_pkey PRIMARY KEY (list_id)
               )
        """)
        cursor.execute("TRUNCATE TABLE listsuuid RESTART IDENTITY")
        conn.commit()
        print("listsuuid created!")

        ########################### TABLES COMPLETED #############################################






        #generate synthetic tasks
        synthetic_tasks = generate_synthetic_tasks(n = 25000)
        cursor.executemany(
             "INSERT INTO TasksUUID (task_id, taskname, estimated_time, total_time, assignee_id, templatename, template_id, start_date, end_date) VALUES (%s,%s, %s, %s, %s, %s, %s, %s ,%s)", synthetic_tasks
        )
        print(f"Inserted {len(synthetic_tasks)} synthetic tasks")
        conn.commit()

        #slight edit to change the 32*"0" into
        cursor.execute("""
               UPDATE tasksuuid
               SET template_ID = NULL
               WHERE template_id = '00000000-0000-0000-0000-000000000000'  """)
        conn.commit()
        print("null templates set to null")
        # Population of templatesid -- listuuid
        cursor.execute("""
               INSERT INTO templatesuuid(template_id, template_name)
               SELECT DISTINCT(template_id) AS "template_id", templatename AS "template_name"
               FROM tasksuuid
               WHERE template_id IS NOT NULL;
                           """)
        conn.commit()
        print("templateuuid table populated not including list_id")
        # population of listuuid
        cursor.execute("""
               INSERT INTO listsuuid(tasks_ids)
               SELECT array_agg(task_id) FROM tasksuuid
               WHERE template_id IS NOT NULL
               GROUP BY template_id
                           """)
        conn.commit()
        print("listuuid table populated")

       # populates the list_id in the templatesuuid table
        cursor.execute("""
          UPDATE templatesuuid
          SET list_id = listsuuid.list_id
          FROM listsuuid
          WHERE templatesuuid.templateNum = listsuuid.listNum                
        """)
        conn.commit()
        print("list_id populated in templatesuuid table")


except Exception as e:
        print("Error:", e)

finally:
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()
        print("Connection closed")

            


