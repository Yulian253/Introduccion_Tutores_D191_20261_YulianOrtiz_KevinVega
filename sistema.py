from modelos import Profesor, Estudiante, Tutoria
from datos import salones
from storage import cargar_datos, guardar_datos

class SistemaTutorias:
    def __init__(self):
        self.usuarios = {}
        self.tutorias = []
        self.indice_salon = 0
        self.cargar()

    def cargar(self):
        data = cargar_datos()
        for u in data["usuarios"]:
            if u["rol"] == "profesor":
                self.usuarios[u["username"]] = Profesor(u["nombre"], u["username"], u["password"], u["materias"])
            else:
                self.usuarios[u["username"]] = Estudiante(u["nombre"], u["username"], u["password"])

    def guardar(self):
        usuarios = []
        for u in self.usuarios.values():
            data = u.__dict__.copy()
            if u.rol == "estudiante":
                data.pop("tutorias", None)
            if u.rol == "profesor":
                data.pop("disponibilidad", None)
            usuarios.append(data)
        guardar_datos({"usuarios": usuarios})

    def registrar_profesor(self, nombre, user, pwd, materias):
        self.usuarios[user] = Profesor(nombre, user, pwd, materias)
        self.guardar()

    def registrar_estudiante(self, nombre, user, pwd):
        self.usuarios[user] = Estudiante(nombre, user, pwd)
        self.guardar()

    def login(self, user, pwd):
        u = self.usuarios.get(user)
        if u and u.password == pwd:
            return u
        return None
    
    def asignar_salon(self):
        salon = salones[self.indice_salon % len(salones)]
        self.indice_salon += 1
        return salon

    def crear_tutoria(self, materia, profesor, dia, hora):
        for t in profesor.disponibilidad:
            if t.dia == dia and t.hora == hora:
                raise ValueError("Horario cruzado")
        tutoria = Tutoria(materia, profesor, dia, hora, self.asignar_salon())
        profesor.disponibilidad.append(tutoria)
        self.tutorias.append(tutoria)

    def reservar(self, estudiante, tutoria):
        for t in estudiante.tutorias:
            if t.dia == tutoria.dia and t.hora == tutoria.hora:
                raise ValueError("Horario ocupado")
        if tutoria.ocupado:
            raise ValueError("Ya reservada")
        tutoria.ocupado = True
        tutoria.estudiante = estudiante
        estudiante.tutorias.append(tutoria)