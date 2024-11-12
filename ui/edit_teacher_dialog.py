from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton

class EditTeacherDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Редактировать преподавателя")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выпадающий список для выбора преподавателя
        self.teacher_combo = QComboBox()
        layout.addWidget(QLabel("Выберите преподавателя"))
        layout.addWidget(self.teacher_combo)

        # Поля редактирования
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

        # Кнопка "Сохранить изменения"
        save_button = QPushButton("Сохранить изменения")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.load_teachers()

    def load_teachers(self):
        # Загрузка списка преподавателей в выпадающий список
        self.db.cursor.execute("SELECT id, name FROM teachers")
        teachers = self.db.cursor.fetchall()
        for teacher in teachers:
            self.teacher_combo.addItem(teacher[1], teacher[0])
        self.teacher_combo.currentIndexChanged.connect(self.load_teacher_data)

    def load_teacher_data(self):
        # Загрузка данных выбранного преподавателя для редактирования
        teacher_id = self.teacher_combo.currentData()
        self.db.cursor.execute("SELECT name, degree, position, experience FROM teachers WHERE id = ?", (teacher_id,))
        teacher = self.db.cursor.fetchone()
        if teacher:
            self.name_input.setText(teacher[0])
            self.degree_input.setText(teacher[1])
            self.position_input.setText(teacher[2])
            self.experience_input.setText(str(teacher[3]))

    def save_changes(self):
        # Сохранение изменений
        teacher_id = self.teacher_combo.currentData()
        name = self.name_input.text()
        degree = self.degree_input.text()
        position = self.position_input.text()
        experience = self.experience_input.text()

        self.db.cursor.execute('''
            UPDATE teachers SET name = ?, degree = ?, position = ?, experience = ? WHERE id = ?
        ''', (name, degree, position, int(experience), teacher_id))
        self.db.conn.commit()
        self.accept()  # Закрываем окно
