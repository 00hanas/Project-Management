from config.db_config import getConnection
from PyQt6.QtWidgets import QDialog
from models.member import loadMember
from controllers.member_controller import addMember, getMemberByID, updateMember

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

            updateMember(originalID, (member_id, name, email))

