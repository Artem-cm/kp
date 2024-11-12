class WorkloadManager:
    def __init__(self, db):
        self.db = db

    def get_workload(self):
        """
        Получает данные о распределении нагрузки для всех преподавателей.
        Возвращает список словарей, где каждый словарь содержит информацию о преподавателе, дисциплине, группе и типе занятия.
        """
        self.db.cursor.execute('''
            SELECT teachers.name AS teacher, subjects.name AS subject, groups.name AS group, workload.type AS type
            FROM workload
            JOIN teachers ON workload.teacher_id = teachers.id
            JOIN subjects ON workload.subject_id = subjects.id
            JOIN groups ON workload.group_id = groups.id
        ''')
        results = self.db.cursor.fetchall()
        workload_data = [
            {"teacher": row[0], "subject": row[1], "group": row[2], "type": row[3]}
            for row in results
        ]
        return workload_data

    def get_teacher_schedule(self, teacher_id):
        """
        Получает расписание для конкретного преподавателя по его ID.
        Возвращает список словарей, где каждый словарь содержит информацию о дисциплине, группе и типе занятия.
        """
        self.db.cursor.execute('''
            SELECT subjects.name AS subject, groups.name AS group, workload.type AS type
            FROM workload
            JOIN subjects ON workload.subject_id = subjects.id
            JOIN groups ON workload.group_id = groups.id
            WHERE workload.teacher_id = ?
        ''', (teacher_id,))
        results = self.db.cursor.fetchall()
        schedule_data = [
            {"subject": row[0], "group": row[1], "type": row[2]}
            for row in results
        ]
        return schedule_data

    def add_teacher(self, name, degree, position, experience):
        """
        Добавляет нового преподавателя в базу данных.
        """
        self.db.cursor.execute('''
            INSERT INTO teachers (name, degree, position, experience) VALUES (?, ?, ?, ?)
        ''', (name, degree, position, experience))
        self.db.conn.commit()

    def add_subject(self, name, lectures, practices):
        """
        Добавляет новую дисциплину в базу данных.
        """
        self.db.cursor.execute('''
            INSERT INTO subjects (name, lectures, practices) VALUES (?, ?, ?)
        ''', (name, lectures, practices))
        self.db.conn.commit()

    def assign_workload(self, teacher_id, subject_id, group_id, type):
        """
        Назначает нагрузку преподавателю, добавляя запись в таблицу workload.
        """
        self.db.cursor.execute('''
            INSERT INTO workload (teacher_id, subject_id, group_id, type) VALUES (?, ?, ?, ?)
        ''', (teacher_id, subject_id, group_id, type))
        self.db.conn.commit()

    def edit_teacher(self, teacher_id, name=None, degree=None, position=None, experience=None):
        """
        Обновляет информацию о преподавателе по его ID.
        Принимает новые значения, если они не равны None.
        """
        update_fields = []
        update_values = []

        if name:
            update_fields.append("name = ?")
            update_values.append(name)
        if degree:
            update_fields.append("degree = ?")
            update_values.append(degree)
        if position:
            update_fields.append("position = ?")
            update_values.append(position)
        if experience is not None:
            update_fields.append("experience = ?")
            update_values.append(experience)

        update_values.append(teacher_id)
        update_query = f"UPDATE teachers SET {', '.join(update_fields)} WHERE id = ?"
        self.db.cursor.execute(update_query, update_values)
        self.db.conn.commit()

    def edit_subject(self, subject_id, name=None, lectures=None, practices=None):
        """
        Обновляет информацию о дисциплине по её ID.
        Принимает новые значения, если они не равны None.
        """
        update_fields = []
        update_values = []

        if name:
            update_fields.append("name = ?")
            update_values.append(name)
        if lectures is not None:
            update_fields.append("lectures = ?")
            update_values.append(lectures)
        if practices is not None:
            update_fields.append("practices = ?")
            update_values.append(practices)

        update_values.append(subject_id)
        update_query = f"UPDATE subjects SET {', '.join(update_fields)} WHERE id = ?"
        self.db.cursor.execute(update_query, update_values)
        self.db.conn.commit()

    def delete_teacher(self, teacher_id):
        """
        Удаляет преподавателя из базы данных.
        """
        self.db.cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
        self.db.cursor.execute("DELETE FROM workload WHERE teacher_id = ?", (teacher_id,))
        self.db.conn.commit()

    def delete_subject(self, subject_id):
        """
        Удаляет дисциплину из базы данных.
        """
        self.db.cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        self.db.cursor.execute("DELETE FROM workload WHERE subject_id = ?", (subject_id,))
        self.db.conn.commit()
