from PyQt5.QtWidgets import QApplication
from database import Database
from auth_manager import AuthManager
from ui.main_window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    db = Database()
    auth_manager = AuthManager(db)
    main_window = MainWindow(auth_manager, db, app)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
