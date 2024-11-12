import sqlite3

class Database:
    def __init__(self, db_name="department_workload.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA busy_timeout = 3000")
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.add_head_account()

    def create_tables(self):
        # Создание таблицы преподавателей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                degree TEXT,
                position TEXT,
                experience INTEGER,
                password TEXT
            )
        ''')

        # Создание таблицы дисциплин
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                lectures INTEGER,
                practices INTEGER
            )
        ''')

        # Создание таблицы учебных групп
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''')

        # Создание таблицы нагрузки
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS workload (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER,
                subject_id INTEGER,
                group_id INTEGER,
                type TEXT,
                day_of_week TEXT,
                FOREIGN KEY(teacher_id) REFERENCES teachers(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id),
                FOREIGN KEY(group_id) REFERENCES groups(id)
            )
        ''')

        # Проверка и добавление столбца day_of_week, если его нет
        self.cursor.execute("PRAGMA table_info(workload)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "day_of_week" not in columns:
            self.cursor.execute("ALTER TABLE workload ADD COLUMN day_of_week TEXT")
            self.conn.commit()

    def add_head_account(self):
        # Добавление учетной записи заведующего кафедрой
        self.cursor.execute("SELECT * FROM teachers WHERE name = ?", ("head",))
        if not self.cursor.fetchone():
            self.cursor.execute('''
                INSERT INTO teachers (name, degree, position, experience, password)
                VALUES (?, ?, ?, ?, ?)
            ''', ("head", "Доктор наук", "Заведующий кафедрой", 15, "admin123"))
            self.conn.commit()

    def close(self):
        self.conn.close()
