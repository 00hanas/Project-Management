from config.db_config import getConnection
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout
from models.task import loadTask, loadTasks
from controllers.task_controller import (
    addTask, getTaskByID, updateTask, searchTasks,
    assignMemberToTask, removeMemberFromTask, updateTaskStatus, setTaskAccomplished
)

class AddTaskForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_TaskForm()  # Replace with your actual UI class
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.saveTask)

    def saveTask(self):
        task_id = self.ui.lineEdit.text().strip()         # Assume
        name = self.ui.lineEdit_1.text().strip()          # Assume
        desc = self.ui.lineEdit_2.text().strip()          # Assume
        status = self.ui.comboBox.currentText().strip()   # Assume
        due = self.ui.lineEdit_3.text().strip()           # Assume
        accomplished = self.ui.lineEdit_4.text().strip()  # Assume
        project_id = self.ui.lineEdit_5.text().strip()    # Assume

        addTask({
            "taskID": task_id,
            "taskName": name,
            "shortDescrip": desc,
            "currentStatus": status,
            "dueDate": due,
            "dateAccomplished": accomplished,
            "projectID": project_id
        })

class EditTaskForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_TaskForm()  # Replace with your actual UI class
        self.ui.setupUi(self)

        # Load existing data into the form
        data = getTaskByID(originalID)
        if data:
            self.ui.lineEdit.setText(data["taskID"])
            self.ui.lineEdit_1.setText(data["taskName"])
            self.ui.lineEdit_2.setText(data["shortDescrip"])
            self.ui.comboBox.setCurrentText(data["currentStatus"])
            self.ui.lineEdit_3.setText(str(data["dueDate"]))
            self.ui.lineEdit_4.setText(str(data["dateAccomplished"]))
            self.ui.lineEdit_5.setText(data["projectID"])

        self.ui.pushButton.clicked.connect(self.saveTask)

    def saveTask(self):
        task_id = self.ui.lineEdit.text().strip()
        name = self.ui.lineEdit_1.text().strip()
        desc = self.ui.lineEdit_2.text().strip()
        status = self.ui.comboBox.currentText().strip()
        due = self.ui.lineEdit_3.text().strip()
        accomplished = self.ui.lineEdit_4.text().strip()
        project_id = self.ui.lineEdit_5.text().strip()

        updateTask(self.originalID, {
            "taskID": task_id,
            "taskName": name,
            "shortDescrip": desc,
            "currentStatus": status,
            "dueDate": due,
            "dateAccomplished": accomplished,
            "projectID": project_id
        })

class TaskView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        task_board = loadTasks(self)
        layout.addWidget(task_board)
        self.setLayout(layout)