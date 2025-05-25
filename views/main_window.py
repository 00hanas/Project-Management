import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QMessageBox
from testui import Ui_MainWindow
from models.member import loadMember
from views.member_view import expandRow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #For the members' table
        self.expanded_row = None
        self.default_row_height = 30
        self.original_items = {}
        #Functions for the members' table
        self.setupTableInteractions()

        #Load members into the table
        if hasattr(self.ui, 'tableWidget'):
            loadMember(self.ui.tableWidget)

    def setupTableInteractions(self):
        table = self.ui.tableWidget
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
        loadMember(self.ui.tableWidget)


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
            loadMember(self.ui.tableWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())