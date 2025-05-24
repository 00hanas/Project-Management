from config.db_config import getConnection
from PyQt6.QtWidgets import QDialog, QWidget, QScrollArea, QGridLayout, QVBoxLayout
from models.project import loadProject
from controllers.project_controller import addProject, getProjectByID, updateProject, getAllProjects
from widgets.project_widget import ProjectWidget

class AddProjectForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_ProjectForm()  # Replace with your actual UI class
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.saveProject)

    def saveProject(self):
        project_id = self.ui.lineEdit.text().strip()      # Assume
        name = self.ui.lineEdit_1.text().strip()          # Assume
        desc = self.ui.lineEdit_2.text().strip()          # Assume
        start = self.ui.lineEdit_3.text().strip()         # Assume
        end = self.ui.lineEdit_4.text().strip()           # Assume

        addProject({
            "projectID": project_id,
            "projectName": name,
            "shortDescrip": desc,
            "startDate": start,
            "endDate": end
        })

class EditProjectForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_ProjectForm()  # Replace with your actual UI class
        self.ui.setupUi(self)

        # Load existing data into the form
        data = getProjectByID(originalID)
        if data:
            self.ui.lineEdit.setText(data["projectID"])
            self.ui.lineEdit_1.setText(data["projectName"])
            self.ui.lineEdit_2.setText(data["shortDescrip"])
            self.ui.lineEdit_3.setText(data["startDate"])
            self.ui.lineEdit_4.setText(data["endDate"])

        self.ui.pushButton.clicked.connect(self.saveProject)

    def saveProject(self):
        project_id = self.ui.lineEdit.text().strip()
        name = self.ui.lineEdit_1.text().strip()
        desc = self.ui.lineEdit_2.text().strip()
        start = self.ui.lineEdit_3.text().strip()
        end = self.ui.lineEdit_4.text().strip()

        updateProject(self.originalID, {
            "projectID": project_id,
            "projectName": name,
            "shortDescrip": desc,
            "startDate": start,
            "endDate": end
        })
        
        
class loadProject (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        scroll = QScrollArea(self) 
        scroll.setWidgetResizable(True) 
        container = QWidget() 
        grid = QGridLayout(container) # create a grid layout to organize widgets inside the container widget
        grid.setSpacing(10)

        projects = getAllProjects() # get all projects from the controller, returns a list of tuples
        columns = 3
        headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]
        # Create a ProjectWidget for each project and add it to the grid layout
        for index, project in enumerate(projects):
            # Convert each project tuple to a dictionary using headers
            project_dict = dict(zip(headers, project))
            project_widget = ProjectWidget(project_dict)
            row = index // columns
            col = index % columns
            grid.addWidget(project_widget, row, col)

        scroll.setWidget(container)
        layout = QGridLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

class ProjectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)  # Main layout for the Project Section
        project_grid = loadProject(self)
        layout.addWidget(project_grid)
        self.setLayout(layout)