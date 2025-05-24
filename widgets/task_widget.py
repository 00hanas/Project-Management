from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class TaskWidget(QWidget):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.setFixedSize(250, 150)  # Make it rectangular
        
        # Style the widget as a card
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Task name in bold
        name_label = QLabel(f"<b>{task_data['taskName']}</b>")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Description
        if task_data.get('shortDescrip'):
            desc_label = QLabel(task_data['shortDescrip'])
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Due date
        if task_data.get('dueDate'):
            layout.addWidget(QLabel(f"Due: {task_data['dueDate']}"))
            
        # Project ID
        layout.addWidget(QLabel(f"Project: {task_data['projectID']}"))
        
        self.setLayout(layout)