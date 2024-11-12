from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog
from ui.login_dialog import LoginDialog
from ui.head_window import HeadWindow
from ui.teacher_window import TeacherWindow

class MainWindow(QMainWindow):
    def __init__(self, auth_manager, db, app):
        super().__init__()
        self.auth_manager = auth_manager
        self.db = db
        self.app = app
        self.head_window = None
        self.teacher_window = None
        self.setWindowTitle("Расписание")

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        days_layout = QVBoxLayout()
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

        self.schedule_labels = {}

        for day in days:
            day_label = QLabel(day)
            day_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            days_layout.addWidget(day_label)

            schedule_label = QLabel()
            days_layout.addWidget(schedule_label)
            self.schedule_labels[day] = schedule_label

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.open_login_dialog)

        main_layout.addLayout(days_layout)
        main_layout.addWidget(self.login_button)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.update_schedule()

    def update_schedule(self):
        for day in self.schedule_labels:
            self.schedule_labels[day].setText("")

        self.db.cursor.execute('''
            SELECT teachers.name, workload.type, groups.name, workload.day_of_week
            FROM workload
            JOIN teachers ON workload.teacher_id = teachers.id
            JOIN groups ON workload.group_id = groups.id
        ''')
        workload_data = self.db.cursor.fetchall()

        for teacher_name, workload_type, group_name, day_of_week in workload_data:
            schedule_text = f"{teacher_name}, {workload_type}, группа {group_name}"
            current_text = self.schedule_labels[day_of_week].text()
            updated_text = current_text + schedule_text + "\n"
            self.schedule_labels[day_of_week].setText(updated_text)

    def open_login_dialog(self):
        login_dialog = LoginDialog(self.auth_manager, self.db)
        if login_dialog.exec_() == QDialog.Accepted:
            # Определяем, какое окно открыть
            if login_dialog.user_role == "Заведующий кафедрой":
                self.open_head_window()
            elif login_dialog.user_role == "Преподаватель":
                self.open_teacher_window(login_dialog.user_login)

    def open_head_window(self):
        # Открываем окно заведующего кафедрой
        self.hide()  # Скрываем главное окно
        self.head_window = HeadWindow(self.db, self)
        self.head_window.show()

    def open_teacher_window(self, login):
        # Открываем окно преподавателя
        teacher_id = self.auth_manager.get_teacher_id(login)
        if teacher_id is not None:
            self.hide()  # Скрываем главное окно
            self.teacher_window = TeacherWindow(self.db, teacher_id)
            self.teacher_window.show()
