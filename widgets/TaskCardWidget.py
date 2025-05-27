from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from controllers.task_controller import getMembersForTask
from datetime import datetime

class TaskCardWidget(QWidget):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.setObjectName("TaskCard")
        
        self.setMinimumSize(QSize(200, 220))
        self.setMaximumSize(QSize(800, 220))
        
        container_layout = QVBoxLayout(self)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(12, 0, 6, 0)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        content = QWidget()
        content.setObjectName("content")
        content.setStyleSheet("""
            #content {
                background-color: #FFEEB5;
                border-radius: 8px;
            }
        """)
        
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # First Row - Task ID
        toprow = QWidget()
        toprow.setObjectName("toprow")
        toprow.setStyleSheet("""
            #toprow {
                background-color: #fe9137;
                border-top-right-radius: 8px 8px;
                border-top-left-radius: 8px 8px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QLabel {
                background-color: transparent;
                color: #2A2A2A;
                border-radius: 0px;
                margin: 0px;
                margin-left: 2px;
                padding: 0px;
            }
        """)
        
        toprow_layout = QHBoxLayout()
        TaskIDBase = QLabel("Task ID:")
        TaskIDBase.setStyleSheet("color: #2A2A2A; font-weight: bold;")
        TaskIDLabel = QLabel(f"{task_data['taskID']}")
        TaskIDLabel.setStyleSheet("color: #2A2A2A; font-weight: normal;")
        toprow_layout.addWidget(TaskIDBase)
        toprow_layout.addStretch()
        toprow_layout.addWidget(TaskIDLabel)
        toprow.setLayout(toprow_layout)
        
        # Second Row - Task Name
        secrow = QWidget()
        secrow.setObjectName("secrow")
        secrow.setStyleSheet("""
            #secrow {
                background-color: #FFEEB5;
                border-radius: 0px;
            }
            QLabel {
                background-color: transparent;
                font-size: 12px;
                font-weight: bold;
                color: #2A2A2A;
                margin: 0px;
                margin-left: 2px;
                padding: 0px;
            }
        """)
        
        secrow_layout = QHBoxLayout()
        secrow_layout.setContentsMargins(10, 10, 0, 0)
        TaskNameLabel = QLabel(f"{task_data['taskName']}")
        TaskNameLabel.setWordWrap(True)
        TaskNameLabel.setObjectName("TaskNameLabel")
        secrow_layout.addWidget(TaskNameLabel)
        secrow.setLayout(secrow_layout)
        
        # Third Row - Project ID
        thirdrow = QWidget()
        thirdrow.setObjectName("thirdrow")
        thirdrow.setStyleSheet("""
            #thirdrow {
                background-color: #FFEEB5;
                border-radius: 0px;
            }
            QLabel {
                background-color: #FFEEB5;
                font-size: 10px;
                font-weight: normal;
                color: #2A2A2A;
                margin: 0px;
                margin-left: 3px;
                padding: 0px;
            }
        """)
        
        thirdrow_layout = QHBoxLayout()
        thirdrow_layout.setContentsMargins(10, 0, 0, 0)
        ProjectIDLabel = QLabel(f"{task_data['projectID']}")
        thirdrow_layout.addWidget(ProjectIDLabel)
        thirdrow.setLayout(thirdrow_layout)
        
        # Fourth Row - Status
        fourthrow = QWidget()
        fourthrow.setObjectName("fourthrow")
        fourthrow.setStyleSheet("""
            #fourthrow {
                background-color: #FFEEB5;
                border-radius: 0px;
            }
            QLabel {
                background-color: transparent;
                font-size: 10px;
                font-weight: bold;
                color: #2A2A2A;
                margin-left: 3px;
            }
        """)
        
        fourthrow_layout = QHBoxLayout()
        fourthrow_layout.setContentsMargins(10, 5, 0, 10)
        StatusLabel = QLabel(f"{task_data.get('currentStatus', 'Unknown')}")
        fourthrow_layout.addWidget(StatusLabel)
        fourthrow.setLayout(fourthrow_layout)
        
        # Last Row - Due Date and Members
        lastrow = QWidget()
        lastrow.setObjectName("lastrow")
        lastrow.setStyleSheet("""
            #lastrow {
                background-color: #FFEEB5;
                border-bottom-right-radius: 8px 8px;
                border-bottom-left-radius: 8px 8px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QLabel {
                background-color: transparent;
                font-size: 12px;
                font-weight: bold;
                color: #D6A400;
            }
        """)
        
        lastrow_layout = QHBoxLayout()
        lastrow_layout.setContentsMargins(15, 0, 10, 10)
        
        # Due Date
        DueDateIcon = QPushButton()
        DueDateIcon.setIcon(QIcon("icons/taskduedate.svg"))
        DueDateIcon.setMaximumSize(QSize(20, 20))
        DueDateIcon.setMinimumSize(QSize(20, 20))
        
        # Fix the date parsing
        due_date = task_data['dueDate']
        if isinstance(due_date, str):
            # If it's a string, parse it
            formatted_date = datetime.strptime(due_date.split()[0], '%Y-%m-%d').strftime("%B %d")
        else:
            # If it's already a datetime object
            formatted_date = due_date.strftime("%B %d")
            
        DueDateLabel = QLabel(formatted_date)
        
        # Members
        MemberIcon = QPushButton()
        MemberIcon.setIcon(QIcon("icons/taskuserno.svg"))
        MemberIcon.setMaximumSize(QSize(20, 20))
        MemberIcon.setMinimumSize(QSize(20, 20))
        
        members = getMembersForTask(task_data['taskID'])
        MemberCountLabel = QLabel(f"{len(members)}")
        
        lastrow_layout.addWidget(DueDateIcon)
        lastrow_layout.addWidget(DueDateLabel)
        lastrow_layout.addStretch()
        lastrow_layout.addWidget(MemberIcon)
        lastrow_layout.addWidget(MemberCountLabel)
        lastrow.setLayout(lastrow_layout)
        
        # Add all rows to content layout
        content_layout.addWidget(toprow)
        content_layout.addWidget(secrow)
        content_layout.addWidget(thirdrow)
        content_layout.addWidget(fourthrow)
        content_layout.addWidget(lastrow)
        
        container_layout.addWidget(content)
        self.setLayout(container_layout)