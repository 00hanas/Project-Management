from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import QSize, Qt, pyqtSignal  # Add this import
from PyQt6.QtGui import QIcon, QCursor
from controllers.project_controller import getTotalTasks, getCompletedTasks, getMembersForProject
from datetime import datetime


class ProjectCardWidget(QWidget):
    clicked = pyqtSignal(dict)  # Signal is already defined

    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.project_data = project_data  # Store the project data
        self.setObjectName("ProjectCard")


        self.setMinimumSize(QSize(200, 220))
        self.setMaximumSize(QSize(800, 220))


        container_layout  = QVBoxLayout(self)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(12, 0, 6, 0)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        content = QWidget()
        content.setObjectName("content")
        content.setStyleSheet("""
            #content {
                background-color: #84BDFF;
                border-radius: 8px;
                }
                """)
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(0)  # No space between widgets
        content_layout.setContentsMargins(0, 0, 0, 0)

        toprow = QWidget()
        toprow.setObjectName("toprow")
        toprow.setStyleSheet("""
            #toprow {
                background-color: #4A90E2;
                border-top-right-radius: 8px 8px;\
                border-top-left-radius: 8px 8px;\
                border-bottom-right-radius: 0px 0px;\
                border-bottom-left-radius: 0px 0px;\
                margin-bottom: 0px;\
                padding: 0px;\
            }\
            QLabel {\
                background-color: transparent;\
                color: white;\
                border-radius: 0px;\
                margin: 0px;\
                margin-left: 2px;\
                padding: 0px;\
            }\
        """)
        toprow_layout = QHBoxLayout()
        ProjectIDBase = QLabel("Project ID:")
        ProjectIDBase.setStyleSheet("color: white; font-weight: bold;")
        ProjectIDLabel = QLabel(f"{project_data['projectID']} ")
        toprow_layout.addWidget(ProjectIDBase)
        toprow_layout.addStretch()
        toprow_layout.addWidget(ProjectIDLabel)
        toprow.setLayout(toprow_layout)

        secrow = QWidget()
        secrow.setObjectName("secrow")
        secrow.setStyleSheet("""
            #secrow {
                background-color: #DBECFF;
                border-radius: 0px;
                margin: 0px;
                padding: 0px;
            }
            QLabel {
                background-color: transparent;
                font-size: 12px;
                font-weight: bold;
                color: #2A2A2A;
                margin: 0px;
                margin-left: 2px;
                padding: 0px;
                border-radius: 0px;
            }
        """)

        secrow_layout = QHBoxLayout()
        ProjectNameLabel = QLabel(f"{project_data['projectName']}")
        ProjectNameLabel.setObjectName("ProjectNameLabel")
        secrow_layout.addWidget(ProjectNameLabel)
        secrow.setLayout(secrow_layout)

        thirdrow = QWidget()
        thirdrow.setObjectName("thirdrow")
        thirdrow.setStyleSheet("""
            #thirdrow {
                background-color: #DBECFF;
                border-radius: 0px;
                margin: 0px;
                padding: 0px;
            }
        """)

        thirdrow_layout = QHBoxLayout()
        thirdrow_layout.setContentsMargins(10, 0, 10, 8)
        ProjectProgressBar = QProgressBar()
        ProjectProgressBar.setMaximumHeight(10)
        ProjectProgressBar.setObjectName("ProjectProgressBar")
        ProjectProgressBar.setStyleSheet("""
            #ProjectProgressBar {
                background-color: #9EC2FF;
                border-radius: 5px;
                margin: 0px;
                margin-left: 5px;
                margin-right: 5px;
                padding: 0px;
            }
            #ProjectProgressBar::chunk {
                background-color: #0350D5;
                border-radius: 5px;
                margin: 0px;
                margin-left: 0px;
                padding: 0px;
            }
            """)

        total = getTotalTasks(project_data['projectID'])
        completed = getCompletedTasks(project_data['projectID'])
        progress = int((completed/total)*100) if total > 0 else 0
        ProjectProgressBar.setValue(progress)
        ProjectProgressBar.setTextVisible(False)
        thirdrow_layout.addWidget(ProjectProgressBar)
        thirdrow.setLayout(thirdrow_layout)



        lastrow = QWidget()
        lastrow.setObjectName("lastrow")
        lastrow.setStyleSheet("""
            #lastrow {
                background-color: #DBECFF;
                border: none;
                border-radius: 0px;
                border-bottom-right-radius: 8px 8px;
                border-bottom-left-radius: 8px 8px;
                border-bottom: solid;
                border-bottom-color: #DBECFF;
                border-bottom-width: 8px;

                margin: 0px;
                padding: 0px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                padding: 0px;
                margin: 0px;
            }
            QLabel {
                background-color: transparent;
                font-size: 12px;
                font-weight: bold;
                color: #4A90E2;
                margin: 0px;
                padding: 0px;
            }
        """)

        lastrow_layout = QHBoxLayout()
        lastrow_layout.setContentsMargins(10, 0, 10, 10)

        ProjectEndDateIcon = QPushButton()
        ProjectEndDateIcon.setObjectName("ProjectEndDateIcon")
        ProjectEndDateIcon.setStyleSheet("""
            #ProjectEndDateIcon {
                margin-left: 4px;
            }
            """)
        ProjectEndDateIcon.setIcon(QIcon("icons/projectdue.svg"))
        ProjectEndDateIcon.setMaximumSize(QSize(20, 20))
        ProjectEndDateIcon.setMinimumSize(QSize(20, 20))
        ProjectEndDateLabel = QLabel(f"{project_data['endDate']}")

        project_end_date_str = project_data['endDate']  # or whatever your variable is

        # Ensure project_end_date_str is a datetime object before formatting
        if isinstance(project_end_date_str, str):
             try:
                 # Attempt to parse from the format it might be stored in
                 project_end_date_dt = datetime.strptime(project_end_date_str, '%Y-%m-%d %H:%M:%S')
             except ValueError:
                 # Handle cases where the string format might be different
                 print(f"Warning: Could not parse date string: {project_end_date_str}")
                 formatted_date = str(project_end_date_str) # Use original string if parsing fails
             else:
                 formatted_date = project_end_date_dt.strftime("%B %d")
        elif isinstance(project_end_date_str, datetime):
             formatted_date = project_end_date_str.strftime("%B %d")
        else:
             formatted_date = str(project_end_date_str) # Fallback for unexpected types


        # Set this to your label
        ProjectEndDateLabel.setText(formatted_date)

        ProjectTaskNoIcon = QPushButton()
        ProjectTaskNoIcon.setIcon(QIcon("icons/projecttaskno.svg"))
        ProjectTaskNoIcon.setMaximumSize(QSize(20, 20))
        ProjectTaskNoIcon.setMinimumSize(QSize(20, 20))
        ProjectTaskNoLabel = QLabel(f"{total}")


        ProjectMemberNoIcon = QPushButton()
        ProjectMemberNoIcon.setIcon(QIcon("icons/projectusers.svg"))
        ProjectMemberNoIcon.setMaximumSize(QSize(20, 20))
        ProjectMemberNoIcon.setMinimumSize(QSize(20, 20))
        members = getMembersForProject(project_data['projectID'])
        ProjectMemberNoLabel = QLabel(f"{len(members)}")

        lastrow_layout.addWidget(ProjectEndDateIcon)
        lastrow_layout.addWidget(ProjectEndDateLabel)
        lastrow_layout.addStretch()
        lastrow_layout.addWidget(ProjectTaskNoIcon)
        lastrow_layout.addWidget(ProjectTaskNoLabel)
        lastrow_layout.addStretch()
        lastrow_layout.addWidget(ProjectMemberNoIcon)
        lastrow_layout.addWidget(ProjectMemberNoLabel)
        lastrow.setLayout(lastrow_layout)


        content_layout.addWidget(toprow)
        content_layout.addWidget(secrow)
        content_layout.addWidget(thirdrow)
        content_layout.addWidget(lastrow)

        container_layout.addWidget(content)
        self.setLayout(container_layout)

        # Make widget focusable and clickable
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Changes cursor to hand when hovering

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print(f"Project card {self.project_data.get('projectID', 'N/A')} clicked!") # Added print statement
        self.clicked.emit(self.project_data)  # Emit signal with project data
