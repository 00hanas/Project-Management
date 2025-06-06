from PyQt6.QtCore import QObject, pyqtSignal, QRunnable
from controllers.task_controller import searchTasks, getAllTasks

# In both TaskSearchWorker.py and ProjectSearchWorker.py
# Add a signal for incremental updates
class TaskSearchWorkerSignals(QObject):
    finished = pyqtSignal(list)
    incremental = pyqtSignal(list)  # New signal for partial results
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
                results = getAllTasks()  # Or getAllProjects()
                self.signals.incremental.emit(results[:10])  # Emit first batch
                self.signals.incremental.emit(results[10:])  # Emit remaining
            else:
                results = searchTasks(self.keyword, self.search_by)
                self.signals.incremental.emit(results[:10])  # Emit first batch
                self.signals.incremental.emit(results[10:])  # Emit remaining
            
            self.signals.finished.emit(results)
        except Exception as e:
            self.signals.error.emit(str(e))