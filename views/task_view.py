from config.db_config import getConnection
from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QMessageBox, QListWidgetItem
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QDateTime, QRegularExpression
from models.task import loadTasks
from controllers.task_controller import (
    addTask, getTaskByID, updateTask, searchTasks,
    assignMemberToTask, removeMemberFromTask, updateTaskStatus, setTaskAccomplished,
    getMembersForTask, deleteTask # Ensure getMembersForTask and deleteTask are imported
)
from controllers.project_controller import getAllProjects
from ui.addtask_interface import Ui_addtask_dialog
from ui.tasks_expand import Ui_tasks_expand # Import the expand UI for tasks
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
        
        due = datetime.strptime(due, "%d/%m/%Y %I:%M %p")

        accomplished = datetime.strptime(accomplished, "%d/%m/%Y %I:%M %p")

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

class EditTaskForm(QDialog): # Ensure EditTaskForm is defined
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addtask_dialog()
        self.ui.setupUi(self)
        self.originalID = originalID

        # Populate projects combobox
        projects = getAllProjects()
        for project in projects:
            self.ui.task_project_info.addItem(project[1], project[0]) # Store ID as data

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.task_id_info.setValidator(id_validator)

        data = getTaskByID(originalID)
        if data:
            self.ui.task_id_info.setText(data.get("taskID", ""))
            self.ui.task_name_info.setText(data.get("taskName", ""))
            self.ui.task_shortDescrip_info.setPlainText(data.get("shortDescrip", ""))
            self.ui.task_status_info.setCurrentText(data.get("currentStatus", "Unassigned"))

            due_date = data.get("dueDate")
            if due_date:
                if isinstance(due_date, str):
                    try:
                        due_date_dt = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
                    except ValueError: # Try another common format if the first fails
                        try:
                            due_date_dt = datetime.strptime(due_date, '%Y-%m-%d')
                        except ValueError:
                             due_date_dt = QDateTime(2000,1,1,0,0).toPyDateTime() # Fallback
                elif isinstance(due_date, datetime):
                    due_date_dt = due_date
                else: # Fallback for unexpected types
                    due_date_dt = QDateTime(2000,1,1,0,0).toPyDateTime()
                self.ui.task_dueDate_info.setDateTime(QDateTime(due_date_dt))

            accomplished_date = data.get("dateAccomplished")
            if accomplished_date:
                if isinstance(accomplished_date, str):
                    try:
                        accomplished_date_dt = datetime.strptime(accomplished_date, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                         try:
                            accomplished_date_dt = datetime.strptime(accomplished_date, '%Y-%m-%d')
                         except ValueError:
                            accomplished_date_dt = QDateTime(2000,1,1,0,0).toPyDateTime() # Fallback
                elif isinstance(accomplished_date, datetime):
                    accomplished_date_dt = accomplished_date
                else: # Fallback
                    accomplished_date_dt = QDateTime(2000,1,1,0,0).toPyDateTime()
                self.ui.task_dateAccomplished_info.setDateTime(QDateTime(accomplished_date_dt))
            else: # If no accomplished date, set to a default or disable
                self.ui.task_dateAccomplished_info.setDateTime(QDateTime(2000,1,1,0,0))


            # Set project in combobox
            project_id_to_select = data.get("projectID")
            for i in range(self.ui.task_project_info.count()):
                if self.ui.task_project_info.itemData(i) == project_id_to_select:
                    self.ui.task_project_info.setCurrentIndex(i)
                    break
        
        self.ui.task_save_button.setText("Update") # Change save button text for clarity
        self.ui.task_save_button.clicked.connect(self.updateExistingTask)
        self.ui.task_clear_button.clicked.connect(self.clearTaskFields) # Assuming you want clear for edit too
        self.ui.task_cancel_button.clicked.connect(self.close)

    def updateExistingTask(self):
        task_id = self.ui.task_id_info.text().strip()
        name = self.ui.task_name_info.text().strip()
        desc = self.ui.task_shortDescrip_info.toPlainText().strip()
        status = self.ui.task_status_info.currentText().strip()
        
        due_qdatetime = self.ui.task_dueDate_info.dateTime()
        due_datetime = due_qdatetime.toPyDateTime()

        accomplished_qdatetime = self.ui.task_dateAccomplished_info.dateTime()
        accomplished_datetime = accomplished_qdatetime.toPyDateTime() if accomplished_qdatetime > QDateTime(2000,1,1,0,1) else None


        project_index = self.ui.task_project_info.currentIndex()
        project_id = self.ui.task_project_info.itemData(project_index) if project_index >=0 else None


        if not task_id or not name or not project_id:
            QMessageBox.warning(self, "Input Error", "Task ID, Name, and Project cannot be empty.")
            return

        error = uniqueEditTask(task_id, self.originalID)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return

        updated_data = {
            "taskID": task_id,
            "taskName": name,
            "shortDescrip": desc,
            "currentStatus": status,
            "dueDate": due_datetime,
            "dateAccomplished": accomplished_datetime,
            "projectID": project_id
        }

        try:
            updateTask(self.originalID, updated_data)
            QMessageBox.information(self, "Success", "Task updated successfully.")
            self.main_window.refresh_container('task')
            self.main_window.refresh_container('project')
            self.main_window.refresh_container('home')
            self.main_window.refreshTable()
            self.main_window.update_task_details(getTaskByID(task_id)) # Update details pane
            self.accept() # Close dialog
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update task: {str(e)}")

    def clearTaskFields(self): # Renamed for clarity
        # Potentially reset to original data or just clear
        self.ui.task_name_info.clear()
        self.ui.task_id_info.clear() # Or reset to self.originalID
        self.ui.task_shortDescrip_info.clear()
        self.ui.task_status_info.setCurrentIndex(0)
        self.ui.task_project_info.setCurrentIndex(0)
        self.ui.task_dueDate_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))
        self.ui.task_dateAccomplished_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))


class TaskExpandDialog(QDialog):
    def __init__(self, task_data, main_window_instance, parent=None):
        super().__init__(parent)
        self.ui = Ui_tasks_expand()
        self.ui.setupUi(self)
        self.task_data = task_data
        self.main_window = main_window_instance # Reference to MainApp

        self.setWindowTitle(f"Task Details: {self.task_data.get('taskName', 'N/A')}")
        self._populate_data()
        self._connect_signals()

    def _populate_data(self):
        if not self.task_data:
            QMessageBox.warning(self, "Data Error", "No task data to display.")
            return

        task_id = self.task_data.get('taskID', 'N/A')
        self.ui.task_name.setText(self.task_data.get('taskName', 'N/A'))
        self.ui.task_id_info.setText(task_id)
        self.ui.task_project_info.setText(self.task_data.get('projectID', 'N/A'))
        self.ui.task_status_info.setText(self.task_data.get('currentStatus', 'N/A'))

        due_date_val = self.task_data.get('dueDate')
        if isinstance(due_date_val, datetime):
            self.ui.task_dueDate_info.setText(due_date_val.strftime('%B %d, %Y'))
        elif isinstance(due_date_val, str):
            try:
                dt_obj = datetime.strptime(due_date_val, '%Y-%m-%d %H:%M:%S') # Adjust format if needed
                self.ui.task_dueDate_info.setText(dt_obj.strftime('%B %d, %Y'))
            except ValueError:
                 try:
                    dt_obj = datetime.strptime(due_date_val, '%Y-%m-%d')
                    self.ui.task_dueDate_info.setText(dt_obj.strftime('%B %d, %Y'))
                 except ValueError:
                    self.ui.task_dueDate_info.setText(due_date_val) # Fallback
        else:
            self.ui.task_dueDate_info.setText('N/A')

        accomplished_date_val = self.task_data.get('dateAccomplished')
        if accomplished_date_val:
            if isinstance(accomplished_date_val, datetime):
                self.ui.task_dateAccomplished_info.setText(accomplished_date_val.strftime('%B %d, %Y'))
            elif isinstance(accomplished_date_val, str):
                try:
                    dt_obj = datetime.strptime(accomplished_date_val, '%Y-%m-%d %H:%M:%S') # Adjust format
                    self.ui.task_dateAccomplished_info.setText(dt_obj.strftime('%B %d, %Y'))
                except ValueError:
                    try:
                        dt_obj = datetime.strptime(accomplished_date_val, '%Y-%m-%d')
                        self.ui.task_dateAccomplished_info.setText(dt_obj.strftime('%B %d, %Y'))
                    except ValueError:
                        self.ui.task_dateAccomplished_info.setText(accomplished_date_val) # Fallback
            else:
                self.ui.task_dateAccomplished_info.setText('N/A')
        else:
            self.ui.task_dateAccomplished_info.setText('Not Accomplished')


        self.ui.task_shortDescrip_info.setPlainText(self.task_data.get('shortDescrip', ''))
        self.ui.task_shortDescrip_info.setReadOnly(True)

        # Populate Members
        self.ui.task_members_info.clear()
        members = getMembersForTask(task_id)
        if members:
            for member in members:
                item_text = f"{member.get('fullname', 'Unnamed Member')} (ID: {member.get('memberID', 'N/A')})"
                self.ui.task_members_info.addItem(QListWidgetItem(item_text))
        else:
            self.ui.task_members_info.addItem(QListWidgetItem("No members assigned to this task."))

    def _connect_signals(self):
        self.ui.task_update_button.clicked.connect(self._handle_update)
        self.ui.task_delete_button.clicked.connect(self._handle_delete)

    def _handle_update(self):
        self.accept() # Close this dialog
        edit_task_dialog = EditTaskForm(self.main_window, self.task_data.get('taskID'))
        edit_task_dialog.exec()

    def _handle_delete(self):
        task_id = self.task_data.get('taskID')
        task_name = self.task_data.get('taskName', 'this task')
        
        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete task '{task_name}' ({task_id})? This action cannot be undone.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                deleteTask(task_id) # Use the deleteTask controller function
                QMessageBox.information(self, "Success", f"Task '{task_name}' has been deleted.")
                self.main_window.refresh_container('task') # Refresh the main task list
                self.main_window.refresh_container('project') # Refresh the main project 
                self.main_window.refresh_container('home') # Refresh the main member list
                self.main_window.refreshTable()
                
                self.main_window.clear_task_details_pane() # Clear details pane
                self.accept() # Close this dialog
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete task: {str(e)}")


class TaskView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        task_board = loadTasks(self)
        layout.addWidget(task_board)
        self.setLayout(layout)

