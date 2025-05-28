from PyQt6.QtCore import QObject, pyqtSignal, QRunnable
from controllers.project_controller import searchProjects, getAllProjects

class ProjectSearchWorkerSignals(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

class ProjectSearchWorker(QRunnable):
    def __init__(self, keyword, search_by):
        super().__init__()
        self.keyword = keyword.strip()
        self.search_by = search_by
        self.signals = ProjectSearchWorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            if not self.keyword:
                # Return all projects when search is empty
                results = getAllProjects()
                project_ids = [project[0] for project in results]  # Assuming projectID is first column
            else:
                results = searchProjects(self.keyword, self.search_by)
                project_ids = [proj["projectID"] for proj in results]
            
            self.signals.finished.emit(project_ids)
        except Exception as e:
            self.signals.error.emit(str(e))