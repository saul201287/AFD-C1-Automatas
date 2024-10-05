import unittest
import os
from io import StringIO
from automata import AdjustedTemperatureAutomata, escribir_temperaturas_csv


class TestAdjustedTemperatureAutomata(unittest.TestCase):
    
    def setUp(self):
        self.automata = AdjustedTemperatureAutomata()
    
    def test_single_temperature_Celsius(self):
        text = "La temperatura es 25°C."
        expected = [('25°C', 1)]  
        result = self.automata.run(text)
        self.assertEqual(result, expected)
    
    def test_single_temperature_Fahrenheit(self):
        text = "El clima es de 75.5°F hoy."
        expected = [('75.5°F', 1)]  
        result = self.automata.run(text)
        self.assertEqual(result, expected)
    
    def test_single_temperature_Kelvin(self):
        text = "El cero absoluto es -273.15K."
        expected = [('-273.15K', 1)]  
        result = self.automata.run(text)
        self.assertEqual(result, expected)
    
    def test_multiple_temperatures(self):
        text = "Las temperaturas fueron 30°C, 298 K y 100°F."
        expected = [('30°C', 1), ('298 K', 1), ('100°F', 1)] 
        result = self.automata.run(text)
        self.assertEqual(result, expected)
    
    def test_invalid_temperature(self):
        text = "La medición errónea fue 20°celci."
        expected = []  
        result = self.automata.run(text)
        self.assertEqual(result, expected)
    
    def test_csv_output(self):
        data = [('25°C', 1), ('75.5°F', 2)]
        output_csv = 'output_test.csv'
        escribir_temperaturas_csv(data, output_csv)
        
        with open(output_csv, 'r', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()
            self.assertEqual(lines[0].strip(), "Temperatura válida,Linea")
            self.assertEqual(lines[1].strip(), "25°C,1")
            self.assertEqual(lines[2].strip(), "75.5°F,2")
        
        os.remove(output_csv)
    

if __name__ == '__main__':
    unittest.main()
