# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:11:55 2025

@author: hilar
"""
import tkinter as tk
from tkinter import ttk, messagebox

def multiplicador_constante_variable(x0, x1, n):
    """
    Genera n números pseudoaleatorios usando el método:
    - Primera iteración: y0 = x0 * x1
    - Luego: y_n = x_(n-1) * x_n
    Aplicando reglas de ajuste de dígitos y tomando 4 dígitos centrales.
    """
    resultados = []
    prev = x0
    const = x1
    
    for i in range(n):
        y = prev * const
        y_str = str(y)
        
        # Aplicar las reglas según la cantidad de dígitos
        if len(y_str) == 7:
            # 7 dígitos: agregar un cero a la izquierda para tener 8
            y_str = '0' + y_str
        elif len(y_str) == 6:
            # 6 dígitos: dejar así porque es par
            pass
        elif len(y_str) == 5:
            # 5 dígitos: agregar un cero a la izquierda para tener 6 (par)
            y_str = '0' + y_str
        elif len(y_str) == 4:
            # 4 dígitos: agregar dos ceros para poder extraer 4 centrales
            y_str = '00' + y_str
        elif len(y_str) == 3:
            # 3 dígitos: agregar un cero para tener 4 (par)
            y_str = '0' + y_str
        elif len(y_str) == 2:
            # 2 dígitos: agregar dos ceros para poder extraer centrales
            y_str = '00' + y_str
        elif len(y_str) == 1:
            # 1 dígito: agregar un cero para tener 2 (par)
            y_str = '0' + y_str
        elif len(y_str) == 8:
            # 8 dígitos: ya es par, no hacer nada
            pass
        
        # Extraer los 4 dígitos centrales
        longitud = len(y_str)
        inicio = (longitud - 4) // 2
        fin = inicio + 4
        x_new = int(y_str[inicio:fin])
        
        r = x_new / 10000
        resultados.append((y, y_str, x_new, r))
        
        # Preparar para la siguiente iteración
        prev = const
        const = x_new
    
    return resultados

def generar():
    try:
        x0 = int(entry_x0.get())
        x1 = int(entry_x1.get())
        n = int(entry_n.get())
        if x0 < 1000 or x0 > 9999 or x1 < 1000 or x1 > 9999:
            messagebox.showerror("Error", "x0 y x1 deben ser números de 4 dígitos.")
            return
        if n <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return
        
        # Limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)
        
        resultados = multiplicador_constante_variable(x0, x1, n)
        for i, (y, y_str, x, r) in enumerate(resultados, start=1):
            tabla.insert("", "end", values=(i, y, y_str, x, f"{r:.4f}"))
            
    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos.")

# Crear ventana principal
root = tk.Tk()
root.title("Algoritmo del Multiplicador Constante Variable")
root.geometry("900x500")
root.configure(bg="#1e1e2f")

# Estilos
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview",
                background="#2e2e3e",
                foreground="white",
                rowheight=25,
                fieldbackground="#2e2e3e")
style.map("Treeview",
          background=[("selected", "#4a90e2")])

# Título
label_title = tk.Label(root, text="Método del Multiplicador Constante Variable",
                       font=("Arial", 18, "bold"),
                       bg="#1e1e2f", fg="white")
label_title.pack(pady=10)

# Frame de entrada
frame_input = tk.Frame(root, bg="#1e1e2f")
frame_input.pack(pady=10)

tk.Label(frame_input, text="x0 (semilla):",
         bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
entry_x0 = tk.Entry(frame_input, font=("Arial", 12))
entry_x0.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="x1 (constante inicial):",
         bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=5)
entry_x1 = tk.Entry(frame_input, font=("Arial", 12))
entry_x1.grid(row=0, column=3, padx=5)

tk.Label(frame_input, text="Cantidad de números:",
         bg="#1e1e2f", fg="white", font=("Arial", 12)).grid(row=0, column=4, padx=5)
entry_n = tk.Entry(frame_input, font=("Arial", 12))
entry_n.grid(row=0, column=5, padx=5)

btn_generar = tk.Button(frame_input, text="Generar", command=generar,
                        font=("Arial", 12, "bold"),
                        bg="#4a90e2", fg="white",
                        activebackground="#357ABD", activeforeground="white",
                        relief="flat", padx=10, pady=5)
btn_generar.grid(row=0, column=6, padx=10)

# Tabla con scrollbar integrada
frame_tabla = tk.Frame(root, bg="#1e1e2f")
frame_tabla.pack(pady=10, fill="both", expand=True, padx=20)

cols = ("Iteración", "y = prev*const", "y ajustado", "x_n (4 centrales)", "r")
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=12)

# Configurar encabezados y columnas
tabla.heading("Iteración", text="Iteración")
tabla.heading("y = prev*const", text="y = prev*const")
tabla.heading("y ajustado", text="y ajustado")
tabla.heading("x_n (4 centrales)", text="x_n (4 centrales)")
tabla.heading("r", text="r")

tabla.column("Iteración", width=100, anchor="center")
tabla.column("y = prev*const", width=150, anchor="center")
tabla.column("y ajustado", width=150, anchor="center")
tabla.column("x_n (4 centrales)", width=150, anchor="center")
tabla.column("r", width=120, anchor="center")

# Scrollbar
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll_y.set)

# Empaquetar tabla y scrollbar
tabla.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

root.mainloop()
