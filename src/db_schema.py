import psycopg2
import numpy as np
from psycopg2 import Error
import sys
import pickle


'''
local data schema: 
students: student_id (PK), age, first_name, last_name
healthcenters: center_id (PK), location_id
activity: actitvity_id (PK), location_id, date
participation: participationid (PK), activity_id, student_id
location: location_id (PK), address, city
testlog: test_id (PK), result, date, student_id
vaccination: brand_id (PK)
vaccinationhistory: history_id (PK), brand_id, student_id, dose_number, date
'''


def create_schema(username, password, database):

    try:
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      database=database)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        # SQL query to create tables
        create_table_query = '''CREATE TABLE STUDENTS
          (studentid DECIMAL(7) PRIMARY KEY  NOT NULL,
          age INTEGER NOT NULL,
          firstname VARCHAR(20) NOT NULL,
          lastname  VARCHAR(20) NOT NULL); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE LOCATION
          (locationid DECIMAL(9) PRIMARY KEY  NOT NULL,
          address VARCHAR(100) NOT NULL,
          city VARCHAR(20) NOT NULL); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE HEALTHCENTERS
          (centerid DECIMAL(3) PRIMARY KEY  NOT NULL,
          locationid DECIMAL(9) NOT NULL,
          FOREIGN KEY (locationid) REFERENCES LOCATION(locationid)); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE ACTIVITY
          (activityid DECIMAL(5) PRIMARY KEY  NOT NULL,
          locationid DECIMAL(9) NOT NULL,
          date DATE NOT NULL,
          FOREIGN KEY (locationid) REFERENCES LOCATION(locationid)); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE PARTICIPATION
          (participationid DECIMAL(9) PRIMARY KEY  NOT NULL,
          activityid DECIMAL(5) NOT NULL,
          studentid DECIMAL(7) NOT NULL,
          FOREIGN KEY (studentid) REFERENCES STUDENTS(studentid),
          FOREIGN KEY (activityid) REFERENCES ACTIVITY(activityid)); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE TESTLOG
          (testid DECIMAL(9) PRIMARY KEY  NOT NULL,
          result BOOLEAN NOT NULL,
          date DATE NOT NULL,
          studentid DECIMAL(7) NOT NULL,
          FOREIGN KEY (studentid) REFERENCES STUDENTS(studentid)); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE VACCINATION
          (brandid DECIMAL(5) PRIMARY KEY  NOT NULL); '''
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE VACCINATIONHISTORY
          (historyid DECIMAL(9) PRIMARY KEY  NOT NULL,
          brandid DECIMAL(5) NOT NULL,
          studentid DECIMAL(7) NOT NULL,
          dosenumber DECIMAL(1) NOT NULL,
          date DATE NOT NULL,
          FOREIGN KEY (brandid) REFERENCES VACCINATION(brandid),
          FOREIGN KEY (studentid) REFERENCES STUDENTS(studentid)); '''
        cursor.execute(create_table_query)

        connection.commit()
        print("8 tables created successfully in PostgreSQL ")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def insert_instance(username, password, database):
    try:
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      database=database)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        with open('./data/students.pickle', 'rb') as f:
          students = pickle.load(f)
        # SQL query to insert instances into table STUDENTS
        for i in range(len(students)):
            a = 'INSERT INTO STUDENTS (studentid, age, firstname, lastname)'
            b = 'VALUES ( {}, {}, \'{}\', \'{}\' )'.format(students[i]['student_id'], students[i]['age'], students[i]['first_name'], students[i]['last_name'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into STUDENTS')

        with open('./data/locations.pickle', 'rb') as f:
          locations = pickle.load(f)
        # SQL query to insert instances into table LOCATION
        for i in range(len(locations)):
            a = 'INSERT INTO LOCATION (locationid, address, city)'
            b = 'VALUES ( {}, \'{}\', \'{}\' )'.format(locations[i]['location_id'], locations[i]['address'], locations[i]['city'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into LOCATION')
        
        with open('./data/healthcenters.pickle', 'rb') as f:
          healthcenters = pickle.load(f)
        # SQL query to insert instances into table HEALTHCENTERS
        for i in range(len(healthcenters)):
            a = 'INSERT INTO HEALTHCENTERS (centerid, locationid)'
            b = 'VALUES ( {}, {} )'.format(healthcenters[i]['center_id'], healthcenters[i]['location_id'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into HEALTHCENTERS')

        with open('./data/activitys.pickle', 'rb') as f:
          activitys = pickle.load(f)
        # SQL query to insert instances into table ACTIVITY
        for i in range(len(activitys)):
            a = 'INSERT INTO ACTIVITY (activityid, locationid, date)'
            b = 'VALUES ( {}, {}, \'{}\' )'.format(activitys[i]['activity_id'], activitys[i]['location_id'], activitys[i]['date'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into ACTIVITY')

        with open('./data/participations.pickle', 'rb') as f:
          participations = pickle.load(f)
        # SQL query to insert instances into table PARTICIPATION
        for i in range(len(participations)):
            a = 'INSERT INTO PARTICIPATION (participationid, activityid, studentid)'
            b = 'VALUES ( {}, {}, {} )'.format(participations[i]['participation_id'], participations[i]['activity_id'], participations[i]['student_id'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into PARTICIPATION')

        with open('./data/testlogs.pickle', 'rb') as f:
          testlogs = pickle.load(f)
        # SQL query to insert instances into table TESTLOG
        for i in range(len(testlogs)):
            a = 'INSERT INTO TESTLOG (testid, result, date, studentid)'
            b = 'VALUES ( {}, {}, \'{}\', {} )'.format(testlogs[i]['test_id'], testlogs[i]['result'], testlogs[i]['date'], testlogs[i]['student_id'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into TESTLOG')

        with open('./data/vaccinations.pickle', 'rb') as f:
          vaccinations = pickle.load(f)
        # SQL query to insert instances into table VACCINATION
        for i in range(len(vaccinations)):
            a = 'INSERT INTO VACCINATION (brandid)'
            b = 'VALUES ( {} )'.format(vaccinations[i]['brand_id'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into VACCINATION')

        with open('./data/vaccinationhistorys.pickle', 'rb') as f:
          vaccinationhistorys = pickle.load(f)
        # SQL query to insert instances into table VACCINATIONHISTORY
        for i in range(len(vaccinationhistorys)):
            a = 'INSERT INTO VACCINATIONHISTORY (historyid, brandid, studentid, dosenumber, date)'
            b = 'VALUES ( {}, {}, {}, {}, \'{}\' )'.format(vaccinationhistorys[i]['history_id'], vaccinationhistorys[i]['brand_id'], vaccinationhistorys[i]['student_id'], vaccinationhistorys[i]['dose_number'], vaccinationhistorys[i]['date'])
            insert_query = a + b
            print(insert_query)
            cursor.execute(insert_query)
            print('==> inserted one instance into VACCINATION')

        connection.commit()
        print('==> finished inserting instances')

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':

  username = 'mfcuser'
  password = '12345678'
  database = 'mfcdb'

  args = sys.argv[1]
  username = sys.argv[2]
  password = sys.argv[3]

  if args == 'create_table':
    create_schema(username, password, database)
  elif args == 'insert_instance':
    insert_instance(username, password, database)
  else:
    print('==> no such argument!')
