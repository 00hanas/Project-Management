from PyQt6.QtWidgets import QDialog, QWidget, QScrollArea, QGridLayout, QVBoxLayout, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QDateTime, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from models.project import loadProjects
from controllers.project_controller import addProject, getProjectByID, updateProject, getAllProjects, deleteProject, getMembersForProject
from controllers.task_controller import getTasksByProjectID # Import the new function
from ui.addproject_interface import Ui_addproject_dialog
from ui.projects_expand import Ui_projects_expand # Import the expand UI
from utils.project_validators import uniqueProject, uniqueEditProject
from datetime import datetime

class AddProjectForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addproject_dialog()
        self.ui.setupUi(self)

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.project_id_info.setValidator(id_validator)

        self.ui.project_save_button.clicked.connect(self.saveProject)
        self.ui.project_clear_button.clicked.connect(self.clearProject)
        self.ui.project_cancel_button.clicked.connect(self.cancelProject)

    def validate_dates(self):
        """Validate that end date is not before start date, allowing empty or default dates"""
        start_date = self.ui.project_startDate_info.dateTime()
        end_date = self.ui.project_endDate_info.dateTime()
        
        # Check if end date is default/unset value (January 1, 2000 12:00 AM)
        default_date = QDateTime(2000, 1, 1, 0, 0)
        if end_date == default_date:
            self.ui.project_endDate_info.setToolTip("")
            return True
        
        if end_date < start_date:
            self.ui.project_endDate_info.setToolTip("End date cannot be before start date")
            return False
        else:
            self.ui.project_endDate_info.setToolTip("")
            return True

    def saveProject(self):
        project_id = self.ui.project_id_info.text().strip()
        name = self.ui.project_name_info.text().strip()
        desc = self.ui.project_shortDescrip_info.toPlainText()
        start = self.ui.project_startDate_info.text().strip()
        end = self.ui.project_endDate_info.text().strip()

        if not project_id or not name:
            QMessageBox.warning(self, "Input Error", "Project ID and Name cannot be empty.")
            return
        
        # Validate dates before proceeding
        if not self.validate_dates():
            QMessageBox.warning(self, "Date Error", "End date cannot be before start date")
            return
        
        error = uniqueProject(project_id)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return

        start = datetime.strptime(start, "%d/%m/%Y %I:%M %p")

        # Handle case where end date is default/unset value
        default_date = QDateTime(2000, 1, 1, 0, 0)
        if self.ui.project_endDate_info.dateTime() == default_date:
            end = None
        else:
            end = datetime.strptime(end, "%d/%m/%Y %I:%M %p")

        addProject({
            "projectID": project_id,
            "projectName": name,
            "shortDescrip": desc,
            "startDate": start,
            "endDate": end
        })

        self.main_window.refresh_container('project')

        QMessageBox.information(self, "Success", "Project saved successfully.")
        self.close()

    def clearProject(self):
        self.ui.project_name_info.clear()
        self.ui.project_id_info.clear()
        self.ui.project_shortDescrip_info.clear()
        self.ui.project_startDate_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))
        self.ui.project_endDate_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))

    def cancelProject(self):
        self.close()

class EditProjectForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addproject_dialog()
        self.ui.setupUi(self)
        self.originalID = originalID

        # Set up ID validator
        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.project_id_info.setValidator(id_validator)

        # Load existing data into the form
        data = getProjectByID(originalID)
        if data:
            self.ui.project_id_info.setText(data["projectID"])
            self.ui.project_name_info.setText(data["projectName"])
            self.ui.project_shortDescrip_info.setText(data["shortDescrip"])

            # Convert string dates to QDateTime for the date/time editors
            if data["startDate"]:
                if isinstance(data["startDate"], str):
                    start_date = datetime.strptime(data["startDate"], '%Y-%m-%d %H:%M:%S')
                else:
                    start_date = data["startDate"]
                self.ui.project_startDate_info.setDateTime(QDateTime(start_date)) # Use QDateTime constructor with datetime object

            if data["endDate"]:
                if isinstance(data["endDate"], str):
                    end_date = datetime.strptime(data["endDate"], '%Y-%m-%d %H:%M:%S')
                else:
                    end_date = data["endDate"]
                self.ui.project_endDate_info.setDateTime(QDateTime(end_date)) # Use QDateTime constructor with datetime object


        # Connect buttons
        self.ui.project_save_button.clicked.connect(self.saveProject)
        # self.ui.project_clear_button.clicked.connect(self.clearProject) # Remove or comment out this line
        self.ui.project_cancel_button.clicked.connect(self.cancelProject)

    def saveProject(self):
        project_id = self.ui.project_id_info.text().strip()
        name = self.ui.project_name_info.text().strip()
        desc = self.ui.project_shortDescrip_info.toPlainText().strip()
        start = self.ui.project_startDate_info.text().strip()
        end = self.ui.project_endDate_info.text().strip()

        if not project_id or not name:
            QMessageBox.warning(self, "Input Error", "Project ID and Name cannot be empty.")
            return

        error = uniqueEditProject(project_id, self.originalID)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return

        # Ensure correct format for parsing dates from QDateTimeEdit
        start = datetime.strptime(start, "%d/%m/%Y %I:%M %p") # Corrected format string
        end = datetime.strptime(end, "%d/%m/%Y %I:%M %p") # Corrected format string


        try:
            updated_data = { # Store updated data in a dictionary
                "projectID": project_id,
                "projectName": name,
                "shortDescrip": desc,
                "startDate": start,
                "endDate": end
            }
            updateProject(self.originalID, updated_data)


            # Refresh container
            self.main_window.refresh_container('project')

            # Update the details pane with the saved project data
            self.main_window.update_project_details(updated_data)


            QMessageBox.information(self, "Success", "Project updated successfully.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update project: {str(e)}")

    def clearProject(self):
        # This method is not needed for EditProjectForm, but keeping it here
        # to avoid potential issues if it's called elsewhere unexpectedly.
        # However, the connection in __init__ should be removed.
        pass

    def cancelProject(self):
        self.close()


class ProjectExpandDialog(QDialog):
    def __init__(self, project_data, main_window_instance, parent=None):
        super().__init__(parent)
        self.ui = Ui_projects_expand()
        self.ui.setupUi(self)
        self.project_data = project_data
        self.main_window = main_window_instance # Reference to MainApp

        self.setWindowTitle(f"Project Details: {self.project_data.get('projectName', 'N/A')}")
        self._populate_data()
        self._connect_signals()

    def _populate_data(self):
        if not self.project_data:
            QMessageBox.warning(self, "Data Error", "No project data to display.")
            return

        project_id = self.project_data.get('projectID', 'N/A')
        self.ui.project_name.setText(self.project_data.get('projectName', 'N/A'))
        self.ui.project_id_info.setText(project_id)

        start_date_val = self.project_data.get('startDate')
        if isinstance(start_date_val, datetime):
            self.ui.project_startDate_info.setText(start_date_val.strftime('%B %d, %Y'))
        elif isinstance(start_date_val, str):
             try:
                dt_obj = datetime.strptime(start_date_val, '%Y-%m-%d %H:%M:%S')
                self.ui.project_startDate_info.setText(dt_obj.strftime('%B %d, %Y'))
             except ValueError:
                self.ui.project_startDate_info.setText(start_date_val) # Fallback
        else:
            self.ui.project_startDate_info.setText('N/A')

        end_date_val = self.project_data.get('endDate')
        if isinstance(end_date_val, datetime):
            self.ui.project_endDate_info.setText(end_date_val.strftime('%B %d, %Y'))
        elif isinstance(end_date_val, str):
            try:
                dt_obj = datetime.strptime(end_date_val, '%Y-%m-%d %H:%M:%S')
                self.ui.project_endDate_info.setText(dt_obj.strftime('%B %d, %Y'))
            except ValueError:
                self.ui.project_endDate_info.setText(end_date_val) # Fallback
        else:
            self.ui.project_endDate_info.setText('N/A')

        self.ui.project_shortDescrip_info.setPlainText(self.project_data.get('shortDescrip', ''))
        self.ui.project_shortDescrip_info.setReadOnly(True) # Description is view-only here

        # Populate Tasks
        self.ui.project_tasks_info.clear()
        tasks = getTasksByProjectID(project_id)
        if tasks:
            for task in tasks:
                item_text = f"{task.get('taskName', 'Unnamed Task')} (ID: {task.get('taskID', 'N/A')})"
                self.ui.project_tasks_info.addItem(QListWidgetItem(item_text))
        else:
            self.ui.project_tasks_info.addItem(QListWidgetItem("No tasks assigned to this project."))

        # Populate Members
        self.ui.project_members_info.clear()
        members = getMembersForProject(project_id)
        if members:
            for member in members:
                item_text = f"{member.get('fullname', 'Unnamed Member')} (ID: {member.get('memberID', 'N/A')})"
                self.ui.project_members_info.addItem(QListWidgetItem(item_text))
        else:
            self.ui.project_members_info.addItem(QListWidgetItem("No members assigned to this project."))

    def _connect_signals(self):
        self.ui.project_update_button.clicked.connect(self._handle_update)
        self.ui.project_delete_button.clicked.connect(self._handle_delete)

    def _handle_update(self):
        # Open the EditProjectForm
        self.accept() # Close this dialog
        edit_dialog = EditProjectForm(self.main_window, self.project_data.get('projectID'))
        edit_dialog.exec()

    def _handle_delete(self):
        project_id = self.project_data.get('projectID')
        project_name = self.project_data.get('projectName', 'this project')
        
        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete project '{project_name}' ({project_id})? This action cannot be undone.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                deleteProject(project_id)
                QMessageBox.information(self, "Success", f"Project '{project_name}' has been deleted.")
                self.main_window.refresh_container('project') # Refresh the main list
                self.accept() # Close this dialog
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete project: {str(e)}")

class ProjectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)  # Main layout for the Project Section
        project_grid = loadProjects(self)
        layout.addWidget(project_grid)
        self.setLayout(layout)
