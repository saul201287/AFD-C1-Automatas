import csv

class AdjustedTemperatureAutomata:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.state = 'q0'
        self.temp_value = ""
        self.unit = ""
        self.current_temp = ""

    def process_char(self, char, next_char=None):
        if self.state == 'q0':
            if char == ' ':
                self.state = 'start'  
            else:
                pass

        if self.state == 'start':
            if char in "+-":
                self.unit += char
                self.state = 'q1'
            elif char.isdigit():
                self.unit += char
                self.state = 'q2'
            elif char == ' ':
                pass  
            else:
                self.reset()

        elif self.state == 'q1':
            if char.isdigit():
                self.unit += char
                self.state = 'q2'
            else:
                self.reset()

        elif self.state == 'q2':
            if char.isdigit():
                self.unit += char
            elif char == '.':
                self.unit += char
                self.state = 'q3'
            elif char == ' ':
                self.unit += char
                self.state = 'q4'
            elif char == '°':
                self.unit += '°'
                self.state = 'q7'  
            elif char == 'K':  
                self.unit += char  
                self.state = 'q5'
            else:
                self.reset()

        elif self.state == 'q3':
            if char.isdigit():
                self.unit += char
            elif char == ' ':
                self.unit += char
                self.state = 'q4'
            elif char == '°':
                self.unit += '°'
                self.state = 'q7' 
            elif char == 'K': 
                self.unit += char  
                self.state = 'q5'
            else:
                self.reset()

        elif self.state == 'q4':
            if char in 'Cc':
                self.unit += char  
                self.state = 'q10'
            elif char == 'K':
                self.unit += char  
                self.state = 'q5'
            elif char == 'k':
                self.unit += char  
                self.state = 'q6'
            elif char in '°':
                self.unit += char  
                self.state = 'q7'
            elif char in 'Ff':
                self.unit += char  
                self.state = 'q8'  
            elif char == ' ':
                pass  
            else:
                self.reset()

        elif self.state == 'q5':
            if char == 'e':
                self.unit += 'e' 
                self.state = 'q9'  
            else:
                self.current_temp = f"{self.unit}".strip()  
                return True  

        elif self.state == 'q6':
            if char == 'e':
                self.unit += char 
                self.state = 'q9'
            else:
                self.reset()

        elif self.state == 'q7':
            if char in 'CF':
                self.unit += char 
                self.state = 'q27'
            else:
                self.reset()

        elif self.state == 'q8':
            if char == 'a':
                self.unit += char
                self.state = 'q11'
            else:
                self.reset()

        elif self.state == 'q9':
            if char == 'l':
                self.unit += char 
                self.state = 'q24'
            else:
                self.reset()
        elif self.state == 'q24':
            if char == 'v':
                self.unit += char
                self.state ='q25'
            else:
                self.reset()  
        elif self.state == 'q25':
            if char == 'i':
                self.unit += char
                self.state ='q26'
            else:
                self.reset()
        elif self.state == 'q26':
            if char == 'n':
                self.unit += char
                self.state ='q27'
            else:
                self.reset()             
        elif self.state == 'q10':
            if char == 'e':
                self.unit += char 
                self.state = 'q19'
            else:
                self.reset()

        elif self.state == 'q19':
            if char == 'l':
                self.unit += char 
                self.state = 'q20'
            else:
                self.reset()

        elif self.state == 'q20':
            if char == 's':
                self.unit += char 
                self.state = 'q21'
            else:
                self.reset()

        elif self.state == 'q21':
            if char == 'i':
                self.unit += char 
                self.state = 'q22'
            else:
                self.reset()

        elif self.state == 'q22':
            if char == 'u':
                self.unit += char 
                self.state = 'q23'
            else:
                self.reset()

        elif self.state == 'q23':
            if char == 's':
                self.unit += char 
                self.state = 'q27'  
            else:
                self.reset()

        elif self.state == 'q11':
            if char == 'h':
                self.unit += char
                self.state = 'q12'  
            else:
                self.reset()

        elif self.state == 'q12':
            if char == 'r':
                self.unit += char 
                self.state = 'q13'  
            else:
                self.reset()

        elif self.state == 'q13':
            if char == 'e':
                self.unit += char 
                self.state = 'q14'  
            else:
                self.reset()

        elif self.state == 'q14':
            if char == 'n':
                self.unit += char 
                self.state = 'q15'  
            else:
                self.reset()

        elif self.state == 'q15':
            if char == 'h':
                self.unit += char
                self.state = 'q16'  
            else:
                self.reset()

        elif self.state == 'q16':
            if char == 'e':
                self.unit += char
                self.state = 'q17'  
            else:
                self.reset()

        elif self.state == 'q17':
            if char == 'i':
                self.unit += char
                self.state = 'q18'  
            else:
                self.reset()

        elif self.state == 'q18':
            if char == 't':
                self.unit += char
                self.state = 'q27'  
            else:
                self.reset()

        elif self.state == 'q27':
            if char in (' ', '.', ','):
                self.state = 'q28'  
            else:
                self.reset()

        if self.state in ['q28', 'q27'] and self.unit:
            self.current_temp = f"{self.unit}".strip()  
            return True

        return False

    def run(self, text):
        valid_temperatures = []
        lines = text.splitlines()
        for line_num, line in enumerate(lines, start=1):
            for i, char in enumerate(line):
                next_char = line[i + 1] if i + 1 < len(line) else None
                if self.process_char(char, next_char):
                    column = i - len(self.unit) + 1
                    valid_temperatures.append((self.current_temp, line_num, column))
                    self.reset()
        return valid_temperatures


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def escribir_temperaturas_csv(data, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Temperatura válida', 'Línea', 'Columna'])
        for temp, line_num, column in data:
            writer.writerow([temp, line_num, column])

# Ejemplo de uso
texto = read_text_file('ruta_del_archivo.txt')
automata = AdjustedTemperatureAutomata()
resultados = automata.run(texto)
escribir_temperaturas_csv(resultados, 'salida.csv')
