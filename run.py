import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from controller.turingMachine import TuringMachine

machine = TuringMachine("./assets/fibonacci_json.json")

inputs = []
times = []

with open('fibonacci_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Input Decimal', 'Input Binario', 'Resultado Binario', 'Resultado Decimal', 'Tiempo Ejecucion (ms)'])

    for input_decimal in range(1, 501):
        binary_input = machine.decimal_to_binary(input_decimal)
        machine.set_input(binary_input)

        start_time = time.time()
        machine.run()
        execution_time = (time.time() - start_time) * 1000  # Convertido a milisegundos
        execution_time = max(execution_time, 0.0001)  

        binary_output = machine.get_last_value()
        decimal_output = machine.binary_to_decimal(binary_output)

        writer.writerow([input_decimal, binary_input, binary_output, decimal_output, execution_time])

        inputs.append(input_decimal)
        times.append(execution_time)