import tkinter as tk
from tkinter import ttk, messagebox
from sistema import SistemaTutorias
from datos import dias, horas

# ── Paleta UTS ───────────────────────────────────────────────────────────────
COLOR_AMARILLO   = "#CAD225"
COLOR_AMARILLO_H = "#b8bb1e"
COLOR_BLANCO     = "#FFFFFF"
COLOR_FONDO      = "#F4F5F0"
COLOR_SIDEBAR_BG = "#FFFFFF"
COLOR_SIDEBAR_BD = "#D6D8C8"
COLOR_TEXTO      = "#2B2D1E"
COLOR_GRIS_MED   = "#7A7C6A"
COLOR_GRIS_SUAVE = "#E8E9E0"
COLOR_LINEA      = "#D0D2C0"
COLOR_ACENTO     = "#3A5A2A"
COLOR_ROJO       = "#C0392B"
COLOR_ROJO_H     = "#a93226"

FUENTE_TITULO  = ("Georgia", 20, "bold")
FUENTE_SUBTIT  = ("Georgia", 14, "bold")
FUENTE_LABEL   = ("Palatino Linotype", 10)
FUENTE_BOTON   = ("Palatino Linotype", 10, "bold")
FUENTE_TABLA   = ("Palatino Linotype", 10)
FUENTE_SIDEBAR = ("Georgia", 10, "bold")
FUENTE_STAT_N  = ("Georgia", 22, "bold")
FUENTE_STAT_L  = ("Palatino Linotype", 9)

LOGO_URL = "https://www.uts.edu.co/sitio/wp-content/uploads/2019/10/Logo-UTS-1.png"


def _estilo_ttk():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TEntry",
        fieldbackground=COLOR_BLANCO, foreground=COLOR_TEXTO,
        bordercolor=COLOR_LINEA, lightcolor=COLOR_LINEA,
        darkcolor=COLOR_LINEA, relief="flat", padding=6, font=FUENTE_LABEL)

    style.configure("Accent.TButton",
        background=COLOR_AMARILLO, foreground=COLOR_TEXTO,
        font=FUENTE_BOTON, relief="flat", padding=(14, 8))
    style.map("Accent.TButton",
        background=[("active", COLOR_AMARILLO_H), ("pressed", COLOR_AMARILLO_H)])

    style.configure("Secondary.TButton",
        background=COLOR_GRIS_SUAVE, foreground=COLOR_TEXTO,
        font=FUENTE_BOTON, relief="flat", padding=(14, 8))
    style.map("Secondary.TButton",
        background=[("active", COLOR_LINEA)])

    style.configure("Danger.TButton",
        background=COLOR_ROJO, foreground=COLOR_BLANCO,
        font=FUENTE_BOTON, relief="flat", padding=(14, 8))
    style.map("Danger.TButton",
        background=[("active", COLOR_ROJO_H), ("pressed", COLOR_ROJO_H)])

    style.configure("TCombobox",
        fieldbackground=COLOR_BLANCO, foreground=COLOR_TEXTO,
        selectbackground=COLOR_AMARILLO, selectforeground=COLOR_TEXTO,
        font=FUENTE_LABEL)

    style.configure("Treeview",
        background=COLOR_BLANCO, foreground=COLOR_TEXTO,
        rowheight=32, fieldbackground=COLOR_BLANCO,
        font=FUENTE_TABLA, bordercolor=COLOR_LINEA)
    style.configure("Treeview.Heading",
        background=COLOR_GRIS_SUAVE, foreground=COLOR_ACENTO,
        font=("Georgia", 10, "bold"), relief="flat", padding=8)
    style.map("Treeview",
        background=[("selected", COLOR_AMARILLO)],
        foreground=[("selected", COLOR_TEXTO)])


def _sep(parent, color=COLOR_LINEA, pady=8):
    tk.Frame(parent, height=1, bg=color).pack(fill="x", pady=pady)


class Interfaz:
    def __init__(self, root):
        self.sistema = SistemaTutorias()
        self.root = root
        self.root.title("Sistema de Tutorías — UTS")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(True, True)
        _estilo_ttk()

        self._logo_img = None
        self._logo_sidebar_img = None
        try:
            import urllib.request
            from PIL import Image, ImageTk
            import io
            req = urllib.request.Request(LOGO_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                raw = r.read()
            img = Image.open(io.BytesIO(raw)).convert("RGBA")
            w0, h0 = img.size
            for h_new, attr in [(80, "_logo_img"), (46, "_logo_sidebar_img")]:
                setattr(self, attr, ImageTk.PhotoImage(
                    img.resize((int(w0 * h_new / h0), h_new), Image.LANCZOS)))
        except Exception:
            pass

        self.login()

    # ── Utilidades ───────────────────────────────────────────────────────────
    def limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def clear(self, parent):
        for w in parent.winfo_children():
            w.destroy()

    def _logo_widget(self, parent, tipo="login"):
        img = self._logo_img if tipo == "login" else self._logo_sidebar_img
        bg = parent["bg"]
        if img:
            tk.Label(parent, image=img, bg=bg).pack(pady=(0, 6))
        else:
            tk.Label(parent, text="UTS", font=("Georgia", 22, "bold"),
                     bg=bg, fg=COLOR_AMARILLO).pack(pady=(0, 2))
            tk.Label(parent, text="Unidades Tecnológicas de Santander",
                     font=("Palatino Linotype", 8), bg=bg,
                     fg=COLOR_GRIS_MED).pack(pady=(0, 6))

    def _campo(self, parent, texto, oculto=False, bg=COLOR_BLANCO):
        tk.Label(parent, text=texto, font=FUENTE_LABEL,
                 bg=bg, fg=COLOR_TEXTO).pack(anchor="w")
        e = ttk.Entry(parent, width=34, show="*" if oculto else "")
        e.pack(pady=(2, 10), ipady=3)
        return e

    def crear_campo(self, parent, texto, oculto=False):
        return self._campo(parent, texto, oculto)

    def _tabla(self, parent, cols, anchos=None):
        frame = tk.Frame(parent, bg=COLOR_FONDO)
        frame.pack(expand=True, fill="both", padx=30, pady=8)
        sy = ttk.Scrollbar(frame, orient="vertical")
        sx = ttk.Scrollbar(frame, orient="horizontal")
        tabla = ttk.Treeview(frame, columns=cols, show="headings",
                             yscrollcommand=sy.set, xscrollcommand=sx.set)
        sy.config(command=tabla.yview)
        sx.config(command=tabla.xview)
        for c in cols:
            w = (anchos or {}).get(c, 130)
            tabla.heading(c, text=c)
            tabla.column(c, anchor="center", width=w, minwidth=60)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        tabla.pack(expand=True, fill="both")
        return tabla

    def crear_tabla(self, parent):
        cols = ("Materia", "Día", "Hora", "Salón", "Estado")
        return self._tabla(parent, cols)

    def _header_vista(self, parent, titulo, subtitulo=""):
        tk.Label(parent, text=titulo, font=("Georgia", 15, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor="w", padx=30, pady=(26, 2))
        if subtitulo:
            tk.Label(parent, text=subtitulo, font=("Palatino Linotype", 10),
                     bg=COLOR_FONDO, fg=COLOR_GRIS_MED).pack(anchor="w", padx=30, pady=(0, 4))
        _sep(parent, COLOR_LINEA, pady=6)

    def _mensaje_error(self, parent, texto):
        f = tk.Frame(parent, bg="#fdecea", highlightbackground="#e57373",
                     highlightthickness=1)
        f.pack(fill="x", padx=30, pady=(0, 8))
        tk.Label(f, text=f"⚠  {texto}", font=FUENTE_LABEL,
                 bg="#fdecea", fg=COLOR_ROJO, wraplength=700,
                 justify="left").pack(padx=12, pady=8, anchor="w")
        parent.after(4000, f.destroy)

    # ── Login ─────────────────────────────────────────────────────────────────
    def login(self):
        self.limpiar()
        tk.Frame(self.root, bg=COLOR_AMARILLO, height=6).pack(fill="x", side="top")
        tk.Frame(self.root, bg=COLOR_AMARILLO, height=6).pack(fill="x", side="bottom")

        outer = tk.Frame(self.root, bg=COLOR_FONDO)
        outer.pack(expand=True, fill="both")

        card = tk.Frame(outer, bg=COLOR_BLANCO,
                        highlightbackground=COLOR_LINEA, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        inner = tk.Frame(card, bg=COLOR_BLANCO, padx=54, pady=46)
        inner.pack()

        self._logo_widget(inner, tipo="login")
        _sep(inner, COLOR_AMARILLO, pady=6)

        tk.Label(inner, text="Sistema de Tutorías", font=FUENTE_TITULO,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(pady=(4, 2))
        tk.Label(inner, text="Ingrese sus credenciales para continuar",
                 font=("Palatino Linotype", 9), bg=COLOR_BLANCO,
                 fg=COLOR_GRIS_MED).pack(pady=(0, 22))

        tk.Label(inner, text="Usuario", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
        self.user = ttk.Entry(inner, width=34)
        self.user.pack(pady=(2, 10), ipady=3)
        self.user.focus()

        tk.Label(inner, text="Contraseña", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
        self.pwd = ttk.Entry(inner, show="*", width=34)
        self.pwd.pack(pady=(2, 20), ipady=3)
        self.pwd.bind("<Return>", lambda e: self.validar_login())

        ttk.Button(inner, text="Ingresar", style="Accent.TButton",
                   command=self.validar_login).pack(fill="x", pady=(0, 8))
        ttk.Button(inner, text="Crear cuenta", style="Secondary.TButton",
                   command=self.registro).pack(fill="x")

    def validar_login(self):
        u = self.sistema.login(self.user.get().strip(), self.pwd.get())
        if not u:
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")
            return
        self.usuario = u
        self.dashboard()

    # ── Registro ──────────────────────────────────────────────────────────────
    def registro(self):
        self.limpiar()
        tk.Frame(self.root, bg=COLOR_AMARILLO, height=6).pack(fill="x", side="top")
        tk.Frame(self.root, bg=COLOR_AMARILLO, height=6).pack(fill="x", side="bottom")

        outer = tk.Frame(self.root, bg=COLOR_FONDO)
        outer.pack(expand=True, fill="both")

        card = tk.Frame(outer, bg=COLOR_BLANCO,
                        highlightbackground=COLOR_LINEA, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        inner = tk.Frame(card, bg=COLOR_BLANCO, padx=54, pady=40)
        inner.pack()

        self._logo_widget(inner, tipo="login")
        _sep(inner, COLOR_AMARILLO, pady=4)

        tk.Label(inner, text="Registro de Usuario", font=FUENTE_SUBTIT,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(pady=(4, 18))

        self.nombre  = self._campo(inner, "Nombre completo")
        self.newuser = self._campo(inner, "Nombre de usuario")
        self.newpwd  = self._campo(inner, "Contraseña", oculto=True)

        tk.Label(inner, text="Rol", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
        self.rol = ttk.Combobox(inner, values=["profesor", "estudiante"],
                                state="readonly", width=32)
        self.rol.pack(pady=(2, 10))

        # Frame materias — solo visible si rol = profesor
        self.frame_materias = tk.Frame(inner, bg=COLOR_BLANCO)
        tk.Label(self.frame_materias, text="Materias (separar con coma)",
                 font=FUENTE_LABEL, bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
        self.materias = ttk.Entry(self.frame_materias, width=34)
        self.materias.pack(pady=(2, 10), ipady=3)

        frame_botones = tk.Frame(inner, bg=COLOR_BLANCO)
        frame_botones.pack(fill="x")

        def on_rol_change(event):
            if self.rol.get() == "profesor":
                self.frame_materias.pack(fill="x", before=frame_botones)
            else:
                self.frame_materias.pack_forget()

        self.rol.bind("<<ComboboxSelected>>", on_rol_change)

        _sep(frame_botones, COLOR_LINEA, pady=10)
        ttk.Button(frame_botones, text="Registrar", style="Accent.TButton",
                   command=self.guardar_usuario).pack(fill="x", pady=(0, 8))
        ttk.Button(frame_botones, text="← Volver al inicio", style="Secondary.TButton",
                   command=self.login).pack(fill="x")

    def guardar_usuario(self):
        nombre = self.nombre.get().strip()
        user   = self.newuser.get().strip()
        pwd    = self.newpwd.get()
        rol    = self.rol.get()

        if not nombre or not user or not pwd or not rol:
            messagebox.showwarning("Campos incompletos",
                                   "Por favor complete todos los campos obligatorios.")
            return
        try:
            if rol == "profesor":
                materias = [m.strip() for m in self.materias.get().split(",") if m.strip()]
                if not materias:
                    messagebox.showwarning("Materias", "Ingrese al menos una materia.")
                    return
                self.sistema.registrar_profesor(nombre, user, pwd, materias)
            else:
                self.sistema.registrar_estudiante(nombre, user, pwd)
            messagebox.showinfo("Registro exitoso", "El usuario ha sido creado correctamente.")
            self.login()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ── Dashboard ─────────────────────────────────────────────────────────────
    def dashboard(self):
        self.limpiar()
        tk.Frame(self.root, bg=COLOR_AMARILLO, height=5).pack(fill="x", side="top")

        main = tk.Frame(self.root, bg=COLOR_FONDO)
        main.pack(expand=True, fill="both")

        sidebar = tk.Frame(main, bg=COLOR_SIDEBAR_BG, width=238,
                           highlightbackground=COLOR_SIDEBAR_BD, highlightthickness=1)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR_BG, pady=18)
        logo_frame.pack(fill="x", padx=16)
        self._logo_widget(logo_frame, tipo="sidebar")

        _sep(sidebar, COLOR_LINEA, pady=0)

        tk.Label(sidebar, text=self.usuario.nombre, font=("Georgia", 10, "bold"),
                 bg=COLOR_SIDEBAR_BG, fg=COLOR_TEXTO,
                 wraplength=200).pack(padx=16, pady=(14, 2))
        rol_txt = "Profesor" if self.usuario.rol == "profesor" else "Estudiante"
        tk.Label(sidebar, text=rol_txt, font=("Palatino Linotype", 9),
                 bg=COLOR_SIDEBAR_BG, fg=COLOR_GRIS_MED).pack(padx=16, pady=(0, 14))

        _sep(sidebar, COLOR_LINEA, pady=0)

        nav = tk.Frame(sidebar, bg=COLOR_SIDEBAR_BG)
        nav.pack(fill="x", pady=8)

        content = tk.Frame(main, bg=COLOR_FONDO)
        content.pack(side="right", expand=True, fill="both")

        def nav_btn(texto, icono, comando):
            f = tk.Frame(nav, bg=COLOR_SIDEBAR_BG, cursor="hand2")
            f.pack(fill="x", padx=10, pady=2)

            def on_enter(e):
                f.config(bg=COLOR_GRIS_SUAVE)
                for w in f.winfo_children(): w.config(bg=COLOR_GRIS_SUAVE)
            def on_leave(e):
                f.config(bg=COLOR_SIDEBAR_BG)
                for w in f.winfo_children(): w.config(bg=COLOR_SIDEBAR_BG)
            def on_click(e):
                for child in nav.winfo_children():
                    child.config(bg=COLOR_SIDEBAR_BG)
                    for w in child.winfo_children(): w.config(bg=COLOR_SIDEBAR_BG)
                f.config(bg=COLOR_AMARILLO)
                for w in f.winfo_children(): w.config(bg=COLOR_AMARILLO)
                comando(content)

            for ev, fn in [("<Enter>", on_enter), ("<Leave>", on_leave), ("<Button-1>", on_click)]:
                f.bind(ev, fn)

            li = tk.Label(f, text=icono, font=("Segoe UI Emoji", 13),
                          bg=COLOR_SIDEBAR_BG, fg=COLOR_TEXTO, width=3)
            li.pack(side="left", padx=(8, 4), pady=10)
            lt = tk.Label(f, text=texto, font=FUENTE_SIDEBAR,
                          bg=COLOR_SIDEBAR_BG, fg=COLOR_TEXTO, anchor="w")
            lt.pack(side="left", pady=10)

            for w in [li, lt]:
                for ev, fn in [("<Enter>", on_enter), ("<Leave>", on_leave), ("<Button-1>", on_click)]:
                    w.bind(ev, fn)

        if self.usuario.rol == "profesor":
            nav_btn("Inicio",               "🏠", self._bienvenida)
            nav_btn("Crear Disponibilidad", "📅", self.vista_crear)
            nav_btn("Mis Tutorías",         "📋", self.vista_profesor)
        else:
            nav_btn("Inicio",          "🏠", self._bienvenida)
            nav_btn("Ver Disponibles", "🔍", self.vista_tutorias)
            nav_btn("Mis Reservas",    "📌", self.vista_estudiante)

        _sep(sidebar, COLOR_LINEA, pady=0)

        bottom = tk.Frame(sidebar, bg=COLOR_SIDEBAR_BG)
        bottom.pack(side="bottom", fill="x", pady=16, padx=12)
        btn_logout = tk.Button(bottom, text="⏏  Cerrar Sesión",
                               font=FUENTE_BOTON, bg=COLOR_GRIS_SUAVE, fg=COLOR_TEXTO,
                               relief="flat", cursor="hand2", padx=10, pady=8,
                               command=self.login)
        btn_logout.pack(fill="x")
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg=COLOR_LINEA))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=COLOR_GRIS_SUAVE))

        self._bienvenida(content)

    # ── Bienvenida con estadísticas ───────────────────────────────────────────
    def _bienvenida(self, parent):
        self.clear(parent)

        tk.Label(parent, text=f"Bienvenido, {self.usuario.nombre}",
                 font=("Georgia", 16, "bold"), bg=COLOR_FONDO,
                 fg=COLOR_TEXTO).pack(anchor="w", padx=34, pady=(30, 4))
        tk.Label(parent, text="Resumen de tu actividad en el sistema.",
                 font=("Palatino Linotype", 10), bg=COLOR_FONDO,
                 fg=COLOR_GRIS_MED).pack(anchor="w", padx=34)
        _sep(parent, COLOR_LINEA, pady=10)

        stats_frame = tk.Frame(parent, bg=COLOR_FONDO)
        stats_frame.pack(anchor="w", padx=34, pady=8)

        def stat_card(numero, etiqueta, color_num=COLOR_ACENTO):
            card = tk.Frame(stats_frame, bg=COLOR_BLANCO,
                            highlightbackground=COLOR_LINEA, highlightthickness=1)
            card.pack(side="left", padx=(0, 14), pady=4, ipadx=24, ipady=16)
            tk.Label(card, text=str(numero), font=FUENTE_STAT_N,
                     bg=COLOR_BLANCO, fg=color_num).pack()
            tk.Label(card, text=etiqueta, font=FUENTE_STAT_L,
                     bg=COLOR_BLANCO, fg=COLOR_GRIS_MED).pack()

        if self.usuario.rol == "profesor":
            s = self.sistema.stats_profesor(self.usuario)
            stat_card(s["total"],      "Tutorías publicadas")
            stat_card(s["reservadas"], "Ya reservadas",    COLOR_AMARILLO_H)
            stat_card(s["libres"],     "Aún disponibles",  COLOR_ACENTO)
        else:
            s = self.sistema.stats_estudiante(self.usuario)
            stat_card(s["mis_reservas"], "Mis reservas activas")
            stat_card(s["disponibles"],  "Tutorías disponibles", COLOR_ACENTO)

        _sep(parent, COLOR_LINEA, pady=14)

        if self.usuario.rol == "profesor":
            tip = "💡  Puedes publicar hasta 10 tutorías. Las reservadas no se pueden eliminar."
        else:
            tip = "💡  Puedes cancelar una reserva desde 'Mis Reservas' si cambian tus planes."
        tk.Label(parent, text=tip, font=("Palatino Linotype", 9),
                 bg=COLOR_FONDO, fg=COLOR_GRIS_MED,
                 wraplength=700, justify="left").pack(anchor="w", padx=34)

    # ── Vista: crear disponibilidad ───────────────────────────────────────────
    def vista_crear(self, parent):
        self.clear(parent)
        self._header_vista(parent, "Registrar Disponibilidad",
                           "Complete los datos para publicar una nueva tutoría.")

        card = tk.Frame(parent, bg=COLOR_BLANCO,
                        highlightbackground=COLOR_LINEA, highlightthickness=1)
        card.pack(anchor="nw", padx=30, pady=6)
        inner = tk.Frame(card, bg=COLOR_BLANCO, padx=36, pady=30)
        inner.pack()

        def lbl(t):
            tk.Label(inner, text=t, font=FUENTE_LABEL,
                     bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w", pady=(10, 2))

        lbl("Materia")
        materia = ttk.Entry(inner, width=38)
        materia.pack(ipady=3)
        materia.focus()

        lbl("Día")
        dia = ttk.Combobox(inner, values=dias, state="readonly", width=36)
        dia.pack()

        lbl("Hora de inicio")
        hora = ttk.Combobox(inner, values=horas, state="readonly", width=36)
        hora.pack()

        _sep(inner, COLOR_LINEA, pady=14)

        def guardar():
            try:
                self.sistema.crear_tutoria(materia.get(), self.usuario, dia.get(), hora.get())
                materia.delete(0, "end")
                dia.set("")
                hora.set("")
                messagebox.showinfo("Tutoría registrada",
                                    "La disponibilidad ha sido publicada correctamente.")
            except ValueError as e:
                self._mensaje_error(parent, str(e))

        ttk.Button(inner, text="  ✔  Guardar disponibilidad",
                   style="Accent.TButton", command=guardar).pack(fill="x")

    # ── Vista: mis tutorías (profesor) ────────────────────────────────────────
    def vista_profesor(self, parent):
        self.clear(parent)
        self._header_vista(parent, "Mis Tutorías",
                           "Tutorías publicadas. Las reservadas muestran el estudiante asignado.")

        cols   = ("Materia", "Día", "Hora", "Salón", "Estado", "Estudiante")
        anchos = {"Materia": 170, "Día": 105, "Hora": 85, "Salón": 75,
                  "Estado": 105, "Estudiante": 170}
        tabla = self._tabla(parent, cols, anchos)

        def recargar():
            tabla.delete(*tabla.get_children())
            for t in self.usuario.disponibilidad:
                estado = "Reservada" if t.ocupado else "Disponible"
                est    = t.estudiante.nombre if t.estudiante else "—"
                tabla.insert("", "end", values=(t.materia, t.dia, t.hora,
                                                t.salon, estado, est))
        recargar()

        btn_frame = tk.Frame(parent, bg=COLOR_FONDO)
        btn_frame.pack(anchor="w", padx=30, pady=4)

        def eliminar():
            item = tabla.selection()
            if not item:
                messagebox.showwarning("Sin selección", "Seleccione una tutoría para eliminar.")
                return
            idx = tabla.index(item[0])
            t   = self.usuario.disponibilidad[idx]
            if t.ocupado:
                messagebox.showerror("No permitido",
                                     "No puedes eliminar una tutoría que ya fue reservada.")
                return
            confirmar = messagebox.askyesno("Confirmar eliminación",
                f"¿Eliminar la tutoría de '{t.materia}' el {t.dia} a las {t.hora}?")
            if confirmar:
                self.sistema.eliminar_tutoria(self.usuario, t)
                recargar()

        ttk.Button(btn_frame, text="  🗑  Eliminar seleccionada",
                   style="Danger.TButton", command=eliminar).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="↻  Actualizar",
                   style="Secondary.TButton", command=recargar).pack(side="left")

    # ── Vista: tutorías disponibles (estudiante) ──────────────────────────────
    def vista_tutorias(self, parent):
        self.clear(parent)
        self._header_vista(parent, "Tutorías Disponibles",
                           "Filtre y seleccione una tutoría para reservar.")

        filtro_frame = tk.Frame(parent, bg=COLOR_BLANCO,
                                highlightbackground=COLOR_LINEA, highlightthickness=1)
        filtro_frame.pack(fill="x", padx=30, pady=(0, 8))

        ff = tk.Frame(filtro_frame, bg=COLOR_BLANCO, padx=16, pady=12)
        ff.pack(fill="x")

        tk.Label(ff, text="Filtrar por:", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_GRIS_MED).pack(side="left", padx=(0, 12))
        tk.Label(ff, text="Materia", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(side="left")
        f_materia = ttk.Entry(ff, width=18)
        f_materia.pack(side="left", padx=(4, 16), ipady=2)

        tk.Label(ff, text="Día", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(side="left")
        f_dia = ttk.Combobox(ff, values=["Todos"] + dias, state="readonly", width=12)
        f_dia.set("Todos")
        f_dia.pack(side="left", padx=(4, 16))

        tk.Label(ff, text="Hora", font=FUENTE_LABEL,
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(side="left")
        f_hora = ttk.Combobox(ff, values=["Todas"] + horas, state="readonly", width=10)
        f_hora.set("Todas")
        f_hora.pack(side="left", padx=(4, 0))

        cols   = ("Materia", "Profesor", "Día", "Hora", "Salón")
        anchos = {"Materia": 160, "Profesor": 170, "Día": 105, "Hora": 85, "Salón": 75}
        tabla  = self._tabla(parent, cols, anchos)

        disponibles_filtradas = []

        def recargar():
            disponibles_filtradas.clear()
            tabla.delete(*tabla.get_children())
            mat  = f_materia.get().strip().lower()
            dia  = f_dia.get()
            hora = f_hora.get()
            for t in self.sistema.tutorias:
                if t.ocupado:
                    continue
                if mat and mat not in t.materia.lower():
                    continue
                if dia  != "Todos" and t.dia != dia:
                    continue
                if hora != "Todas" and t.hora != hora:
                    continue
                disponibles_filtradas.append(t)
                tabla.insert("", "end", values=(t.materia, t.profesor.nombre,
                                                t.dia, t.hora, t.salon))

        recargar()
        ttk.Button(ff, text="Buscar", style="Accent.TButton",
                   command=recargar).pack(side="left", padx=(16, 0))

        btn_frame = tk.Frame(parent, bg=COLOR_FONDO)
        btn_frame.pack(anchor="w", padx=30, pady=4)

        def reservar():
            item = tabla.selection()
            if not item:
                messagebox.showwarning("Sin selección", "Seleccione una tutoría para reservar.")
                return
            idx = tabla.index(item[0])
            t   = disponibles_filtradas[idx]
            confirmar = messagebox.askyesno("Confirmar reserva",
                f"¿Reservar '{t.materia}' con {t.profesor.nombre}\nel {t.dia} a las {t.hora}?")
            if confirmar:
                try:
                    self.sistema.reservar(self.usuario, t)
                    messagebox.showinfo("Reserva exitosa",
                                        "La tutoría ha sido reservada correctamente.")
                    recargar()
                except ValueError as e:
                    self._mensaje_error(parent, str(e))

        ttk.Button(btn_frame, text="  ✔  Reservar seleccionada",
                   style="Accent.TButton", command=reservar).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="↻  Actualizar",
                   style="Secondary.TButton", command=recargar).pack(side="left")

    # ── Vista: mis reservas (estudiante) ──────────────────────────────────────
    def vista_estudiante(self, parent):
        self.clear(parent)
        self._header_vista(parent, "Mis Reservas",
                           "Tutorías reservadas. Puede cancelar si cambian sus planes.")

        cols   = ("Materia", "Profesor", "Día", "Hora", "Salón")
        anchos = {"Materia": 160, "Profesor": 170, "Día": 105, "Hora": 85, "Salón": 75}
        tabla  = self._tabla(parent, cols, anchos)

        def recargar():
            tabla.delete(*tabla.get_children())
            for t in self.usuario.tutorias:
                tabla.insert("", "end", values=(t.materia, t.profesor.nombre,
                                                t.dia, t.hora, t.salon))
        recargar()

        btn_frame = tk.Frame(parent, bg=COLOR_FONDO)
        btn_frame.pack(anchor="w", padx=30, pady=4)

        def cancelar():
            item = tabla.selection()
            if not item:
                messagebox.showwarning("Sin selección", "Seleccione una reserva para cancelar.")
                return
            idx = tabla.index(item[0])
            t   = self.usuario.tutorias[idx]
            confirmar = messagebox.askyesno("Confirmar cancelación",
                f"¿Cancelar la reserva de '{t.materia}' el {t.dia} a las {t.hora}?\n"
                "La tutoría quedará disponible para otros estudiantes.")
            if confirmar:
                self.sistema.cancelar_reserva(self.usuario, t)
                messagebox.showinfo("Reserva cancelada",
                                    "Su reserva ha sido cancelada correctamente.")
                recargar()

        ttk.Button(btn_frame, text="  ✖  Cancelar reserva",
                   style="Danger.TButton", command=cancelar).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="↻  Actualizar",
                   style="Secondary.TButton", command=recargar).pack(side="left")

    # ── Helper legacy ─────────────────────────────────────────────────────────
    def label_entry(self, parent, text):
        tk.Label(parent, text=text, bg=COLOR_FONDO,
                 font=FUENTE_LABEL, fg=COLOR_TEXTO).pack(anchor="w", padx=28)
        e = ttk.Entry(parent, width=30)
        e.pack(pady=5, padx=28)
        return e