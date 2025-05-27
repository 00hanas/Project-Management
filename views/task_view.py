from config.db_config import getConnection
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QDateTime, QRegularExpression
from models.task import loadTasks
from controllers.task_controller import (
    addTask, getTaskByID, updateTask, searchTasks,
    assignMemberToTask, removeMemberFromTask, updateTaskStatus, setTaskAccomplished
)
from controllers.project_controller import getAllProjects
from ui.addtask_interface import Ui_addtask_dialog
from utils.task_validators import uniqueTask, uniqueEditTask
from datetime import datetime

class AddTaskForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addtask_dialog()  # Replace with your actual UI class
        self.ui.setupUi(self)

        #populate combobox for projectIDS
        self.populateProjectsComboBox()

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.task_id_info.setValidator(id_validator)

        self.ui.task_save_button.clicked.connect(self.saveTask)
        self.ui.task_clear_button.clicked.connect(self.clearTask)
        self.ui.task_cancel_button.clicked.connect(self.cancelTask)

    def populateProjectsComboBox(self):
        projects = getAllProjects()
        for project in projects:
            projectName = project[1]
            self.ui.task_project_info.addItem(projectName)

    def saveTask(self):
        task_id = self.ui.task_id_info.text().strip()         
        name = self.ui.task_name_info.text().strip()          
        desc = self.ui.task_shortDescrip_info.toPlainText()      
        status = self.ui.task_status_info.currentText().strip()   
        due = self.ui.task_dueDate_info.text().strip()           
        accomplished = self.ui.task_dateAccomplished_info.text().strip()  
        project_name = self.ui.task_project_info.currentText().strip()

        if not task_id or not name or not project_name:
            QMessageBox.warning(self, "Input Error", "Task ID, Name, and Project ID cannot be empty.")
            return

        projects = getAllProjects()
        for project in projects:
            if project[1] == project_name:
                project_id = project[0]
                break  

        error = uniqueTask(task_id)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return
        
        due = datetime.strptime(due, "%m/%d/%Y %I:%M %p")

        accomplished = datetime.strptime(accomplished, "%m/%d/%Y %I:%M %p")

        addTask({
            "taskID": task_id,
            "taskName": name,
            "shortDescrip": desc,
            "currentStatus": status,
            "dueDate": due,
            "dateAccomplished": accomplished,
            "projectID": project_id
        })

        # insert here statement to load task widgets #

        QMessageBox.information(self, "Success", "Task saved successfully.")
        self.close()

    def clearTask(self):
        self.ui.task_project_info.setCurrentIndex(0)
        self.ui.task_status_info.setCurrentIndex(0)
        self.ui.task_name_info.clear()
        self.ui.task_id_info.clear()
        self.ui.task_shortDescrip_info.clear()
        self.ui.task_dueDate_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))
        self.ui.task_dateAccomplished_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))

    def cancelTask(self):
        self.close()

class EditTaskForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addtask_dialog()  # Replace with your actual UI class
        self.ui.setupUi(self)

        self.originalID = originalID
        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.task_id_info.setValidator(id_validator)

        # Load existing data into the form
        data = getTaskByID(originalID)
        if data:
            self.ui.task_id_info.setText(data["taskID"])
            self.ui.task_name_info.setText(data["taskName"])
            self.ui.task_shortDescrip_info.setText(data["shortDescrip"])
            self.ui.task_status_info.setCurrentText(data["currentStatus"])
            self.ui.task_dueDate_info.setText(str(data["dueDate"]))
            self.ui.task_dateAccomplished_info.setText(str(data["dateAccomplished"]))
            self.ui.task_project_info.setText(data["projectID"])

        self.ui.pushButton.clicked.connect(self.saveTask)

    def saveTask(self):
        task_id = self.ui.lineEdit.text().strip()
        name = self.ui.lineEdit_1.text().strip()
        desc = self.ui.lineEdit_2.text().strip()
        status = self.ui.comboBox.currentText().strip()
        due = self.ui.lineEdit_3.text().strip()
        accomplished = self.ui.lineEdit_4.text().strip()
        project_id = self.ui.lineEdit_5.text().strip()

        if not task_id or not name or not project_id:
            QMessageBox.warning(self, "Input Error", "Task ID, Name, and Project ID cannot be empty.")
            return
        
        error = uniqueEditTask(task_id, self.originalID)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return

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