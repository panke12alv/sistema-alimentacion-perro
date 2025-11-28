# src/app_gui.py
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from src.models.perro import Perro
from src.models.alimento import Alimento
from src.models.historial import HistorialComida

def registrar_perro_ui(root):
    nombre = simpledialog.askstring("Registrar perro", "Nombre:")
    if not nombre: return
    raza = simpledialog.askstring("Raza", "Raza:")
    edad = simpledialog.askinteger("Edad", "Edad (años):", initialvalue=1)
    peso = simpledialog.askfloat("Peso", "Peso (kg):", initialvalue=5.0)
    propietario = simpledialog.askstring("Propietario", "Nombre del dueño:")
    p = Perro.crear(nombre, raza or "", edad or 1, peso or 1.0, propietario or "")
    messagebox.showinfo("OK", f"Perro registrado: {p.nombre} (id={p.id})")
    listar_perros(lb_output)

def listar_perros(lb):
    perros = Perro.listar_todos()
    lb.delete(0, tk.END)
    if not perros:
        lb.insert(tk.END, "No hay perros.")
        return
    for p in perros:
        lb.insert(tk.END, f"[{p.id}] {p.nombre} — {p.raza} — {p.peso}kg — dueño: {p.propietario_nombre}")

def registrar_alimento_ui():
    tipo = simpledialog.askstring("Alimento", "Tipo (ej. Seco, Húmedo):")
    if not tipo: return
    marca = simpledialog.askstring("Marca", "Marca:")
    kcal = simpledialog.askfloat("Calorías por 100g", "kcal:", initialvalue=350)
    a = Alimento.crear(tipo, marca or "", kcal or 350)
    messagebox.showinfo("OK", f"Alimento creado: {a.describir()} (id={a.id})")
    listar_alimentos(lb_output2)

def listar_alimentos(lb):
    alimentos = Alimento.listar_todos()
    lb.delete(0, tk.END)
    if not alimentos: lb.insert(tk.END, "No hay alimentos.")
    for a in alimentos:
        lb.insert(tk.END, f"[{a.id}] {a.tipo} — {a.marca} — {a.calorias_por_100g} kcal/100g")

def registrar_comida_ui():
    pid = simpledialog.askinteger("Perro ID", "ID del perro:")
    if not pid: return
    aid = simpledialog.askinteger("Alimento ID", "ID del alimento:")
    if not aid: return
    cantidad = simpledialog.askfloat("Cantidad (g)", "Cantidad en gramos:", initialvalue=100)
    notas = simpledialog.askstring("Notas", "Notas opcionales:")
    registro = HistorialComida.registrar(pid, aid, cantidad, notas)
    messagebox.showinfo("OK", f"Comida registrada en {registro.fecha}")
    # actualizar listado de historial no implementado en mini gui

# Interfaz principal
root = tk.Tk()
root.title("Dog Feeder - Mini GUI")
root.geometry("900x500")

menubar = tk.Menu(root)
acciones = tk.Menu(menubar, tearoff=0)
acciones.add_command(label="Registrar perro", command=lambda: registrar_perro_ui(root))
acciones.add_command(label="Registrar alimento", command=registrar_alimento_ui)
acciones.add_command(label="Registrar comida", command=registrar_comida_ui)
menubar.add_cascade(label="Acciones", menu=acciones)
root.config(menu=menubar)

frame = ttk.Frame(root, padding=(10,10))
frame.pack(fill=tk.BOTH, expand=True)

lbl = ttk.Label(frame, text="Perros registrados:", font=("Segoe UI", 11))
lbl.pack(anchor="w")
lb_output = tk.Listbox(frame, height=10)
lb_output.pack(fill=tk.BOTH, expand=True)

lbl2 = ttk.Label(frame, text="Alimentos:", font=("Segoe UI", 11))
lbl2.pack(anchor="w", pady=(8,0))
lb_output2 = tk.Listbox(frame, height=6)
lb_output2.pack(fill=tk.BOTH, expand=True)

# botones para refrescar
btns = ttk.Frame(frame)
btns.pack(fill=tk.X, pady=(8,0))
ttk.Button(btns, text="Listar perros", command=lambda: listar_perros(lb_output)).pack(side=tk.LEFT, padx=6)
ttk.Button(btns, text="Listar alimentos", command=lambda: listar_alimentos(lb_output2)).pack(side=tk.LEFT, padx=6)

try:
    listar_perros(lb_output)
    listar_alimentos(lb_output2)
except Exception:
    lb_output.delete(0, tk.END)
    lb_output.insert(tk.END, "Error al listar: verifica conexión a BD.")

root.mainloop()
