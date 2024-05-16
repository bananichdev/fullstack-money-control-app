from httpx import Client
from PyQt6.QtCore import pyqtSignal
from workers.base import BaseWorker


class AccountInfoWorker(BaseWorker):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client

    def run(self):
        response = self.client.get(url="/passport/account/")
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class GetCategoriesWorker(BaseWorker):
    success = pyqtSignal(list)

    def __init__(self, client: Client):
        super().__init__()
        self.client = client

    def run(self):
        response = self.client.get(url="/products/category/")
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class PostCategoryWorker(BaseWorker):
    def __init__(self, client: Client, name: str):
        super().__init__()
        self.client = client
        self.name = name

    def run(self):
        response = self.client.post(url="/products/category/", json={"name": self.name})
        response_json = response.json()
        if response.status_code != 201:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class PutCategoryWorker(BaseWorker):
    def __init__(self, client: Client, id: int, new_name: str):
        super().__init__()
        self.client = client
        self.id = id
        self.new_name = new_name

    def run(self):
        response = self.client.put(url=f"/products/category/{self.id}?new_name={self.new_name}")
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class DeleteCategoryWorker(BaseWorker):
    def __init__(self, client: Client, id: int):
        super().__init__()
        self.client = client
        self.id = id

    def run(self):
        response = self.client.delete(url=f"/products/category/{self.id}")
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class GetOperationsWorker(GetCategoriesWorker):
    def __init__(self, client: Client):
        super().__init__(client)

    def run(self):
        response = self.client.get(url="/passport/account/operation")
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class PutBalanceWorker(BaseWorker):
    def __init__(self, client: Client, amount: str):
        super().__init__()
        self.client = client
        self.amount = amount

    def run(self):
        try:
            self.amount = float(self.amount)
        except ValueError:
            self.error.emit(f'Invalid amount "{self.amount}"')
            return
        if self.amount <= 0:
            self.error.emit("Amount must be greater than zero.")
            return
        response = self.client.put(
            url="/passport/account/replenishment", json={"amount": self.amount}
        )
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class GetPurchasesWorker(GetCategoriesWorker):
    def __init__(self, client: Client, filters: dict | None):
        super().__init__(client)
        self.filters = filters

    def run(self):
        if not self.filters:
            response = self.client.get(url="/products/product/", params={"limit": 1000})
        else:
            response = self.client.get(
                url="/products/product/", params={"limit": 1000} | self.filters
            )
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class PostPurchaseWorker(BaseWorker):
    def __init__(self, client: Client, name: str, price: float, category_id: int):
        super().__init__()
        self.client = client
        self.name = name
        self.price = price
        self.category_id = category_id

    def run(self):
        response = self.client.post(
            url="/products/product/",
            json={
                "name": self.name,
                "price": self.price,
                "category_id": self.category_id,
            },
        )
        response_json = response.json()
        if response.status_code != 201:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)


class DeletePurchaseWorker(BaseWorker):
    def __init__(self, client: Client, id: int):
        super().__init__()
        self.client = client
        self.id = id

    def run(self):
        response = self.client.delete(url=f"/products/product/{self.id}")
        response_json = response.json()
        if response.status_code != 200:
            self.error.emit(response_json["detail"])
        else:
            self.success.emit(response_json)
