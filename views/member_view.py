from PyQt6.QtWidgets import QDialog
from controllers.member_controller import addMember, getMemberByID, updateMember
from controllers.member_controller import addMember, getMemberByID, updateMember, getProjectsTasksandDateByMemberID, getAllMembers, getProjectsByMemberID
from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QTableWidget, QHBoxLayout, QAbstractItemView, QHeaderView, QPushButton, QMessageBox
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QObject, pyqtProperty
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
from PyQt6.QtWidgets import QSizePolicy

class AddMemberForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_MemberForm() #change this to the actual UI class name
        self.ui.setupUi(self)

        self.main_window = main_window

        
        self.ui.pushButton.clicked.connect(self.saveMember)

    def saveMember(self):
        member_id = self.ui.lineEdit.text().strip() #assume
        name = self.ui.lineEdit_1.text().strip() #assume
        email = self.ui.lineEdit_2.text().strip() #assume

        addMember((member_id, name, email))
        from models.member import loadMember
        loadMember(self.main_window.ui.members_table)
        
class EditMemberForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_MemberForm() #change this to the actual UI class name
        self.ui.setupUi(self)

        self.main_window = main_window

        #Load existing data into the form
        data = getMemberByID(originalID)
        if data:
            self.ui.lineEdit.setText(data["memberID"]) #assume
            self.ui.lineEdit_1.setText(data["fullname"]) #assume
            self.ui.lineEdit_2.setText(data["email"]) #assume
        
        self.ui.pushButton.clicked.connect(self.saveMember)
        
    def saveMember(self):
        member_id = self.ui.lineEdit.text().strip() #assume
        name = self.ui.lineEdit_1.text().strip() #assume
        email = self.ui.lineEdit_2.text().strip() #assume

        # ga pass kag tuple instead of a dictionary (not sure if this is correct)
        updateMember(self.originalID, (member_id, name, email))

        from models.member import loadMember
        loadMember(self.main_window.ui.members_table)

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
    table.setSpan(row, 0, 1, table.columnCount())

    # Fetch member and task data
    members = getAllMembers()
    user_data = next((m for m in members if m[0] == member_id), None)
    if not user_data:
        return
    tasks = getProjectsTasksandDateByMemberID(member_id)

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
    delete_button.setIcon(QIcon("icons/delete.svg")) #assume
    delete_button.setFixedSize(20, 20)
    delete_button.setToolTip("Delete Member")
    
    for btn in [minimize_button, edit_button, delete_button]:
        btn.setStyleSheet("border: none;")
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
    task_count = max(1, len(tasks))
    task_table = QTableWidget(task_count, 3)
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
    task_table.verticalHeader().setDefaultSectionSize(10)   # row height
    task_table.verticalHeader().setFixedWidth(20)   # row height
    task_table.horizontalHeader().setDefaultSectionSize(100)  # column width (optional)
    task_table.setMaximumHeight(100)  # limit total widget height
    task_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    header = task_table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    row_height = task_table.verticalHeader().defaultSectionSize()
    header_height = task_table.horizontalHeader().height()
    table_margin = 8  # layout padding/margins around the table
    row_count = task_table.rowCount()

    inner_table_height = header_height + (row_height * row_count) + table_margin
    container_total_height = inner_table_height + 60  # add extra height for labels, spacing, etc.

    table.setRowHeight(row, container_total_height)
    task_table.setFixedHeight(inner_table_height)


    spacing = 10  # padding or layout margins

    total_rows = task_table.rowCount()
    total_height = header_height + (row_height * total_rows) + spacing

    if tasks:
        for i, t in enumerate(tasks):
            task_table.setItem(i, 0, QTableWidgetItem(t["projectName"]))
            task_table.setItem(i, 1, QTableWidgetItem(t["taskName"]))
            task_table.setItem(i, 2, QTableWidgetItem(t["formattedDate"]))
    else:
        projects = getProjectsByMemberID(member_id)
        if not projects:
            task_table.setItem(0, 0, QTableWidgetItem("No Projects Assigned"))
            task_table.setItem(0, 1, QTableWidgetItem("No Tasks Assigned"))
            task_table.setItem(0, 2, QTableWidgetItem("N/A"))
        else:
            task_table.setRowCount(len(projects))
            for i, project in enumerate(projects):
                task_table.setItem(i, 0, QTableWidgetItem(project["projectName"]))
                task_table.setItem(i, 1, QTableWidgetItem("No Tasks Assigned"))
                task_table.setItem(i, 2, QTableWidgetItem("N/A"))


    layout.addWidget(task_table, stretch=1)

    # Add widget to the row
    table.setCellWidget(row, 0, container)
    table.setRowHeight(row, total_height)


    # Animate row height
    animation = QPropertyAnimation(main_window, b"dummy")
    animation.setDuration(300)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.setStartValue(main_window.default_row_height)
    dynamic_height = 50 + total_height
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