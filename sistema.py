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

        for u in data.get("usuarios", []):
            if u["rol"] == "profesor":
                self.usuarios[u["username"]] = Profesor(
                    u["nombre"], u["username"], u["password"], u["materias"])
            else:
                self.usuarios[u["username"]] = Estudiante(
                    u["nombre"], u["username"], u["password"])

        for t in data.get("tutorias", []):
            profesor = self.usuarios.get(t["profesor_username"])
            if not profesor:
                continue
            tutoria = Tutoria(t["materia"], profesor, t["dia"], t["hora"], t["salon"])
            tutoria.ocupado = t["ocupado"]
            if t.get("estudiante_username"):
                est = self.usuarios.get(t["estudiante_username"])
                if est:
                    tutoria.estudiante = est
                    est.tutorias.append(tutoria)
            profesor.disponibilidad.append(tutoria)
            self.tutorias.append(tutoria)
            self.indice_salon += 1

    def guardar(self):
        usuarios = []
        for u in self.usuarios.values():
            d = {
                "nombre": u.nombre,
                "username": u.username,
                "password": u.password,
                "rol": u.rol
            }
            if u.rol == "profesor":
                d["materias"] = u.materias
            usuarios.append(d)

        tutorias = []
        for t in self.tutorias:
            tutorias.append({
                "materia": t.materia,
                "profesor_username": t.profesor.username,
                "profesor_nombre": t.profesor.nombre,
                "dia": t.dia,
                "hora": t.hora,
                "salon": t.salon,
                "ocupado": t.ocupado,
                "estudiante_username": t.estudiante.username if t.estudiante else None
            })

        guardar_datos({"usuarios": usuarios, "tutorias": tutorias})

    def registrar_profesor(self, nombre, user, pwd, materias):
        if user in self.usuarios:
            raise ValueError("El nombre de usuario ya existe.")
        self.usuarios[user] = Profesor(nombre, user, pwd, materias)
        self.guardar()

    def registrar_estudiante(self, nombre, user, pwd):
        if user in self.usuarios:
            raise ValueError("El nombre de usuario ya existe.")
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
        if not materia.strip():
            raise ValueError("La materia no puede estar vacía.")
        if not dia or not hora:
            raise ValueError("Debe seleccionar día y hora.")
        activas = [t for t in profesor.disponibilidad]
        if len(activas) >= 10:
            raise ValueError("Has alcanzado el límite de 10 tutorías publicadas.")
        for t in profesor.disponibilidad:
            if t.dia == dia and t.hora == hora:
                raise ValueError(f"Ya tienes una tutoría el {dia} a las {hora}.")
        tutoria = Tutoria(materia.strip(), profesor, dia, hora, self.asignar_salon())
        profesor.disponibilidad.append(tutoria)
        self.tutorias.append(tutoria)
        self.guardar()

    def eliminar_tutoria(self, profesor, tutoria):
        if tutoria.ocupado:
            raise ValueError("No puedes eliminar una tutoría que ya fue reservada.")
        profesor.disponibilidad.remove(tutoria)
        self.tutorias.remove(tutoria)
        self.guardar()

    def reservar(self, estudiante, tutoria):
        if tutoria.ocupado:
            raise ValueError("Esta tutoría ya fue reservada por otro estudiante.")
        for t in estudiante.tutorias:
            if t.dia == tutoria.dia and t.hora == tutoria.hora:
                raise ValueError(f"Ya tienes una reserva el {tutoria.dia} a las {tutoria.hora}.")
        tutoria.ocupado = True
        tutoria.estudiante = estudiante
        estudiante.tutorias.append(tutoria)
        self.guardar()

    def cancelar_reserva(self, estudiante, tutoria):
        tutoria.ocupado = False
        tutoria.estudiante = None
        estudiante.tutorias.remove(tutoria)
        self.guardar()

    def stats_profesor(self, profesor):
        total      = len(profesor.disponibilidad)
        reservadas = sum(1 for t in profesor.disponibilidad if t.ocupado)
        return {"total": total, "reservadas": reservadas, "libres": total - reservadas}

    def stats_estudiante(self, estudiante):
        mis_reservas = len(estudiante.tutorias)
        disponibles  = sum(1 for t in self.tutorias if not t.ocupado)
        return {"mis_reservas": mis_reservas, "disponibles": disponibles}