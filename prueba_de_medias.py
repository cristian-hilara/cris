# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 00:18:46 2025

@author: hilar
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import numpy as np

class PruebaMediasConGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba de Medias - Números Pseudoaleatorios")
        self.root.geometry("1400x800")
        self.root.configure(bg="#1e1e2f")
        
        # Variables
        self.numeros = []
        self.resultados = {}
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg="#1e1e2f")
        title_frame.pack(pady=15)
        
        tk.Label(title_frame, text="PRUEBA DE MEDIAS CON VISUALIZACIÓN", 
                font=("Arial", 20, "bold"), 
                bg="#1e1e2f", fg="#4a90e2").pack()
        
        tk.Label(title_frame, text="Evaluación de Números Pseudoaleatorios", 
                font=("Arial", 12), 
                bg="#1e1e2f", fg="white").pack()
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg="#1e1e2f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Columna izquierda (controles y resultados)
        left_frame = tk.Frame(main_frame, bg="#1e1e2f")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sección de entrada
        self.crear_entrada(left_frame)
        
        # Sección de resultados
        self.crear_resultados(left_frame)
        
        # Sección de conclusión
        self.crear_conclusion(left_frame)
        
        # Columna derecha (gráfica)
        right_frame = tk.Frame(main_frame, bg="#1e1e2f")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        self.crear_grafica(right_frame)
    
    def crear_entrada(self, parent):
        input_frame = tk.LabelFrame(parent, text="Entrada de Datos", 
                                   bg="#2e2e3e", fg="white", 
                                   font=("Arial", 12, "bold"))
        input_frame.pack(fill=tk.X, pady=10)
        
        # Entrada de números
        tk.Label(input_frame, text="Ingresa los números separados por comas:", 
                bg="#2e2e3e", fg="white", font=("Arial", 11)).pack(anchor=tk.W, padx=10, pady=5)
        
        self.entrada_numeros = tk.Text(input_frame, height=3, width=60, 
                                      font=("Arial", 10))
        self.entrada_numeros.pack(padx=10, pady=5)
        
        # Valores predeterminados
        numeros_ejemplo = "0.2778, 0.3487, 0.2869, 0.9825, 0.4311"
        self.entrada_numeros.insert("1.0", numeros_ejemplo)
        
        # Frame para controles
        control_frame = tk.Frame(input_frame, bg="#2e2e3e")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nivel de significancia
        tk.Label(control_frame, text="Nivel de significancia (α):", 
                bg="#2e2e3e", fg="white", font=("Arial", 11)).pack(side=tk.LEFT)
        
        self.alpha_var = tk.StringVar(value="0.05")
        alpha_combo = ttk.Combobox(control_frame, textvariable=self.alpha_var, 
                                  values=["0.01", "0.05", "0.10"], 
                                  state="readonly", width=8)
        alpha_combo.pack(side=tk.LEFT, padx=10)
        
        # Botones
        btn_frame = tk.Frame(control_frame, bg="#2e2e3e")
        btn_frame.pack(side=tk.RIGHT)
        
        btn_calcular = tk.Button(btn_frame, text="Calcular Prueba", 
                               command=self.calcular_prueba,
                               bg="#4a90e2", fg="white", 
                               font=("Arial", 11, "bold"),
                               padx=15, pady=5)
        btn_calcular.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(btn_frame, text="Limpiar", 
                              command=self.limpiar,
                              bg="#e74c3c", fg="white", 
                              font=("Arial", 11, "bold"),
                              padx=15, pady=5)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
    
    def crear_resultados(self, parent):
        results_frame = tk.LabelFrame(parent, text="Resultados Detallados", 
                                    bg="#2e2e3e", fg="white", 
                                    font=("Arial", 12, "bold"))
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configurar estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#1e1e2f",
                       foreground="white",
                       rowheight=25,
                       fieldbackground="#1e1e2f")
        style.map("Treeview", 
                 background=[("selected", "#4a90e2")])
        
        # Tabla de resultados
        self.tabla_resultados = ttk.Treeview(results_frame, 
                                           columns=("Parámetro", "Fórmula", "Valor"), 
                                           show="headings", height=6)
        
        # Configurar columnas
        self.tabla_resultados.heading("Parámetro", text="Parámetro")
        self.tabla_resultados.heading("Fórmula", text="Fórmula")
        self.tabla_resultados.heading("Valor", text="Valor")
        
        self.tabla_resultados.column("Parámetro", width=80, anchor="center")
        self.tabla_resultados.column("Fórmula", width=120, anchor="center")
        self.tabla_resultados.column("Valor", width=100, anchor="center")
        
        self.tabla_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def crear_conclusion(self, parent):
        conclusion_frame = tk.LabelFrame(parent, text="Evaluación Final", 
                                       bg="#2e2e3e", fg="white", 
                                       font=("Arial", 12, "bold"))
        conclusion_frame.pack(fill=tk.X, pady=10)
        
        self.texto_conclusion = tk.Text(conclusion_frame, height=4, width=60, 
                                       font=("Arial", 10), bg="#1e1e2f", fg="white",
                                       wrap=tk.WORD, state=tk.DISABLED)
        self.texto_conclusion.pack(padx=10, pady=10)
        
        # Texto inicial
        self.mostrar_mensaje_inicial()
    
    def crear_grafica(self, parent):
        grafica_frame = tk.LabelFrame(parent, text="Visualización de la Prueba", 
                                     bg="#2e2e3e", fg="white", 
                                     font=("Arial", 12, "bold"))
        grafica_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configurar matplotlib para fondo oscuro
        plt.style.use('dark_background')
        
        # Crear figura
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 10))
        self.fig.patch.set_facecolor('#2e2e3e')
        
        # Canvas para mostrar la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, grafica_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Gráfica inicial
        self.mostrar_grafica_inicial()
    
    def mostrar_grafica_inicial(self):
        # Limpiar gráficas
        self.ax1.clear()
        self.ax2.clear()
        
        # Configurar gráfica 1 (números)
        self.ax1.set_title("Números Pseudoaleatorios", color='white', fontsize=14, pad=20)
        self.ax1.set_xlabel("Índice", color='white')
        self.ax1.set_ylabel("Valor", color='white')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.text(0.5, 0.5, "Ingresa números y presiona\n'Calcular Prueba'", 
                     transform=self.ax1.transAxes, ha='center', va='center',
                     fontsize=12, color='white', alpha=0.7)
        
        # Configurar gráfica 2 (distribución)
        self.ax2.set_title("Evaluación de la Media", color='white', fontsize=14, pad=20)
        self.ax2.set_xlabel("Valor", color='white')
        self.ax2.set_ylabel("Densidad", color='white')
        self.ax2.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def mostrar_mensaje_inicial(self):
        mensaje = """
 Ingresa números pseudoaleatorios separados por comas
Selecciona el nivel de significancia (α)
 Presiona 'Calcular Prueba' para evaluar y visualizar
        """
        self.actualizar_conclusion(mensaje, "white")
    
    def calcular_prueba(self):
        try:
            # Obtener y procesar números
            texto_numeros = self.entrada_numeros.get("1.0", tk.END).strip()
            numeros_str = [x.strip() for x in texto_numeros.split(',')]
            self.numeros = [float(x) for x in numeros_str if x]
            
            if len(self.numeros) < 2:
                messagebox.showerror("Error", "Ingresa al menos 2 números")
                return
            
            # Validar rango de números
            numeros_fuera_rango = [num for num in self.numeros if not (0 <= num <= 1)]
            if numeros_fuera_rango:
                messagebox.showwarning("Advertencia", 
                                     f"Los siguientes números no están entre 0 y 1:\n{numeros_fuera_rango}")
            
            # Parámetros
            alpha = float(self.alpha_var.get())
            n = len(self.numeros)
            z_critico = self.obtener_z_critico(alpha)
            
            # Cálculos principales
            suma = sum(self.numeros)
            media = suma / n
            sigma = 1 / math.sqrt(12)  # Desviación estándar teórica
            error_estandar = sigma / math.sqrt(n)
            
            # Límites de confianza
            li = 0.5 - z_critico * error_estandar
            ls = 0.5 + z_critico * error_estandar
            
            # Estadístico Z0
            z0 = (media - 0.5) / error_estandar
            
            # Evaluación
            pasa_limites = li <= media <= ls
            pasa_z = abs(z0) <= z_critico
            pasa_prueba = pasa_limites and pasa_z
            
            # Guardar resultados
            self.resultados = {
                'n': n,
                'suma': suma,
                'alpha': alpha,
                'z_critico': z_critico,
                'media': media,
                'sigma': sigma,
                'error_estandar': error_estandar,
                'li': li,
                'ls': ls,
                'z0': z0,
                'pasa_limites': pasa_limites,
                'pasa_z': pasa_z,
                'pasa_prueba': pasa_prueba
            }
            
            # Actualizar interfaz
            self.actualizar_tabla()
            self.mostrar_conclusion()
            self.actualizar_grafica()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos ingresados:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
    
    def obtener_z_critico(self, alpha):
        z_valores = {
            0.01: 2.576,
            0.05: 1.96,
            0.10: 1.645
        }
        return z_valores.get(alpha, 1.96)
    
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(item)
        
        # Datos para la tabla
        datos = [
            ("n", f"{self.resultados['n']}", f"{self.resultados['n']}"),
            ("X̄", "Σri / n", f"{self.resultados['media']:.4f}"),
            ("α", "Nivel sig.", f"{self.resultados['alpha']:.2f}"),
            ("Z_{α/2}", "Valor crítico", f"{self.resultados['z_critico']:.3f}"),
            ("LI", "0.5 - Z·σx̄", f"{self.resultados['li']:.4f}"),
            ("LS", "0.5 + Z·σx̄", f"{self.resultados['ls']:.4f}"),
            ("Z₀", "(X̄-0.5)/σx̄", f"{self.resultados['z0']:.4f}")
        ]
        
        for parametro, formula, valor in datos:
            self.tabla_resultados.insert("", tk.END, values=(parametro, formula, valor))
    
    def actualizar_grafica(self):
        # Limpiar gráficas
        self.ax1.clear()
        self.ax2.clear()
        
        # Gráfica 1: Números pseudoaleatorios con límites
        indices = range(1, len(self.numeros) + 1)
        
        # Plotear números
        self.ax1.scatter(indices, self.numeros, c='cyan', s=50, alpha=0.8, zorder=3, label='Números')
        self.ax1.plot(indices, self.numeros, 'cyan', alpha=0.5, linewidth=1)
        
        # Líneas de referencia
        self.ax1.axhline(y=0.5, color='yellow', linestyle='--', linewidth=2, alpha=0.8, label='Media teórica (0.5)')
        self.ax1.axhline(y=self.resultados['media'], color='orange', linestyle='-', linewidth=2, label=f'Media calculada ({self.resultados["media"]:.4f})')
        self.ax1.axhline(y=self.resultados['li'], color='red', linestyle=':', linewidth=2, alpha=0.8, label=f'LI ({self.resultados["li"]:.4f})')
        self.ax1.axhline(y=self.resultados['ls'], color='red', linestyle=':', linewidth=2, alpha=0.8, label=f'LS ({self.resultados["ls"]:.4f})')
        
        # Zona de aceptación
        self.ax1.fill_between([0, len(self.numeros) + 1], self.resultados['li'], self.resultados['ls'], 
                             alpha=0.2, color='green' if self.resultados['pasa_prueba'] else 'red',
                             label='Zona de aceptación')
        
        self.ax1.set_title("Números Pseudoaleatorios con Límites de Confianza", color='white', fontsize=14, pad=20)
        self.ax1.set_xlabel("Índice del número", color='white')
        self.ax1.set_ylabel("Valor", color='white')
        self.ax1.set_ylim(-0.1, 1.1)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(loc='upper right', fontsize=9)
        
        # Gráfica 2: Distribución y evaluación de la media
        x_dist = np.linspace(0, 1, 1000)
        y_dist = np.ones_like(x_dist)  # Distribución uniforme
        
        # Distribución teórica
        self.ax2.plot(x_dist, y_dist, 'white', linewidth=2, alpha=0.7, label='Distribución uniforme teórica')
        
        # Histograma de los números
        counts, bins, patches = self.ax2.hist(self.numeros, bins=min(10, len(self.numeros)//2 + 1), 
                                             alpha=0.6, color='cyan', density=True, 
                                             edgecolor='white', linewidth=1, label='Histograma de números')
        
        # Líneas verticales para la evaluación
        self.ax2.axvline(x=0.5, color='yellow', linestyle='--', linewidth=3, alpha=0.9, label='Media teórica (0.5)')
        self.ax2.axvline(x=self.resultados['media'], color='orange', linestyle='-', linewidth=3, label=f'Media calculada ({self.resultados["media"]:.4f})')
        self.ax2.axvline(x=self.resultados['li'], color='red', linestyle=':', linewidth=2, alpha=0.8, label=f'LI ({self.resultados["li"]:.4f})')
        self.ax2.axvline(x=self.resultados['ls'], color='red', linestyle=':', linewidth=2, alpha=0.8, label=f'LS ({self.resultados["ls"]:.4f})')
        
        # Zona de aceptación
        self.ax2.axvspan(self.resultados['li'], self.resultados['ls'], alpha=0.2, 
                        color='green' if self.resultados['pasa_prueba'] else 'red',
                        label='Zona de aceptación')
        
        # Texto con el resultado
        resultado_texto = "PASA" if self.resultados['pasa_prueba'] else "NO PASA"
        color_resultado = 'green' if self.resultados['pasa_prueba'] else 'red'
        
        self.ax2.text(0.02, 0.95, f"Resultado: {resultado_texto}", 
                     transform=self.ax2.transAxes, fontsize=12, fontweight='bold',
                     color=color_resultado, bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        self.ax2.set_title("Evaluación de la Media vs Distribución Teórica", color='white', fontsize=14, pad=20)
        self.ax2.set_xlabel("Valor", color='white')
        self.ax2.set_ylabel("Densidad", color='white')
        self.ax2.set_xlim(-0.05, 1.05)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.legend(loc='upper right', fontsize=9)
        
        # Ajustar layout
        self.fig.tight_layout()
        self.canvas.draw()
    
    def mostrar_conclusion(self):
        resultado = self.resultados['pasa_prueba']
        
        conclusion = f"""
 EVALUACIÓN DE LA PRUEBA DE MEDIAS:

DATOS: n={self.resultados['n']}, X̄={self.resultados['media']:.4f}, α={self.resultados['alpha']:.2f}

LÍMITES: [{self.resultados['li']:.4f}, {self.resultados['ls']:.4f}]
   ➤ {'CUMPLE' if self.resultados['pasa_limites'] else 'NO CUMPLE'}

 Z₀: {self.resultados['z0']:.4f} (debe ser ≤ {self.resultados['z_critico']:.3f})
   ➤ {'CUMPLE' if self.resultados['pasa_z'] else 'NO CUMPLE'}

CONCLUSIÓN: {'PASA LA PRUEBA' if resultado else 'NO PASA LA PRUEBA'}
        """
        
        color = "#27ae60" if resultado else "#e74c3c"
        self.actualizar_conclusion(conclusion, color)
    
    def actualizar_conclusion(self, texto, color):
        self.texto_conclusion.config(state=tk.NORMAL)
        self.texto_conclusion.delete("1.0", tk.END)
        self.texto_conclusion.insert("1.0", texto)
        self.texto_conclusion.config(fg=color, state=tk.DISABLED)
    
    def limpiar(self):
        # Limpiar entrada
        self.entrada_numeros.delete("1.0", tk.END)
        
        # Limpiar tabla
        for item in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(item)
        
        # Resetear conclusión
        self.mostrar_mensaje_inicial()
        
        # Resetear gráfica
        self.mostrar_grafica_inicial()
        
        # Limpiar variables
        self.resultados = {}
        self.numeros = []

if __name__ == "__main__":
    root = tk.Tk()
    app = PruebaMediasConGrafica(root)
    root.mainloop()