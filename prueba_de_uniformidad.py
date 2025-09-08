# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 16:57:16 2025

@author: hilar
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import chi2

class PruebaUniformidadConGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba de Uniformidad - Números Pseudoaleatorios")
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
        
        tk.Label(title_frame, text="PRUEBA DE UNIFORMIDAD CON VISUALIZACIÓN", 
                font=("Arial", 20, "bold"), 
                bg="#1e1e2f", fg="#4a90e2").pack()
        
        tk.Label(title_frame, text="Evaluación de Distribución Uniforme", 
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
        numeros_ejemplo = "0.12, 0.34, 0.67, 0.89, 0.23, 0.56, 0.78, 0.45, 0.91, 0.15, 0.38, 0.62, 0.85, 0.29, 0.73"
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
        
        # Número de intervalos
        tk.Label(control_frame, text="Intervalos (k):", 
                bg="#2e2e3e", fg="white", font=("Arial", 11)).pack(side=tk.LEFT, padx=(20,5))
        
        self.k_var = tk.StringVar(value="5")
        k_combo = ttk.Combobox(control_frame, textvariable=self.k_var, 
                              values=["3", "4", "5", "6", "8", "10"], 
                              state="readonly", width=5)
        k_combo.pack(side=tk.LEFT, padx=5)
        
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
                                           columns=("Intervalo", "Observada", "Esperada", "Contribución"), 
                                           show="headings", height=8)
        
        # Configurar columnas
        self.tabla_resultados.heading("Intervalo", text="Intervalo")
        self.tabla_resultados.heading("Observada", text="Obs (Oi)")
        self.tabla_resultados.heading("Esperada", text="Esp (Ei)")
        self.tabla_resultados.heading("Contribución", text="(Oi-Ei)²/Ei")
        
        self.tabla_resultados.column("Intervalo", width=100, anchor="center")
        self.tabla_resultados.column("Observada", width=70, anchor="center")
        self.tabla_resultados.column("Esperada", width=70, anchor="center")
        self.tabla_resultados.column("Contribución", width=100, anchor="center")
        
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
        grafica_frame = tk.LabelFrame(parent, text="Histograma de Uniformidad", 
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
        self.ax.set_title("Histograma de Uniformidad", color='white', fontsize=14, pad=20)
        self.ax.set_xlabel("Intervalos", color='white')
        self.ax.set_ylabel("Frecuencia", color='white')
        self.ax.grid(True, alpha=0.3)
        self.ax.text(0.5, 0.5, "Ingresa números y presiona\n'Calcular Prueba'", 
                     transform=self.ax.transAxes, ha='center', va='center',
                     fontsize=12, color='white', alpha=0.7)
        
        self.canvas.draw()
    
    def mostrar_mensaje_inicial(self):
        mensaje = """
📊 Ingresa números pseudoaleatorios separados por comas
📈 Selecciona nivel de significancia (α) y número de intervalos (k)
🔍 Presiona 'Calcular Prueba' para evaluar la uniformidad
📏 La prueba verificará si los números se distribuyen uniformemente
        """
        self.actualizar_conclusion(mensaje, "white")
    
    def calcular_prueba(self):
        try:
            # Obtener y procesar números
            texto_numeros = self.entrada_numeros.get("1.0", tk.END).strip()
            numeros_str = [x.strip() for x in texto_numeros.split(',')]
            self.numeros = [float(x) for x in numeros_str if x]
            
            if len(self.numeros) < 5:
                messagebox.showerror("Error", "Ingresa al menos 5 números")
                return
            
            # Validar rango de números
            numeros_fuera_rango = [num for num in self.numeros if not (0 <= num <= 1)]
            if numeros_fuera_rango:
                messagebox.showwarning("Advertencia", 
                                     f"Los siguientes números no están entre 0 y 1:\n{numeros_fuera_rango}")
            
            # Parámetros
            alpha = float(self.alpha_var.get())
            k = int(self.k_var.get())
            n = len(self.numeros)
            
            # Verificar que cada intervalo tenga al menos 5 observaciones esperadas
            frecuencia_esperada = n / k
            if frecuencia_esperada < 5:
                messagebox.showwarning("Advertencia", 
                                     f"Frecuencia esperada por intervalo ({frecuencia_esperada:.1f}) es menor a 5.\n"
                                     f"Considera usar menos intervalos o más números.")
            
            # Crear intervalos y contar frecuencias
            intervalos = np.linspace(0, 1, k+1)
            frecuencias_observadas = []
            intervalos_texto = []
            
            for i in range(k):
                inicio = intervalos[i]
                fin = intervalos[i+1]
                
                # Contar números en este intervalo
                if i == k-1:  # Último intervalo incluye el límite superior
                    count = sum(1 for num in self.numeros if inicio <= num <= fin)
                else:
                    count = sum(1 for num in self.numeros if inicio <= num < fin)
                
                frecuencias_observadas.append(count)
                intervalos_texto.append(f"[{inicio:.2f}, {fin:.2f}{']' if i == k-1 else ')'})")
            
            # Cálculos del estadístico Chi-cuadrado
            chi2_calculado = 0
            contribuciones = []
            
            for oi in frecuencias_observadas:
                contribucion = (oi - frecuencia_esperada)**2 / frecuencia_esperada
                contribuciones.append(contribucion)
                chi2_calculado += contribucion
            
            # Valor crítico
            grados_libertad = k - 1
            chi2_critico = chi2.ppf(1 - alpha, grados_libertad)
            
            # Evaluación
            pasa_prueba = chi2_calculado <= chi2_critico
            
            # Guardar resultados
            self.resultados = {
                'n': n,
                'k': k,
                'alpha': alpha,
                'intervalos_texto': intervalos_texto,
                'intervalos': intervalos,
                'frecuencias_observadas': frecuencias_observadas,
                'frecuencia_esperada': frecuencia_esperada,
                'contribuciones': contribuciones,
                'chi2_calculado': chi2_calculado,
                'chi2_critico': chi2_critico,
                'grados_libertad': grados_libertad,
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
        
        # Agregar datos de cada intervalo
        for i in range(self.resultados['k']):
            self.tabla_resultados.insert("", tk.END, values=(
                self.resultados['intervalos_texto'][i],
                self.resultados['frecuencias_observadas'][i],
                f"{self.resultados['frecuencia_esperada']:.1f}",
                f"{self.resultados['contribuciones'][i]:.4f}"
            ))
        
        # Agregar fila de totales
        self.tabla_resultados.insert("", tk.END, values=(
            "TOTAL",
            sum(self.resultados['frecuencias_observadas']),
            f"{self.resultados['frecuencia_esperada'] * self.resultados['k']:.1f}",
            f"χ² = {self.resultados['chi2_calculado']:.4f}"
        ), tags=("total",))
    
    def actualizar_grafica(self):
        # Limpiar gráfica
        self.ax.clear()
        
        # Crear histograma
        x_pos = range(self.resultados['k'])
        
        # Barras de frecuencias observadas
        bars_obs = self.ax.bar(x_pos, self.resultados['frecuencias_observadas'], 
                              alpha=0.7, color='cyan', label='Frecuencias Observadas (Oi)',
                              edgecolor='white', linewidth=1)
        
        # Línea de frecuencia esperada
        self.ax.axhline(y=self.resultados['frecuencia_esperada'], 
                       color='yellow', linestyle='--', linewidth=2, 
                       label=f'Frecuencia Esperada ({self.resultados["frecuencia_esperada"]:.1f})')
        
        # Agregar valores en las barras
        for i, (bar, freq) in enumerate(zip(bars_obs, self.resultados['frecuencias_observadas'])):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{freq}', ha='center', va='bottom', color='white', fontweight='bold')
        
        # Texto con el resultado
        resultado_texto = "✅ PASA" if self.resultados['pasa_prueba'] else "❌ NO PASA"
        color_resultado = 'green' if self.resultados['pasa_prueba'] else 'red'
        
        self.ax.text(0.02, 0.95, f"Resultado: {resultado_texto}", 
                     transform=self.ax.transAxes, fontsize=12, fontweight='bold',
                     color=color_resultado, bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
        
        # Información estadística
        info_text = f"χ² = {self.resultados['chi2_calculado']:.3f}\nχ²crítico = {self.resultados['chi2_critico']:.3f}\ngl = {self.resultados['grados_libertad']}"
        self.ax.text(0.98, 0.95, info_text, 
                     transform=self.ax.transAxes, fontsize=10,
                     color='white', bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.5),
                     ha='right', va='top')
        
        # Configurar ejes y etiquetas
        self.ax.set_title("Prueba de Uniformidad - Distribución de Frecuencias", color='white', fontsize=14, pad=20)
        self.ax.set_xlabel("Intervalos", color='white')
        self.ax.set_ylabel("Frecuencia", color='white')
        self.ax.set_xticks(x_pos)
        self.ax.set_xticklabels([f"Int {i+1}" for i in range(self.resultados['k'])])
        self.ax.set_ylim(0, max(self.resultados['frecuencias_observadas']) * 1.2)
        self.ax.grid(True, alpha=0.3, axis='y')
        self.ax.legend(loc='upper left', fontsize=10)
        
        # Ajustar layout
        self.fig.tight_layout()
        self.canvas.draw()
    
    def mostrar_conclusion(self):
        resultado = self.resultados['pasa_prueba']
        
        conclusion = f"""
🔍 EVALUACIÓN DE LA PRUEBA DE UNIFORMIDAD:

📊 DATOS: n={self.resultados['n']}, k={self.resultados['k']} intervalos, α={self.resultados['alpha']:.2f}
   Frecuencia esperada por intervalo: {self.resultados['frecuencia_esperada']:.1f}

📈 CHI-CUADRADO: χ² = {self.resultados['chi2_calculado']:.3f}
   ➤ Valor crítico: χ²({self.resultados['alpha']:.2f}, {self.resultados['grados_libertad']}) = {self.resultados['chi2_critico']:.3f}
   ➤ {'✅ CUMPLE' if self.resultados['pasa_prueba'] else '❌ NO CUMPLE'} (χ² {'≤' if self.resultados['pasa_prueba'] else '>'} χ²crítico)

🎯 CONCLUSIÓN: {'✅ PASA LA PRUEBA' if resultado else '❌ NO PASA LA PRUEBA'}
   {'→ Los números siguen una distribución uniforme' if resultado else '→ Los números NO siguen una distribución uniforme'}
   {'→ Las frecuencias son estadísticamente similares' if resultado else '→ Hay desviaciones significativas en las frecuencias'}
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
    app = PruebaUniformidadConGrafica(root)
    root.mainloop()