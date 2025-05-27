from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QScrollArea, QVBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from controllers.project_controller import getAllProjects
from widgets.ProjectCardWidget import ProjectCardWidget

def loadProjects(parent=None) -> QWidget:
    # Main container
    container = QWidget(parent) #whole projects display area
    container.setObjectName("#ProjectVContainer")
    container.setStyleSheet("""
        #ProjectVContainer {
            background-color: transparent;
            border-radius: 0px;
            margin: 0px;
            padding: 0px;
        }
    """)
    
    # Create scroll area
    scroll = QScrollArea(container)
    scroll.setObjectName("ProjectScrollArea")
    scroll.setStyleSheet("""
        #ProjectScrollArea {
            background-color: transparent;
        }
        QScrollBar:vertical {
            background: transparent;
            width: 12px;
            margin: 0px;
            border-radius: 8px;
        }

        QScrollBar::handle:vertical {
            background: transparent;  /* Or use transparent if you want it invisible */
            min-height: 2px;
            border-radius: 6px;
            border: none;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: transparent;
            border: none;
        }

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: transparent;
        }
        """)
    scroll.setWidgetResizable(True)
    
    # Content widget
    content = QWidget() #card
    content.setMinimumHeight(0) 
    content.setObjectName("scrollContent")
    content.setStyleSheet("""
        #scrollContent {
            background-color: transparent;
            border-radius: 0px;
            margin: 0px;
            padding: 0px;
        }
        """)
    
    # Grid layout
    grid = QGridLayout(content)
    grid.setAlignment(Qt.AlignmentFlag.AlignTop)
    grid.setContentsMargins(1, 0, 1, 0)  # Margins around the grid
    grid.setVerticalSpacing(0)

    # Add projects
    projects = getAllProjects()
    columns = 2
    headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]
    
    for index, project in enumerate(projects):
        project_dict = dict(zip(headers, project))
        project_widget = ProjectCardWidget(project_dict)
        
        # Connect the click signal to the parent's update_project_details method
        if hasattr(parent, 'update_project_details'):
            project_widget.clicked.connect(parent.update_project_details)
        
        row = index // columns
        col = index % columns
        grid.addWidget(project_widget, row, col)

    columns = 2
    card_height = 150  
    rows = (len(projects) + columns - 1) // columns

    content.setFixedHeight(rows * card_height)
    spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    grid.addItem(spacer, grid.rowCount(), 0, 1, columns)

    scroll.setWidget(content)
    layout = QGridLayout(container)
    layout.addWidget(scroll)
    container.setLayout(layout)
    return container






