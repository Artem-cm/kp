from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class AddSubjectDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Добавить учебную дисциплину")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода
        self.name_input = QLineEdit()
        self.lectures_input = QLineEdit()
        self.practices_input = QLineEdit()

        layout.addWidget(QLabel("Название дисциплины"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Количество лекций"))
        layout.addWidget(self.lectures_input)
        layout.addWidget(QLabel("Количество практик"))
        layout.addWidget(self.practices_input)

        # Кнопка "Сохранить"
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_subject)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_subject(self):
        # Сохранение дисциплины в базе
        name = self.name_input.text()
        lectures = int(self.lectures_input.text())
        practices = int(self.practices_input.text())

        self.db.cursor.execute('''
            INSERT INTO subjects (name, lectures, practices) VALUES (?, ?, ?)
        ''', (name, lectures, practices))
        self.db.conn.commit()
        self.accept()  # Закрываем окно
