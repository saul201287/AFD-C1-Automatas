from automata import AdjustedTemperatureAutomata  

def debug_automata(text):
    automata = AdjustedTemperatureAutomata()
    print("Procesando texto carácter por carácter:")
    for i, char in enumerate(text):
        try:
            result = automata.process_char(char)
            print(f"Caracter {i}: '{char}' - Estado: {automata.state} - Temp: {automata.temp_value} - Unidad: {automata.unit}")
            if result:
                print(f"Temperatura detectada: {automata.current_temp} ({automata.temp_value} {automata.unit})")
                automata.reset()
            else:
                if automata.state == 'q0':
                    print(f"Carácter no reconocido en estado inicial: '{char}'")
        except Exception as e:
            print(f"Error procesando el carácter {i}: '{char}' - {str(e)}")

    if automata.state in ['q6', 'q7', 'q8'] and automata.temp_value and automata.unit:
        print(f"Temperatura final detectada: {automata.temp_value} {automata.unit}")

    print("\nEjecutando el método run:")
    valid_temperatures = automata.run(text)
    print(f"Temperaturas válidas detectadas: {valid_temperatures}")
    print(f"Número de temperaturas detectadas: {len(valid_temperatures)}")

test_text = ''' 300 Kelvin
 +0 K
 -10 Kelvin
 1.0 K
 100 K'''

debug_automata(test_text)

