from datetime import date

from httpx import Client
from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QCalendarWidget,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from settings import BASE_API_V1_URL
from utils.internal import get_category_id_by_name, get_category_name_by_id
from workers.main import (
    AccountInfoWorker,
    DeleteCategoryWorker,
    DeletePurchaseWorker,
    GetCategoriesWorker,
    GetOperationsWorker,
    GetPurchasesWorker,
    PostCategoryWorker,
    PostPurchaseWorker,
    PutBalanceWorker,
    PutCategoryWorker,
)


class MainWindow(QMainWindow):
    change = pyqtSignal()

    def __init__(self, login: str, authorization: str):
        super().__init__()

        self.client = Client(base_url=BASE_API_V1_URL, cookies={"authorization": authorization})
        self.categories = []

        worker = GetCategoriesWorker(self.client)
        worker.success.connect(self.get_categories)
        worker.error.connect(self.error_handler)
        worker.start()

        self.setWindowTitle("Control your money app")
        self.setGeometry(600, 300, 800, 600)

        self.start_widget = QWidget()
        start_layout = QVBoxLayout()
        account_label = QLabel("Account:")
        login_button = QPushButton(login)
        login_button.clicked.connect(self.account_info)
        start_layout.addWidget(account_label)
        start_layout.addWidget(login_button)
        operations_label = QLabel("Operations:")
        start_layout.addWidget(operations_label)
        self.start_widget.setLayout(start_layout)
        navigation_layout = QHBoxLayout()
        my_purchases_button = QPushButton("My purchases")
        my_purchases_button.clicked.connect(self.my_purchases)
        my_categories_button = QPushButton("My categories")
        my_categories_button.clicked.connect(self.my_categories)
        my_wallet_button = QPushButton("My wallet")
        my_wallet_button.clicked.connect(self.my_wallet)
        navigation_layout.addWidget(my_purchases_button)
        navigation_layout.addWidget(my_categories_button)
        navigation_layout.addWidget(my_wallet_button)
        start_layout.addLayout(navigation_layout)
        start_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.add_purchase_widget = QWidget()
        add_purchase_layout = QVBoxLayout()
        add_purchase_button = QPushButton("Add purchase")
        add_purchase_button.setStyleSheet("background: #F75E25;")
        add_purchase_button.clicked.connect(self.post_purchase)
        filters_layout = QVBoxLayout()
        category_label = QLabel("Category:")
        date_label = QLabel("Date:")
        filters_layout.addWidget(category_label)
        self.category_filter_box = QComboBox()
        self.category_filter_box.addItem("Any")
        for category in self.categories:
            self.category_filter_box.addItem(category["name"])
        filters_layout.addWidget(self.category_filter_box)
        filters_layout.addWidget(date_label)
        self.date_filter_button = QPushButton("Show Calendar")
        self.date_filter_button.clicked.connect(self.show_calendar)
        filters_layout.addWidget(self.date_filter_button)
        self.date_filter_edit = QLineEdit()
        self.date_filter_edit.setPlaceholderText("Date (Format: DD.MM.YYYY)")
        filters_layout.addWidget(self.date_filter_edit)

        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(300, 200)
        filters_layout.addWidget(self.calendar)
        self.calendar.hide()
        self.calendar.clicked.connect(self.select_date)

        apply_button = QPushButton("Apply")
        apply_button.setStyleSheet("background: #F75E25;")
        apply_button.clicked.connect(self.apply_filters)
        filters_layout.addWidget(apply_button)
        self.purchases_table = QTableWidget()
        self.purchases_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.purchases_table.setColumnCount(5)
        for column in range(0, 5):
            self.purchases_table.setColumnWidth(column, 147)
        self.purchases_table.setHorizontalHeaderLabels(
            ["Name", "Price", "Category", "Date", "Delete"]
        )
        add_purchase_layout.addWidget(add_purchase_button)
        add_purchase_layout.addLayout(filters_layout)
        add_purchase_layout.addWidget(self.purchases_table)
        self.add_purchase_widget.setLayout(add_purchase_layout)
        self.add_purchase_widget.hide()

        self.post_purchase_widget = QWidget()
        post_purchase_layout = QVBoxLayout()
        self.name_purchase_edit = QLineEdit()
        self.name_purchase_edit.setPlaceholderText("Purchase name")
        self.price_purchase_edit = QLineEdit()
        self.price_purchase_edit.setPlaceholderText("Purchase price")
        category_purchase_label = QLabel("Category:")
        self.category_purchase_box = QComboBox()
        post_purchase_button = QPushButton("Submit")
        post_purchase_button.setStyleSheet("background: #F75E25;")
        post_purchase_button.clicked.connect(self.submit_post_purchase)
        post_purchase_layout.addWidget(self.name_purchase_edit)
        post_purchase_layout.addWidget(self.price_purchase_edit)
        post_purchase_layout.addWidget(self.price_purchase_edit)
        post_purchase_layout.addWidget(category_purchase_label)
        post_purchase_layout.addWidget(self.category_purchase_box)
        post_purchase_layout.addWidget(post_purchase_button)
        self.post_purchase_widget.setLayout(post_purchase_layout)
        self.post_purchase_widget.hide()

        self.add_category_widget = QWidget()
        add_category_layout = QVBoxLayout()
        add_category_button = QPushButton("Add category")
        add_category_button.setStyleSheet("background: #F75E25;")
        add_category_button.clicked.connect(self.post_category)
        self.categories_table = QTableWidget()
        self.categories_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.categories_table.setColumnCount(3)
        self.categories_table.setColumnWidth(0, 335)
        self.categories_table.setColumnWidth(1, 200)
        self.categories_table.setColumnWidth(2, 200)
        self.categories_table.setHorizontalHeaderLabels(["Name", "Edit", "Delete"])
        add_category_layout.addWidget(add_category_button)
        add_category_layout.addWidget(self.categories_table)
        self.add_category_widget.setLayout(add_category_layout)
        self.add_category_widget.hide()

        self.post_category_widget = QWidget()
        post_category_layout = QVBoxLayout()
        self.name_category_edit = QLineEdit()
        self.name_category_edit.setPlaceholderText("Category name")
        post_category_button = QPushButton("Submit")
        post_category_button.setStyleSheet("background: #F75E25;")
        post_category_button.clicked.connect(self.submit_post_category)
        post_category_layout.addWidget(self.name_category_edit)
        post_category_layout.addWidget(post_category_button)
        self.post_category_widget.setLayout(post_category_layout)
        self.post_category_widget.hide()

        self.put_category_widget = QWidget()
        put_category_layout = QVBoxLayout()
        self.name_put_category_name = QLineEdit()
        self.name_put_category_name.setReadOnly(True)
        self.name_put_category_edit = QLineEdit()
        self.name_put_category_edit.setPlaceholderText("New category name")
        put_category_button = QPushButton("Submit")
        put_category_button.setStyleSheet("background: #F75E25;")
        put_category_button.clicked.connect(self.submit_put_category)
        put_category_layout.addWidget(self.name_put_category_name)
        put_category_layout.addWidget(self.name_put_category_edit)
        put_category_layout.addWidget(put_category_button)
        self.put_category_widget.setLayout(put_category_layout)
        self.put_category_widget.hide()

        self.top_up_balance_widget = QWidget()
        top_up_balance_layout = QVBoxLayout()
        top_up_balance_button = QPushButton("Top up balance")
        top_up_balance_button.setStyleSheet("background: #F75E25;")
        top_up_balance_button.clicked.connect(self.top_up_balance)
        self.operations_table = QTableWidget()
        self.operations_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.operations_table.setColumnCount(3)
        self.operations_table.setColumnWidth(0, 326)
        self.operations_table.setColumnWidth(1, 200)
        self.operations_table.setColumnWidth(2, 200)
        self.operations_table.setHorizontalHeaderLabels(["Type", "Amount", "Date"])
        top_up_balance_layout.addWidget(top_up_balance_button)
        top_up_balance_layout.addWidget(self.operations_table)
        self.top_up_balance_widget.setLayout(top_up_balance_layout)
        self.top_up_balance_widget.hide()

        self.put_balance_widget = QWidget()
        put_balance_layout = QVBoxLayout()
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Amount")
        put_balance_button = QPushButton("Submit")
        put_balance_button.setStyleSheet("background: #F75E25;")
        put_balance_button.clicked.connect(self.submit_put_balance)
        put_balance_layout.addWidget(self.amount_edit)
        put_balance_layout.addWidget(put_balance_button)
        self.put_balance_widget.setLayout(put_balance_layout)
        self.put_balance_widget.hide()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.start_widget)
        main_layout.addWidget(self.add_purchase_widget)
        main_layout.addWidget(self.add_category_widget)
        main_layout.addWidget(self.post_category_widget)
        main_layout.addWidget(self.put_category_widget)
        main_layout.addWidget(self.top_up_balance_widget)
        main_layout.addWidget(self.put_balance_widget)
        main_layout.addWidget(self.post_purchase_widget)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        account_menu = menu_bar.addMenu("Account")
        change_action = QAction("Change account", self)
        change_action.triggered.connect(self.change.emit)
        account_menu.addAction(change_action)

        reference_menu = menu_bar.addMenu("Reference")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        reference_menu.addAction(about_action)

    def show_about_dialog(self):
        about_text = "App for control your money"
        QMessageBox.about(self, "About", about_text)

    def account_info(self):
        worker = AccountInfoWorker(self.client)
        worker.success.connect(self.success_account_info_handler)
        worker.error.connect(self.error_handler)
        worker.start()

    def success_account_info_handler(self, data: dict):
        result = f"ID - {data["id"]}\nLogin - {data["login"]}\nBalance - {data["balance"]}\n"
        if data["balance_replenishment_date"] is None:
            result += "You can top up your balance"
        else:
            now = date.today()
            replenishment_month, replenishment_day = map(
                int, data["balance_replenishment_date"].split("-")[1:]
            )
            if replenishment_month == now.month or replenishment_day < now.day:
                remaining_days = (
                    date(year=now.year, month=now.month + 1, day=replenishment_day) - now
                ).days
                result += f"You can top up your balance after {remaining_days} days"
            else:
                result += "You can top up your balance"
        QMessageBox.about(self, "Account info", result)

    def hide_all(self):
        self.calendar.hide()
        self.date_filter_edit.clear()
        self.add_category_widget.hide()
        self.post_category_widget.hide()
        self.put_category_widget.hide()
        self.top_up_balance_widget.hide()
        self.put_balance_widget.hide()
        self.post_purchase_widget.hide()
        self.add_purchase_widget.hide()

    def my_purchases(self, filters: dict | None = None):
        worker = GetCategoriesWorker(self.client)
        worker.success.connect(self.get_categories)
        worker.error.connect(self.error_handler)
        worker.start()
        self.hide_all()
        self.category_filter_box.clear()
        self.category_filter_box.addItem("Any")
        for category in self.categories:
            self.category_filter_box.addItem(category["name"])
        self.add_purchase_widget.show()
        worker = GetPurchasesWorker(self.client, filters=filters)
        worker.success.connect(self.success_get_purchases_handler)
        worker.error.connect(self.error_handler)
        worker.start()

    def success_get_purchases_handler(self, data: list):
        self.purchases_table.setRowCount(len(data))
        for row, purchase in enumerate(data):
            self.purchases_table.setItem(row, 0, QTableWidgetItem(purchase["name"]))
            self.purchases_table.setItem(row, 1, QTableWidgetItem(str(purchase["price"])))
            self.purchases_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    get_category_name_by_id(id=purchase["category_id"], data=self.categories)
                ),
            )
            self.purchases_table.setItem(
                row, 3, QTableWidgetItem(".".join(purchase["created_date"].split("-")[::-1]))
            )
            delete_button = QPushButton("Delete purchase")
            delete_button.clicked.connect(lambda ch, d=purchase: self.delete_purchase(data=d))
            delete_button.setStyleSheet("background: rgb(100, 0, 0)")
            self.purchases_table.setCellWidget(row, 4, delete_button)

    def show_calendar(self):
        self.calendar.show()

    def select_date(self, selected_date: QDate):
        selected_date = selected_date.toString("yyyy-MM-dd")
        self.date_filter_edit.setText(".".join(selected_date.split("-")[::-1]))

    def apply_filters(self):
        filters = {}
        category = self.category_filter_box.currentText()
        if category != "Any":
            filters["category_id"] = get_category_id_by_name(category, self.categories)
        selected_date = "-".join(self.date_filter_edit.text().split(".")[::-1])
        if selected_date:
            try:
                date.fromisoformat(selected_date)
                filters["created_date"] = selected_date
            except ValueError:
                self.error_handler("Invalid date")
                return
        self.calendar.hide()
        self.my_purchases(filters=filters if filters else None)

    def get_categories(self, data: list):
        self.categories = data

    def post_purchase(self):
        worker = GetCategoriesWorker(self.client)
        worker.success.connect(self.get_categories)
        worker.error.connect(self.error_handler)
        worker.start()

        if not self.categories:
            self.error_handler("First you should create category")
            return

        self.category_purchase_box.clear()
        for category in self.categories:
            self.category_purchase_box.addItem(category["name"])

        self.name_purchase_edit.clear()
        self.price_purchase_edit.clear()
        self.hide_all()
        self.post_purchase_widget.show()

    def submit_post_purchase(self):
        name = self.name_purchase_edit.text()
        price = self.price_purchase_edit.text()

        try:
            assert len(name) > 0
        except AssertionError:
            self.error_handler(f"Name must not be empty")
            return

        try:
            price = float(price)
            assert price > 0
        except ValueError:
            self.error_handler(f"Invalid price {price}")
            return
        except AssertionError:
            self.error_handler(f"Price must be greater than zero")
            return

        worker = PostPurchaseWorker(
            self.client,
            name,
            price,
            get_category_id_by_name(self.category_purchase_box.currentText(), self.categories),
        )
        worker.success.connect(lambda ch, filters=None: self.my_purchases(filters=filters))
        worker.error.connect(self.error_handler)
        worker.start()

    def delete_purchase(self, data: dict):
        worker = DeletePurchaseWorker(self.client, data["id"])
        worker.success.connect(self.my_purchases)
        worker.error.connect(self.error_handler)
        worker.start()

    def my_categories(self):
        self.hide_all()
        self.add_category_widget.show()
        worker = GetCategoriesWorker(self.client)
        worker.success.connect(self.success_get_categories_handler)
        worker.error.connect(self.error_handler)
        worker.start()

    def success_get_categories_handler(self, data: list):
        self.categories = data
        self.categories_table.setRowCount(len(data))
        for row, category in enumerate(data):
            self.categories_table.setItem(row, 0, QTableWidgetItem(category["name"]))
            edit_button = QPushButton("Edit name")
            edit_button.setStyleSheet("background: #F75E25")
            edit_button.clicked.connect(lambda ch, d=category: self.put_category(data=d))
            delete_button = QPushButton("Delete category")
            delete_button.clicked.connect(lambda ch, d=category: self.delete_category(data=d))
            delete_button.setStyleSheet("background: rgb(100, 0, 0)")
            self.categories_table.setCellWidget(row, 1, edit_button)
            self.categories_table.setCellWidget(row, 2, delete_button)

    def post_category(self):
        self.hide_all()
        self.name_category_edit.clear()
        self.post_category_widget.show()

    def submit_post_category(self):
        name = self.name_category_edit.text()

        try:
            assert len(name) > 0
        except AssertionError:
            self.error_handler(f"Name must not be empty")
            return

        worker = PostCategoryWorker(self.client, name)
        worker.success.connect(self.my_categories)
        worker.error.connect(self.error_handler)
        worker.start()

    def put_category(self, data: dict):
        self.hide_all()
        self.name_put_category_name.setText(data["name"])
        self.put_category_widget.show()
        self.name_put_category_edit.clear()

    def submit_put_category(self):
        name = self.name_put_category_name.text()
        id = get_category_id_by_name(name=name, data=self.categories)
        new_name = self.name_put_category_edit.text()

        try:
            assert len(new_name) > 0
        except AssertionError:
            self.error_handler(f"New name must not be empty")
            return

        worker = PutCategoryWorker(self.client, id, new_name)
        worker.success.connect(self.my_categories)
        worker.error.connect(self.error_handler)
        worker.start()

    def delete_category(self, data: dict):
        worker = DeleteCategoryWorker(self.client, data["id"])
        worker.success.connect(self.my_categories)
        worker.error.connect(self.error_handler)
        worker.start()

    def my_wallet(self):
        self.hide_all()
        self.top_up_balance_widget.show()
        worker = GetOperationsWorker(self.client)
        worker.success.connect(self.success_get_operations_handler)
        worker.error.connect(self.error_handler)
        worker.start()

    def success_get_operations_handler(self, data: list):
        self.operations_table.setRowCount(len(data))
        for row, operation in enumerate(data):
            operation_type = " ".join(operation["type"].split("_")).title()
            operation_amount = str(operation["amount"])
            operation_date = ".".join(operation["operation_date"].split("-")[::-1])
            self.operations_table.setItem(row, 0, QTableWidgetItem(operation_type))
            self.operations_table.setItem(row, 1, QTableWidgetItem(operation_amount))
            self.operations_table.setItem(row, 2, QTableWidgetItem(operation_date))

    def top_up_balance(self):
        self.hide_all()
        self.amount_edit.clear()
        self.put_balance_widget.show()

    def submit_put_balance(self):
        amount = self.amount_edit.text()
        worker = PutBalanceWorker(self.client, amount)
        worker.success.connect(self.my_wallet)
        worker.error.connect(self.error_handler)
        worker.start()

    def error_handler(self, detail: str):
        QMessageBox.warning(self, "Error", detail)
