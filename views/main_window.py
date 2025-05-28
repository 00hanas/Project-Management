import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QCalendarWidget, QMainWindow, QAbstractItemView, QMessageBox, QTableWidgetItem, QListWidget, QListWidgetItem, QGridLayout, QSizePolicy, QScrollArea
from PyQt6.QtWidgets import QWidget, QVBoxLayout # Import QVBoxLayout
from ui.main_interface import Ui_MainWindow
from views.project_view import AddProjectForm, EditProjectForm, ProjectExpandDialog
from views.task_view import AddTaskForm, EditTaskForm, TaskExpandDialog
from views.member_view import expandRow, EditMemberForm, AddMemberForm
from controllers.dashboard_controller import getTotalProjectCount, getTotalTaskCount, getTotalMemberCount, getCalendarEvents, getAllProjectsTasksMembers
from controllers.member_controller import searchMembers, getAllMembersForSearch
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QDate, Qt, QTimer, QThreadPool, QPoint, QDateTime # Import QDateTime
from datetime import datetime
from controllers.project_controller import getTotalTasks, getMembersForProject, searchProjects, getAllProjectsForSearch, getAllProjects
from controllers.task_controller import getMembersForTask
from widgets.TaskCardWidget import TaskCardWidget
from widgets.ProjectCardWidget import ProjectCardWidget
from utils.searchworker_homesearch import SearchWorker
from utils.ProjectSearchWorker import ProjectSearchWorker
from models.project import loadProjects
from models.task import loadTasks
from PyQt6 import QtWidgets 
from utils.TaskSearchWorker import TaskSearchWorker
from controllers.task_controller import getAllTasksForSearch

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

        # Navigation to pages
        self.ui.home_button.clicked.connect(lambda: self.switchPage(0)) 
        self.ui.projects_button.clicked.connect(lambda: self.switchPage(1))
        self.ui.tasks_button.clicked.connect(lambda: self.switchPage(2))
        self.ui.members_button.clicked.connect(lambda: self.switchPage(3))

        self.ui.projects_total_count.clicked.connect(lambda: self.switchPage(1))
        self.ui.tasks_total_count.clicked.connect(lambda: self.switchPage(2))
        self.ui.members_total_count.clicked.connect(lambda: self.switchPage(3))

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
        self.threadpool = QThreadPool()
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.performHomeSearch)
        self.ui.home_search.textChanged.connect(lambda: self.search_timer.start(200))
        self.ui.home_searchby.currentIndexChanged.connect(self.performHomeSearch)
        self.ui.home_search.setPlaceholderText("Search projects, tasks, or members...")
        self.search_suggestion = QListWidget()
        self.search_suggestion.setParent(None)  # No parent (acts as top-level window)
        self.search_suggestion.setWindowFlags(Qt.WindowType.ToolTip)  # Allows interaction without blocking focus
        self.search_suggestion.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search_suggestion.setMouseTracking(True)
        self.search_suggestion.setParent(self)

        self.search_suggestion.hide()
        self.search_suggestion.itemClicked.connect(self.handleSuggestionClicked)
        self.search_suggestion.setStyleSheet("""
            QListWidget {
                border: 1px solid #edf4fa;
                border-radius: 8px;
                padding: 4px;
                font-family: "Poppins", sans-serif;
                font-size: 14px;
                background-color: #edf4fa;
                color: black;
            }
            QListWidget::item {
                padding: 4px 10px;
                border-radius: 8px;
            }
            QListWidget::item:hover {
                background-color: #bbddfa;
                color: black;
            }
            QListWidget::item:selected {
                background-color: #8f89fa;
                color: black;
            }
            """)

        # Member search functionality
        self.ui.members_search.textChanged.connect(self.performSearchforMembers)
        self.ui.members_searchby.currentIndexChanged.connect(self.performSearchforMembers)

        # Project search functionality
        self.currently_showing_all_projects = True  # Start by showing all projects
        self.project_search_timer = QTimer(self)
        self.project_search_timer.setSingleShot(True)
        self.project_search_timer.setInterval(100)  # 300ms delay after typing stops
        self.project_search_timer.timeout.connect(self.performSearchforProjects)

        self.ui.projects_search.textChanged.connect(self.handleProjectSearchChanged)
        self.ui.projects_searchby.currentIndexChanged.connect(self.performSearchforProjects)

        # Task search functionality
        self.currently_showing_all_tasks = True
        self.task_search_timer = QTimer(self)
        self.task_search_timer.setSingleShot(True)
        self.task_search_timer.setInterval(100)
        self.task_search_timer.timeout.connect(self.performSearchforTasks)

        self.ui.tasks_search.textChanged.connect(self.handleTaskSearchChanged)
        self.ui.tasks_searchby.currentIndexChanged.connect(self.performSearchforTasks)

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

        # Setup project connections
        self.setup_project_connections()

        # Setup task connections
        self.setup_task_connections()

        # Track selected project
        self.selected_project = None
        # Track selected task
        self.selected_task = None

        # Connect expand buttons
        self.ui.project_expand_button.clicked.connect(self.handle_project_expand)
        self.ui.task_expand_button.clicked.connect(self.handle_task_expand)

    def setup_project_connections(self):
        """Setup connections for project cards"""
        print("Setting up project connections...")

        # The ProjectVContainer is the widget added to horizontalLayout_7
        h_layout = self.ui.horizontalLayout_7
        if h_layout.count() == 0:
            print("Error: horizontalLayout_7 is empty in setup_project_connections.")
            return

        # Assuming the ProjectVContainer is the first (and only) widget in this layout after refresh
        project_v_container_widget = h_layout.itemAt(0).widget()

        if not project_v_container_widget or project_v_container_widget.objectName() != "ProjectVContainer":
            print(f"Error: Could not find ProjectVContainer in horizontalLayout_7. Found: {project_v_container_widget}")
            return
        
        print(f"Found projects_container (ProjectVContainer): {project_v_container_widget.objectName()}")

        project_cards = project_v_container_widget.findChildren(ProjectCardWidget)
        print(f"Found {len(project_cards)} project cards within ProjectVContainer")

        # Connect each card's signal
        for project_card in project_cards:
            try:
                # Disconnect any existing connections first
                try:
                    project_card.clicked.disconnect()
                except:
                    pass # No existing connection to disconnect

                # Connect with lambda to preserve project data
                project_card.clicked.connect(
                    lambda checked, data=project_card.project_data: self.update_project_details(data)
                )
            except Exception as e:
                print(f"Error connecting project card: {e}")
        print("Finished setting up project connections.")


    def setup_task_connections(self):
        """Setup connections for task cards"""
        print("Setting up task connections...")

        h_layout = self.ui.horizontalLayout_14 # Assuming this is the layout for tasks
        if h_layout.count() == 0:
            print("Error: horizontalLayout_14 is empty in setup_task_connections.")
            return

        task_v_container_widget = h_layout.itemAt(0).widget()

        if not task_v_container_widget or task_v_container_widget.objectName() != "TaskVContainer": # Ensure correct object name
            print(f"Error: Could not find TaskVContainer in horizontalLayout_14. Found: {task_v_container_widget}")
            return
            
        print(f"Found tasks_container (TaskVContainer): {task_v_container_widget.objectName()}")

        task_cards = task_v_container_widget.findChildren(TaskCardWidget)
        print(f"Found {len(task_cards)} task cards within TaskVContainer")

        for task_card in task_cards:
            try:
                try:
                    task_card.clicked.disconnect()
                except:
                    pass
                task_card.clicked.connect(
                    lambda checked, data=task_card.task_data: self.update_task_details(data)
                )
            except Exception as e:
                print(f"Error connecting task card: {e}")
        print("Finished setting up task connections.")

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
            self.refresh_container('home')
            self.refresh_container('task')
            self.refresh_container('project')

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

    def handleProjectSearchChanged(self):
        """Handle text changes in project search field"""
        if not self.ui.projects_search.text().strip():
            # If field is being cleared, perform search immediately
            self.project_search_timer.stop()  # Cancel any pending timer
            self.performSearchforProjects()
        else:
            # For normal typing, use the timer
            self.project_search_timer.start()

    def performSearchforProjects(self):
        """Perform the project search with current parameters"""
        keyword = self.ui.projects_search.text().strip()
        search_by = self.ui.projects_searchby.currentText()
        
        worker = ProjectSearchWorker(keyword, search_by)
        worker.signals.finished.connect(self.updateProjectWidgets)
        worker.signals.error.connect(self.showSearchError)
        QThreadPool.globalInstance().start(worker)

    def loadAllProjects(self):
        """Load all projects when search field is empty"""
        all_projects = getAllProjects()  # This should return all projects
        project_ids = [project[0] for project in all_projects]  # Assuming projectID is first element
        self.updateProjectWidgets(project_ids)

    def showSearchError(self, error_msg):
        QMessageBox.warning(self, "Search Error", f"An error occurred during search:\n{error_msg}")

    def updateProjectWidgets(self, project_ids: list[str]):
        # Find the projects container in the stacked widget
        projects_page = self.ui.stackedWidget.widget(1)  # Projects page is index 1
        projects_container = projects_page.findChild(QWidget, "ProjectVContainer")

        if not projects_container:
            print("Error: Could not find ProjectVContainer")
            return
        
        # Find the scroll area and content widget
        scroll_area = projects_container.findChild(QScrollArea, "ProjectScrollArea")
        if not scroll_area:
            print("Error: Could not find ProjectScrollArea")
            return
        
        content = scroll_area.widget()
        if not content:
            print("Error: Scroll area has no content widget")
            return


        grid = content.layout()
        if grid is None:
            print("[DEBUG] Layout is None! This should not happen unless content was replaced.")
            print(f"[DEBUG] content type: {type(content)} repr: {repr(content)}")
            return

        # Clear existing widgets
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            else:
                # Remove spacers or other items
                del item

        #all_projects = getAllProjectsForSearch(project_ids)
        all_projects = getAllProjectsForSearch(project_ids)
        headers = ["projectID", "projectName", "shortDescrip", "startDate", "endDate"]

        scroll_area.setWidgetResizable(True)
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        columns = 3
        for index, project in enumerate(all_projects):
            project_dict = dict(zip(headers, project))
            widget = ProjectCardWidget(project_dict)
            widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            
            # Connect the clicked signal
            widget.clicked.connect(
                lambda checked, data=project_dict: self.update_project_details(data)
            )
            
            row = index // columns
            col = index % columns
            grid.addWidget(widget, row, col)

        # Adjust content height
        card_height = 150
        rows = (len(all_projects) + columns - 1) // columns
        content.setFixedHeight(rows * card_height)
        content.updateGeometry()
        content.repaint()


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

        if search_by == "Search by":
            search_by = ""

        results = getAllProjectsTasksMembers(keyword, search_by)
        self.updateSearchSuggestions(results)

        self.ui.home_search.setFocus()  # Give focus back to the search box

        worker = SearchWorker(keyword, search_by)
        worker.signals.finished.connect(self.updateSearchSuggestions)
        self.threadpool.start(worker)

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

        if not self.search_suggestion.isVisible():
            self.search_suggestion.setParent(None)
            self.search_suggestion.setWindowFlags(
                Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint
            )

        # Position and show suggestion popup
        home_search = self.ui.home_search
        global_pos = home_search.mapToGlobal(home_search.rect().bottomLeft())
        self.search_suggestion.move(global_pos + QPoint(0, 1))

        self.search_suggestion.resize(
            self.ui.home_search.width(),
            min(200, self.search_suggestion.sizeHintForRow(0) * self.search_suggestion.count() + 10)
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
        self.ui.home_search.clear()

    def navigateToProject(self, project_id):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.home_search.clear()
        # Optionally scroll to or highlight project row in table

    def navigateToTask(self, task_id):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.home_search.clear()
        # Optionally scroll to or highlight task row in table

    def navigateToMember(self, member_id):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.home_search.clear()
        table = self.ui.members_table
        table.clearSelection()
        table.setFocus()
        table.setStyleSheet("""
            QTableWidget::item:selected {
            background-color: #01c28e;
            color: white;
            }
            """)

        for row in range(table.rowCount()):
            item = table.item(row, 0)  # Assuming member_id is in column 0
            if item and item.text().strip() == member_id.strip():
                table.selectRow(row)
                table.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
                return  # stop once found

    def update_project_details(self, project_data: dict):
        print(f"--- MainApp.update_project_details called for project: {project_data.get('projectID', 'N/A')} ---")
        self.selected_project = project_data
        print(f"self.selected_project is NOW: {self.selected_project.get('projectID') if self.selected_project else 'None'}")


        try:
            # Project Name
            self.ui.project_name_info.setText(project_data['projectName'])
            # Project ID
            self.ui.project_id_info.setText(project_data['projectID'])

            # Format and set dates
            start_date = project_data.get('startDate', '')
            if start_date:
                try:
                    date_obj = start_date if isinstance(start_date, datetime) else datetime.strptime(str(start_date).split()[0], '%Y-%m-%d')
                    formatted_start = date_obj.strftime("%B %d, %Y")
                    self.ui.project_startDate_info.setText(formatted_start)
                except Exception as e:
                    print(f"Error formatting start date in update_project_details: {e}")
                    self.ui.project_startDate_info.setText(str(start_date))

            end_date = project_data.get('endDate', '')
            if end_date:
                try:
                    date_obj = end_date if isinstance(end_date, datetime) else datetime.strptime(str(end_date).split()[0], '%Y-%m-%d')
                    formatted_end = date_obj.strftime("%B %d, %Y")
                    self.ui.project_endDate_info.setText(formatted_end)
                except Exception as e:
                    print(f"Error formatting end date in update_project_details: {e}")
                    self.ui.project_endDate_info.setText(str(end_date))

            # Get and set task count
            total_tasks = getTotalTasks(project_data['projectID'])
            self.ui.project_totalTasks_info.setText(str(total_tasks))

            # Get and set member count
            try:
                members = getMembersForProject(project_data['projectID'])
                self.ui.project_totalMembers_info.setText(str(len(members)))
            except Exception as e:
                print(f"Error getting members: {e}")
                self.ui.project_totalMembers_info.setText('0')
            
            print(f"--- MainApp.update_project_details FINISHED for project: {project_data['projectID']} ---")

        except Exception as e:
            print(f"Error in update_project_details: {e}")
            import traceback
            print(traceback.format_exc())


    def update_task_details(self, task_data: dict):
        """Update task details in the UI"""
        print(f"--- MainApp.update_task_details called for task: {task_data.get('taskID', 'N/A')} ---")
        self.selected_task = task_data
        print(f"self.selected_task is NOW: {self.selected_task.get('taskID') if self.selected_task else 'None'}")

        try:
            # Task Name
            self.ui.task_name_info.setText(task_data['taskName'])
            # Task ID
            self.ui.task_id_info.setText(task_data['taskID'])
            # Project ID
            self.ui.task_project_info.setText(task_data['projectID'])
            # Status
            self.ui.task_status_info.setText(task_data.get('currentStatus', 'Not Set'))

            # Due Date
            due_date = task_data.get('dueDate', '')
            if due_date:
                try:
                    date_obj = due_date if isinstance(due_date, datetime) else datetime.strptime(str(due_date).split()[0], '%Y-%m-%d')
                    formatted_date = date_obj.strftime("%B %d, %Y")
                    self.ui.task_dueDate_info.setText(formatted_date)
                except Exception as e:
                    print(f"Error formatting due date in update_task_details: {e}")
                    self.ui.task_dueDate_info.setText(str(due_date))

            # Member Count
            try:
                members = getMembersForTask(task_data['taskID'])
                self.ui.task_totalMembers_info.setText(str(len(members)))
            except Exception as e:
                print(f"Error getting members for task: {e}")
                self.ui.task_totalMembers_info.setText('0')
            
            print(f"--- MainApp.update_task_details FINISHED for task: {task_data['taskID']} ---")

        except Exception as e:
            print(f"Error in update_task_details: {e}")
            import traceback
            print(traceback.format_exc())

    def switchPage(self, page_index: int):
        self.ui.stackedWidget.setCurrentIndex(page_index)
        self.ui.home_search.clear()
        self.search_suggestion.hide()

    def handle_project_expand(self):
        if not self.selected_project:
            QMessageBox.warning(self, "No Selection", "Please select a project first.")
            return

        try:
            print(f"Opening project expand dialog for project: {self.selected_project['projectID']}")
            # Pass the MainApp instance (self) as the main_window_instance
            expand_dialog = ProjectExpandDialog(self.selected_project, main_window_instance=self)
            expand_dialog.exec()
            self.refreshTable()
            # After the dialog closes, the main window's project list might need an update
            # if a delete happened, which is handled by the dialog itself calling refresh_container.
            # If an update happened via EditProjectForm, that form also calls refresh_container.
        except Exception as e:
            print(f"Error handling project expand: {e}")
            import traceback
            print(traceback.format_exc())

    def handle_task_expand(self):
        if not self.selected_task:
            QMessageBox.warning(self, "No Selection", "Please select a task first")
            return

        try:
            print(f"Opening task expand dialog for task: {self.selected_task['taskID']}")
            expand_dialog = TaskExpandDialog(self.selected_task, main_window_instance=self)
            expand_dialog.exec()
            self.refreshTable()
            # Refreshing and clearing details pane is handled by TaskExpandDialog's delete/update methods
        except Exception as e:
            print(f"Error handling task expand: {e}")
            import traceback
            print(traceback.format_exc())

    def clear_project_details_pane(self):
        """Clears the project details pane and the selected_project variable."""
        print("Clearing project details pane...")
        self.selected_project = None
        self.ui.project_name_info.setText("")
        self.ui.project_id_info.setText("")
        self.ui.project_startDate_info.setText("")
        self.ui.project_endDate_info.setText("")
        self.ui.project_totalTasks_info.setText("")
        self.ui.project_totalMembers_info.setText("")
        print("Project details pane cleared.")

    def clear_task_details_pane(self):
        """Clears the task details pane and the selected_task variable."""
        print("Clearing task details pane...")
        self.selected_task = None
        self.ui.task_name_info.setText("")
        self.ui.task_id_info.setText("")
        self.ui.task_project_info.setText("")
        self.ui.task_status_info.setText("")
        self.ui.task_dueDate_info.setText("")
        self.ui.task_totalMembers_info.setText("")
        print("Task details pane cleared.")


    def refresh_container(self, container_type: str):
        """Refresh project or task container"""
        print(f"Entering refresh_container for {container_type}")
        try:
            if container_type == 'project':
                layout = self.ui.horizontalLayout_7
                print(f"Before deletion - Widget count in horizontalLayout_7: {layout.count()}")
                print(f"Before deletion - Widget at index 0: {layout.itemAt(0).widget() if layout.count() > 0 else 'None'}")

                # Explicitly remove and delete all items in the layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                QtWidgets.QApplication.processEvents() # Process events to ensure deletion
                print("All old widgets removed from layout")


                # Create and add new container
                new_container = loadProjects(self.ui.projects_container)
                layout.addWidget(new_container)

                # Setup connections for new container
                self.setup_project_connections()
                self.clear_project_details_pane() # Clear details after refreshing

                print(f"After refresh - Widget count in horizontalLayout_7: {layout.count()}")
                print(f"After refresh - Widget at index 0: {layout.itemAt(0).widget() if layout.count() > 0 else 'None'}")
                print("Project container refreshed")

            elif container_type == 'task':
                layout = self.ui.horizontalLayout_14
                print(f"Before deletion - Widget count in horizontalLayout_14: {layout.count()}")
                print(f"Before deletion - Widget at index 0: {layout.itemAt(0).widget() if layout.count() > 0 else 'None'}")

                # Explicitly remove and delete all items in the layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                QtWidgets.QApplication.processEvents() # Process events to ensure deletion
                print("All old widgets removed from layout")

                # Create and add new container
                new_container = loadTasks(self.ui.tasks_container)
                layout.addWidget(new_container)

                # Setup connections for new container
                self.setup_task_connections()
                self.clear_task_details_pane() # You would create a similar method for tasks

                print(f"After refresh - Widget count in horizontalLayout_14: {layout.count()}")
                print(f"After refresh - Widget at index 0: {layout.itemAt(0).widget() if layout.count() > 0 else 'None'}")
                print("Task container refreshed")
            
            elif container_type == 'home':
                layout = self.ui. verticalLayout_9
                print(f"Before deletion - Widget count in verticalLayout_9: {layout.count()}")
                print(f"Before deletion - Widget at index 0: {layout.itemAt(0).widget() if layout.count() > 0 else 'None'}")
                
                # Explicitly remove and delete all items in the layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                QtWidgets.QApplication.processEvents() # Process events to ensure deletion
                print("All old widgets removed from layout")
                
                new_container = loadProjects(self.ui.view_projects)
                layout.addWidget(new_container)
                                 


        except Exception as e:
            print(f"Error refreshing {container_type} container: {e}")
            import traceback
            print(traceback.format_exc())

    def handleTaskSearchChanged(self):
        """Handle text changes in task search field"""
        if not self.ui.tasks_search.text().strip():
            # If field is being cleared, perform search immediately
            self.task_search_timer.stop()
            self.performSearchforTasks()
        else:
            # For normal typing, use the timer
            self.task_search_timer.start()

    def performSearchforTasks(self):
        """Perform the task search with current parameters"""
        keyword = self.ui.tasks_search.text().strip()
        search_by = self.ui.tasks_searchby.currentText()
        
        worker = TaskSearchWorker(keyword, search_by)
        worker.signals.finished.connect(self.updateTaskWidgets)
        worker.signals.error.connect(self.showSearchError)
        QThreadPool.globalInstance().start(worker)

    def updateTaskWidgets(self, task_ids: list[str]):
        # Find the tasks container in the stacked widget
        tasks_page = self.ui.stackedWidget.widget(2)  # Tasks page is index 2
        tasks_container = tasks_page.findChild(QWidget, "TaskVContainer")

        if not tasks_container:
            print("Error: Could not find TaskVContainer")
            return
        
        # Find the scroll area and content widget
        scroll_area = tasks_container.findChild(QScrollArea, "TaskScrollArea")
        if not scroll_area:
            print("Error: Could not find TaskScrollArea")
            return
        
        content = scroll_area.widget()
        if not content:
            print("Error: Scroll area has no content widget")
            return

        grid = content.layout()
        if grid is None:
            print("[DEBUG] Layout is None! This should not happen unless content was replaced.")
            print(f"[DEBUG] content type: {type(content)} repr: {repr(content)}")
            return

        # Clear existing widgets
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            else:
                # Remove spacers or other items
                del item

        all_tasks = getAllTasksForSearch(task_ids)
        headers = ["taskID", "taskName", "shortDescrip", "currentStatus", "dueDate", "dateAccomplished", "projectID"]

        scroll_area.setWidgetResizable(True)
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        columns = 3
        for index, task in enumerate(all_tasks):
            task_dict = dict(zip(headers, task))
            widget = TaskCardWidget(task_dict)
            widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            
            # Connect the clicked signal
            widget.clicked.connect(
                lambda checked, data=task_dict: self.update_task_details(data)
            )
            
            row = index // columns
            col = index % columns
            grid.addWidget(widget, row, col)

        # Adjust content height
        card_height = 170
        rows = (len(all_tasks) + columns - 1) // columns
        content.setFixedHeight(rows * card_height)
        content.updateGeometry()
        content.repaint()