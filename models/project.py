from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea
from controllers.project_controller import getAllProjects
from widgets.project_widget import ProjectWidget

def loadProject(parent=None) -> QWidget:
    container = QWidget(parent)
    scroll = QScrollArea(container) 
    scroll.setWidgetResizable(True) 
    
    content = QWidget() 
    grid = QGridLayout(content)
    grid.setSpacing(10)

    projects = getAllProjects()
    columns = 3
    headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]
    
    for index, project in enumerate(projects):
        project_dict = dict(zip(headers, project))
        project_widget = ProjectWidget(project_dict)
        row = index // columns
        col = index % columns
        grid.addWidget(project_widget, row, col)

    scroll.setWidget(content)
    layout = QGridLayout(container)
    layout.addWidget(scroll)
    container.setLayout(layout)
    
    return container






