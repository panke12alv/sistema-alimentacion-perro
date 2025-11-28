# ------------------- Imports -------------------
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime, date
from src.models.perro import Perro
from src.models.alimento import Alimento
from src.models.historial import HistorialComida
from src.models.rutina import RutinaAlimentacion

# ------------------- Funciones -------------------
# esta funcion me permite registrar un perro usando dialogos
def registrar_perro_ui(root):
    nombre = simpledialog.askstring("Registrar perro", "Nombre:", parent=root)  # pido nombre
    if not nombre: return
    raza = simpledialog.askstring("Raza", "Raza:", parent=root)  # pido raza
    edad = simpledialog.askinteger("Edad", "Edad (años):", initialvalue=1, parent=root)  # pido edad
    peso = simpledialog.askfloat("Peso", "Peso (kg):", initialvalue=5.0, parent=root)  # pido peso
    propietario = simpledialog.askstring("Propietario", "Nombre del dueño:", parent=root)  # pido nombre del dueño
    p = Perro.crear(nombre, raza or "", edad or 1, peso or 1.0, propietario or "")  # creo el perro
    messagebox.showinfo("OK", f"Perro registrado: {p.nombre} (id={p.id})", parent=root)  # muestro info
    listar_perros()  # actualizo la lista de perros

# aqui listamos todos los perros en el listbox
def listar_perros():
    lb_perros.delete(0, tk.END)  # limpio listbox
    perros = Perro.listar_todos()  # obtengo todos los perros
    if not perros:
        lb_perros.insert(tk.END, "No hay perros.")  # si no hay perros muestro mensaje
        return
    for p in perros:  # recorro perros
        lb_perros.insert(tk.END, f"[{p.id}] {p.nombre} — {p.raza} — {p.peso}kg — dueño: {p.propietario_nombre}")  # agrego info

# esta funcion me permite registrar un alimento
def registrar_alimento_ui():
    tipo = simpledialog.askstring("Alimento", "Tipo (ej. Seco, Húmedo):", parent=root)
    if not tipo: return
    marca = simpledialog.askstring("Marca", "Marca:", parent=root)
    kcal = float(simpledialog.askfloat("Calorias por 100g", "kcal:", initialvalue=350, parent=root) or 350)
    a = Alimento.crear(tipo, marca or "", kcal)  # creo alimento
    messagebox.showinfo("OK", f"Alimento creado: {a.describir()} (id={a.id})", parent=root)
    listar_alimentos()  # actualizo lista de alimentos

# aqui listamos todos los alimentos en el listbox
def listar_alimentos():
    lb_alimentos.delete(0, tk.END)  # limpio listbox
    alimentos = Alimento.listar_todos()
    if not alimentos:
        lb_alimentos.insert(tk.END, "No hay alimentos.")  # muestro mensaje si esta vacio
        return
    for a in alimentos:
        lb_alimentos.insert(tk.END, f"[{a.id}] {a.tipo} — {a.marca} — {a.calorias_por_100g} kcal/100g")  # agrego info

# ------------------- Registro de comida -------------------
def registrar_comida_ui():
    top = tk.Toplevel(root)  # creo ventana nueva
    top.title("Registrar comida del dia")
    top.geometry("400x300")
    top.config(bg="#ffc0cb")  # fondo rosa
    top.grab_set()  # bloqueo ventana principal mientras esta abierta

    # obtengo listas de perros y alimentos
    perros = Perro.listar_todos()
    alimentos = Alimento.listar_todos()

    # creo diccionarios para ComboBox
    perro_map = {f"{p.nombre} (dueño: {p.propietario_nombre})": p.id for p in perros}
    alimento_map = {f"{a.tipo} ({a.marca})": a.id for a in alimentos}

    # ------------------- Widgets -------------------
    ttk.Label(top, text="Selecciona el perro:", background="#ffc0cb", font=("Segoe UI", 11)).pack(pady=(10,0))
    combo_perro = ttk.Combobox(top, values=list(perro_map.keys()), state="readonly", font=("Segoe UI",10))
    combo_perro.pack(pady=5)

    ttk.Label(top, text="Selecciona el alimento:", background="#ffc0cb", font=("Segoe UI", 11)).pack(pady=(10,0))
    combo_alimento = ttk.Combobox(top, values=list(alimento_map.keys()), state="readonly", font=("Segoe UI",10))
    combo_alimento.pack(pady=5)

    ttk.Label(top, text="Cantidad (g):", background="#ffc0cb", font=("Segoe UI", 11)).pack(pady=(10,0))
    entry_cantidad = tk.Entry(top, font=("Segoe UI",10))
    entry_cantidad.pack(pady=5)

    ttk.Label(top, text="Notas (opcional):", background="#ffc0cb", font=("Segoe UI", 11)).pack(pady=(10,0))
    entry_notas = tk.Entry(top, font=("Segoe UI",10))
    entry_notas.pack(pady=5)

    # funcion que se ejecuta al presionar registrar comida
    def registrar():
        try:
            perro_sel = combo_perro.get()
            alimento_sel = combo_alimento.get()
            if not perro_sel or not alimento_sel:
                messagebox.showwarning("Atencion", "Selecciona perro y alimento", parent=top)
                return
            cantidad = float(entry_cantidad.get())
            notas = entry_notas.get() or None
            pid = perro_map[perro_sel]
            aid = alimento_map[alimento_sel]

            # guardo registro en historial
            registro = HistorialComida.registrar(pid, aid, cantidad, notas)

            # ------------------ NUEVO: actualizo o creo rutina ------------------
            # por simplicidad guardamos rutina diaria con un solo alimento en lista
            RutinaAlimentacion.crear_o_actualizar(
                perro_id=pid,
                alimentos_ids=[aid],
                horarios="08:00,13:00,18:00",
                cantidad_total_por_dia=cantidad
            )

            messagebox.showinfo("OK", f"Comida registrada en {registro.fecha}", parent=top)
            listar_rutina_diaria()  # actualizo rutina
            top.destroy()  # cierro ventana
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la comida.\n{e}", parent=top)

    ttk.Button(top, text="Registrar comida", command=registrar).pack(pady=5)

# ------------------- Listado de rutina diaria -------------------
def listar_rutina_diaria():
    lb_rutina.delete(0, tk.END)  # limpio listbox
    historial = HistorialComida.listar_todos()  # obtengo historial
    hoy = date.today()
    registros_hoy = [h for h in historial if h.fecha.date() == hoy]  # filtro por hoy
    if not registros_hoy:
        lb_rutina.insert(tk.END, "No hay comidas registradas hoy.")
        return
    for h in registros_hoy:
        perro = Perro.buscar_por_id(h.perro_id)
        alimento = Alimento.buscar_por_id(h.alimento_id)
        fecha_str = h.fecha.strftime("%H:%M")
        notas = f" ({h.notas})" if h.notas else ""  # agrego notas si existen
        lb_rutina.insert(
            tk.END,
            f"{fecha_str} - {perro.nombre if perro else 'Desconocido'}: "
            f"{alimento.tipo if alimento else 'Desconocido'} {h.cantidad}g{notas}"
        )


# ------------------- Interfaz -------------------
root = tk.Tk()
root.title("Dog Feeder - App de Rutina Diaria")
root.geometry("1000x600")
root.config(bg="#ffc0cb")  # fondo rosa

# ------------------- Menu -------------------
menubar = tk.Menu(root)
acciones = tk.Menu(menubar, tearoff=0)
acciones.add_command(label="Registrar perro", command=lambda: registrar_perro_ui(root))
acciones.add_command(label="Registrar alimento", command=registrar_alimento_ui)
acciones.add_command(label="Registrar comida del dia", command=registrar_comida_ui)
menubar.add_cascade(label="Acciones", menu=acciones)
root.config(menu=menubar)

# ------------------- Cuadro principal -------------------
frame = ttk.Frame(root, padding=15)
frame.pack(fill=tk.BOTH, expand=True)

# Estilo general
style = ttk.Style()
style.configure("TLabel", background="#ffc0cb", foreground="black", font=("Segoe UI", 11, "bold"))  # labels negro
style.configure("TButton", background="#1a237e", foreground="black", font=("Segoe UI", 10, "bold"))  # botones azul con letras negras
style.map("TButton", background=[("active", "#3949ab")])  # cambio de color al presionar

# ------------------- Secciones -------------------
# Perros
lbl_perros = ttk.Label(frame, text="Perros registrados:")
lbl_perros.grid(row=0, column=0, sticky="w")
lb_perros = tk.Listbox(frame, height=10, bg="white", fg="black", font=("Segoe UI", 10))
lb_perros.grid(row=1, column=0, sticky="nsew", padx=(0,10))
scroll_perros = tk.Scrollbar(frame, command=lb_perros.yview)
scroll_perros.grid(row=1, column=1, sticky="ns")
lb_perros.config(yscrollcommand=scroll_perros.set)

# Alimentos
lbl_alimentos = ttk.Label(frame, text="Alimentos:")
lbl_alimentos.grid(row=2, column=0, sticky="w", pady=(10,0))
lb_alimentos = tk.Listbox(frame, height=6, bg="white", fg="black", font=("Segoe UI", 10))
lb_alimentos.grid(row=3, column=0, sticky="nsew", padx=(0,10))
scroll_alimentos = tk.Scrollbar(frame, command=lb_alimentos.yview)
scroll_alimentos.grid(row=3, column=1, sticky="ns")
lb_alimentos.config(yscrollcommand=scroll_alimentos.set)

# Rutina diaria
lbl_rutina = ttk.Label(frame, text="Rutina diaria de comidas:")
lbl_rutina.grid(row=0, column=2, sticky="w")
lb_rutina = tk.Listbox(frame, height=25, width=50, bg="white", fg="black", font=("Segoe UI", 10))
lb_rutina.grid(row=1, column=2, rowspan=3, sticky="nsew")
scroll_rutina = tk.Scrollbar(frame, command=lb_rutina.yview)
scroll_rutina.grid(row=1, column=3, rowspan=3, sticky="ns")
lb_rutina.config(yscrollcommand=scroll_rutina.set)

# Ajustes de grid para expandir bien
frame.columnconfigure(0, weight=1)
frame.columnconfigure(2, weight=2)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

# ------------------- Inicializo listados -------------------
listar_perros()
listar_alimentos()
listar_rutina_diaria()

root.mainloop()


