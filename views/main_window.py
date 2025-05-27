from PyQt6.QtWidgets import QCalendarWidget, QMainWindow, QAbstractItemView, QMessageBox, QTableWidgetItem, QListWidget, QListWidgetItem
from ui.main_interface import Ui_MainWindow
from views.project_view import AddProjectForm
from views.task_view import AddTaskForm
from views.member_view import expandRow, EditMemberForm, AddMemberForm
from controllers.dashboard_controller import getTotalProjectCount, getTotalTaskCount, getTotalMemberCount, getCalendarEvents, getAllProjectsTasksMembers
from controllers.member_controller import searchMembers, getAllMembersForSearch
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QDate, Qt, QTimer

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Default navigation to home page
        self.ui.stackedWidget.setCurrentIndex(0)
        
        # Total project count, task count, and member count
        self.ui.projects_total_count.setText(str(getTotalProjectCount()))
        self.ui.tasks_total_count.setText(str(getTotalTaskCount()))
        self.ui.members_total_count.setText(str(getTotalMemberCount()))

        self.ui.projects_total_count.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.tasks_total_count.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.members_total_count.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

        # Navigation to pages
        self.ui.home_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.projects_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.tasks_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.members_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3)) 

        # Handling add buttons
        self.ui.addproject_button.clicked.connect(lambda: AddProjectForm(self).exec())
        self.ui.addtask_button.clicked.connect(lambda: AddTaskForm(self).exec())
        self.ui.addmember_button.clicked.connect(lambda: AddMemberForm(self).exec())

        # Handling calendar controls
        self.calendar = self.ui.home_calendar
        self.date_tooltip_map = {}
        self.calendar.style().unpolish(self.calendar)
        self.calendar.style().polish(self.calendar)
        self.highlightEvents()
        
        # Configure calendar selection behavior
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)

        # Home page search functionality
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.performHomeSearch)
        self.ui.home_search.textChanged.connect(lambda: self.search_timer.start(200)) 
        self.ui.home_searchby.currentIndexChanged.connect(self.performHomeSearch)
        self.ui.home_search.setPlaceholderText("Search projects, tasks, or members...")
        self.search_suggestion = QListWidget(self)
        self.search_suggestion.setWindowFlags(Qt.WindowType.Popup)
        self.search_suggestion.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search_suggestion.setMouseTracking(True)
        self.search_suggestion.setParent(self)

        self.search_suggestion.move(self.ui.home_search.mapToGlobal(self.ui.home_search.rect().bottomLeft()))

        self.search_suggestion.hide()
        self.search_suggestion.itemClicked.connect(self.handleSuggestionClicked)
        self.search_suggestion.setStyleSheet("""
QListWidget {
    border: 1px solid #edf4fa;
    border-radius: 8px;
    padding: 4px;
    font-family: "Poppins", sans-serif;
    font-size: 10px;
    background-color: #edf4fa;
    color: black;
}
QListWidget::item {
    padding: 6px 10px;
}
QListWidget::item:hover {
    background-color: #f0f0f0;
    color: black;
}
QListWidget::item:selected {
    background-color: #b8e6d9;
    color: black;
}
""")
        
        # Member search functionality
        self.ui.members_search.textChanged.connect(self.performSearchforMembers)
        self.ui.members_searchby.currentIndexChanged.connect(self.performSearchforMembers)

        #Load members into the table
        if hasattr(self.ui, 'members_table'):
            #For the members' table
            self.expanded_row = None
            self.default_row_height = 30
            self.original_items = {}
            #Functions for the members' table
            self.setupTableInteractions()
            self.refreshTable()

        # Sort Members Table by column header click
        self.ui.members_table.horizontalHeader().sectionClicked.connect(self.sortTableByColumn)

    def setupTableInteractions(self):
        table = self.ui.members_table
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.cellDoubleClicked.connect(self.handlingDoubleClicked)

    def handlingDoubleClicked(self, row, column):
        expandRow(self, row)

    def editMemberFromWidget(self, widget):
        member_id = widget.property("member_id")
        if not member_id:
            print("[DEBUG] No member_id found in widget")
            return
        
        edit_form = EditMemberForm(self, member_id)
        edit_form.exec()
        from models.member import loadMember
        loadMember(self.ui.members_table)

    def deleteMemberFromWidget(self, widget):
        member_id = widget.property("member_id")
        if not member_id:
            print("[DEBUG] No member_id found in widget")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete member ID {member_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            from controllers.member_controller import deleteMemberbyID
            deleteMemberbyID(member_id)
            self.refreshTable()

    def highlightEvents(self):

        project_format = QTextCharFormat()
        project_format.setBackground(QColor("#2b70ff"))
        project_format.setForeground(QColor("white"))
        project_format.setFontWeight(QFont.Weight.Bold)

        task_format = QTextCharFormat()
        task_format.setBackground(QColor("#fe9137"))
        task_format.setForeground(QColor("white"))
        task_format.setFontWeight(QFont.Weight.Bold)

        format_map = {}
        tooltip_map = {}


        for date, title, type_ in getCalendarEvents():
            if type_ == "project":
                fmt = project_format
            elif type_ == "task":
                fmt = task_format
            else:
                continue  # Skip unknown types

            if date not in format_map:
                format_map[date] = QTextCharFormat(fmt)
            else:
                # Optional: Merge formats — here we keep the last applied
                pass

            tooltip_map.setdefault(date, []).append(f"{type_.capitalize()}: {title}")

        # Apply formats and tooltips
        for date, fmt in format_map.items():
            self.calendar.setDateTextFormat(date, fmt)

        for date, tooltips in tooltip_map.items():
            fmt = self.calendar.dateTextFormat(date)
            fmt.setToolTip("\n".join(tooltips))
            self.calendar.setDateTextFormat(date, fmt)

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#e2091e"))
        fmt.setForeground(QColor("white"))
        fmt.setFontWeight(QFont.Weight.Bold)
        self.calendar.setDateTextFormat(QDate.currentDate(), fmt)

        self.calendar.setDateTextFormat(QDate.currentDate(), fmt)

    def performSearchforMembers(self):
        keyword = self.ui.members_search.text()
        search_by = self.ui.members_searchby.currentText()

        # Handle default combo text like "Search By"
        if search_by == "Search By":
            search_by = ""  

        results = searchMembers(keyword, search_by)
        self.updateTable(results)

    def updateTable(self, member_ids: list[str]):
        self.ui.members_table.setRowCount(0)

        for row_num, member_id in enumerate(member_ids):
            data = getAllMembersForSearch(member_id)

            self.ui.members_table.insertRow(row_num)
            self.ui.members_table.setItem(row_num, 0, QTableWidgetItem(data['memberID']))
            self.ui.members_table.setItem(row_num, 1, QTableWidgetItem(data['fullname']))
            self.ui.members_table.setItem(row_num, 2, QTableWidgetItem(data['email']))
            self.ui.members_table.setItem(row_num, 3, QTableWidgetItem(str(data['projectCount'])))
            self.ui.members_table.setItem(row_num, 4, QTableWidgetItem(str(data['taskCount'])))

    def sortTableByColumn(self, column):
        current_order = self.ui.members_table.horizontalHeader().sortIndicatorOrder()
        self.ui.members_table.sortItems(column, current_order)

    def refreshTable(self):
        from models.member import loadMember # Adjust import if needed
        loadMember(self.ui.members_table)
        self.expanded_row = None
        self.original_items = {}

        for row in range(self.ui.members_table.rowCount()):
            self.ui.members_table.setRowHeight(row, self.default_row_height)

    def performHomeSearch(self):
        keyword = self.ui.home_search.text()
        search_by = self.ui.home_searchby.currentText()
        
        if not keyword:
            self.search_suggestion.hide()
            return
        
        if search_by == "Search By":
            search_by = ""
        
        results = getAllProjectsTasksMembers(keyword, search_by)
        self.updateSearchSuggestions(results)
        
    def updateSearchSuggestions(self, results: list[dict]):
        if not results:
            self.search_suggestion.hide()
            print("[DEBUG] No search results found")
            return
        self.search_suggestion.clear()
        for item in results:
            display_text = f"{item['type'].capitalize()}: {item['label']}"
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.search_suggestion.addItem(list_item)

        # Position and show suggestion popup
        input_rect = self.ui.home_search.geometry()
        global_pos = self.ui.home_search.mapToGlobal(input_rect.bottomLeft())
        self.search_suggestion.move(global_pos)
        self.search_suggestion.resize(
            self.ui.home_search.width(),
            min(200, self.search_suggestion.sizeHintForRow(0) * self.search_suggestion.count())
        )
        self.search_suggestion.show()

    def handleSuggestionClicked(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        entity_type = data['type']
        entity_id = data['id']

        if entity_type == 'project':
            self.navigateToProject(entity_id)
        elif entity_type == 'task':
            self.navigateToTask(entity_id)
        elif entity_type == 'member':
            self.navigateToMember(entity_id)

        self.search_suggestion.hide()
        self.ui.search_input.clear()


    def navigateToProject(self, project_id):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.search_input.clear()
        # Optionally scroll to or highlight project row in table

    def navigateToTask(self, task_id):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.search_input.clear()
        # Optionally scroll to or highlight task row in table

    def navigateToMember(self, member_id):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.search_input.clear()
