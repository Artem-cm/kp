from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from ui.edit_teacher_profile_dialog import EditTeacherProfileDialog

class TeacherWindow(QMainWindow):
    def __init__(self, db, teacher_id):
        super().__init__()
        self.db = db
        self.teacher_id = teacher_id
        self.setWindowTitle("Окно преподавателя")
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        self.welcome_label = QLabel("Добро пожаловать, преподаватель!")
        layout.addWidget(self.welcome_label)

        self.edit_profile_button = QPushButton("Редактировать профиль")
        self.view_workload_button = QPushButton("Посмотреть распределение нагрузки")
        self.logout_button = QPushButton("Выйти")

        self.edit_profile_button.clicked.connect(self.open_edit_profile_dialog)
        self.view_workload_button.clicked.connect(self.view_workload)
        self.logout_button.clicked.connect(self.logout)

        layout.addWidget(self.edit_profile_button)
        layout.addWidget(self.view_workload_button)
        layout.addWidget(self.logout_button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_edit_profile_dialog(self):
        dialog = EditTeacherProfileDialog(self.db, self.teacher_id)
        dialog.exec_()

    def view_workload(self):
        # Инициализация счетчиков для лекций и практик
        lecture_hours = 0
        practice_hours = 0

        # Создаем таблицу для отображения распределения нагрузки
        self.workload_table = QTableWidget()
        self.workload_table.setWindowTitle("Распределение нагрузки")
        self.workload_table.setColumnCount(4)
        self.workload_table.setHorizontalHeaderLabels(["Дисциплина", "Группа", "Тип занятия", "День недели"])

        # Получаем данные о нагрузке преподавателя, включая день недели и тип занятия
        self.db.cursor.execute('''
            SELECT subjects.name, groups.name, workload.type, workload.day_of_week
            FROM workload
            JOIN subjects ON workload.subject_id = subjects.id
            JOIN groups ON workload.group_id = groups.id
            WHERE workload.teacher_id = ?
        ''', (self.teacher_id,))
        workload_data = self.db.cursor.fetchall()

        # Настраиваем количество строк и заполняем таблицу данными
        self.workload_table.setRowCount(len(workload_data))
        for row, data in enumerate(workload_data):
            for col, item in enumerate(data):
                self.workload_table.setItem(row, col, QTableWidgetItem(str(item)))

            # Подсчитываем часы в зависимости от типа занятия
            if data[2] == "лекция":
                lecture_hours += 2  # Каждая лекция добавляет 2 часа
            elif data[2] == "практика":
                practice_hours += 2  # Каждое практическое занятие добавляет 2 часа

        # Настройка и показ таблицы
        self.workload_table.resize(600, 400)

        # Создаем метку для отображения общей нагрузки
        total_hours_label = QLabel(f"Общая нагрузка: {lecture_hours} часов лекций и {practice_hours} часов практических занятий")
        total_hours_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Показываем метку с общей нагрузкой
        workload_layout = QVBoxLayout()
        workload_layout.addWidget(self.workload_table)
        workload_layout.addWidget(total_hours_label)

        # Устанавливаем новый виджет для отображения таблицы и общей нагрузки
        self.workload_widget = QWidget()  # Сохраняем ссылку на виджет как атрибут класса
        self.workload_widget.setLayout(workload_layout)
        self.workload_widget.setWindowTitle("Распределение нагрузки")
        self.workload_widget.resize(600, 500)
        self.workload_widget.show()  # Показываем виджет

    def logout(self):
        self.close()
        QMessageBox.information(self, "Выход", "Вы вышли из системы.")
