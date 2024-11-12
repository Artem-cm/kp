from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from ui.head_window import HeadWindow  # Окно для заведующего кафедрой
from ui.teacher_window import TeacherWindow  # Окно для преподавателя

class LoginWindow(QMainWindow):
    def __init__(self, auth_manager, db):
        super().__init__()
        self.auth_manager = auth_manager
        self.db = db  # Сохраняем объект базы данных для передачи в другие окна
        self.setWindowTitle("Окно авторизации")
        self.initUI()

    def initUI(self):
        # Создаем основной виджет и макет
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Поля ввода логина и пароля
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытого ввода для пароля
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Кнопка для входа в систему
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Устанавливаем основной макет
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def login(self):
        # Получаем введенные логин и пароль
        login = self.login_input.text()
        password = self.password_input.text()

        # Проверяем роль пользователя
        role = self.auth_manager.authenticate(login, password)

        if role == "Заведующий кафедрой":
            print("Вход для заведующего кафедрой")
            self.open_head_window()  # Открываем окно заведующего кафедрой
        elif role == "Преподаватель":
            print("Вход для преподавателя")
            self.open_teacher_window(login)  # Открываем окно преподавателя, передаем логин для получения ID
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неправильный логин или пароль")

    def open_head_window(self):
        # Открываем окно заведующего кафедрой
        self.head_window = HeadWindow(self.db)  # Создаем экземпляр окна и передаем базу данных
        self.head_window.show()
        self.close()  # Закрываем окно входа

    def open_teacher_window(self, login):
        # Получаем ID преподавателя по логину
        teacher_id = self.auth_manager.get_teacher_id(login)
        if teacher_id is not None:
            self.teacher_window = TeacherWindow(self.db, teacher_id)  # Создаем окно преподавателя и передаем ID
            self.teacher_window.show()
            self.close()  # Закрываем окно входа
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти ID преподавателя.")
