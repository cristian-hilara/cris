# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 17:30:17 2025

@author: hilar
"""

# -*- coding: utf-8 -*-
"""
Prueba de Uniformidad Chi-cuadrado (bondad de ajuste a U(0,1))
Interfaz estilo dark con Tkinter + Matplotlib
Requiere: numpy, scipy, matplotlib
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import chi2

class PruebaUniformidadChi2GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba de Uniformidad χ² - Números Pseudoaleatorios")
        self.root.geometry("1280x760")
        self.root.configure(bg="#1e1e2f")

        self.numeros = []
        self.resultados = {}

        self._crear_interfaz()

    # ===================== UI =====================
    def _crear_interfaz(self):
        title_frame = tk.Frame(self.root, bg="#1e1e2f")
        title_frame.pack(pady=15)

        tk.Label(
            title_frame,
            text="PRUEBA DE UNIFORMIDAD χ² (U[0,1])",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f", fg="#4a90e2"
        ).pack()
        tk.Label(
            title_frame,
            text="Bondad de ajuste de números pseudoaleatorios a la distribución uniforme en [0,1]",
            font=("Arial", 12),
            bg="#1e1e2f", fg="white"
        ).pack()

        main = tk.Frame(self.root, bg="#1e1e2f")
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left = tk.Frame(main, bg="#1e1e2f")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = tk.Frame(main, bg="#1e1e2f")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        self._crear_entrada(left)
        self._crear_resultados(left)
        self._crear_conclusion(left)
        self._crear_grafica(right)

    def _crear_entrada(self, parent):
        box = tk.LabelFrame(parent, text="Entrada y Parámetros", bg="#2e2e3e", fg="white",
                            font=("Arial", 12, "bold"))
        box.pack(fill=tk.X, pady=10)

        # Números
        tk.Label(box, text="Ingresa números en [0,1] separados por comas:",
                 bg="#2e2e3e", fg="white", font=("Arial", 11)).pack(anchor=tk.W, padx=10, pady=(8, 4))
        self.txt_numeros = tk.Text(box, height=3, width=70, font=("Arial", 10))
        self.txt_numeros.pack(padx=10, pady=5, fill=tk.X)

        ejemplo = "0.12, 0.34, 0.67, 0.89, 0.23, 0.56, 0.78, 0.45, 0.91, 0.15, 0.38, 0.62, 0.85, 0.29, 0.73"
        self.txt_numeros.insert("1.0", ejemplo)

        # Parámetros
        params = tk.Frame(box, bg="#2e2e3e")
        params.pack(fill=tk.X, padx=10, pady=8)

        # Alpha
        tk.Label(params, text="Significancia (α):", bg="#2e2e3e", fg="white",
                 font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.var_alpha = tk.StringVar(value="0.05")
        cmb_alpha = ttk.Combobox(params, textvariable=self.var_alpha, state="readonly", width=8,
                                 values=["0.01", "0.05", "0.10"])
        cmb_alpha.grid(row=0, column=1, padx=(6, 20))

        # Método de intervalos
        tk.Label(params, text="Método de intervalos:", bg="#2e2e3e", fg="white",
                 font=("Arial", 11)).grid(row=0, column=2, sticky="w")
        self.var_metodo = tk.StringVar(value="Manual (k)")
        cmb_metodo = ttk.Combobox(
            params, textvariable=self.var_metodo, state="readonly", width=14,
            values=["Manual (k)", "Sturges", "√n"]
        )
        cmb_metodo.grid(row=0, column=3, padx=(6, 20))
        cmb_metodo.bind("<<ComboboxSelected>>", self._toggle_k)

        # k manual
        tk.Label(params, text="k:", bg="#2e2e3e", fg="white",
                 font=("Arial", 11)).grid(row=0, column=4, sticky="w")
        self.var_k = tk.StringVar(value="5")
        self.cmb_k = ttk.Combobox(params, textvariable=self.var_k, width=6, state="readonly",
                                  values=["3", "4", "5", "6", "8", "10", "12", "15", "20"])
        self.cmb_k.grid(row=0, column=5, padx=(6, 20))

        # Forzar Ei >= 5
        self.var_fusionar = tk.BooleanVar(value=True)
        chk_fusionar = ttk.Checkbutton(
            params, text="Forzar Ei ≥ 5 (fusionar colas)", variable=self.var_fusionar
        )
        chk_fusionar.grid(row=0, column=6, sticky="w")

        # Botones
        btns = tk.Frame(params, bg="#2e2e3e")
        btns.grid(row=0, column=7, sticky="e")

        tk.Button(btns, text="Calcular χ²", command=self.calcular,
                  bg="#4a90e2", fg="white", font=("Arial", 11, "bold"),
                  padx=14, pady=5).pack(side=tk.LEFT, padx=4)
        tk.Button(btns, text="Limpiar", command=self.limpiar,
                  bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                  padx=14, pady=5).pack(side=tk.LEFT, padx=4)

        # Export
        exp = tk.Frame(box, bg="#2e2e3e")
        exp.pack(fill=tk.X, padx=10, pady=(0,10))
        tk.Button(exp, text="Exportar tabla a CSV", command=self.exportar_csv,
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  padx=10, pady=4).pack(side=tk.LEFT, padx=4)
        tk.Button(exp, text="Guardar gráfica PNG", command=self.exportar_png,
                  bg="#9b59b6", fg="white", font=("Arial", 10, "bold"),
                  padx=10, pady=4).pack(side=tk.LEFT, padx=4)

    def _crear_resultados(self, parent):
        box = tk.LabelFrame(parent, text="Resultados por Intervalo", bg="#2e2e3e", fg="white",
                            font=("Arial", 12, "bold"))
        box.pack(fill=tk.BOTH, expand=True, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1e1e2f", foreground="white",
                        rowheight=26, fieldbackground="#1e1e2f")
        style.map("Treeview", background=[("selected", "#4a90e2")])

        self.grid = ttk.Treeview(
            box,
            columns=("Intervalo", "Obs (Oi)", "Esp (Ei)", "(Oi-Ei)²/Ei"),
            show="headings", height=9
        )
        for col, w in [("Intervalo", 150), ("Obs (Oi)", 90), ("Esp (Ei)", 90), ("(Oi-Ei)²/Ei", 120)]:
            self.grid.heading(col, text=col)
            self.grid.column(col, width=w, anchor="center")
        self.grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _crear_conclusion(self, parent):
        box = tk.LabelFrame(parent, text="Evaluación Final", bg="#2e2e3e", fg="white",
                            font=("Arial", 12, "bold"))
        box.pack(fill=tk.X, pady=10)

        self.txt_conclusion = tk.Text(box, height=6, width=60, font=("Arial", 10),
                                      bg="#1e1e2f", fg="white", wrap=tk.WORD, state=tk.DISABLED)
        self.txt_conclusion.pack(padx=10, pady=10, fill=tk.X)
        self._mensaje_inicial()

    def _crear_grafica(self, parent):
        box = tk.LabelFrame(parent, text="Histograma & Estadísticos", bg="#2e2e3e", fg="white",
                            font=("Arial", 12, "bold"))
        box.pack(fill=tk.BOTH, expand=True, pady=10)

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(8.5, 6.2))
        self.fig.patch.set_facecolor('#2e2e3e')

        self.canvas = FigureCanvasTkAgg(self.fig, box)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._grafica_inicial()

    # ===================== LÓGICA =====================
    def _toggle_k(self, *_):
        metodo = self.var_metodo.get()
        self.cmb_k.config(state="readonly" if metodo == "Manual (k)" else "disabled")

    def _mensaje_inicial(self):
        txt = (
            "📊 Ingresa números en [0,1]. Selecciona α y el método de intervalos.\n"
            "🧮 Se aplicará χ² de bondad de ajuste para Uniforme(0,1).\n"
            "⚠️ Puedes fusionar intervalos de las colas para asegurar Ei ≥ 5."
        )
        self._set_conclusion(txt, "white")

    def _grafica_inicial(self):
        self.ax.clear()
        self.ax.set_title("Histograma de Uniformidad", color='white', fontsize=14, pad=20)
        self.ax.set_xlabel("Intervalos", color='white')
        self.ax.set_ylabel("Frecuencia", color='white')
        self.ax.grid(True, alpha=0.3)
        self.ax.text(0.5, 0.5, "Ingresa datos y pulsa\n“Calcular χ²”",
                     transform=self.ax.transAxes, ha='center', va='center',
                     fontsize=12, color='white', alpha=0.7)
        self.canvas.draw()

    def calcular(self):
        try:
            # Parseo
            raw = self.txt_numeros.get("1.0", tk.END).strip()
            nums = [x.strip() for x in raw.split(",")]
            self.numeros = [float(x) for x in nums if x != ""]
            n = len(self.numeros)

            if n < 5:
                messagebox.showerror("Error", "Ingresa al menos 5 números.")
                return

            fuera = [x for x in self.numeros if not (0.0 <= x <= 1.0)]
            if fuera:
                messagebox.showwarning("Advertencia",
                                       f"Se detectaron valores fuera de [0,1]:\n{fuera}\n"
                                       f"Se incluirán para el conteo del último/primer intervalo según límites.")
            alpha = float(self.var_alpha.get())

            # Definir k según método
            metodo = self.var_metodo.get()
            if metodo == "Manual (k)":
                k = int(self.var_k.get())
            elif metodo == "Sturges":
                k = int(math.ceil(math.log2(n) + 1))
            else:  # √n
                k = int(max(3, round(math.sqrt(n))))

            # Intervalos iniciales equiprobables
            bordes = np.linspace(0.0, 1.0, k + 1)
            obs = self._contar_en_intervalos(self.numeros, bordes)

            # Fusionar para Ei >= 5 si corresponde
            if self.var_fusionar.get():
                bordes, obs = self._fusionar_colas_si_necesario(bordes, obs, n)

            k_final = len(obs)
            ei = n / k_final
            gl = k_final - 1

            contrib = [(oi - ei) ** 2 / ei for oi in obs]
            chi2_calc = float(np.sum(contrib))
            chi2_crit = float(chi2.ppf(1 - alpha, gl)) if gl > 0 else float("nan")
            p_val = float(chi2.sf(chi2_calc, gl)) if gl > 0 else float("nan")
            pasa = (chi2_calc <= chi2_crit) if gl > 0 else False

            # Texto de intervalos
            intervalos_texto = []
            for i in range(k_final):
                a = bordes[i]
                b = bordes[i + 1]
                cierre = "]" if i == k_final - 1 else ")"
                intervalos_texto.append(f"[{a:.4f}, {b:.4f}{cierre})")

            self.resultados = {
                "n": n,
                "alpha": alpha,
                "k": k_final,
                "bordes": bordes,
                "intervalos_texto": intervalos_texto,
                "obs": obs,
                "ei": ei,
                "contrib": contrib,
                "chi2": chi2_calc,
                "chi2_crit": chi2_crit,
                "gl": gl,
                "p": p_val,
                "pasa": pasa,
            }

            self._actualizar_tabla()
            self._actualizar_conclusion()
            self._actualizar_grafica()

        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

    def _contar_en_intervalos(self, datos, bordes):
        # Contar en [ai, bi) excepto el último que es [a_k-1, b_k]
        k = len(bordes) - 1
        conteo = [0] * k
        for x in datos:
            # Último intervalo incluye el 1.0
            if x == bordes[-1]:
                conteo[-1] += 1
            else:
                # Buscar posición
                idx = np.searchsorted(bordes, x, side="right") - 1
                idx = max(0, min(idx, k - 1))
                conteo[idx] += 1
        return conteo

    def _fusionar_colas_si_necesario(self, bordes, obs, n):
        """
        Fusiona intervalos de colas hasta que todos los Ei >= 5.
        Estrategia: combinar primero y último con su vecino interno, alternando,
        mientras exista Oi con Ei<5 y queden al menos 2 intervalos.
        """
        k = len(obs)
        if k == 0:
            return bordes, obs

        ei = n / k
        if ei >= 5:
            return bordes, obs

        # Convertir a listas mutables
        bordes = list(bordes)
        obs = list(obs)

        # Alternar fusiones: izquierda, derecha, izquierda...
        lado_izq = True
        while True:
            k = len(obs)
            if k <= 1:
                break
            ei = n / k
            if min(obs) >= 5 and ei >= 5:
                break

            if lado_izq:
                # Fusionar primer con segundo
                obs[1] += obs[0]
                del obs[0]
                # quitar primer borde interno
                del bordes[1]
            else:
                # Fusionar último con penúltimo
                obs[-2] += obs[-1]
                del obs[-1]
                # quitar último borde interno
                del bordes[-2]

            lado_izq = not lado_izq

        return np.array(bordes, dtype=float), obs

    def _actualizar_tabla(self):
        for item in self.grid.get_children():
            self.grid.delete(item)

        for i in range(self.resultados["k"]):
            self.grid.insert(
                "", tk.END,
                values=(
                    self.resultados["intervalos_texto"][i],
                    self.resultados["obs"][i],
                    f"{self.resultados['ei']:.2f}",
                    f"{self.resultados['contrib'][i]:.4f}",
                )
            )

        total_contrib = sum(self.resultados["contrib"])
        self.grid.insert(
            "", tk.END,
            values=(
                "TOTAL",
                sum(self.resultados["obs"]),
                f"{self.resultados['ei'] * self.resultados['k']:.2f}",
                f"χ² = {total_contrib:.4f}",
            ),
            tags=("total",)
        )

    def _actualizar_grafica(self):
        self.ax.clear()

        k = self.resultados["k"]
        x = np.arange(k)
        bars = self.ax.bar(x, self.resultados["obs"], alpha=0.8, edgecolor="white",
                           linewidth=1, label="Frecuencias Observadas (Oi)")

        # Línea de Ei
        self.ax.axhline(y=self.resultados["ei"], linestyle="--", linewidth=2,
                        label=f"Frecuencia Esperada (Ei={self.resultados['ei']:.2f})")

        # Etiquetas en barras
        for b, oi in zip(bars, self.resultados["obs"]):
            h = b.get_height()
            self.ax.text(b.get_x() + b.get_width()/2., h + 0.1, str(oi),
                         ha='center', va='bottom', color='white', fontweight='bold')

        # Caja de info
        pasa = self.resultados["pasa"]
        res_txt = "✅ PASA" if pasa else "❌ NO PASA"
        res_col = "green" if pasa else "red"

        info = (
            f"χ² = {self.resultados['chi2']:.3f}\n"
            f"gl = {self.resultados['gl']}\n"
            f"χ² crítico = {self.resultados['chi2_crit']:.3f}\n"
            f"p-valor = {self.resultados['p']:.4f}"
        )

        self.ax.text(0.02, 0.96, f"Resultado: {res_txt}", transform=self.ax.transAxes,
                     fontsize=12, fontweight="bold", color=res_col,
                     bbox=dict(boxstyle="round,pad=0.35", facecolor='black', alpha=0.7), va="top")

        self.ax.text(0.98, 0.96, info, transform=self.ax.transAxes, ha="right", va="top",
                     fontsize=10, color="white",
                     bbox=dict(boxstyle="round,pad=0.35", facecolor='black', alpha=0.5))

        # Ejes
        self.ax.set_title("Prueba de Uniformidad χ² - Distribución de Frecuencias", color='white', fontsize=14, pad=20)
        self.ax.set_xlabel("Intervalos", color='white')
        self.ax.set_ylabel("Frecuencia", color='white')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels([f"Int {i+1}" for i in range(k)], rotation=0)
        ymax = max(max(self.resultados["obs"]), self.resultados["ei"]) * 1.25
        self.ax.set_ylim(0, max(1, ymax))
        self.ax.grid(True, alpha=0.3, axis='y')
        self.ax.legend(loc="upper left", fontsize=10)

        self.fig.tight_layout()
        self.canvas.draw()

    def _actualizar_conclusion(self):
        r = self.resultados
        pasa = r["pasa"]
        conclusion = (
            f"🔍 EVALUACIÓN χ² DE UNIFORMIDAD (U[0,1])\n\n"
            f"📊 Datos: n={r['n']}, k={r['k']} intervalos, α={r['alpha']:.2f}\n"
            f"   Frecuencia esperada Ei = n/k = {r['ei']:.2f}\n\n"
            f"📈 Estadístico: χ² = {r['chi2']:.3f}\n"
            f"   gl = {r['gl']} | χ² crítico(1-α) = {r['chi2_crit']:.3f} | p-valor = {r['p']:.4f}\n"
            f"   ➤ {'✅ CUMPLE (χ² ≤ χ² crítico)' if pasa else '❌ NO CUMPLE (χ² > χ² crítico)'}\n\n"
            f"🎯 Conclusión: {'✅ PASA la prueba' if pasa else '❌ NO PASA la prueba'}\n"
            f"   {'→ No hay evidencia para rechazar la uniformidad en [0,1]' if pasa else '→ Hay evidencia para rechazar la uniformidad en [0,1]'}"
        )
        color = "#27ae60" if pasa else "#e74c3c"
        self._set_conclusion(conclusion, color)

    def _set_conclusion(self, text, color):
        self.txt_conclusion.config(state=tk.NORMAL)
        self.txt_conclusion.delete("1.0", tk.END)
        self.txt_conclusion.insert("1.0", text)
        self.txt_conclusion.config(fg=color, state=tk.DISABLED)

    def limpiar(self):
        self.txt_numeros.delete("1.0", tk.END)
        self._mensaje_inicial()
        for item in self.grid.get_children():
            self.grid.delete(item)
        self._grafica_inicial()
        self.numeros = []
        self.resultados = {}

    # ===================== EXPORTS =====================
    def exportar_csv(self):
        if not self.resultados:
            messagebox.showinfo("Info", "No hay resultados para exportar.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Guardar tabla como CSV"
        )
        if not path:
            return

        import csv
        r = self.resultados
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Intervalo", "Obs (Oi)", "Esp (Ei)", "(Oi-Ei)^2/Ei"])
            for i in range(r["k"]):
                w.writerow([r["intervalos_texto"][i], r["obs"][i], f"{r['ei']:.4f}", f"{r['contrib'][i]:.6f}"])
            w.writerow([])
            w.writerow(["n", r["n"]])
            w.writerow(["k", r["k"]])
            w.writerow(["alpha", r["alpha"]])
            w.writerow(["gl", r["gl"]])
            w.writerow(["chi2", f"{r['chi2']:.6f}"])
            w.writerow(["chi2_crit", f"{r['chi2_crit']:.6f}"])
            w.writerow(["p", f"{r['p']:.6f}"])
            w.writerow(["pasa", "SI" if r["pasa"] else "NO"])

        messagebox.showinfo("Éxito", f"Tabla exportada a:\n{path}")

    def exportar_png(self):
        if not self.resultados:
            messagebox.showinfo("Info", "No hay gráfica para exportar.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            title="Guardar gráfica como PNG"
        )
        if not path:
            return
        self.fig.savefig(path, dpi=160, bbox_inches="tight")
        messagebox.showinfo("Éxito", f"Gráfica guardada en:\n{path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PruebaUniformidadChi2GUI(root)
    root.mainloop()
