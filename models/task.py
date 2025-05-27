from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QScrollArea, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
)
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from controllers.task_controller import getAllTasks
from widgets.TaskCardWidget import TaskCardWidget



def loadTasks(parent=None) -> QWidget:
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
        #TaskcrollArea {
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
    content = QWidget()
    content.setMaximumHeight(650)
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
    grid.setContentsMargins(0, 10, 5, 10)  # Margins around the grid
    grid.setVerticalSpacing(5)     # Increased from 2 to 10
    grid.setHorizontalSpacing(10)   # Added horizontal spacing

    columns = 2
    
    try:
        tasks = getAllTasks()
        if not tasks:
            # Add an empty state message
            empty_label = QLabel("No tasks found")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(empty_label, 0, 0, 1, 2)
        else:
            for index, task in enumerate(tasks):
                try:
                    task_widget = TaskCardWidget(task)
                    
                    # Connect the click signal to the parent's update_task_details method
                    if hasattr(parent, 'update_task_details'):
                        task_widget.clicked.connect(parent.update_task_details)
                    
                    row = index // columns
                    col = index % columns
                    grid.addWidget(task_widget, row, col)
                    
                    
                except Exception as e:
                    print(f"Error creating task widget: {e}")
                    
            # spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            # grid.addItem(spacer, (len(tasks) // columns) + 1, 0, 1, columns)

    except Exception as e:
        print(f"Error loading tasks: {e}")

    scroll.setWidget(content)
    layout = QGridLayout(container)
    layout.addWidget(scroll)
    container.setLayout(layout)
    return container