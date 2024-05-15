from cache.account import CacheController
from httpx import Client
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from windows.main import MainWindow
from workers.auth import AuthWorker

from client.settings import PASSPORT_SERVICE_URL


class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.client = Client(base_url=PASSPORT_SERVICE_URL)
        self.cache = CacheController()

        self.setWindowTitle("Sign In")
        self.setGeometry(800, 400, 400, 200)

        layout = QVBoxLayout()

        self.label_username = QLabel("Login:")
        self.edit_login = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.edit_login)

        self.label_password = QLabel("Password:")
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)

        self.button_sing_in = QPushButton("Sign In")
        self.button_sing_in.clicked.connect(self.sign_in)
        layout.addWidget(self.button_sing_in)

        self.button_sing_up = QPushButton("Sing Up")
        self.button_sing_up.clicked.connect(self.sign_up)
        layout.addWidget(self.button_sing_up)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_menu()
        self.show()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        operations_menu = menu_bar.addMenu("Operations")
        clear_action = QAction("Clear fields", self)
        clear_action.triggered.connect(self.clear_fields)
        operations_menu.addAction(clear_action)

        reference_menu = menu_bar.addMenu("Reference")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        reference_menu.addAction(about_action)

    def clear_fields(self):
        self.edit_login.clear()
        self.edit_password.clear()

    def show_about_dialog(self):
        about_text = "App for control your money"
        QMessageBox.about(self, "About", about_text)

    def sign_in(self):
        login = self.edit_login.text()
        password = self.edit_password.text()

        try:
            assert len(login) > 0
        except AssertionError:
            self.error_handler("Login must not be empty")
            return

        try:
            assert len(password) > 0
        except AssertionError:
            self.error_handler("Password must not be empty")
            return

        worker = AuthWorker(self.client, "/login", login, password)
        worker.success.connect(self.success_handler)
        worker.error.connect(self.error_handler)
        worker.start()

    def sign_up(self):
        login = self.edit_login.text()
        password = self.edit_password.text()

        try:
            assert len(login) > 0
        except AssertionError:
            self.error_handler("Login must not be empty")
            return

        try:
            assert len(password) > 0
        except AssertionError:
            self.error_handler("Password must not be empty")
            return

        worker = AuthWorker(self.client, "/register", login, password)
        worker.success.connect(self.success_handler)
        worker.error.connect(self.error_handler)
        worker.start()

    def success_handler(self, data: dict):
        self.hide()
        self.cache.write_cache(data=data)
        self.main_window = MainWindow(login=data["login"], authorization=data["authorization"])
        self.main_window.change.connect(self.change_handler)
        self.main_window.show()

    def change_handler(self):
        self.show()
        self.cache.clear_cache()
        self.clear_fields()
        self.client.cookies.clear()
        self.main_window.close()

    def error_handler(self, detail: str):
        QMessageBox.warning(self, "Error", detail)

    def redirect(self, data: dict):
        self.hide()
        self.main_window = MainWindow(login=data["login"], authorization=data["authorization"])
        self.main_window.change.connect(self.change_handler)
        self.main_window.show()
