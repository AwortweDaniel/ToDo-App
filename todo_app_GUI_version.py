import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
)
from datetime import datetime
import mysql.connector
from mysql.connector import Error


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Awor's ToDo App GUI")
        self.setGeometry(100, 100, 800, 400)

        # Attempt DB connection
        try:
            self.connection = mysql.connector.connect(
                user='root',
                password='root',
                host='localhost',
                port=3306,
                database='todo_app'
            )
        except Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to database:\n{err}")
            sys.exit(1)

        # Layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Form inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("ToDo Name")

        self.work_time_input = QLineEdit()
        self.work_time_input.setPlaceholderText("ToDo Work Time")

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("ToDo Type")

        self.add_button = QPushButton("Add ToDo")
        self.add_button.clicked.connect(self.add_todo)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.work_time_input)
        form_layout.addWidget(self.type_input)
        form_layout.addWidget(self.add_button)
        self.layout.addLayout(form_layout)

        # ToDo table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Created", "Work Time", "Type"])
        self.layout.addWidget(self.table)

        # Action buttons
        self.update_button = QPushButton("Update Selected")
        self.delete_button = QPushButton("Delete Selected")

        self.update_button.clicked.connect(self.update_todo)
        self.delete_button.clicked.connect(self.delete_todo)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.update_button)
        action_layout.addWidget(self.delete_button)
        self.layout.addLayout(action_layout)

        # Load data
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM todos")
                for row_idx, row_data in enumerate(cursor.fetchall()):
                    self.table.insertRow(row_idx)
                    for col_idx, col_data in enumerate(row_data):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to load data:\n{err}")

    def add_todo(self):
        name = self.name_input.text().strip()
        work_time = self.work_time_input.text().strip()
        todo_type = self.type_input.text().strip()
        created = datetime.now()

        if not name or not work_time or not todo_type:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO todos (todo_name, time_created, todo_work_time, todo_type) VALUES (%s, %s, %s, %s)",
                    (name, created, work_time, todo_type)
                )
                self.connection.commit()
        except Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to insert data:\n{err}")
            return

        self.name_input.clear()
        self.work_time_input.clear()
        self.type_input.clear()
        self.load_data()

    def update_todo(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a row to update.")
            return

        try:
            todo_id_item = self.table.item(selected, 0)
            name_item = self.table.item(selected, 1)
            work_time_item = self.table.item(selected, 3)
            type_item = self.table.item(selected, 4)

            if not all([todo_id_item, name_item, work_time_item, type_item]):
                QMessageBox.warning(self, "Data Error", "Some fields are empty or invalid.")
                return

            todo_id = todo_id_item.text()
            name = name_item.text()
            work_time = work_time_item.text()
            todo_type = type_item.text()

            with self.connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE todos SET todo_name=%s, todo_work_time=%s, todo_type=%s WHERE id=%s",
                    (name, work_time, todo_type, todo_id)
                )
                self.connection.commit()

            QMessageBox.information(self, "Success", "ToDo updated successfully.")
            self.load_data()
        except Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to update data:\n{err}")

    def delete_todo(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")
            return

        todo_id_item = self.table.item(selected, 0)
        if not todo_id_item:
            QMessageBox.warning(self, "Data Error", "Invalid selection.")
            return

        todo_id = todo_id_item.text()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
                self.connection.commit()
            QMessageBox.information(self, "Success", "ToDo deleted successfully.")
            self.load_data()
        except Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to delete data:\n{err}")

    def closeEvent(self, event):
        self.connection.close()
        event.accept()



app = QApplication(sys.argv)
window = ToDoApp()
window.show()
sys.exit(app.exec())
