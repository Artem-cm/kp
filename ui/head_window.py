from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
from ui.add_teacher_dialog import AddTeacherDialog
from ui.edit_teacher_dialog import EditTeacherDialog
from ui.add_subject_dialog import AddSubjectDialog
from ui.edit_subject_dialog import EditSubjectDialog
from ui.assign_workload_dialog import AssignWorkloadDialog
from ui.edit_workload_dialog import EditWorkloadDialog

class HeadWindow(QMainWindow):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window  # Ссылка на главное окно для возврата
        self.setWindowTitle("Окно заведующего кафедрой")
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Приветственное сообщение
        self.welcome_label = QLabel("Добро пожаловать, заведующий кафедрой!")
        layout.addWidget(self.welcome_label)

        # Кнопки для управления преподавателями, дисциплинами и нагрузкой
        self.add_teacher_button = QPushButton("Добавить преподавателя")
        self.edit_teacher_button = QPushButton("Редактировать преподавателей")
        self.add_subject_button = QPushButton("Добавить учебную дисциплину")
        self.edit_subject_button = QPushButton("Редактировать учебные дисциплины")
        self.view_workload_button = QPushButton("Посмотреть распределение нагрузки")
        self.assign_workload_button = QPushButton("Назначить нагрузку")
        self.edit_workload_button = QPushButton("Редактировать нагрузку")

        # Подключаем кнопки к методам
        self.add_teacher_button.clicked.connect(self.open_add_teacher_dialog)
        self.edit_teacher_button.clicked.connect(self.open_edit_teacher_dialog)
        self.add_subject_button.clicked.connect(self.open_add_subject_dialog)
        self.edit_subject_button.clicked.connect(self.open_edit_subject_dialog)
        self.view_workload_button.clicked.connect(self.view_workload)
        self.assign_workload_button.clicked.connect(self.open_assign_workload_dialog)
        self.edit_workload_button.clicked.connect(self.open_edit_workload_dialog)

        # Добавляем кнопки в макет
        layout.addWidget(self.add_teacher_button)
        layout.addWidget(self.edit_teacher_button)
        layout.addWidget(self.add_subject_button)
        layout.addWidget(self.edit_subject_button)
        layout.addWidget(self.view_workload_button)
        layout.addWidget(self.assign_workload_button)
        layout.addWidget(self.edit_workload_button)

        # Кнопка выхода
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        # Устанавливаем основной макет
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_add_teacher_dialog(self):
        dialog = AddTeacherDialog(self.db)
        dialog.exec_()

    def open_edit_teacher_dialog(self):
        dialog = EditTeacherDialog(self.db)
        dialog.exec_()

    def open_add_subject_dialog(self):
        dialog = AddSubjectDialog(self.db)
        dialog.exec_()

    def open_edit_subject_dialog(self):
        dialog = EditSubjectDialog(self.db)
        dialog.exec_()

    def view_workload(self):
        # Создаем новое окно с таблицей для отображения распределения нагрузки
        self.workload_window = QWidget()
        self.workload_window.setWindowTitle("Распределение нагрузки")

        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Дисциплина", "Группа", "Тип занятия", "День недели"])

        # Получаем данные о распределении нагрузки
        self.db.cursor.execute('''
            SELECT subjects.name, groups.name, workload.type, workload.day_of_week
            FROM workload
            JOIN subjects ON workload.subject_id = subjects.id
            JOIN groups ON workload.group_id = groups.id
        ''')
        workload_data = self.db.cursor.fetchall()

        # Заполняем таблицу данными
        table.setRowCount(len(workload_data))
        for row, data in enumerate(workload_data):
            for col, item in enumerate(data):
                table.setItem(row, col, QTableWidgetItem(str(item)))

        layout.addWidget(table)
        self.workload_window.setLayout(layout)
        self.workload_window.resize(600, 400)
        self.workload_window.show()

    def open_assign_workload_dialog(self):
        dialog = AssignWorkloadDialog(self.db)
        dialog.exec_()

    def open_edit_workload_dialog(self):
        dialog = EditWorkloadDialog(self.db)
        dialog.exec_()

    def logout(self):
        # Закрываем окно заведующего и возвращаем главное окно
        self.close()
        self.main_window.show()

