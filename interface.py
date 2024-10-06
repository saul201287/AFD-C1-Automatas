import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from automata import AdjustedTemperatureAutomata, read_text_file, escribir_temperaturas_csv
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TemperatureGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Detector de Temperaturas")
        self.geometry("900x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.input_file = ""
        self.output_file = "output.csv"

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="Detector de Temperaturas", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=1, sticky="w", padx=20)

        file_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        file_frame.grid(row=1, column=0, padx=50, sticky="ew")
        file_frame.grid_columnconfigure(1, weight=1)

        file_button = ctk.CTkButton(file_frame, text="Seleccionar archivo en formato .txt", command=self.browse_file)
        file_button.grid(row=0, column=0, padx=(0, 10))

        self.file_label = ctk.CTkLabel(file_frame, text="Ningún archivo seleccionado", font=ctk.CTkFont(size=14))
        self.file_label.grid(row=0, column=1, sticky="w")

        process_button = ctk.CTkButton(file_frame, text="Procesar", command=self.process_file)
        process_button.grid(row=0, column=2, padx=(10, 0))

        self.progress = ctk.CTkProgressBar(main_frame)
        self.progress.grid(row=2, column=0, pady=30, padx=50, sticky="ew")
        self.progress.set(0)

        results_frame = ctk.CTkFrame(main_frame)
        results_frame.grid(row=3, column=0, pady=10, padx=30, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)

        results_label = ctk.CTkLabel(results_frame, text="Resultados", font=ctk.CTkFont(size=18, weight="bold"))
        results_label.grid(row=0, column=0, pady=(10, 5), padx=20, sticky="w")

        self.result_tree = ttk.Treeview(results_frame, columns=("temperatura", "linea", "columna"), show="headings")
        self.result_tree.heading("temperatura", text="Temperatura")
        self.result_tree.heading("linea", text="Línea")
        self.result_tree.heading("columna", text="Columna")  
        self.result_tree.column("temperatura", width=150)
        self.result_tree.column("linea", width=100)
        self.result_tree.column("columna", width=100)  
        self.result_tree.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.result_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.result_tree.configure(yscrollcommand=scrollbar.set)

    def browse_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.input_file:
            self.file_label.configure(text=os.path.basename(self.input_file))

    def process_file(self):
        if not self.input_file:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo.")
            return

        self.progress.start()
        self.after(100, self.run_automata)

    def run_automata(self):
        text = read_text_file(self.input_file)
        automata = AdjustedTemperatureAutomata()
        valid_temperatures = automata.run(text)

        self.result_tree.delete(*self.result_tree.get_children())
    
        if valid_temperatures:
            for temp, line_num, column in valid_temperatures:  
                self.result_tree.insert("", "end", values=(temp, line_num, column))  
            escribir_temperaturas_csv(valid_temperatures, self.output_file)
            messagebox.showinfo("Éxito", f"Se encontraron {len(valid_temperatures)} temperaturas válidas. Los resultados se guardaron en {self.output_file}.")
        else:
            messagebox.showinfo("Información", "No se encontraron temperaturas válidas.")

        self.progress.stop()
        self.progress.set(0)

if __name__ == "__main__":
    app = TemperatureGUI()
    app.mainloop()
