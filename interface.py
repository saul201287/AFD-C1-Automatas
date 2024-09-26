import tkinter as tk
from tkinter import filedialog, messagebox
from automata import AdjustedTemperatureAutomata, read_text_file, escribir_temperaturas_csv

class TemperatureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Temperaturas")

        self.input_file = ""
        self.output_file = "output.csv"

        self.label = tk.Label(root, text="Selecciona un archivo de texto:")
        self.label.pack()

        self.browse_button = tk.Button(root, text="Buscar archivo", command=self.browse_file)
        self.browse_button.pack()

        self.process_button = tk.Button(root, text="Procesar", command=self.process_file)
        self.process_button.pack()

        self.result_text = tk.Text(root, height=15, width=50)
        self.result_text.pack()

    def browse_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file:
            self.label.config(text=self.input_file)

    def process_file(self):
        if not self.input_file:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo.")
            return

        text = read_text_file(self.input_file)
        automata = AdjustedTemperatureAutomata()
        valid_temperatures = automata.run(text)
        self.result_text.delete(1.0, tk.END)
        
        if valid_temperatures:
            self.result_text.insert(tk.END, "Temperaturas válidas detectadas:\n")
            for temp, line_num in valid_temperatures:
                self.result_text.insert(tk.END, f"{temp} (Línea {line_num})\n")
            escribir_temperaturas_csv(valid_temperatures, self.output_file)
            messagebox.showinfo("Éxito", f"Se encontraron {len(valid_temperatures)} temperaturas válidas. Los resultados se guardaron en {self.output_file}.")
        else:
            self.result_text.insert(tk.END, "No se encontraron temperaturas válidas.\n")

if __name__ == "__main__":
    root = tk.Tk()
    gui = TemperatureGUI(root)
    root.mainloop()
