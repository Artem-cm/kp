class Teacher:
    def __init__(self, id, name, degree, position, experience):
        self.id = id
        self.name = name
        self.degree = degree
        self.position = position
        self.experience = experience

    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.name}', degree='{self.degree}', position='{self.position}', experience={self.experience})"
