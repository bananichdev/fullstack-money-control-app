from PyQt6.QtCore import QThread, pyqtSignal


class BaseWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.success.connect(self.deleteLater)
        self.success.connect(self.wait)
        self.error.connect(self.deleteLater)
        self.error.connect(self.wait)
