from PyQt6.QtWidgets import QDialog, QWidget, QScrollArea, QGridLayout, QVBoxLayout, QMessageBox
from PyQt6.QtCore import QDateTime, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from models.project import loadProjects
from controllers.project_controller import addProject, getProjectByID, updateProject, getAllProjects
from widgets.ProjectCardWidget import ProjectCardWidget
from ui.addproject_interface import Ui_addproject_dialog
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

        loadProjects(self.main_window)
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
        self.ui = Ui_addproject_dialog()  # Replace with your actual UI class
        self.ui.setupUi(self)

        self.originalID = originalID
        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.project_id_info.setValidator(id_validator)  # Assuming lineEdit is for project ID

        # Load existing data into the form
        data = getProjectByID(originalID)
        if data:
            self.ui.project_id_info.setText(data["projectID"])
            self.ui.project_name_info.setText(data["projectName"])
            self.ui.project_shortDescrip_info.setText(data["shortDescrip"])
            self.ui.project_startDate_info.setText(data["startDate"])
            self.ui.project_endDate_info.setText(data["endDate"])

        self.ui.project_save_button.clicked.connect(self.saveProject)
        self.ui.project_clear_button.clicked.connect(self.clearProject)
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
        
        start = datetime.strptime(start, "%d/%m/%Y %I:%M %p")

        end = datetime.strptime(end, "%d/%m/%Y %I:%M %p")

        updateProject(self.originalID, {
            "projectID": project_id,
            "projectName": name,
            "shortDescrip": desc,
            "startDate": start,
            "endDate": end
        })

        # insert here statement to load the widgets #

        QMessageBox.information(self, "Success", "Project updated successfully.")
        self.close()        

    def clearProject(self):
        self.ui.project_name_info.clear()
        self.ui.project_id_info.clear()
        self.ui.project_shortDescrip_info.clear()
        self.ui.project_startDate_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))
        self.ui.project_endDate_info.setDateTime(QDateTime(2000, 1, 1, 0, 0))

    def cancelProject(self):
        self.close()
        

class ProjectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)  # Main layout for the Project Section
        project_grid = loadProjects(self)
        layout.addWidget(project_grid)
        self.setLayout(layout)