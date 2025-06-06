# Form implementation generated from reading ui file 'projects_expand.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class Ui_projects_expand(object):
    def setupUi(self, projects_expand):
        projects_expand.setObjectName("projects_expand")
        projects_expand.resize(643, 506)
        projects_expand.setStyleSheet("QDialog{\n"
"    background-color: #edf4fa;\n"
"}\n"
"\n"
"QFrame {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #FFFFFF;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-family: \"Poppins\", sans-serif;\n"
"    font-size: 15px;\n"
"    color: #000000;\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"#project_id, #project_startDate, #project_endDate, #project_shortDescrip, #project_tasks, #project_members {\n"
"    font-weight: bold;\n"
"    font-size: 9pt;\n"
"    color: #92979d;\n"
"}\n"
"\n"
"QTextEdit, QListWidget {\n"
"    font-family: \"Poppins\", sans-serif;\n"
"    font-weight: normal;\n"
"    font-size: 9pt;\n"
"    color: #000000;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #2b70ff;\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    color: #FFFFFF;\n"
"    text-align: center;\n"
"    font-family: \"Poppins\", sans-serif;\n"
"    font-size: 15px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"#project_id_icon, #project_startDate_icon, #project_endDate_icon, #project_shortDescrip_icon, #project_tasks_icon, #project_members_icon {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"#project_update_button, #project_delete_button {\n"
"    font-size: 10pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"Line {\n"
"    background-color: #92979d;\n"
"    color: #92979d;\n"
"}\n"
"\n"
"#project_name {\n"
"    font-size: 20pt;\n"
"    font-weight: bold;\n"
"    color: #2b70ff;\n"
"}\n"
"\n"
"#project_id_info, #project_startDate_info, #project_endDate_info, #project_shortDescrip_info, #project_tasks_info, #project_members_info {\n"
"    font-weight: normal;\n"
"    font-size: 10pt;\n"
"    color: #000000;\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(projects_expand)
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.gridLayout.setObjectName("gridLayout")
        self.projects_expand_frame = QtWidgets.QFrame(parent=projects_expand)
        self.projects_expand_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.projects_expand_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.projects_expand_frame.setObjectName("projects_expand_frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.projects_expand_frame)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.frame_7 = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.project_name_frame = QtWidgets.QFrame(parent=self.frame_7)
        self.project_name_frame.setMinimumSize(QtCore.QSize(450, 61))
        self.project_name_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_name_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_name_frame.setObjectName("project_name_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.project_name_frame)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.project_name = QtWidgets.QLabel(parent=self.project_name_frame)
        self.project_name.setObjectName("project_name")
        self.gridLayout_5.addWidget(self.project_name, 0, 0, 1, 1)
        self.horizontalLayout_18.addWidget(self.project_name_frame)
        self.project_updateDelete = QtWidgets.QFrame(parent=self.frame_7)
        self.project_updateDelete.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_updateDelete.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_updateDelete.setObjectName("project_updateDelete")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.project_updateDelete)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.project_update_button = QtWidgets.QPushButton(parent=self.project_updateDelete)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/edit.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_update_button.setIcon(icon)
        self.project_update_button.setObjectName("project_update_button")
        self.verticalLayout.addWidget(self.project_update_button)
        self.project_delete_button = QtWidgets.QPushButton(parent=self.project_updateDelete)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/trash-2.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_delete_button.setIcon(icon1)
        self.project_delete_button.setObjectName("project_delete_button")
        self.verticalLayout.addWidget(self.project_delete_button)
        self.horizontalLayout_18.addWidget(self.project_updateDelete)
        self.gridLayout_6.addWidget(self.frame_7, 0, 0, 1, 2)
        self.hline = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.hline.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.hline.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.hline.setObjectName("hline")
        self.gridLayout_6.addWidget(self.hline, 1, 0, 1, 2)
        self.project_id_frame = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.project_id_frame.setMinimumSize(QtCore.QSize(0, 41))
        self.project_id_frame.setMaximumSize(QtCore.QSize(16777215, 41))
        self.project_id_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_id_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_id_frame.setObjectName("project_id_frame")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.project_id_frame)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setSpacing(20)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.project_id_label = QtWidgets.QFrame(parent=self.project_id_frame)
        self.project_id_label.setMinimumSize(QtCore.QSize(151, 41))
        self.project_id_label.setMaximumSize(QtCore.QSize(151, 41))
        self.project_id_label.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_id_label.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_id_label.setObjectName("project_id_label")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.project_id_label)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.project_id_icon = QtWidgets.QPushButton(parent=self.project_id_label)
        self.project_id_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.project_id_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.project_id_icon.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/key_gray.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_id_icon.setIcon(icon2)
        self.project_id_icon.setObjectName("project_id_icon")
        self.horizontalLayout.addWidget(self.project_id_icon)
        self.project_id = QtWidgets.QLabel(parent=self.project_id_label)
        self.project_id.setObjectName("project_id")
        self.horizontalLayout.addWidget(self.project_id)
        self.horizontalLayout_15.addWidget(self.project_id_label)
        self.project_id_info = QtWidgets.QLabel(parent=self.project_id_frame)
        self.project_id_info.setText("")
        self.project_id_info.setObjectName("project_id_info")
        self.horizontalLayout_15.addWidget(self.project_id_info)
        self.gridLayout_6.addWidget(self.project_id_frame, 2, 0, 1, 2)
        self.project_startDate_frame = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.project_startDate_frame.setMinimumSize(QtCore.QSize(0, 41))
        self.project_startDate_frame.setMaximumSize(QtCore.QSize(16777215, 41))
        self.project_startDate_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_startDate_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_startDate_frame.setObjectName("project_startDate_frame")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.project_startDate_frame)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setSpacing(20)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.project_startDate_label = QtWidgets.QFrame(parent=self.project_startDate_frame)
        self.project_startDate_label.setMinimumSize(QtCore.QSize(151, 41))
        self.project_startDate_label.setMaximumSize(QtCore.QSize(151, 41))
        self.project_startDate_label.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_startDate_label.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_startDate_label.setObjectName("project_startDate_label")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.project_startDate_label)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.project_startDate_icon = QtWidgets.QPushButton(parent=self.project_startDate_label)
        self.project_startDate_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.project_startDate_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.project_startDate_icon.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/calendar_gray.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_startDate_icon.setIcon(icon3)
        self.project_startDate_icon.setObjectName("project_startDate_icon")
        self.horizontalLayout_4.addWidget(self.project_startDate_icon)
        self.project_startDate = QtWidgets.QLabel(parent=self.project_startDate_label)
        self.project_startDate.setObjectName("project_startDate")
        self.horizontalLayout_4.addWidget(self.project_startDate)
        self.horizontalLayout_16.addWidget(self.project_startDate_label)
        self.project_startDate_info = QtWidgets.QLabel(parent=self.project_startDate_frame)
        self.project_startDate_info.setText("")
        self.project_startDate_info.setObjectName("project_startDate_info")
        self.horizontalLayout_16.addWidget(self.project_startDate_info)
        self.gridLayout_6.addWidget(self.project_startDate_frame, 3, 0, 1, 2)
        self.project_endDate_frame = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.project_endDate_frame.setMinimumSize(QtCore.QSize(0, 41))
        self.project_endDate_frame.setMaximumSize(QtCore.QSize(16777215, 41))
        self.project_endDate_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_endDate_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_endDate_frame.setObjectName("project_endDate_frame")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.project_endDate_frame)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setSpacing(20)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.project_endDate_label = QtWidgets.QFrame(parent=self.project_endDate_frame)
        self.project_endDate_label.setMinimumSize(QtCore.QSize(151, 41))
        self.project_endDate_label.setMaximumSize(QtCore.QSize(151, 41))
        self.project_endDate_label.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_endDate_label.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_endDate_label.setObjectName("project_endDate_label")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.project_endDate_label)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.project_endDate_icon = QtWidgets.QPushButton(parent=self.project_endDate_label)
        self.project_endDate_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.project_endDate_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.project_endDate_icon.setText("")
        self.project_endDate_icon.setIcon(icon3)
        self.project_endDate_icon.setObjectName("project_endDate_icon")
        self.horizontalLayout_7.addWidget(self.project_endDate_icon)
        self.project_endDate = QtWidgets.QLabel(parent=self.project_endDate_label)
        self.project_endDate.setObjectName("project_endDate")
        self.horizontalLayout_7.addWidget(self.project_endDate)
        self.horizontalLayout_17.addWidget(self.project_endDate_label)
        self.project_endDate_info = QtWidgets.QLabel(parent=self.project_endDate_frame)
        self.project_endDate_info.setText("")
        self.project_endDate_info.setObjectName("project_endDate_info")
        self.horizontalLayout_17.addWidget(self.project_endDate_info)
        self.gridLayout_6.addWidget(self.project_endDate_frame, 4, 0, 1, 2)
        self.project_shortDescrip_frame = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.project_shortDescrip_frame.setMinimumSize(QtCore.QSize(0, 80))
        self.project_shortDescrip_frame.setMaximumSize(QtCore.QSize(16777215, 80))
        self.project_shortDescrip_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_shortDescrip_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_shortDescrip_frame.setObjectName("project_shortDescrip_frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.project_shortDescrip_frame)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setHorizontalSpacing(20)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.project_shortDescrip_label = QtWidgets.QFrame(parent=self.project_shortDescrip_frame)
        self.project_shortDescrip_label.setMinimumSize(QtCore.QSize(151, 41))
        self.project_shortDescrip_label.setMaximumSize(QtCore.QSize(151, 41))
        self.project_shortDescrip_label.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_shortDescrip_label.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_shortDescrip_label.setObjectName("project_shortDescrip_label")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.project_shortDescrip_label)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.project_shortDescrip_icon = QtWidgets.QPushButton(parent=self.project_shortDescrip_label)
        self.project_shortDescrip_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.project_shortDescrip_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.project_shortDescrip_icon.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/edit-3_gray.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_shortDescrip_icon.setIcon(icon4)
        self.project_shortDescrip_icon.setObjectName("project_shortDescrip_icon")
        self.horizontalLayout_11.addWidget(self.project_shortDescrip_icon)
        self.project_shortDescrip = QtWidgets.QLabel(parent=self.project_shortDescrip_label)
        self.project_shortDescrip.setObjectName("project_shortDescrip")
        self.horizontalLayout_11.addWidget(self.project_shortDescrip)
        self.gridLayout_4.addWidget(self.project_shortDescrip_label, 0, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(parent=self.project_shortDescrip_frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4.addWidget(self.frame_4, 1, 0, 1, 1)
        self.project_shortDescrip_info = QtWidgets.QTextEdit(parent=self.project_shortDescrip_frame)
        self.project_shortDescrip_info.setReadOnly(False)
        self.project_shortDescrip_info.setPlaceholderText("")
        self.project_shortDescrip_info.setObjectName("project_shortDescrip_info")
        self.gridLayout_4.addWidget(self.project_shortDescrip_info, 0, 1, 2, 1)
        self.gridLayout_6.addWidget(self.project_shortDescrip_frame, 5, 0, 1, 2)
        self.project_tasks_frame = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.project_tasks_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_tasks_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_tasks_frame.setObjectName("project_tasks_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.project_tasks_frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.project_tasks_label = QtWidgets.QFrame(parent=self.project_tasks_frame)
        self.project_tasks_label.setMinimumSize(QtCore.QSize(151, 41))
        self.project_tasks_label.setMaximumSize(QtCore.QSize(151, 41))
        self.project_tasks_label.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_tasks_label.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_tasks_label.setObjectName("project_tasks_label")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.project_tasks_label)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.project_tasks_icon = QtWidgets.QPushButton(parent=self.project_tasks_label)
        self.project_tasks_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.project_tasks_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.project_tasks_icon.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/clipboard_gray.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_tasks_icon.setIcon(icon5)
        self.project_tasks_icon.setObjectName("project_tasks_icon")
        self.horizontalLayout_12.addWidget(self.project_tasks_icon)
        self.project_tasks = QtWidgets.QLabel(parent=self.project_tasks_label)
        self.project_tasks.setObjectName("project_tasks")
        self.horizontalLayout_12.addWidget(self.project_tasks)
        self.gridLayout_2.addWidget(self.project_tasks_label, 0, 0, 1, 2)
        self.frame = QtWidgets.QFrame(parent=self.project_tasks_frame)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2.addWidget(self.frame, 0, 2, 1, 1)
        self.frame_5 = QtWidgets.QFrame(parent=self.project_tasks_frame)
        self.frame_5.setMinimumSize(QtCore.QSize(35, 0))
        self.frame_5.setMaximumSize(QtCore.QSize(35, 16777215))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_2.addWidget(self.frame_5, 1, 0, 1, 1)
        self.project_tasks_info = QtWidgets.QListWidget(parent=self.project_tasks_frame)
        self.project_tasks_info.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.project_tasks_info.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.project_tasks_info.setObjectName("project_tasks_info")
        self.gridLayout_2.addWidget(self.project_tasks_info, 1, 1, 1, 2)
        self.gridLayout_6.addWidget(self.project_tasks_frame, 6, 0, 1, 1)
        self.project_members_frame = QtWidgets.QFrame(parent=self.projects_expand_frame)
        self.project_members_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_members_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_members_frame.setObjectName("project_members_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.project_members_frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.project_members_label = QtWidgets.QFrame(parent=self.project_members_frame)
        self.project_members_label.setMinimumSize(QtCore.QSize(151, 41))
        self.project_members_label.setMaximumSize(QtCore.QSize(151, 41))
        self.project_members_label.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.project_members_label.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.project_members_label.setObjectName("project_members_label")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.project_members_label)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.project_members_icon = QtWidgets.QPushButton(parent=self.project_members_label)
        self.project_members_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.project_members_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.project_members_icon.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/users_gray.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.project_members_icon.setIcon(icon6)
        self.project_members_icon.setObjectName("project_members_icon")
        self.horizontalLayout_14.addWidget(self.project_members_icon)
        self.project_members = QtWidgets.QLabel(parent=self.project_members_label)
        self.project_members.setObjectName("project_members")
        self.horizontalLayout_14.addWidget(self.project_members)
        self.gridLayout_3.addWidget(self.project_members_label, 0, 0, 1, 2)
        self.frame_3 = QtWidgets.QFrame(parent=self.project_members_frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3.addWidget(self.frame_3, 0, 2, 1, 1)
        self.frame_6 = QtWidgets.QFrame(parent=self.project_members_frame)
        self.frame_6.setMinimumSize(QtCore.QSize(35, 0))
        self.frame_6.setMaximumSize(QtCore.QSize(35, 16777215))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_3.addWidget(self.frame_6, 1, 0, 1, 1)
        self.project_members_info = QtWidgets.QListWidget(parent=self.project_members_frame)
        self.project_members_info.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.project_members_info.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.project_members_info.setObjectName("project_members_info")
        self.gridLayout_3.addWidget(self.project_members_info, 1, 1, 1, 2)
        self.gridLayout_6.addWidget(self.project_members_frame, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.projects_expand_frame, 0, 0, 1, 1)

        frames = [self.projects_expand_frame]
        for frame in frames:
            shadow = QGraphicsDropShadowEffect(frame)
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 0)
            shadow.setColor(QColor(0, 0, 0, 80))
            frame.setGraphicsEffect(shadow)

        self.retranslateUi(projects_expand)
        QtCore.QMetaObject.connectSlotsByName(projects_expand)

    def retranslateUi(self, projects_expand):
        _translate = QtCore.QCoreApplication.translate
        projects_expand.setWindowTitle(_translate("projects_expand", "Dialog"))
        self.project_name.setText(_translate("projects_expand", "Project Name"))
        self.project_update_button.setText(_translate("projects_expand", "Update"))
        self.project_delete_button.setText(_translate("projects_expand", "Delete"))
        self.project_id.setText(_translate("projects_expand", "Project ID"))
        self.project_startDate.setText(_translate("projects_expand", "Start Date"))
        self.project_endDate.setText(_translate("projects_expand", "End Date"))
        self.project_shortDescrip.setText(_translate("projects_expand", "Description"))
        self.project_shortDescrip_info.setHtml(_translate("projects_expand", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Poppins,sans-serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.project_tasks.setText(_translate("projects_expand", "Tasks"))
        self.project_members.setText(_translate("projects_expand", "Members"))
