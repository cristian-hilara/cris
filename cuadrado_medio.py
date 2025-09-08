# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:01:23 2025

@author: hilara calle cristian ramiro
"""
import tkinter as tk
from tkinter import ttk, messagebox

def cuadrados_medios(seed, n):
    resultados = []
    x = seed
    for i in range(n):
        y = x * x
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
        x = int(y_str[inicio:fin])
        
        r = x / 10000
        resultados.append((y, y_str, x, r))
    return resultados

def generar():
    try:
        semilla = int(entry_seed.get())
        n = int(entry_n.get())
        if semilla < 1000 or semilla > 9999:
            messagebox.showerror("Error", "La semilla debe ser un número de 4 dígitos.")
            return
        if n <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return

        # limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)

        resultados = cuadrados_medios(semilla, n)
        for i, (y, y_str, x, r) in enumerate(resultados, start=1):
            tabla.insert("", "end", values=(i, y, y_str, x, f"{r:.4f}"))

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos.")

# Crear ventana principal
root = tk.Tk()
root.title("Generador - Método de Cuadrados Medios")
root.geometry("700x450")

# Título
label_title = tk.Label(root, text="Algoritmo de Cuadrados Medios",
                       font=("Arial", 18, "bold"),
                       bg="#1e1e2f", fg="white")
label_title.pack(pady=10)

# Frame de entrada
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Semilla (4 dígitos):").grid(row=0, column=0, padx=5)
entry_seed = tk.Entry(frame_input)
entry_seed.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Cantidad de números:").grid(row=0, column=2, padx=5)
entry_n = tk.Entry(frame_input)
entry_n.grid(row=0, column=3, padx=5)

btn_generar = tk.Button(frame_input, text="Generar", command=generar)
btn_generar.grid(row=0, column=4, padx=10)

# Tabla para mostrar resultados
cols = ("Iteración", "y = x^2", "y ajustado", "x (4 centrales)", "r")
tabla = ttk.Treeview(root, columns=cols, show="headings", height=12)
tabla.heading("Iteración", text="Iteración")
tabla.heading("y = x^2", text="y = x²")
tabla.heading("y ajustado", text="y ajustado")
tabla.heading("x (4 centrales)", text="x (4 centrales)")
tabla.heading("r", text="r")

tabla.column("Iteración", width=80, anchor="center")
tabla.column("y = x^2", width=120, anchor="center")
tabla.column("y ajustado", width=120, anchor="center")
tabla.column("x (4 centrales)", width=120, anchor="center")
tabla.column("r", width=100, anchor="center")

tabla.pack(pady=10)

# Iniciar la interfaz
root.mainloop()