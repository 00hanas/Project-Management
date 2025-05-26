from PyQt6.QtWidgets import QCalendarWidget, QMainWindow, QAbstractItemView, QMessageBox, QTableWidgetItem
from ui.main_interface import Ui_MainWindow
from models.member import loadMember
from views.member_view import expandRow, EditMemberForm, AddMemberForm
from controllers.dashboard_controller import getTotalProjectCount, getTotalTaskCount, getTotalMemberCount, getCalendarEvents
from controllers.member_controller import searchMembers, getAllMembersForSearch
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QDate

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

        # Navigation to member's page
        self.ui.members_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3)) 

        # Navigation to home's page
        self.ui.home_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0)) 

        # Handling calendar controls
        self.calendar = self.ui.home_calendar
        self.date_tooltip_map = {}
        self.calendar.style().unpolish(self.calendar)
        self.calendar.style().polish(self.calendar)
        self.highlightEvents()
        
        # Configure calendar selection behavior
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        
        # Functionality in members' page
        self.ui.members_search.textChanged.connect(self.performSearch)
        self.ui.members_searchby.currentIndexChanged.connect(self.performSearch)
        self.ui.addmember_button.clicked.connect(self.showAddMember)


        #Load members into the table
        if hasattr(self.ui, 'members_table'):
            #For the members' table
            self.expanded_row = None
            self.default_row_height = 30
            self.original_items = {}
            #Functions for the members' table
            self.setupTableInteractions()
            loadMember(self.ui.members_table)

        self.ui.members_table.horizontalHeader().sectionClicked.connect(self.sortTableByColumn)

    def setupTableInteractions(self):
        table = self.ui.members_table
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.cellDoubleClicked.connect(self.handlingDoubleClicked)

    def handlingDoubleClicked(self, row, column):
        expandRow(self, row)

    def showAddMember(self):
        add_form = AddMemberForm(self)
        add_form.show()
        add_form.exec()

        from models.member import loadMember
        loadMember(self.ui.members_table)

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
            loadMember(self.ui.members_table)

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

    def performSearch(self):
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