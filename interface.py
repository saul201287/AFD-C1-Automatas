import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from automata import AdjustedTemperatureAutomata, read_text_file, escribir_temperaturas_csv

class TemperatureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Temperaturas")
        self.root.geometry("500x400")
        self.root.config(bg="#f0f0f0")
        
        self.input_file = ""
        self.output_file = "output.csv"


        self.title_label = tk.Label(root, text="Detector de Temperaturas", font=("Helvetica", 16), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.label = tk.Label(root, text="Selecciona un archivo de texto:", font=("Helvetica", 12), bg="#f0f0f0", fg="#555")
        self.label.pack(pady=5)

        self.browse_button = tk.Button(root, text="Buscar archivo", font=("Helvetica", 12), command=self.browse_file, bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5)
        self.browse_button.pack(pady=10)

        self.process_button = tk.Button(root, text="Procesar", font=("Helvetica", 12), command=self.process_file, bg="#2196F3", fg="white", relief="flat", padx=10, pady=5)
        self.process_button.pack(pady=10)

     
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

     
        self.result_text = tk.Text(root, height=10, width=50, state="disabled", font=("Courier", 10), bg="#e8e8e8", fg="#333")
        self.result_text.pack(pady=10)

    def browse_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file:
            self.label.config(text=self.input_file)

    def process_file(self):
        if not self.input_file:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo.")
            return

        self.progress.start(10)  
        self.root.after(100, self.run_automata)  

    def run_automata(self):
        text = read_text_file(self.input_file)
        automata = AdjustedTemperatureAutomata()
        valid_temperatures = automata.run(text)

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        
        if valid_temperatures:
            self.result_text.insert(tk.END, "Temperaturas válidas detectadas:\n")
            for temp, line_num in valid_temperatures:
                self.result_text.insert(tk.END, f"{temp} (Línea {line_num})\n")
            escribir_temperaturas_csv(valid_temperatures, self.output_file)
            messagebox.showinfo("Éxito", f"Se encontraron {len(valid_temperatures)} temperaturas válidas. Los resultados se guardaron en {self.output_file}.")
        else:
            self.result_text.insert(tk.END, "No se encontraron temperaturas válidas.\n")

        self.result_text.config(state="disabled")
        self.progress.stop()  

if __name__ == "__main__":
    root = tk.Tk()
    gui = TemperatureGUI(root)
    root.mainloop()
