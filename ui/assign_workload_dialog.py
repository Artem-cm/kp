from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
import re

class AssignWorkloadDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Назначить нагрузку преподавателю")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выпадающий список преподавателей
        self.teacher_combo = QComboBox()
        layout.addWidget(QLabel("Выберите преподавателя"))
        layout.addWidget(self.teacher_combo)

        # Выпадающий список дисциплин
        self.subject_combo = QComboBox()
        layout.addWidget(QLabel("Выберите дисциплину"))
        layout.addWidget(self.subject_combo)

        # Поле для выбора учебной группы
        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Например, КИ22-06Б")
        layout.addWidget(QLabel("Введите учебную группу"))
        layout.addWidget(self.group_input)

        # Выпадающий список для выбора типа занятия
        self.type_combo = QComboBox()
        self.type_combo.addItems(["лекция", "практика"])
        layout.addWidget(QLabel("Тип занятия"))
        layout.addWidget(self.type_combo)

        # Выпадающий список для выбора дня недели
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
        layout.addWidget(QLabel("День недели"))
        layout.addWidget(self.day_combo)

        # Кнопка "Назначить нагрузку"
        assign_button = QPushButton("Назначить нагрузку")
        assign_button.clicked.connect(self.assign_workload)
        layout.addWidget(assign_button)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        # Загрузка преподавателей
        self.db.cursor.execute("SELECT id, name FROM teachers")
        teachers = self.db.cursor.fetchall()
        for teacher in teachers:
            self.teacher_combo.addItem(teacher[1], teacher[0])

        # Загрузка дисциплин
        self.db.cursor.execute("SELECT id, name FROM subjects")
        subjects = self.db.cursor.fetchall()
        for subject in subjects:
            self.subject_combo.addItem(subject[1], subject[0])

    def assign_workload(self):
        teacher_id = self.teacher_combo.currentData()
        subject_id = self.subject_combo.currentData()
        group_name = self.group_input.text()
        workload_type = self.type_combo.currentText()
        day_of_week = self.day_combo.currentText()

        if not re.match(r"^[А-Я]{2}\d{2}-\d{2}[А-Я]$", group_name):
            QMessageBox.warning(self, "Ошибка", "Учебная группа должна быть в формате КИ22-06Б")
            return

        # Проверка, существует ли группа
        self.db.cursor.execute("SELECT id FROM groups WHERE name = ?", (group_name,))
        group = self.db.cursor.fetchone()
        if group:
            group_id = group[0]
        else:
            self.db.cursor.execute("INSERT INTO groups (name) VALUES (?)", (group_name,))
            self.db.conn.commit()
            group_id = self.db.cursor.lastrowid

        # Назначение нагрузки
        self.db.cursor.execute('''
            INSERT INTO workload (teacher_id, subject_id, group_id, type, day_of_week) VALUES (?, ?, ?, ?, ?)
        ''', (teacher_id, subject_id, group_id, workload_type, day_of_week))
        self.db.conn.commit()
        QMessageBox.information(self, "Успешно", "Нагрузка успешно назначена!")
        self.accept()
