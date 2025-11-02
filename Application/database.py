import psycopg2
from psycopg2 import errors

#connecting to postgres and to my database 'university'
database_connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    database= "university",
    password="###", # put your password to your database
)

#setting up connections
cursor = database_connection.cursor()

#create table function to create a table based on a schema
#if table already exists then you drop the table
def createTable(schema, dropSchema):
    try:
        cursor.execute(schema)
    except errors.DuplicateTable:
        database_connection.rollback()
        cursor.execute(dropSchema)
        cursor.execute(schema)
        

#gets all students from the student table
#displays the results in fstring formatted sections/rows
def getAllStudents():
    cursor.execute("Select * from students ORDER BY student_id")
    rows = cursor.fetchall()

    print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date':<12}")
    print("-------------------------------------------------------------------------------------")
    for row in rows:
        student_id, first_name, last_name, email, enrollment_date = row
        
        enrollment_date_str = enrollment_date.strftime("%Y-%m-%d")
        
        print(f"{student_id:<5} {first_name:<15} {last_name:<15} {email:<30} {enrollment_date_str:<12}")

    print()
    

#adds a new student to the student table
def addStudent(first_name, last_name, email, enrollment_date):
    cursor.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date)
    VALUES (%s, %s, %s, %s)""",(first_name, last_name, email, enrollment_date))
    
#updates a student's email with a new email
def updateStudentEmail(student_id, new_email):
    cursor.execute("UPDATE students SET email = %s where student_id = %s ", (new_email,student_id))
   
#deletes a student from the students table
def deleteStudent(student_id):
    cursor.execute("DELETE FROM students where student_id = %s ", (student_id,))
   
#main function to test different functions
def main():
    schema = """
        CREATE TABLE students(
            student_id SERIAL PRIMARY KEY,
            first_name Text NOT NULL,
            last_name Text NOT NULL,
            email Text NOT NULL UNIQUE,
            enrollment_date Date
        );
        """
    dropSchema = "DROP TABLE students"
    createTable(schema, dropSchema)

    addStudent('John', 'Doe', 'john.doe@example.com', '2023-09-01')
    addStudent('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01')
    addStudent('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')

    getAllStudents()

    updateStudentEmail(1, 'test.beam@example.com')

    getAllStudents()

    deleteStudent(1)

    getAllStudents()

#calling main
if __name__ == "__main__":
    main()