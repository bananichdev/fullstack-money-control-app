from httpx import Client
from utils.enums import AuthMethodType
from workers.base import BaseWorker


class AuthWorker(BaseWorker):
    def __init__(self, client: Client, auth_method: AuthMethodType, login: str, password: str):
        super().__init__()
        self.client = client
        self.auth_method = auth_method
        self.login = login
        self.password = password

    def run(self):
        response = self.client.post(
            url=self.auth_method,
            json={
                "login": self.login,
                "password": self.password,
            },
        )
        response_json = response.json()
        if response.status_code not in [200, 201]:
            self.error.emit(response_json["detail"])
        else:
            data = {
                "login": self.login,
                "authorization": response.cookies["authorization"],
            }
            self.success.emit(data)
