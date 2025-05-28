from PyQt6.QtWidgets import QDialog, QListWidgetItem, QMessageBox
from controllers.member_controller import addMember, getMemberByID, updateMember
from controllers.member_controller import addMember, getMemberByID, updateMember, getProjectsTasksandDateByMemberID, getAllMembers, getProjectsByMemberID, assignTasktoMember, assignProjecttoMember, getProjectIDbyTaskID, getTaskIDbyMemberID, getProjectIDbyMemberID, clearProjectMember, clearTaskMember
from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QTableWidget, QHBoxLayout, QAbstractItemView, QHeaderView, QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QObject, pyqtProperty, QRegularExpression, QSize
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PyQt6 import QtCore
from PyQt6.QtWidgets import QSizePolicy
from ui.addmember_interface import Ui_addmember_dialog
from controllers.project_controller import getAllProjects
from controllers.task_controller import getAllTasks
from datetime import datetime
from utils.member_validator import uniqueMember, uniqueEditMember

class AddMemberForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addmember_dialog()
        self.ui.setupUi(self)

        self.main_window = main_window

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.member_id_info.setValidator(id_validator)

        populateProjectList(self.ui.member_project_info)
        # Start with empty task list
        self.ui.member_task_info.clear()
        
        # Connect project list changes to update task list
        self.ui.member_project_info.itemChanged.connect(
            lambda: onProjectSelectionChange(self.ui.member_project_info, self.ui.member_task_info)
        )
        
        self.ui.member_save_button.clicked.connect(self.saveMember)
        self.ui.member_clear_button.clicked.connect(self.clearMember)
        self.ui.member_cancel_button.clicked.connect(self.cancelMember)

    def saveMember(self):
        member_id = self.ui.member_id_info.text().strip() 
        name = self.ui.member_name_info.text().strip() 
        email = self.ui.member_email_info.text().strip() 

        if not member_id or not name or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        
        error = uniqueMember(member_id)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return

        member = (member_id, name, email)
        addMember(member)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        assigned_project_ids = set()

        for i in range(self.ui.member_project_info.count()):
            item = self.ui.member_project_info.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                project_id = item.data(Qt.ItemDataRole.UserRole)
                assignProjecttoMember((project_id, member_id))
                assigned_project_ids.add(project_id)


        for i in range(self.ui.member_task_info.count()):
            item = self.ui.member_task_info.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                task_id = item.data(Qt.ItemDataRole.UserRole)
                assignTasktoMember((task_id, member_id, now))

                project_id = getProjectIDbyTaskID(task_id)
                if project_id and project_id not in assigned_project_ids:
                    assignProjecttoMember((project_id, member_id))
                    assigned_project_ids.add(project_id)
                

        self.main_window.refreshTable()
        self.main_window.refresh_container('task')
        self.main_window.refresh_container('project')
        self.main_window.refresh_container('home')

        QMessageBox.information(self, "Success", "Member saved successfully.")
        self.close()
        
    def clearMember(self):
        self.ui.member_name_info.clear()
        self.ui.member_id_info.clear()
        self.ui.member_email_info.clear()

        for i in range(self.ui.member_project_info.count()):
            item = self.ui.member_project_info.item(i)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

        for i in range(self.ui.member_task_info.count()):
            item = self.ui.member_task_info.item(i)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def cancelMember(self):
        self.close()

class EditMemberForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_addmember_dialog() 
        self.ui.setupUi(self)

        self.originalID = originalID


        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.member_id_info.setValidator(id_validator)

        #Load existing data into the form
        data = getMemberByID(originalID)
        if data:
            self.ui.member_id_info.setText(data["memberID"]) 
            self.ui.member_name_info.setText(data["fullname"]) 
            self.ui.member_email_info.setText(data["email"]) 

        # Get currently assigned projects and tasks
        self.assigned_projects = set(getProjectIDbyMemberID(originalID))
        self.assigned_tasks = set(getTaskIDbyMemberID(originalID))

        # Populate project list and check assigned ones
        populateProjectList(self.ui.member_project_info)
        for i in range(self.ui.member_project_info.count()):
            item = self.ui.member_project_info.item(i)
            project_id = item.data(Qt.ItemDataRole.UserRole)
            if project_id in self.assigned_projects:
                item.setCheckState(Qt.CheckState.Checked)

        # Immediately populate tasks from checked projects
        self.populateAndCheckTasks()

        # Connect project list changes to update task list
        self.ui.member_project_info.itemChanged.connect(self.onProjectSelectionChanged)
        
        self.ui.member_save_button.clicked.connect(self.saveMember)
        self.ui.member_clear_button.clicked.connect(self.clearMember)
        self.ui.member_cancel_button.clicked.connect(self.cancelMember)

    def populateAndCheckTasks(self):
        """Populate task list based on checked projects and check assigned tasks"""
        self.ui.member_task_info.clear()
        
        # Get checked projects
        checked_projects = set()
        for i in range(self.ui.member_project_info.count()):
            item = self.ui.member_project_info.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_projects.add(item.data(Qt.ItemDataRole.UserRole))

        # Populate tasks from checked projects
        for task in getAllTasks():
            if task['projectID'] in checked_projects:
                item = QListWidgetItem(f"{task['projectID']}: {task['taskName']}")
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                # Check if this task was previously assigned
                if task["taskID"] in self.assigned_tasks:
                    item.setCheckState(Qt.CheckState.Checked)
                else:
                    item.setCheckState(Qt.CheckState.Unchecked)
                item.setData(Qt.ItemDataRole.UserRole, task["taskID"])
                self.ui.member_task_info.addItem(item)

    def onProjectSelectionChanged(self):
        """Handle project selection changes while preserving task check states"""
        # Save currently checked tasks from visible items
        checked_tasks = set()
        for i in range(self.ui.member_task_info.count()):
            item = self.ui.member_task_info.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_tasks.add(item.data(Qt.ItemDataRole.UserRole))

        # Update the assigned tasks set with any newly checked tasks
        self.assigned_tasks.update(checked_tasks)
        
        # Repopulate tasks based on new project selection
        self.populateAndCheckTasks()
        
    def saveMember(self):
        member_id = self.ui.member_id_info.text().strip() 
        name = self.ui.member_name_info.text().strip() 
        email = self.ui.member_email_info.text().strip() 

        if not member_id or not name or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        
        error = uniqueEditMember(member_id, self.originalID)
        if error:
            QMessageBox.warning(self, "Validation Error", error)
            return

        member = (member_id, name, email)
        updateMember(self.originalID, member)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        current_project_ids = set(getProjectIDbyMemberID(self.originalID))
        current_task_ids = set(getTaskIDbyMemberID(self.originalID))

        new_project_ids = {
            self.ui.member_project_info.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.ui.member_project_info.count())
            if self.ui.member_project_info.item(i).checkState() == Qt.CheckState.Checked
        }

        new_task_ids = {
            self.ui.member_task_info.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.ui.member_task_info.count())
            if self.ui.member_task_info.item(i).checkState() == Qt.CheckState.Checked
        }

        if new_project_ids != current_project_ids:
            clearProjectMember(self.originalID)
            for project_id in new_project_ids:
                assignProjecttoMember((project_id, member_id))

        if new_task_ids != current_task_ids:
            clearTaskMember(self.originalID)
            for task_id in new_task_ids:
                assignTasktoMember((task_id, member_id, now))
                project_id = getProjectIDbyTaskID(task_id)
                if project_id and project_id not in new_project_ids:
                    assignProjecttoMember((project_id, member_id))
                    new_project_ids.add(project_id)

        self.main_window.refreshTable()  
        self.main_window.refresh_container('task')
        self.main_window.refresh_container('project')
        self.main_window.refresh_container('home')
    
        QMessageBox.information(self, "Success", "Member updated successfully.")
        self.close()

    def clearMember(self):
        self.ui.member_name_info.clear()
        self.ui.member_id_info.clear()
        self.ui.member_email_info.clear()

        for i in range(self.ui.member_project_info.count()):
            item = self.ui.member_project_info.item(i)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

        for i in range(self.ui.member_task_info.count()):
            item = self.ui.member_task_info.item(i)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def cancelMember(self):
        self.close()


def expandRow(main_window, row):
    table = main_window.ui.members_table
    member_id = table.item(row, 0).text() if table.item(row, 0) else None
    if not member_id:
        return
    
    if main_window.expanded_row == row:
        prev_row = main_window.expanded_row
        # Collapse previous row immediately (no animation)
        for col in range(table.columnCount()):
            item = main_window.original_items[prev_row][col]
            table.setItem(prev_row, col, item)
        table.removeCellWidget(prev_row, 0)
        table.setSpan(prev_row, 0, 1, 1)
        table.setRowHeight(prev_row, main_window.default_row_height)
        main_window.expanded_row = None
        return

    # Collapse previous expanded row
    if main_window.expanded_row is not None:
        prev_row = main_window.expanded_row
        # Collapse previous row immediately (no animation)
        for col in range(table.columnCount()):
            item = main_window.original_items[prev_row][col]
            table.setItem(prev_row, col, item)
        table.removeCellWidget(prev_row, 0)
        table.setSpan(prev_row, 0, 1, 1)
        table.setRowHeight(prev_row, main_window.default_row_height)
        main_window.expanded_row = None

    # Backup original row items
    main_window.original_items[row] = [
        table.item(row, col).clone() if table.item(row, col) else QTableWidgetItem("")
        for col in range(table.columnCount())
    ]

    # Clear cells and span one for widget
    for col in range(table.columnCount()):
        table.setItem(row, col, QTableWidgetItem(""))
    col_span = table.columnCount()
    if col_span > 1:
        table.setSpan(row, 0, 1, col_span)

    # Fetch member and task data
    members = getAllMembers()
    user_data = next((m for m in members if m[0] == member_id), None)
    if not user_data:
        return
    tasks = getProjectsTasksandDateByMemberID(member_id)

    # Flatten into table rows
    projects = getProjectsByMemberID(member_id)
    project_task_map = {p["projectID"]: {"projectName": p["projectName"], "tasks": []} for p in projects}
    for t in tasks:
        pid = t["projectID"]
        if pid in project_task_map:
            project_task_map[pid]["tasks"].append(t)
            
    rows = []
    for project_data in project_task_map.values():
        if project_data["tasks"]:
            for t in project_data["tasks"]:
                rows.append((project_data["projectName"], t["taskName"], t["formattedDate"]))
        else:
            rows.append((project_data["projectName"], "No Tasks Assigned", "N/A"))

    if not projects and not tasks:
        rows.append(("No Projects Assigned", "No Tasks Assigned", "N/A"))

    # --- Build widget manually ---
    container = QWidget()
    container.setProperty("member_id", member_id)
    container.setStyleSheet("font-family: Poppins;")
    layout = QVBoxLayout(container)
    layout.setContentsMargins(10, 0, 10, 0)
    layout.setSpacing(0) 

    # Header section with image and text
    header = QHBoxLayout()
    header.setSpacing(5)  # reduce space between widgets
    header.setContentsMargins(0, 0, 0, 0) 
    profile_pic = QLabel()
    profile_pic.setPixmap(QPixmap("icons/accountprof.svg").scaled(35, 35)) 
    profile_pic.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    profile_pic.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    header.addWidget(profile_pic, stretch=0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    text_block = QVBoxLayout()
    text_block.setSpacing(0)
    text_block.setContentsMargins(0, 0, 0, 0)
    name_label = QLabel(f"<b>{user_data[1]}</b>, {user_data[0]}")
    email_label = QLabel(user_data[2])
    for label in [name_label, email_label]:
        label.setStyleSheet("color: black; font-family: Poppins; font-size: 12px;")
    text_block.addWidget(name_label)
    text_block.addWidget(email_label)
    text_block.setAlignment(Qt.AlignmentFlag.AlignLeft)
    header.addLayout(text_block, stretch=1)
    header.setAlignment(text_block, Qt.AlignmentFlag.AlignTop)

    stats_label = QLabel(f"Assigned Projects: <b>{user_data[3]}</b><br>Assigned Tasks: <b>{user_data[4]}</b>")
    stats_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
    stats_label.setStyleSheet("color: black; font-family: Poppins; font-size: 11px;")
    header.addWidget(stats_label, stretch=1)
    layout.addLayout(header, stretch=0)

    #Button_layout
    button_layout = QHBoxLayout()
    button_layout.setContentsMargins(0, 0, 0, 0)
    button_layout.setSpacing(3) 
    
    minimize_button = QPushButton()
    minimize_button.setIcon(QIcon("icons/minimize.svg")) #assume
    minimize_button.setFixedSize(20, 20)
    minimize_button.setToolTip("Collapse row")

    edit_button = QPushButton()
    edit_button.setIcon(QIcon("icons/edit1.svg")) #assume
    edit_button.setFixedSize(20, 20)
    edit_button.setToolTip("Edit Member")

    delete_button = QPushButton()
    delete_button.setIcon(QIcon("icons/delete_black.svg")) #assume
    delete_button.setFixedSize(20, 20)
    delete_button.setToolTip("Delete Member")

    icon_size = QSize(20, 20)
    
    for btn in [minimize_button, edit_button, delete_button]:
        btn.setIconSize(icon_size)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignVCenter)

    minimize_button.clicked.connect(lambda _, r=row: collapseRow(main_window, r))
    edit_button.clicked.connect(lambda _, w=container: main_window.editMemberFromWidget(w))
    delete_button.clicked.connect(lambda _, w=container: main_window.deleteMemberFromWidget(w))

    button_layout.addWidget(minimize_button)
    button_layout.addWidget(edit_button)
    button_layout.addWidget(delete_button)

    # Wrap buttons in a QWidget and align to top-right
    button_container = QWidget()
    button_container.setLayout(button_layout)
    button_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    button_style = """
QPushButton {
    background-color: #e0e0e0;
    border: 1px solid #aaa;
    border-radius: 4px;
    padding: 2px 6px;
    text-align: center;
}
QPushButton:hover {
    background-color: #c0c0c0;
    color: black;
}
QPushButton:pressed {
    background-color: #a0a0a0;
}
"""
    minimize_button.setStyleSheet(button_style)
    edit_button.setStyleSheet(button_style)
    delete_button.setStyleSheet(button_style)
    header.addWidget(button_container, stretch=0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

    # Tasks table
    task_table = QTableWidget(len(rows), 3)
    task_table.setHorizontalHeaderLabels(["Project", "Task", "Assigned On"])

    task_table.verticalHeader().setVisible(False)
    task_table.horizontalHeader().setStretchLastSection(True)
    task_table.horizontalHeader().setHighlightSections(False)
    task_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    task_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    task_table.setShowGrid(True)
    task_table.setStyleSheet("""
    QTableWidget {
        background-color: transparent;
        font-size: 10px;
        font-family: Poppins;
    }
    QHeaderView::section {
        background-color: transparent;
        border: none;
        font-weight: bold;
        border: 1px solid black;
        color: black;
        font-size: 10px;
        font-family: Poppins;
    }
    QTableWidget::item {
        border: 1px solid black;
        font-family: Poppins;
    }
""")
    
    header = task_table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # Fill table
    task_table.setRowCount(len(rows))
    for i, row_data in enumerate(rows):
        for j, cell in enumerate(row_data):
            task_table.setItem(i, j, QTableWidgetItem(cell))

    #Compute height needed for task_table
    row_height = task_table.verticalHeader().defaultSectionSize()
    header_height = task_table.horizontalHeader().height()
    vertical_padding = 10 # Add slight padding for safety
    task_table_total_height = header_height + (row_height * len(rows)) + vertical_padding
    task_table.setFixedHeight(task_table_total_height)

    layout.addWidget(task_table, stretch=1)

    # Add widget to the row
    table.setCellWidget(row, 0, container)
    
    # Animate row height
    animation = QPropertyAnimation(main_window, b"dummy")
    animation.setDuration(300)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.setStartValue(main_window.default_row_height)
    dynamic_height = 50 + task_table_total_height
    animation.setEndValue(dynamic_height)

    def update_height(value):
        table.setRowHeight(row, int(value))

    animation.valueChanged.connect(update_height)
    animation.start()

    main_window.current_animation = animation
    main_window.expanded_row = row

# Custom class to allow animating a dummy property
class DummyObject(QObject):
    def __init__(self, table, row):
        super().__init__()
        self._height = 0
        self.table = table
        self.row = row

    def getHeight(self):
        return self._height

    def setHeight(self, value):
        self._height = value
        self.table.setRowHeight(self.row, int(value))

    height = pyqtProperty(int, fget=getHeight, fset=setHeight)

def collapseRow(main_window, row):

    table = main_window.ui.members_table
    if main_window.expanded_row != row:
        return

    current_height = table.rowHeight(row)

    # Set up animation to collapse the row
    animation = QPropertyAnimation(main_window, b"dummy")
    animation.setDuration(300)
    animation.setEasingCurve(QEasingCurve.Type.InCubic)
    animation.setStartValue(current_height)
    animation.setEndValue(main_window.default_row_height)

    def update_height(value):
        table.setRowHeight(row, int(value))

    def on_finished():
        # Restore original row items
        for col in range(table.columnCount()):
            item = main_window.original_items[row][col]
            table.setItem(row, col, item)
        table.removeCellWidget(row, 0)
        table.setSpan(row, 0, 1, 1)
        main_window.expanded_row = None

    animation.valueChanged.connect(update_height)
    animation.finished.connect(on_finished)
    animation.start()

    main_window.current_animation = animation 

def populateProjectList(member_project_info):
    member_project_info.clear()
    for project in getAllProjects():
        item = QListWidgetItem(f"{project[0]}: {project[1]}")
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        item.setData(Qt.ItemDataRole.UserRole, project[0])
        member_project_info.addItem(item)

def populateTaskList(member_task_info, member_project_info=None, force_empty=False):
    member_task_info.clear()
    
    # If forced empty or no projects checked, return empty list
    if force_empty or member_project_info is None:
        return
    
    # Get currently checked projects
    checked_projects = set()
    for i in range(member_project_info.count()):
        item = member_project_info.item(i)
        if item.checkState() == Qt.CheckState.Checked:
            checked_projects.add(item.data(Qt.ItemDataRole.UserRole))
    
    # Only proceed if there are checked projects
    if not checked_projects:
        return
    
    # Show only tasks from checked projects
    for task in getAllTasks():
        if task['projectID'] in checked_projects:
            item = QListWidgetItem(f"{task['projectID']}: {task['taskName']}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, task["taskID"])
            member_task_info.addItem(item)

def onProjectSelectionChange(member_project_info, member_task_info):
    # Save currently checked tasks
    checked_tasks = set()
    for i in range(member_task_info.count()):
        item = member_task_info.item(i)
        if item.checkState() == Qt.CheckState.Checked:
            checked_tasks.add(item.data(Qt.ItemDataRole.UserRole))
    
    # Repopulate tasks only if projects are checked
    populateTaskList(member_task_info, member_project_info)
    
    # Restore checked state for tasks that are still visible
    for i in range(member_task_info.count()):
        item = member_task_info.item(i)
        task_id = item.data(Qt.ItemDataRole.UserRole)
        if task_id in checked_tasks:
            item.setCheckState(Qt.CheckState.Checked)
    