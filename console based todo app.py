import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


config ={'user': 'root',
         'port': 3306,
         'password': 'root',
         'host': 'localhost',
         'database': 'todo_app'}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Database connection establised...")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Check your username and password...")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist...")
    else:
        print(err)

def createToDo(todo_name, time_created, todo_work_time, todo_type):
    cursor = connection.cursor()
    query = "INSERT INTO todos (todo_name, time_created, todo_work_time, todo_type) VALUES (%s,%s,%s,%s)"
    values = (todo_name, time_created, todo_work_time, todo_type)

    cursor.execute(query, values)
    connection.commit()
    print("Student data created successfully")

    cursor.close()


def readToDo():
    cursor = connection.cursor()
    query = "SELECT * FROM todos"

    cursor.execute(query)
    rows = cursor.fetchall()

    todos = [{"Id":row[0], "Name":row[1],"Created_Time":row[2],"Todo_Work_Time":row[3], "Type":row[4]}
             for row in rows]
    print(todos)

    cursor.close()


def updateToDo(todo_name):
    cursor = connection.cursor()
    updateWhat = input("Enter what to update(name/todo_work_time/todo_type):\n")
    if updateWhat.lower() == 'name':
        new_name = input("Enter new name: ")
        query = "UPDATE todos SET todo_name = %s WHERE todo_name = %s"
        values = (new_name, todo_name)
    elif updateWhat.lower() == 'todo_work_time':
        new_work_time = input("Enter new todo_work_time: ")
        query = "UPDATE todos SET todo_work_time = %s WHERE todo_name = %s"
        values = (new_work_time, todo_name)
    elif updateWhat.lower() == 'todo_type':
        new_type = input("Enter new todo_type: ")
        query = "UPDATE todos SET todo_type = %s WHERE todo_name = %s"
        values = (new_type, todo_name)
    else:
        print("Invalid input or missing update value.")
        return

    cursor.execute(query, values)
    connection.commit()

    print(f"Updated {updateWhat} successfully for {todo_name}")


def deleteToDo(todo_name):
    cursor = connection.cursor()

    query = "DELETE FROM todos WHERE todo_name = %s"
    values = (todo_name,)

    cursor.execute(query, values)
    connection.commit()

    print("Data deleted successfully.")

    cursor.close()



print("Hello! Welcome to Awor's ToDo App System,\nIt supports ToDo Creation, ToDo Reading, ToDo Update, and ToDo Deletion.\n\n")
print("1. Create ToDo\n"
      "2. Read ToDo\n"
      "3. Update ToDo\n"
      "4. Delete ToDo\n")

while True:
    activity = input("\nEnter CRUD activity to perform [(1 OR create), (2 OR read), (3 OR update), (4 OR delete), (q to quit)]:\n")

    if activity.lower() == "read" or activity == "2":
        readToDo()

    elif activity.lower() == "update" or activity == "3":
        updatingToDo = input("Enter the name of the ToDo to update:\n")
        updateToDo(updatingToDo)

    elif activity.lower() == "delete" or activity == "4":
        deletingTodo = input("Enter the name of the ToDo to be deleted:\n")
        deleteToDo(deletingTodo)

    elif activity.lower() == "create" or activity == "1":
        todo_name = input("Enter todo's name: ")
        time_created = datetime.now()
        todo_work_time = input("Enter todo's work time: ")
        todo_type = input("Enter todo's type: ")
        createToDo(todo_name, time_created, todo_work_time, todo_type)

    elif activity.lower() in ["q", "quit", "exit"]:
        print("Exiting the program.")
        break

    else:
        print("Invalid input. Please choose a valid option.")



connection.close()
print("Database connection closed.")
