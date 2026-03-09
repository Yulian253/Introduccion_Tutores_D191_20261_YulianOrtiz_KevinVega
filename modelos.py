class Usuario:
    def __init__(self, nombre, username, password, rol):
        self.nombre = nombre
        self.username = username
        self.password = password
        self.rol = rol

class Profesor(Usuario):
    def __init__(self, nombre, username, password, materias):
        if len(materias) > 2:
            raise ValueError("Máximo 2 materias")
        super().__init__(nombre, username, password, "profesor")
        self.materias = materias
        self.disponibilidad = []

class Estudiante(Usuario):
    def __init__(self, nombre, username, password):
        super().__init__(nombre, username, password, "estudiante")
        self.tutorias = []

class Tutoria:
    def __init__(self, materia, profesor, dia, hora, salon):
        self.materia = materia
        self.profesor = profesor
        self.dia = dia
        self.hora = hora
        self.salon = salon
        self.ocupado = False
        self.estudiante = None