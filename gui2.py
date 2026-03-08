import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.geometry('1000x680')
root.title("AgroControl - Campos Fértiles S.A.")
root.configure(bg="#f0f4f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#2d5a27", tabmargins=[2, 5, 2, 0])
style.configure("TNotebook.Tab", background="#4a7c43", foreground="white",
                padding=[12, 6], font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", background=[("selected", "#f0f4f0")],
          foreground=[("selected", "#2d5a27")])
style.configure("TFrame", background="#f0f4f0")

header = tk.Frame(root, bg="#2d5a27", height=60)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="🌿 AGROCONTROL — Campos Fértiles S.A.",
         font=("Segoe UI", 16, "bold"), bg="#2d5a27", fg="white").pack(side="left", padx=20, pady=12)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab_fincas     = ttk.Frame(notebook)
tab_cultivos   = ttk.Frame(notebook)
tab_insumos    = ttk.Frame(notebook)
tab_maquinaria = ttk.Frame(notebook)
tab_empleados  = ttk.Frame(notebook)
tab_cosechas   = ttk.Frame(notebook)
tab_clientes   = ttk.Frame(notebook)

notebook.add(tab_fincas,     text="  Fincas  ")
notebook.add(tab_cultivos,   text="  Cultivos  ")
notebook.add(tab_insumos,    text="  Insumos  ")
notebook.add(tab_maquinaria, text="  Maquinaria  ")
notebook.add(tab_empleados,  text="  Empleados  ")
notebook.add(tab_cosechas,   text="  Cosechas  ")
notebook.add(tab_clientes,   text="  Clientes  ")

LABEL_FONT  = ("Segoe UI", 11)
ENTRY_FONT  = ("Segoe UI", 11)
TITLE_FONT  = ("Segoe UI", 15, "bold")
BTN_FONT    = ("Segoe UI", 11, "bold")
BG          = "#f0f4f0"

def make_buttons(parent, save_cmd, update_cmd, delete_cmd, clear_cmd):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(pady=18)
    tk.Button(frame, text="Guardar",    font=BTN_FONT, bg="#4CAF50", fg="white",
              width=11, relief="flat", cursor="hand2", command=save_cmd).pack(side="left", padx=6)
    tk.Button(frame, text="Actualizar", font=BTN_FONT, bg="#2196F3", fg="white",
              width=11, relief="flat", cursor="hand2", command=update_cmd).pack(side="left", padx=6)
    tk.Button(frame, text="Eliminar",   font=BTN_FONT, bg="#f44336", fg="white",
              width=11, relief="flat", cursor="hand2", command=delete_cmd).pack(side="left", padx=6)
    tk.Button(frame, text="Limpiar",    font=BTN_FONT, bg="#FF9800", fg="white",
              width=11, relief="flat", cursor="hand2", command=clear_cmd).pack(side="left", padx=6)

def make_label_entry(parent, row, text, width=28):
    tk.Label(parent, text=text, font=LABEL_FONT, bg=BG, anchor="w"
             ).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=8)
    e = tk.Entry(parent, width=width, font=ENTRY_FONT, relief="solid", bd=1)
    e.grid(row=row, column=1, sticky="w", pady=8)
    return e

def make_label_combo(parent, row, text, values, width=26):
    tk.Label(parent, text=text, font=LABEL_FONT, bg=BG, anchor="w"
             ).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=8)
    c = ttk.Combobox(parent, values=values, width=width, font=ENTRY_FONT, state="readonly")
    c.grid(row=row, column=1, sticky="w", pady=8)
    return c

def build_form(tab, title, fields, color="#2d5a27"):
    canvas = tk.Canvas(tab, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scroll_frame, text=title, font=TITLE_FONT, fg=color, bg=BG
             ).pack(pady=(18, 5))
    tk.Frame(scroll_frame, bg=color, height=2).pack(fill="x", padx=40, pady=(0, 12))

    form = tk.Frame(scroll_frame, bg=BG)
    form.pack(pady=5, anchor="w", padx=60)

    entries = {}
    for i, field in enumerate(fields):
        if isinstance(field, tuple) and len(field) == 3:
            name, ftype, opts = field
        else:
            name, ftype, opts = field[0], field[1], []

        if ftype == "entry":
            entries[name] = make_label_entry(form, i, name + ":", 28)
        elif ftype == "combo":
            entries[name] = make_label_combo(form, i, name + ":", opts, 26)
        elif ftype == "text":
            tk.Label(form, text=name + ":", font=LABEL_FONT, bg=BG
                     ).grid(row=i, column=0, sticky="nw", padx=(0, 12), pady=8)
            t = tk.Text(form, width=28, height=4, font=ENTRY_FONT, relief="solid", bd=1)
            t.grid(row=i, column=1, sticky="w", pady=8)
            entries[name] = t

    return scroll_frame, entries

def clear_entries(entries):
    for widget in entries.values():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)
        elif isinstance(widget, ttk.Combobox):
            widget.set("")

def generic_save(name):
    messagebox.showinfo("Guardar", f"{name} guardado/a correctamente.")

def generic_update(name):
    messagebox.showinfo("Actualizar", f"{name} actualizado/a correctamente.")

def generic_delete(name, entries):
    if messagebox.askyesno("Eliminar", f"¿Está seguro de eliminar este/a {name}?"):
        messagebox.showinfo("Eliminar", f"{name} eliminado/a correctamente.")

finca_fields = [
    ("Código Finca",       "entry", []),
    ("Nombre",             "entry", []),
    ("Ubicación",          "entry", []),
    ("Latitud",            "entry", []),
    ("Longitud",           "entry", []),
    ("Extensión (ha)",     "entry", []),
    ("Altitud (msnm)",     "entry", []),
    ("Temp. Promedio (°C)","entry", []),
    ("Tipo de Suelo",      "combo", ["Franco", "Arcilloso", "Arenoso", "Limoso", "Franco-Arcilloso"]),
]
sf, ef = build_form(tab_fincas, "GESTIÓN DE FINCAS", finca_fields, "#2d5a27")
make_buttons(sf,
    lambda: generic_save("Finca"),
    lambda: generic_update("Finca"),
    lambda: generic_delete("Finca", ef),
    lambda: clear_entries(ef))

cultivo_fields = [
    ("Código Cultivo",        "entry", []),
    ("Nombre Científico",     "entry", []),
    ("Nombre Común",          "entry", []),
    ("Tiempo de Crecimiento", "entry", []),
    ("Temp. Mínima (°C)",     "entry", []),
    ("Temp. Máxima (°C)",     "entry", []),
    ("Req. Agua (mm/año)",    "entry", []),
    ("Tipo",                  "combo", ["Cereal", "Leguminosa", "Hortaliza", "Frutal", "Tubérculo", "Forraje"]),
]
sc, ec = build_form(tab_cultivos, "GESTIÓN DE CULTIVOS", cultivo_fields, "#5a6e27")
make_buttons(sc,
    lambda: generic_save("Cultivo"),
    lambda: generic_update("Cultivo"),
    lambda: generic_delete("Cultivo", ec),
    lambda: clear_entries(ec))

insumo_fields = [
    ("Código Insumo",      "entry", []),
    ("Nombre Comercial",   "entry", []),
    ("Tipo",               "combo", ["Semilla", "Fertilizante", "Plaguicida", "Herbicida", "Fungicida", "Otro"]),
    ("Unidad de Medida",   "combo", ["kg", "litro", "unidad", "bulto", "tonelada"]),
    ("Cantidad en Stock",  "entry", []),
    ("Ubicación Almacén",  "entry", []),
    ("Fecha de Caducidad", "entry", []),
    ("Precio Unitario",    "entry", []),
]
si, ei = build_form(tab_insumos, "GESTIÓN DE INSUMOS", insumo_fields, "#7a5c1e")
make_buttons(si,
    lambda: generic_save("Insumo"),
    lambda: generic_update("Insumo"),
    lambda: generic_delete("Insumo", ei),
    lambda: clear_entries(ei))

maquinaria_fields = [
    ("Código Máquina",    "entry", []),
    ("Marca",             "entry", []),
    ("Modelo",            "entry", []),
    ("Año Fabricación",   "entry", []),
    ("Potencia (HP)",     "entry", []),
    ("Tipo Combustible",  "combo", ["Diésel", "Gasolina", "Eléctrico", "Gas"]),
    ("Horómetro (hrs)",   "entry", []),
    ("Estado Operativo",  "combo", ["Operativo", "En Mantenimiento", "Fuera de Servicio"]),
]
sm, em = build_form(tab_maquinaria, "GESTIÓN DE MAQUINARIA", maquinaria_fields, "#3d5c7a")
make_buttons(sm,
    lambda: generic_save("Máquina"),
    lambda: generic_update("Máquina"),
    lambda: generic_delete("Máquina", em),
    lambda: clear_entries(em))

empleado_fields = [
    ("DNI",                "entry", []),
    ("Nombres",            "entry", []),
    ("Apellidos",          "entry", []),
    ("Fecha Nacimiento",   "entry", []),
    ("Dirección",          "entry", []),
    ("Teléfono",           "entry", []),
    ("Especialidad",       "combo", ["Agrónomo", "Operario", "Técnico", "Administrador", "Conductor"]),
    ("Fecha Contratación", "entry", []),
    ("Salario",            "entry", []),
    ("Área Asignada",      "combo", ["Finca Norte", "Finca Sur", "Almacén", "Oficina", "Mantenimiento"]),
]
se, ee = build_form(tab_empleados, "GESTIÓN DE EMPLEADOS", empleado_fields, "#6b3d7a")
make_buttons(se,
    lambda: generic_save("Empleado"),
    lambda: generic_update("Empleado"),
    lambda: generic_delete("Empleado", ee),
    lambda: clear_entries(ee))

cosecha_fields = [
    ("Código Cosecha",     "entry", []),
    ("Parcela",            "entry", []),
    ("Cultivo",            "entry", []),
    ("Fecha Inicio",       "entry", []),
    ("Fecha Fin",          "entry", []),
    ("Cantidad (kg)",      "entry", []),
    ("Calidad",            "combo", ["Premium", "Primera", "Segunda", "Tercera"]),
    ("Método Cosecha",     "combo", ["Manual", "Mecanizada", "Semi-mecanizada"]),
]
sh, eh = build_form(tab_cosechas, "REGISTRO DE COSECHAS", cosecha_fields, "#2d7a5a")
make_buttons(sh,
    lambda: generic_save("Cosecha"),
    lambda: generic_update("Cosecha"),
    lambda: generic_delete("Cosecha", eh),
    lambda: clear_entries(eh))

cliente_fields = [
    ("Código Cliente",  "entry", []),
    ("Razón Social",    "entry", []),
    ("RUC / DNI",       "entry", []),
    ("Dirección Fiscal","entry", []),
    ("Teléfono",        "entry", []),
    ("Correo",          "entry", []),
    ("Línea de Crédito","entry", []),
    ("Tipo",            "combo", ["Minorista", "Mayorista", "Exportador", "Distribuidor"]),
]
scl, ecl = build_form(tab_clientes, "GESTIÓN DE CLIENTES", cliente_fields, "#7a3d2d")
make_buttons(scl,
    lambda: generic_save("Cliente"),
    lambda: generic_update("Cliente"),
    lambda: generic_delete("Cliente", ecl),
    lambda: clear_entries(ecl))

root.mainloop()