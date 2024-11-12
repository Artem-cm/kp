from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, auth_manager, db):
        super().__init__()
        self.auth_manager = auth_manager
        self.db = db
        self.user_role = None
        self.user_login = None
        self.setWindowTitle("Авторизация")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода для логина и пароля
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрытый ввод для пароля

        # Метки и кнопка для входа
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        # Кнопка входа
        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.authenticate_user)

        layout.addWidget(login_button)
        self.setLayout(layout)

    def authenticate_user(self):
        # Получаем введенные логин и пароль
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        # Проверка учетных данных
        role = self.auth_manager.authenticate(login, password)

        if role:
            self.user_role = role
            self.user_login = login
            self.accept()  # Закрываем диалог только если аутентификация успешна
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неправильный логин или пароль")
            print("Ошибка: Неправильный логин или пароль")
