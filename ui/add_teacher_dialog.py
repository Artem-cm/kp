from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class AddTeacherDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Добавить преподавателя")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля ввода
        self.name_input = QLineEdit()
        self.degree_input = QLineEdit()
        self.position_input = QLineEdit()
        self.experience_input = QLineEdit()

        # Метки и поля ввода
        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Ученая степень"))
        layout.addWidget(self.degree_input)
        layout.addWidget(QLabel("Должность"))
        layout.addWidget(self.position_input)
        layout.addWidget(QLabel("Стаж"))
        layout.addWidget(self.experience_input)

        # Кнопка "Сохранить"
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_teacher)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_teacher(self):
        # Сохранение данных преподавателя в базе
        name = self.name_input.text()
        degree = self.degree_input.text()
        position = self.position_input.text()
        experience = self.experience_input.text()

        self.db.cursor.execute('''
            INSERT INTO teachers (name, degree, position, experience) VALUES (?, ?, ?, ?)
        ''', (name, degree, position, int(experience)))
        self.db.conn.commit()
        self.accept()  # Закрываем окно
