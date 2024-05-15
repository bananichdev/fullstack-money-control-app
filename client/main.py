import sys

from cache.account import CacheController
from PyQt6.QtWidgets import QApplication
from windows.auth import AuthWindow


def main():
    cache = CacheController()
    data = cache.read_cache()
    app = QApplication(sys.argv)
    window = AuthWindow()
    if data:
        window.redirect(data=data)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
