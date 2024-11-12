from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton

class EditSubjectDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Редактировать учебную дисциплину")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выпадающий список для выбора дисциплины
        self.subject_combo = QComboBox()
        layout.addWidget(QLabel("Выберите дисциплину"))
        layout.addWidget(self.subject_combo)

        # Поля редактирования
        self.name_input = QLineEdit()
        self.lectures_input = QLineEdit()
        self.practices_input = QLineEdit()

        layout.addWidget(QLabel("Название дисциплины"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Количество лекций"))
        layout.addWidget(self.lectures_input)
        layout.addWidget(QLabel("Количество практик"))
        layout.addWidget(self.practices_input)

        # Кнопка "Сохранить изменения"
        save_button = QPushButton("Сохранить изменения")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.load_subjects()

    def load_subjects(self):
        # Загрузка списка дисциплин в выпадающий список
        self.db.cursor.execute("SELECT id, name FROM subjects")
        subjects = self.db.cursor.fetchall()
        for subject in subjects:
            self.subject_combo.addItem(subject[1], subject[0])
        self.subject_combo.currentIndexChanged.connect(self.load_subject_data)

    def load_subject_data(self):
        # Загрузка данных выбранной дисциплины для редактирования
        subject_id = self.subject_combo.currentData()
        self.db.cursor.execute("SELECT name, lectures, practices FROM subjects WHERE id = ?", (subject_id,))
        subject = self.db.cursor.fetchone()
        if subject:
            self.name_input.setText(subject[0])
            self.lectures_input.setText(str(subject[1]))
            self.practices_input.setText(str(subject[2]))

    def save_changes(self):
        # Сохранение изменений
        subject_id = self.subject_combo.currentData()
        name = self.name_input.text()
        lectures = int(self.lectures_input.text())
        practices = int(self.practices_input.text())

        self.db.cursor.execute('''
            UPDATE subjects SET name = ?, lectures = ?, practices = ? WHERE id = ?
        ''', (name, lectures, practices, subject_id))
        self.db.conn.commit()
        self.accept()  # Закрываем окно
