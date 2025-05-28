from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QScrollArea, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
)
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from controllers.task_controller import getAllTasks, getMembersForTask
from widgets.TaskCardWidget import TaskCardWidget


def loadTasks(parent=None, tasks_data=None) -> QWidget:
    """Load tasks into a container. If tasks_data is provided, use that instead of fetching from database."""
    # Main container
    container = QWidget(parent)
    container.setObjectName("TaskVContainer")
    container.setStyleSheet("""
        #TaskVContainer {
            background-color: transparent;
            border-radius: 0px;
            margin: 0px;
            padding: 0px;
        }
    """)
    
    # Create scroll area
    scroll = QScrollArea(container)
    scroll.setObjectName("TaskScrollArea")
    scroll.setStyleSheet("""
        #TaskScrollArea {
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
    
    # Get tasks data - either from parameter or database
    if tasks_data is None:
        tasks = getAllTasks()
    else:
        tasks = tasks_data

    columns = 3
    headers = ["taskID", "taskName", "shortDescrip", "currentStatus", "dueDate", "dateAccomplished", "projectID"]
    
    try:
        if not tasks:
            # Add an empty state message
            empty_label = QLabel("No tasks found")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(empty_label, 0, 0, 1, columns)
        else:
            for index, task in enumerate(tasks):
                try:
                    # Get the number of members for the task
                    taskID = task['taskID']
                    NoOFMembers = len(getMembersForTask(taskID))
                    
                    # Set the current status based on the number of members
                    if NoOFMembers == 0:
                        task['currentStatus'] = 'Unassigned'
                    elif task.get('dateAccomplished') is None:
                        task['currentStatus'] = 'Pending'
                        
                    task_widget = TaskCardWidget(task)
                    
                    # Connect the click signal to the parent's update_task_details method
                    if hasattr(parent, 'update_task_details'):
                        task_widget.clicked.connect(parent.update_task_details)
                    
                    row = index // columns
                    col = index % columns
                    grid.addWidget(task_widget, row, col)
                    
                except Exception as e:
                    print(f"Error creating task widget: {e}")

            # Calculate height
            card_height = 170  
            rows = (len(tasks) + columns - 1) // columns
            content.setFixedHeight(rows * card_height)

    except Exception as e:
        print(f"Error loading tasks: {e}")

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