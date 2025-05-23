# NOTE: NEED TO RUN uuidSynthetic FILE FIRST TO CREATE AND POPULATE TABLES




import random as rd
import pandas as pd
import psycopg2
import uuid
import numpy as np
import psycopg2.extras
from sklearn.preprocessing import LabelEncoder
from pandasql import sqldf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV


psycopg2.extras.register_uuid() # allows for the use of uuids passed for postgres queries
pysqldf = lambda q: sqldf(q, globals())


db_name = "postgres"
db_user = "postgres"
db_password = "password" # this should be changed to your password here
db_host = "localhost"
db_port = "5432"

with psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port 
    ) as connection:
         with connection.cursor() as cursor:
            cursor.execute("SELECT template_id, template_name FROM templatesuuid WHERE template_id IS NOT NULL")
            templateCol = np.array(cursor.fetchall()) # both columns fetched for dataframe
            cursor.execute("SELECT template_id FROM templatesuuid WHERE template_id IS NOT NULL")
            templateRavel = np.array(cursor.fetchall()) # single column fetched for encoding
           
tempSize = templateRavel.size

templateRows = []

for x in range(tempSize): # sets up initial dataframe for template options
    id = str(templateCol[x,0])
    name = templateCol[x,1]
    templateRows.append([id, name])

dataframeTem = pd.DataFrame(templateRows) # Creation of dataframe that stores template id and template name - this is generalized to intake whatever is produced in the synthetic data
dataframeTem.columns =["Template_ID","Template_Name"]

####################################### INPUTS BEGINNING ############################################

#templateChoiceName = str(input("Enter template name: (Marketing, Reports, Orders, Sprints) ")) # This will be a drop down on the front end ### This allows for manual template input by name (Reports, a
#assigneeChoiceNum = int(input("Enter assignee Identification: (1-13) ")) # Another drop down field of ints
assigneeChoiceNum = 5  #hard coded values that show we can input values and get results
templateChoiceName = "Reports" #hard coded template choice name

#################################### INPUTS END #####################################################


###################################### SUBSET PULL FILTERED BY TEMPLATE ############################
tIDdf = pysqldf("SELECT template_id FROM dataframeTem WHERE Template_Name = '{}'".format(templateChoiceName))
print(tIDdf)
template_id = tIDdf.at[0,'Template_ID']
print(template_id)

with psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port 
    ) as connection:
         with connection.cursor() as cursor:
            cursor.execute("SELECT list_id FROM templatesuuid WHERE template_id = %(value)s", {"value": str(template_id)})
            lID = cursor.fetchone()
            list_id = lID[0]

            cursor.execute("""
                            SELECT assignee_id, total_time FROM tasksuuid 
                            JOIN templatesuuid ON tasksuuid.template_id = templatesuuid.template_id
                            JOIN listsuuid ON templatesuuid.list_id = listsuuid.list_id
                            WHERE listsuuid.list_id = %(value)s
                           """, {"value": str(list_id)})
            PartialArr = cursor.fetchall()
            cursor.execute("""
                            SELECT DISTINCT (assignee_id) FROM tasksuuid
                           """)
            AssigneeArr = np.array(cursor.fetchall())

####################################### ASSIGNEE LABEL ENCODER (SEE DOCUMENTATION) ##############################
assigneeSize = AssigneeArr.size
AssigneeArr = AssigneeArr.ravel()
rows = []
rowsAssign = []

encoder = LabelEncoder()
assigneeEncoded = encoder.fit_transform(AssigneeArr)
tempAssignee = []

     
for row in PartialArr:
    rows.append(row)


PartialDataset = pd.DataFrame(rows)
PartialDataset.columns =["Assignee_ID", "Total_time"]

assigneeStuff = (PartialDataset["Assignee_ID"].to_numpy()).ravel()
encoder = LabelEncoder()
assigneeEncoded = encoder.fit_transform(assigneeStuff)
PartialDataset['Assignee_encoded'] = assigneeEncoded

#print(PartialDataset) # can be used to see the subset used

######################## Actionable Data Extracted #########################

####################### Model Calculations #######################

print("Starting Model Calculations")
getX =np.array(PartialDataset["Assignee_encoded"]) #Extracts X values
getY = np.array(PartialDataset["Total_time"]) #Extracts Y values
getX = getX.reshape(-1,1)
getY = getY.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(getX, getY, test_size=0.4,random_state=4)

lasso = Lasso()
lasso.fit(X_train, y_train)
param_grid = {'alpha' :[0.001, 0.01, 0.1, 1.0]}

lasso_cv = GridSearchCV(lasso, param_grid, cv=3, n_jobs=-1)
lasso_cv.fit(X_train, y_train)

diffLasso = lasso_cv.best_estimator_
diffLasso.fit(X_train, y_train)
X_Input = np.array([[assigneeChoiceNum]])
y_pred = diffLasso.predict(X_Input)

print("The prediction for this template with the given assignee value is: ", y_pred) #Final prediction output 



        
