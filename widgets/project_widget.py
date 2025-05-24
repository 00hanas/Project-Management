from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ProjectWidget(QWidget):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)  # Make it square (adjust size as needed)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel(f"<b>{project_data['projectName']}</b>"))
        layout.addWidget(QLabel(project_data.get('shortDescrip', '')))
        layout.addWidget(QLabel(f"Start: {project_data.get('startDate', '')}"))
        layout.addWidget(QLabel(f"End: {project_data.get('endDate', '')}"))
        self.setLayout(layout)
        
