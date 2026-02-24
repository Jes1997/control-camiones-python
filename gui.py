import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from repository import Repository


class ControlCamionesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Camiones")
        self.root.geometry("850x500")
        self.root.configure(bg="#f0f0f0")  # fondo neutro tipo app
        self.root.resizable(False, False)

        self.repo = Repository()
        self.create_styles()
        self.create_widgets()
        self.refresh_table()

    # ------------------------------
    # Estilos personalizados
    # ------------------------------
    def create_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        # Estilo general del Treeview
        style.configure(
            "Treeview",
            background="#fdfdfd",
            foreground="black",
            rowheight=25,
            fieldbackground="#fdfdfd",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            background="#4a7abc",
            foreground="white",
            font=("Segoe UI", 11, "bold"),
        )
        style.map("Treeview", background=[("selected", "#347083")])

        # -----------------------------
        # Estilo elegante centrado
        # -----------------------------
        style.configure("Centered.Treeview", font=("Segoe UI", 10), justify="center")

    # ------------------------------
    # Widgets principales
    # ------------------------------
    def create_widgets(self):
        # Tabla con scroll
        frame_table = tk.Frame(self.root, bg="#f0f0f0")
        frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("matricula", "empresa", "entrada", "salida", "estado")
        self.tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            height=15,
            style="Centered.Treeview",  # <- aplicamos el estilo centrado
        )

        for col in columns:
            self.tree.heading(
                col, text=col.capitalize(), anchor="center"
            )  # encabezado centrado
            if col == "matricula" or col == "empresa":
                self.tree.column(col, width=180, anchor="center")  # contenido centrado
            else:
                self.tree.column(col, width=130, anchor="center")  # contenido centrado

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones principales
        frame_buttons = tk.Frame(self.root, bg="#f0f0f0")
        frame_buttons.pack(pady=5)

        btn_entrada = tk.Button(
            frame_buttons,
            text="Registrar Entrada",
            width=18,
            command=self.registrar_entrada,
            bg="#4caf50",
            fg="white",
        )
        btn_salida = tk.Button(
            frame_buttons,
            text="Registrar Salida",
            width=18,
            command=self.registrar_salida,
            bg="#2196f3",
            fg="white",
        )
        btn_editar = tk.Button(
            frame_buttons,
            text="Editar Registro",
            width=18,
            command=self.editar_registro,
            bg="#ff9800",
            fg="white",
        )
        btn_actualizar = tk.Button(
            frame_buttons,
            text="Actualizar Lista",
            width=18,
            command=self.refresh_table,
            bg="#9c27b0",
            fg="white",
        )
        btn_salir = tk.Button(
            frame_buttons,
            text="Salir",
            width=18,
            command=self.root.quit,
            bg="#f44336",
            fg="white",
        )

        btn_entrada.grid(row=0, column=0, padx=5, pady=5)
        btn_salida.grid(row=0, column=1, padx=5, pady=5)
        btn_editar.grid(row=0, column=2, padx=5, pady=5)
        btn_actualizar.grid(row=0, column=3, padx=5, pady=5)
        btn_salir.grid(row=0, column=4, padx=5, pady=5)

    # ------------------------------
    # Actualizar tabla y colorear filas
    # ------------------------------
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        registros = self.repo.listar_camiones()
        for reg in registros:
            tag = "dentro" if reg["estado"] == "Dentro" else "Fuera"
            salida = reg["salida"] if reg["salida"] is not None else "❌"  # <-- X rojo
            self.tree.insert(
                "",
                tk.END,
                values=(
                    reg["matricula"],
                    reg["empresa"],
                    reg["entrada"],
                    salida,
                    reg["estado"],
                ),
                tags=(tag,),
            )

        # Colores por estado
        self.tree.tag_configure("dentro", background="#d0f0c0")  # verde claro
        self.tree.tag_configure("fuera", background="#f0d0d0")  # rojo claro

    # ------------------------------
    # Ventanas modales
    # ------------------------------
    def registrar_entrada(self):
        def guardar():
            matricula = entry_matricula.get().upper()
            empresa = entry_empresa.get()
            if not matricula:
                messagebox.showerror("Error", "La matrícula es obligatoria")
                return
            try:
                # 1️⃣ Guardar en la tabla de movimientos
                self.repo.registrar_entrada(matricula, empresa)
                # 2️⃣ Guardar/actualizar en la tabla de referencia
                self.repo.add_or_update_camion_ref(matricula, empresa)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            top.destroy()
            self.refresh_table()

        top = tk.Toplevel(self.root)
        top.title("Registrar Entrada")
        top.geometry("350x150")
        top.resizable(False, False)

        tk.Label(top, text="Matrícula:", font=("Segoe UI", 10)).grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        entry_matricula = tk.Entry(top, width=25, font=("Segoe UI", 10))
        entry_matricula.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top, text="Empresa:", font=("Segoe UI", 10)).grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        entry_empresa = tk.Entry(top, width=25, font=("Segoe UI", 10))
        entry_empresa.grid(row=1, column=1, padx=5, pady=5)

        def autocompletar_empresa(event):
            matricula = entry_matricula.get().upper()
            entry_matricula.delete(0, tk.END)
            entry_matricula.insert(0, matricula)  # fuerza mayúsculas

            empresa = self.repo.get_empresa_by_matricula(matricula)
            entry_empresa.delete(0, tk.END)
            if empresa:
                entry_empresa.insert(0, empresa)

        entry_matricula.bind("<KeyRelease>", autocompletar_empresa)

        tk.Button(
            top, text="Guardar", width=20, command=guardar, bg="#4caf50", fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def registrar_salida(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un registro primero")
            return

        values = self.tree.item(selected, "values")
        matricula = values[0]

        registros = self.repo.listar_camiones()
        registro = self.repo.get_registro_activo_por_matricula(matricula)
        if registro is None:
            messagebox.showerror(
                "Error", "No se puede registrar salida para este camión"
            )
            return

        registro_id = registro["id"]

        if registro_id is None:
            messagebox.showerror(
                "Error", "No se puede registrar salida para este camión"
            )
            return

        try:
            self.repo.registrar_salida(registro_id)
            messagebox.showinfo("Salida", "Salida registrada correctamente")
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_registro(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un registro primero")
            return

        values = self.tree.item(selected, "values")
        matricula, empresa, entrada, salida, estado = values

        registros = self.repo.listar_camiones()
        registro_id = None
        for r in registros:
            if r["matricula"] == matricula and r["entrada"] == entrada:
                registro_id = r["id"]
                break

        if registro_id is None:
            messagebox.showerror("Error", "No se puede editar este registro")
            return

        def guardar():
            nueva_matricula = entry_matricula.get()
            nueva_empresa = entry_empresa.get()
            try:
                self.repo.editar_registro(registro_id, nueva_matricula, nueva_empresa)
                self.repo.add_or_update_camion_ref(nueva_matricula, nueva_empresa)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            top.destroy()
            self.refresh_table()

        top = tk.Toplevel(self.root)
        top.title("Editar Registro")
        top.geometry("350x150")
        top.resizable(False, False)

        tk.Label(top, text="Matrícula:", font=("Segoe UI", 10)).grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        entry_matricula = tk.Entry(top, width=25, font=("Segoe UI", 10))
        entry_matricula.insert(0, matricula)
        entry_matricula.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top, text="Empresa:", font=("Segoe UI", 10)).grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        entry_empresa = tk.Entry(top, width=25, font=("Segoe UI", 10))
        entry_empresa.insert(0, empresa)
        entry_empresa.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            top, text="Guardar", width=20, command=guardar, bg="#ff9800", fg="white"
        ).grid(row=2, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlCamionesGUI(root)
    root.mainloop()
