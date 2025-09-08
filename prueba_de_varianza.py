# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:06:42 2025

@author: hilar
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import chi2

class PruebaVarianzaConGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba de Varianza - Números Pseudoaleatorios")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e2f")
        
        # Variables
        self.numeros = []
        self.resultados = {}
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg="#1e1e2f")
        title_frame.pack(pady=15)
        
        tk.Label(title_frame, text="PRUEBA DE VARIANZA CON VISUALIZACIÓN", 
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
                                           show="headings", height=8)
        
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
        
        self.texto_conclusion = tk.Text(conclusion_frame, height=5, width=60, 
                                       font=("Arial", 10), bg="#1e1e2f", fg="white",
                                       wrap=tk.WORD, state=tk.DISABLED)
        self.texto_conclusion.pack(padx=10, pady=10)
        
        # Texto inicial
        self.mostrar_mensaje_inicial()
    
    def crear_grafica(self, parent):
        grafica_frame = tk.LabelFrame(parent, text="Visualización de la Prueba de Varianza", 
                                     bg="#2e2e3e", fg="white", 
                                     font=("Arial", 12, "bold"))
        grafica_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configurar matplotlib para fondo oscuro
        plt.style.use('dark_background')
        
        # Crear figura
        self.fig, self.ax = plt.subplots(1, 1, figsize=(8, 6))
        self.fig.patch.set_facecolor('#2e2e3e')
        
        # Canvas para mostrar la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, grafica_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Gráfica inicial
        self.mostrar_grafica_inicial()
    
    def mostrar_grafica_inicial(self):
        # Limpiar gráfica
        self.ax.clear()
        
        # Configurar gráfica
        self.ax.set_title("Evaluación de Varianza - Números Pseudoaleatorios", color='white', fontsize=14, pad=20)
        self.ax.set_xlabel("Índice del número", color='white')
        self.ax.set_ylabel("Varianza", color='white')
        self.ax.grid(True, alpha=0.3)
        self.ax.text(0.5, 0.5, "Ingresa números y presiona\n'Calcular Prueba'", 
                     transform=self.ax.transAxes, ha='center', va='center',
                     fontsize=12, color='white', alpha=0.7)
        
        self.canvas.draw()
    
    def mostrar_mensaje_inicial(self):
        mensaje = """
📊 Ingresa números pseudoaleatorios separados por comas
📈 Selecciona el nivel de significancia (α)
🔍 Presiona 'Calcular Prueba' para evaluar la varianza
📏 La prueba verificará si la varianza se aproxima a 1/12 ≈ 0.0833
        """
        self.actualizar_conclusion(mensaje, "white")
    
    def calcular_prueba(self):
        try:
            # Obtener y procesar números
            texto_numeros = self.entrada_numeros.get("1.0", tk.END).strip()
            numeros_str = [x.strip() for x in texto_numeros.split(',')]
            self.numeros = [float(x) for x in numeros_str if x]
            
            if len(self.numeros) < 3:
                messagebox.showerror("Error", "Ingresa al menos 3 números")
                return
            
            # Validar rango de números
            numeros_fuera_rango = [num for num in self.numeros if not (0 <= num <= 1)]
            if numeros_fuera_rango:
                messagebox.showwarning("Advertencia", 
                                     f"Los siguientes números no están entre 0 y 1:\n{numeros_fuera_rango}")
            
            # Parámetros
            alpha = float(self.alpha_var.get())
            n = len(self.numeros)
            grados_libertad = n - 1
            sigma2_teorica = 1/12  # Varianza teórica
            
            # Cálculos principales
            media = sum(self.numeros) / n
            
            # Calcular varianza muestral S²
            suma_cuadrados = sum((x - media)**2 for x in self.numeros)
            varianza_muestral = suma_cuadrados / grados_libertad
            
            # Estadístico Chi-cuadrado
            chi2_calculado = grados_libertad * varianza_muestral / sigma2_teorica
            
            # Valores críticos de Chi-cuadrado
            chi2_inferior = chi2.ppf(alpha/2, grados_libertad)
            chi2_superior = chi2.ppf(1-alpha/2, grados_libertad)
            
            # Límites de confianza para la varianza
            li_varianza = sigma2_teorica * chi2_inferior / grados_libertad
            ls_varianza = sigma2_teorica * chi2_superior / grados_libertad
            
            # Evaluación
            pasa_chi2 = chi2_inferior <= chi2_calculado <= chi2_superior
            pasa_limites = li_varianza <= varianza_muestral <= ls_varianza
            pasa_prueba = pasa_chi2 and pasa_limites
            
            # Guardar resultados
            self.resultados = {
                'n': n,
                'alpha': alpha,
                'grados_libertad': grados_libertad,
                'media': media,
                'varianza_muestral': varianza_muestral,
                'sigma2_teorica': sigma2_teorica,
                'chi2_calculado': chi2_calculado,
                'chi2_inferior': chi2_inferior,
                'chi2_superior': chi2_superior,
                'li_varianza': li_varianza,
                'ls_varianza': ls_varianza,
                'pasa_chi2': pasa_chi2,
                'pasa_limites': pasa_limites,
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
    
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(item)
        
        # Datos para la tabla
        datos = [
            ("n", f"{self.resultados['n']}", f"{self.resultados['n']}"),
            ("X̄", "Σxi / n", f"{self.resultados['media']:.4f}"),
            ("S²", "Σ(xi-X̄)²/(n-1)", f"{self.resultados['varianza_muestral']:.4f}"),
            ("σ²", "1/12", f"{self.resultados['sigma2_teorica']:.4f}"),
            ("χ²", "(n-1)S²/σ²", f"{self.resultados['chi2_calculado']:.4f}"),
            ("χ²inf", f"χ²({self.resultados['alpha']/2:.3f})", f"{self.resultados['chi2_inferior']:.4f}"),
            ("χ²sup", f"χ²({1-self.resultados['alpha']/2:.3f})", f"{self.resultados['chi2_superior']:.4f}"),
            ("LI", "σ²×χ²inf/(n-1)", f"{self.resultados['li_varianza']:.4f}"),
            ("LS", "σ²×χ²sup/(n-1)", f"{self.resultados['ls_varianza']:.4f}")
        ]
        
        for parametro, formula, valor in datos:
            self.tabla_resultados.insert("", tk.END, values=(parametro, formula, valor))
    
    def actualizar_grafica(self):
        # Limpiar gráfica
        self.ax.clear()
        
        # Datos para la gráfica
        indices = range(1, len(self.numeros) + 1)
        
        # Plotear números individuales (como referencia en el fondo)
        self.ax.scatter(indices, self.numeros, c='lightblue', s=30, alpha=0.6, zorder=1, label='Números individuales')
        
        # Líneas horizontales principales
        self.ax.axhline(y=self.resultados['sigma2_teorica'], color='yellow', linestyle='--', 
                       linewidth=2, alpha=0.9, label=f'Varianza teórica ({self.resultados["sigma2_teorica"]:.4f})')
        
        self.ax.axhline(y=self.resultados['varianza_muestral'], color='orange', linestyle='-', 
                       linewidth=3, label=f'Varianza calculada (S² = {self.resultados["varianza_muestral"]:.4f})')
        
        # Límites de confianza
        self.ax.axhline(y=self.resultados['li_varianza'], color='red', linestyle=':', 
                       linewidth=2, alpha=0.8, label=f'LI ({self.resultados["li_varianza"]:.4f})')
        
        self.ax.axhline(y=self.resultados['ls_varianza'], color='red', linestyle=':', 
                       linewidth=2, alpha=0.8, label=f'LS ({self.resultados["ls_varianza"]:.4f})')
        
        # Zona de aceptación
        self.ax.fill_between([0, len(self.numeros) + 1], 
                            self.resultados['li_varianza'], 
                            self.resultados['ls_varianza'], 
                            alpha=0.2, color='green' if self.resultados['pasa_prueba'] else 'red',
                            label='Zona de aceptación', zorder=2)
        
        # Texto con el resultado
        resultado_texto = "✅ PASA" if self.resultados['pasa_prueba'] else "❌ NO PASA"
        color_resultado = 'green' if self.resultados['pasa_prueba'] else 'red'
        
        self.ax.text(0.02, 0.95, f"Resultado: {resultado_texto}", 
                     transform=self.ax.transAxes, fontsize=12, fontweight='bold',
                     color=color_resultado, bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        # Información adicional
        info_text = f"χ² = {self.resultados['chi2_calculado']:.3f}\n[{self.resultados['chi2_inferior']:.3f}, {self.resultados['chi2_superior']:.3f}]"
        self.ax.text(0.02, 0.85, info_text, 
                     transform=self.ax.transAxes, fontsize=10,
                     color='white', bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.5))
        
        self.ax.set_title("Prueba de Varianza con Límites de Confianza", color='white', fontsize=14, pad=20)
        self.ax.set_xlabel("Índice del número", color='white')
        self.ax.set_ylabel("Varianza", color='white')
        self.ax.set_ylim(-0.01, max(0.15, self.resultados['ls_varianza'] * 1.1))
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='upper right', fontsize=9)
        
        # Ajustar layout
        self.fig.tight_layout()
        self.canvas.draw()
    
    def mostrar_conclusion(self):
        resultado = self.resultados['pasa_prueba']
        
        conclusion = f"""
🔍 EVALUACIÓN DE LA PRUEBA DE VARIANZA:

📊 DATOS: n={self.resultados['n']}, S²={self.resultados['varianza_muestral']:.4f}, α={self.resultados['alpha']:.2f}

📏 LÍMITES DE VARIANZA: [{self.resultados['li_varianza']:.4f}, {self.resultados['ls_varianza']:.4f}]
   ➤ {'✅ CUMPLE' if self.resultados['pasa_limites'] else '❌ NO CUMPLE'} (S² {'∈' if self.resultados['pasa_limites'] else '∉'} límites)

📈 CHI-CUADRADO: χ² = {self.resultados['chi2_calculado']:.3f}
   ➤ Debe estar en [{self.resultados['chi2_inferior']:.3f}, {self.resultados['chi2_superior']:.3f}]
   ➤ {'✅ CUMPLE' if self.resultados['pasa_chi2'] else '❌ NO CUMPLE'}

🎯 CONCLUSIÓN: {'✅ PASA LA PRUEBA' if resultado else '❌ NO PASA LA PRUEBA'}
   {'→ La varianza es estadísticamente similar a la teórica (1/12)' if resultado else '→ La varianza difiere significativamente de la teórica'}
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
    app = PruebaVarianzaConGrafica(root)
    root.mainloop()