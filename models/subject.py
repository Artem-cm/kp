class Subject:
    def __init__(self, id, name, lectures, practices):
        self.id = id
        self.name = name
        self.lectures = lectures  # Количество лекционных часов
        self.practices = practices  # Количество практических часов

    def __repr__(self):
        return f"Subject(id={self.id}, name='{self.name}', lectures={self.lectures}, practices={self.practices})"
