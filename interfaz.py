import tkinter as tk
from tkinter import ttk, messagebox
from sistema import SistemaTutorias
from datos import dias, horas

class Interfaz:
    def __init__(self, root):
        self.sistema = SistemaTutorias()
        self.root = root
        self.root.title("Sistema de Tutorías")
        self.root.geometry("1100x650")
        self.root.configure(bg="#ecf0f1")
        self.login()

    def limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------- LOGIN BONITO ----------
    def login(self):
        self.limpiar()

        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Sistema de Tutorías", font=("Segoe UI", 20, "bold"), bg="white", fg="#2c3e50").pack(pady=10)

        tk.Label(frame, text="Usuario", bg="white").pack(anchor="w")
        self.user = ttk.Entry(frame, width=30)
        self.user.pack(pady=5)

        tk.Label(frame, text="Contraseña", bg="white").pack(anchor="w")
        self.pwd = ttk.Entry(frame, show="*", width=30)
        self.pwd.pack(pady=5)

        ttk.Button(frame, text="Ingresar", command=self.validar_login).pack(pady=10)
        ttk.Button(frame, text="Crear cuenta", command=self.registro).pack()

    def validar_login(self):
        u = self.sistema.login(self.user.get(), self.pwd.get())
        if not u:
            messagebox.showerror("Error", "Datos incorrectos")
            return
        self.usuario = u
        self.dashboard()


    # ---------- REGISTRO CLARO ----------
    def registro(self):
        self.limpiar()
        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Registro de Usuario", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=10)

        self.nombre = self.crear_campo(frame, "Nombre completo")
        self.newuser = self.crear_campo(frame, "Usuario")
        self.newpwd = self.crear_campo(frame, "Contraseña", oculto=True)

        tk.Label(frame, text="Rol", bg="white").pack(anchor="w")
        self.rol = ttk.Combobox(frame, values=["profesor","estudiante"], state="readonly")
        self.rol.pack(pady=5)

        self.materias = self.crear_campo(frame, "Materias (solo profesor, separadas por coma)")

        ttk.Button(frame, text="Registrar", command=self.guardar_usuario).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.login).pack()

    def crear_campo(self, parent, texto, oculto=False):
        tk.Label(parent, text=texto, bg="white").pack(anchor="w")
        e = ttk.Entry(parent, width=35, show="*" if oculto else "")
        e.pack(pady=5)
        return e

    def guardar_usuario(self):
        if self.rol.get() == "profesor":
            materias = [m.strip() for m in self.materias.get().split(",")]
            self.sistema.registrar_profesor(self.nombre.get(), self.newuser.get(), self.newpwd.get(), materias)
        else:
            self.sistema.registrar_estudiante(self.nombre.get(), self.newuser.get(), self.newpwd.get())
        messagebox.showinfo("OK","Usuario creado")
        self.login()

    
    # ---------- DASHBOARD CON SIDEBAR ----------
    def dashboard(self):
        self.limpiar()

        sidebar = tk.Frame(self.root, bg="#2c3e50", width=220)
        sidebar.pack(side="left", fill="y")

        content = tk.Frame(self.root, bg="#ecf0f1")
        content.pack(side="right", expand=True, fill="both")

        def boton(texto, comando):
            tk.Button(sidebar, text=texto, fg="white", bg="#34495e", relief="flat",
                      font=("Segoe UI", 11), padx=10, pady=10,
                      command=lambda: comando(content)).pack(fill="x", pady=2)

        if self.usuario.rol == "profesor":
            boton("Crear Disponibilidad", self.vista_crear)
            boton("Mis Tutorías", self.vista_profesor)
        else:
            boton("Ver Disponibles", self.vista_tutorias)
            boton("Mis Reservas", self.vista_estudiante)

        boton("Cerrar Sesión", lambda c: self.login())


    # ---------- PROFESOR CREA ----------
    def vista_crear(self, parent):
        self.clear(parent)

        materia = self.label_entry(parent, "Materia")

        dia = ttk.Combobox(parent, values=dias, state="readonly")
        dia.pack(pady=5)

        hora = ttk.Combobox(parent, values=horas, state="readonly")
        hora.pack(pady=5)

        def guardar():
            self.sistema.crear_tutoria(materia.get(), self.usuario, dia.get(), hora.get())
            messagebox.showinfo("OK","Tutoría creada")

        ttk.Button(parent, text="Guardar", command=guardar).pack(pady=10)


    # ---------- VER LO QUE EL PROFESOR CREÓ ----------
    def vista_profesor(self, parent):
        self.clear(parent)

        tabla = self.crear_tabla(parent)

        for t in self.usuario.disponibilidad:
            estado = "Reservada" if t.ocupado else "Disponible"
            tabla.insert("","end",values=(t.materia,t.dia,t.hora,t.salon,estado))


    # ---------- ESTUDIANTE VE DISPONIBLES ----------
    def vista_tutorias(self, parent):
        self.clear(parent)
        tabla = self.crear_tabla(parent)

        for t in self.sistema.tutorias:
            if not t.ocupado:
                tabla.insert("","end",values=(t.materia,t.dia,t.hora,t.salon,"Disponible"))

        def reservar():
            item = tabla.selection()
            if not item: return
            t = self.sistema.tutorias[tabla.index(item)]
            self.sistema.reservar(self.usuario, t)
            messagebox.showinfo("OK","Reservada")

        ttk.Button(parent, text="Reservar", command=reservar).pack(pady=10)


    # ---------- VER LO QUE EL ESTUDIANTE RESERVÓ ----------
    def vista_estudiante(self, parent):
        self.clear(parent)
        tabla = self.crear_tabla(parent)

        for t in self.usuario.tutorias:
            tabla.insert("","end",values=(t.materia,t.dia,t.hora,t.salon,"Reservada"))


    # ---------- HELPERS UI ----------
    def clear(self, parent):
        for w in parent.winfo_children(): w.destroy()

    def label_entry(self, parent, text):
        tk.Label(parent, text=text, bg="#ecf0f1", font=("Segoe UI",11)).pack()
        e = ttk.Entry(parent, width=30)
        e.pack(pady=5)
        return e

    def crear_tabla(self, parent):
        cols = ("Materia","Dia","Hora","Salon","Estado")
        tabla = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols:
            tabla.heading(c, text=c)
            tabla.column(c, anchor="center")
        tabla.pack(expand=True, fill="both", pady=20)
        return tabla