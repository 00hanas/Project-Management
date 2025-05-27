from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QScrollArea, QVBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from controllers.project_controller import getAllProjects
from widgets.ProjectCardWidget import ProjectCardWidget

def loadProjects(parent=None) -> QWidget:
    # Main container
    container = QWidget(parent)
    container.setObjectName("ProjectVContainer")
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
    
    # Grid layout - Updated settings
    grid = QGridLayout(content)  # Changed from scroll to content
    grid.setAlignment(Qt.AlignmentFlag.AlignTop)
    grid.setContentsMargins(1, 0, 1, 0)  # Margins around the grid
    grid.setVerticalSpacing(0)
    content.setLayout(grid) 

    # Add projects
    projects = getAllProjects()
    columns = 3
    headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]
    
        
    for index, project in enumerate(projects):
        project_dict = dict(zip(headers, project))
        project_widget = ProjectCardWidget(project_dict)
        
        row = index // columns
        col = index % columns
        grid.addWidget(project_widget, row, col)

    card_height = 150  
    rows = (len(projects) + columns - 1) // columns

    content.setFixedHeight(rows * card_height)
    spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    grid.addItem(spacer, grid.rowCount(), 0, 1, columns)

    scroll.setWidget(content)
    
    # Main layout
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(scroll)
    container.setLayout(layout)
    return container





