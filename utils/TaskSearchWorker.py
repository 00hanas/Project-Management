from PyQt6.QtCore import QObject, pyqtSignal, QRunnable
from controllers.task_controller import searchTasks, getAllTasks

class TaskSearchWorkerSignals(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

class TaskSearchWorker(QRunnable):
    def __init__(self, keyword, search_by):
        super().__init__()
        self.keyword = keyword.strip()
        self.search_by = search_by
        self.signals = TaskSearchWorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            if not self.keyword:
                # Return all tasks when search is empty
                results = getAllTasks()
                task_ids = [task["taskID"] for task in results]
            else:
                results = searchTasks(self.keyword, self.search_by)
                task_ids = [task["taskID"] for task in results]
            
            self.signals.finished.emit(task_ids)
        except Exception as e:
            self.signals.error.emit(str(e))