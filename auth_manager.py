class AuthManager:
    def __init__(self, db):
        self.db = db  # Объект базы данных

    def authenticate(self, login, password):
        """
        Проверяет логин и пароль пользователя в базе данных.
        Если учетные данные верны, возвращает роль пользователя ("Заведующий кафедрой" или "Преподаватель").
        Если данные неверны, возвращает None.
        """
        # Выполняем запрос к базе данных для проверки логина и пароля
        self.db.cursor.execute("SELECT position FROM teachers WHERE name = ? AND password = ?", (login, password))
        result = self.db.cursor.fetchone()

        # Если результат найден, возвращаем роль пользователя
        if result:
            return result[0]  # Возвращаем значение из столбца "position" ("Заведующий кафедрой" или "Преподаватель")
        return None  # Возвращаем None, если логин или пароль неверны

    def get_teacher_id(self, login):
        """
        Получает ID преподавателя по его логину (имени).
        Если логин существует, возвращает ID, иначе возвращает None.
        """
        self.db.cursor.execute("SELECT id FROM teachers WHERE name = ?", (login,))
        result = self.db.cursor.fetchone()
        if result:
            return result[0]
        return None
