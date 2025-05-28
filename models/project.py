from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QScrollArea, QVBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from controllers.project_controller import getAllProjects, sortProjects
from widgets.ProjectCardWidget import ProjectCardWidget

def loadProjects(parent=None, projects_data=None) -> QWidget:
    """Load projects into a container. If projects_data is provided, use that instead of fetching from database."""
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
            background: transparent;
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
    content = QWidget()
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
    grid.setContentsMargins(1, 0, 1, 0)
    grid.setVerticalSpacing(0)
    content.setLayout(grid) 

    # Get projects data - either from parameter or database
    if projects_data is None:
        projects = getAllProjects()
    else:
        projects = projects_data

    columns = 3
    headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]
    
    # Handle both tuple and dict formats
    for index, project in enumerate(projects):
        if isinstance(project, tuple):
            project_dict = dict(zip(headers, project))
        else:  # Assume it's already a dict
            project_dict = project
            
        project_widget = ProjectCardWidget(project_dict)
        
        row = index // columns
        col = index % columns
        grid.addWidget(project_widget, row, col)

    card_height = 150  
    rows = (len(projects) + columns - 1) // columns
    content.setFixedHeight(rows * card_height)
    
    # Add spacer
    spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    grid.addItem(spacer, grid.rowCount(), 0, 1, columns)

    scroll.setWidget(content)
    
    # Main layout
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(scroll)
    container.setLayout(layout)
    return container

def loadOnGoingProjects(parent=None, projects_data=None) -> QWidget:
    """Load projects that have at least one task not completed."""
    from controllers.task_controller import getTasksByProject  # Import here to avoid circular imports
    
    # Main container (same as before)
    container = QWidget(parent)
    container.setObjectName("ProjectHomeContainer")
    container.setStyleSheet("""
        #ProjectHomeContainer {
            background-color: transparent;
            border-radius: 0px;
            margin: 0px;
            padding: 0px;
        }
    """)
    
    # Create scroll area (same as before)
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
            background: transparent;
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
    
    # Content widget (same as before)
    content = QWidget()
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
    
    # Grid layout (same as before)
    grid = QGridLayout(content)
    grid.setAlignment(Qt.AlignmentFlag.AlignTop)
    grid.setContentsMargins(1, 0, 1, 0)
    grid.setVerticalSpacing(0)
    content.setLayout(grid) 

    # Get projects data
    if projects_data is None:
        projects = getAllProjects()
    else:
        projects = projects_data

    columns = 3
    headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]
    
    # Filter ongoing projects (projects with at least one incomplete task)
    ongoing_projects = []
    for project in projects:
        if isinstance(project, tuple):
            project_dict = dict(zip(headers, project))
        else:  # Assume it's already a dict
            project_dict = project
            
        # Get all tasks for this project
        tasks = getTasksByProject(project_dict['projectID'])
        
        # Check if any task is not completed
        has_incomplete_task = any(task['currentStatus'] != 'Completed' for task in tasks)
        
        if has_incomplete_task:
            ongoing_projects.append(project_dict)

    # Add project widgets to grid
    for index, project in enumerate(ongoing_projects):
        project_widget = ProjectCardWidget(project)
        row = index // columns
        col = index % columns
        grid.addWidget(project_widget, row, col)

    card_height = 150  
    rows = (len(ongoing_projects) + columns - 1) // columns
    content.setFixedHeight(rows * card_height)
    
    # Add spacer
    spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    grid.addItem(spacer, grid.rowCount(), 0, 1, columns)

    scroll.setWidget(content)
    
    # Main layout
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(scroll)
    container.setLayout(layout)
    return container    