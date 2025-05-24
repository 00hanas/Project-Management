from dataclasses import dataclass
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from controllers.task_controller import getAllTasks
from widgets.task_widget import TaskWidget



def loadTasks(parent=None) -> QWidget:
    container = QWidget(parent)
    main_layout = QHBoxLayout(container)
    
    # Define status columns
    statuses = ["Unassigned", "Pending", "In Progress", "Completed"]
    
    # Get all tasks
    tasks = getAllTasks()
    
    # Create a column for each status
    for status in statuses:
        # Create a column
        column = QWidget()
        column_layout = QVBoxLayout(column)
        
        # Add header
        header = QLabel(status)
        header.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """)
        column_layout.addWidget(header)
        
        # Create scrollable area for tasks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Add tasks that match this status
        for task in tasks:
            current_status = task.get('currentStatus', 'Unassigned')
            if current_status == status:
                task_widget = TaskWidget(task)
                scroll_layout.addWidget(task_widget)
        
        # Add stretcher at the bottom
        scroll_layout.addStretch()
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        column_layout.addWidget(scroll)
        
        # Add column to main layout
        main_layout.addWidget(column)
    
    container.setLayout(main_layout)
    return container