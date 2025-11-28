# ------------------- Imports -------------------
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime, date
from src.models.perro import Perro
from src.models.alimento import Alimento
from src.models.historial import HistorialComida

# ------------------- Funciones -------------------
def registrar_perro_ui(root):
    nombre = simpledialog.askstring("Registrar perro", "Nombre:", parent=root)
    if not nombre: return
    raza = simpledialog.askstring("Raza", "Raza:", parent=root)
    edad = simpledialog.askinteger("Edad", "Edad (años):", initialvalue=1, parent=root)
    peso = simpledialog.askfloat("Peso", "Peso (kg):", initialvalue=5.0, parent=root)
    propietario = simpledialog.askstring("Propietario", "Nombre del dueño:", parent=root)
    p = Perro.crear(nombre, raza or "", edad or 1, peso or 1.0, propietario or "")
    messagebox.showinfo("OK", f"Perro registrado: {p.nombre} (id={p.id})", parent=root)
    listar_perros()

def listar_perros():
    lb_perros.delete(0, tk.END)
    perros = Perro.listar_todos()
    if not perros:
        lb_perros.insert(tk.END, "No hay perros.")
        return
    for p in perros:
        lb_perros.insert(tk.END, f"[{p.id}] {p.nombre} — {p.raza} — {p.peso}kg — dueño: {p.propietario_nombre}")

def registrar_alimento_ui():
    tipo = simpledialog.askstring("Alimento", "Tipo (ej. Seco, Húmedo):", parent=root)
    if not tipo: return
    marca = simpledialog.askstring("Marca", "Marca:", parent=root)
    kcal = simpledialog.askfloat("Calorías por 100g", "kcal:", initialvalue=350, parent=root)
    a = Alimento.crear(tipo, marca or "", kcal or 350)
    messagebox.showinfo("OK", f"Alimento creado: {a.describir()} (id={a.id})", parent=root)
    listar_alimentos()

def listar_alimentos():
    lb_alimentos.delete(0, tk.END)
    alimentos = Alimento.listar_todos()
    if not alimentos:
        lb_alimentos.insert(tk.END, "No hay alimentos.")
        return
    for a in alimentos:
        lb_alimentos.insert(tk.END, f"[{a.id}] {a.tipo} — {a.marca} — {a.calorias_por_100g} kcal/100g")

def registrar_comida_ui():
    try:
        pid = simpledialog.askinteger("Perro ID", "ID del perro:", parent=root)
        if not pid: return
        aid = simpledialog.askinteger("Alimento ID", "ID del alimento:", parent=root)
        if not aid: return
        cantidad = simpledialog.askfloat("Cantidad (g)", "Cantidad en gramos:", initialvalue=100, parent=root)
        notas = simpledialog.askstring("Notas", "Notas opcionales:", parent=root)
        registro = HistorialComida.registrar(pid, aid, cantidad, notas)
        messagebox.showinfo("OK", f"Comida registrada en {registro.fecha}", parent=root)
        listar_rutina_diaria()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la comida.\n{e}", parent=root)

def listar_rutina_diaria():
    lb_rutina.delete(0, tk.END)
    historial = HistorialComida.listar_todos()
    hoy = date.today()
    registros_hoy = [h for h in historial if h.fecha.date() == hoy]
    if not registros_hoy:
        lb_rutina.insert(tk.END, "No hay comidas registradas hoy.")
        return
    for h in registros_hoy:
        perro = Perro.buscar_por_id(h.perro_id)
        alimento = Alimento.buscar_por_id(h.alimento_id)
        fecha_str = h.fecha.strftime("%H:%M")
        lb_rutina.insert(
            tk.END,
            f"{fecha_str} - {perro.nombre if perro else 'Desconocido'}: "
            f"{alimento.tipo if alimento else 'Desconocido'} {h.cantidad}g"
        )

# ------------------- Interfaz -------------------
root = tk.Tk()
root.title("Dog Feeder - App de Rutina Diaria")
root.geometry("1000x600")
root.config(bg="#ffc0cb")  # fondo rosa

# ------------------- Menú -------------------
menubar = tk.Menu(root)
acciones = tk.Menu(menubar, tearoff=0)
acciones.add_command(label="Registrar perro", command=lambda: registrar_perro_ui(root))
acciones.add_command(label="Registrar alimento", command=registrar_alimento_ui)
acciones.add_command(label="Registrar comida del día", command=registrar_comida_ui)
menubar.add_cascade(label="Acciones", menu=acciones)
root.config(menu=menubar)

# ------------------- Frame principal -------------------
frame = ttk.Frame(root, padding=15)
frame.pack(fill=tk.BOTH, expand=True)

# Estilo
style = ttk.Style()
style.configure("TLabel", background="#ffc0cb", foreground="black", font=("Segoe UI", 11, "bold"))
style.configure("TButton", background="#1a237e", foreground="black", font=("Segoe UI", 10, "bold"))
style.map("TButton", background=[("active", "#3949ab")])

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

# Ajustes de grid
frame.columnconfigure(0, weight=1)
frame.columnconfigure(2, weight=2)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

# ------------------- Inicializar listados -------------------
listar_perros()
listar_alimentos()
listar_rutina_diaria()

root.mainloop()
