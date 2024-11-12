from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class EditTeacherProfileDialog(QDialog):
    def __init__(self, db, teacher_id):
        super().__init__()
        self.db = db
        self.teacher_id = teacher_id
        self.setWindowTitle("Редактировать профиль")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля для редактирования
        self.name_input = QLineEdit()
        self.degree_input = QLineEdit()
        self.position_input = QLineEdit()
        self.experience_input = QLineEdit()

        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Ученая степень"))
        layout.addWidget(self.degree_input)
        layout.addWidget(QLabel("Должность"))
        layout.addWidget(self.position_input)
        layout.addWidget(QLabel("Стаж"))
        layout.addWidget(self.experience_input)

        # Кнопка для сохранения изменений
        save_button = QPushButton("Сохранить изменения")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.load_profile_data()

    def load_profile_data(self):
        # Загрузка данных профиля преподавателя
        self.db.cursor.execute("SELECT name, degree, position, experience FROM teachers WHERE id = ?", (self.teacher_id,))
        profile_data = self.db.cursor.fetchone()
        if profile_data:
            self.name_input.setText(profile_data[0])
            self.degree_input.setText(profile_data[1])
            self.position_input.setText(profile_data[2])
            self.experience_input.setText(str(profile_data[3]))

    def save_changes(self):
        # Сохранение изменений в профиль
        name = self.name_input.text()
        degree = self.degree_input.text()
        position = self.position_input.text()
        experience = self.experience_input.text()

        self.db.cursor.execute('''
            UPDATE teachers SET name = ?, degree = ?, position = ?, experience = ?
            WHERE id = ?
        ''', (name, degree, position, int(experience), self.teacher_id))
        self.db.conn.commit()
        QMessageBox.information(self, "Успешно", "Профиль успешно обновлен!")
        self.accept()
