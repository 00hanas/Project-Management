from PyQt6.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

class SearchWorkerSignals(QObject):
    finished = pyqtSignal(list)

class SearchWorker(QRunnable):
    def __init__(self, keyword, search_by):
        super().__init__()
        self.keyword = keyword
        self.search_by = search_by
        self.signals = SearchWorkerSignals()

    @pyqtSlot()
    def run(self):
        from controllers.dashboard_controller import getAllProjectsTasksMembers
        results = getAllProjectsTasksMembers(self.keyword, self.search_by)
        self.signals.finished.emit(results)
