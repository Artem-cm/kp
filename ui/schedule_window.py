from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel
from workload_manager import WorkloadManager

class ScheduleWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.workload_manager = WorkloadManager(self.db)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Общее расписание занятий")

        # Основной виджет и макет
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Расписание занятий")
        layout.addWidget(title)

        # Таблица для отображения расписания
        self.schedule_table = QTableWidget()
        layout.addWidget(self.schedule_table)

        # Заполнение таблицы расписанием
        self.load_schedule()

        # Установка макета
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def load_schedule(self):
        """
        Загружает полное расписание из базы данных и заполняет таблицу.
        """
        # Получение данных расписания
        schedule_data = self.workload_manager.get_workload()

        # Настройка таблицы
        self.schedule_table.setRowCount(len(schedule_data))
        self.schedule_table.setColumnCount(4)
        self.schedule_table.setHorizontalHeaderLabels(["Преподаватель", "Дисциплина", "Группа", "Тип занятия"])

        # Заполнение таблицы данными расписания
        for row, data in enumerate(schedule_data):
            self.schedule_table.setItem(row, 0, QTableWidgetItem(data['teacher']))
            self.schedule_table.setItem(row, 1, QTableWidgetItem(data['subject']))
            self.schedule_table.setItem(row, 2, QTableWidgetItem(data['group']))
            self.schedule_table.setItem(row, 3, QTableWidgetItem(data['type']))
