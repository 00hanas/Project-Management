from controllers.member_controller import getAllMembers
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

HEADERS = ["Member ID", "Name", "Email", "Projects", "Tasks"]
MAX_ROW_HEIGHT = 40  # Define maximum row height

def loadMember(tableWidget):
    # Store the current row height if rows exist
    current_row_height = min(
        tableWidget.rowHeight(0) if tableWidget.rowCount() > 0 else 30,
        MAX_ROW_HEIGHT
    )
        
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    members = getAllMembers()

    tableWidget.setColumnCount(len(HEADERS))
    tableWidget.setHorizontalHeaderLabels(HEADERS)

    if members:
        tableWidget.setRowCount(len(members))
        for row_idx, row_data in enumerate(members):
            # Set the row height to the stored value or default
            tableWidget.setRowHeight(row_idx, current_row_height)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "N/A")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tableWidget.setItem(row_idx, col_idx, item)