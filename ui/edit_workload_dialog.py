from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox

class EditWorkloadDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Редактировать нагрузку")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выпадающий список с текущими записями нагрузки
        self.workload_combo = QComboBox()
        layout.addWidget(QLabel("Выберите нагрузку для редактирования"))
        layout.addWidget(self.workload_combo)

        # Поля для выбора преподавателя, дисциплины и типа занятия
        self.teacher_combo = QComboBox()
        layout.addWidget(QLabel("Изменить преподавателя"))
        layout.addWidget(self.teacher_combo)

        self.subject_combo = QComboBox()
        layout.addWidget(QLabel("Изменить дисциплину"))
        layout.addWidget(self.subject_combo)

        self.group_combo = QComboBox()
        layout.addWidget(QLabel("Изменить учебную группу"))
        layout.addWidget(self.group_combo)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["лекция", "практика"])
        layout.addWidget(QLabel("Изменить тип занятия"))
        layout.addWidget(self.type_combo)

        # Кнопка для сохранения изменений
        save_button = QPushButton("Сохранить изменения")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        # Загрузка нагрузки для выбора
        self.db.cursor.execute('''
            SELECT workload.id, teachers.name || " - " || subjects.name || " - " || groups.name || " - " || workload.type
            FROM workload
            JOIN teachers ON workload.teacher_id = teachers.id
            JOIN subjects ON workload.subject_id = subjects.id
            JOIN groups ON workload.group_id = groups.id
        ''')
        workload_records = self.db.cursor.fetchall()
        for record in workload_records:
            self.workload_combo.addItem(record[1], record[0])

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

        # Загрузка учебных групп
        self.db.cursor.execute("SELECT id, name FROM groups")
        groups = self.db.cursor.fetchall()
        for group in groups:
            self.group_combo.addItem(group[1], group[0])

    def save_changes(self):
        workload_id = self.workload_combo.currentData()
        teacher_id = self.teacher_combo.currentData()
        subject_id = self.subject_combo.currentData()
        group_id = self.group_combo.currentData()
        workload_type = self.type_combo.currentText()

        # Обновление нагрузки
        self.db.cursor.execute('''
            UPDATE workload
            SET teacher_id = ?, subject_id = ?, group_id = ?, type = ?
            WHERE id = ?
        ''', (teacher_id, subject_id, group_id, workload_type, workload_id))
        self.db.conn.commit()
        QMessageBox.information(self, "Успешно", "Нагрузка успешно обновлена!")
        self.accept()
