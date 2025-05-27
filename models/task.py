from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QScrollArea, QVBoxLayout, QLabel
)
from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from controllers.task_controller import getAllTasks
from widgets.TaskCardWidget import TaskCardWidget



def loadTasks(parent=None) -> QWidget:
    # Main container
    container = QWidget(parent)
    container.setObjectName("#TaskVContainer")
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
                    task_widget.setSizePolicy(
                        QtWidgets.QSizePolicy.Policy.Preferred,  # Horizontal policy
                        QtWidgets.QSizePolicy.Policy.Preferred   # Vertical policy
                    )
                    row = index // columns
                    col = index % columns
                    grid.addWidget(task_widget, row, col)
                except Exception as e:
                    print(f"Error creating task widget: {e}")
    except Exception as e:
        error_label = QLabel(f"Error loading tasks: {e}")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(error_label, 0, 0, 1, 2)

    scroll.setWidget(content)
    layout = QGridLayout(container)
    layout.addWidget(scroll)
    container.setLayout(layout)
    return container