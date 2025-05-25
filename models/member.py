from controllers.member_controller import getAllMembers
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

HEADERS = ["Member ID", "Name", "Email", "Projects", "Tasks"]

def loadMember(tableWidget):
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    members = getAllMembers()

    tableWidget.setColumnCount(len(HEADERS))
    tableWidget.setHorizontalHeaderLabels(HEADERS)

    if members:
        tableWidget.setRowCount(len(members))
        for row_idx, row_data in enumerate(members):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "N/A")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tableWidget.setItem(row_idx, col_idx, item)