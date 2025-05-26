from PyQt6.QtWidgets import QMainWindow, QAbstractItemView, QMessageBox
from ui.main_interface import Ui_MainWindow
from models.member import loadMember
from views.member_view import expandRow
from controllers.dashboard_controller import getTotalProjectCount, getTotalTaskCount, getTotalMemberCount, getCalendarEvents
from PyQt6.QtGui import QTextCharFormat, QColor, QFont

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

        #handling calendar navigation
        self.calendar = self.ui.home_calendar
        self.date_tooltip_map = {}

        self.highlightEvents()


        #Load members into the table
        if hasattr(self.ui, 'members_table'):
            #For the members' table
            self.expanded_row = None
            self.default_row_height = 30
            self.original_items = {}
            #Functions for the members' table
            self.setupTableInteractions()
            loadMember(self.ui.members_table)

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
        

        from views.member_view import EditMemberForm
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

