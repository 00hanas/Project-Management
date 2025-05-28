from PyQt5.QtCore import QObject, pyqtSignal, QRunnable

class ProjectSearchWorkerSignals(QObject):
    finished = pyqtSignal(list)

class ProjectSearchWorker(QRunnable):
    def __init__(self, keyword, search_by):
        super().__init__()
        self.keyword = keyword
        self.search_by = search_by
        self.signals = ProjectSearchWorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        from controllers.project_controller import searchProjects
        results = searchProjects(self.keyword, self.search_by)
        project_ids = [proj["projectID"] for proj in results]
        self.signals.finished.emit(project_ids)
