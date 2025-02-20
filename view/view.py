import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.turingMachine import TuringMachine

def main():
    """Flujo completo para que el usuario interactúe con la Maquina de Turing."""
    print("Bienvenido a la Maquina de Turing de Fibonacci")
    
    # Solicitar al usuario un número decimal
    while True:
        try:
            decimal_input = int(input("Ingrese un numero entero para calcular su Fibonacci: "))
            if decimal_input < 0:
                print("Por favor, ingrese un numero positivo.")
                continue
            break
        except ValueError:
            print("Entrada no valida. Por favor, ingrese un numero entero.")
    
    # Convertir de decimal a binario
    machine = TuringMachine("../assets/fibonacci_json.json")
    binary_input = machine.decimal_to_binary(decimal_input)
    print(f"Numero en binario: {binary_input}")
    
    # Ejecutar la Máquina de Turing
    machine.set_input(binary_input)
    machine.run_with_timer()
    
    # Obtener el resultado en binario
    binary_output = machine.get_last_value()
    print(f"Resultado en binario: {binary_output}")
    
    # Convertir de binario a decimal
    decimal_output = machine.binary_to_decimal(binary_output)
    print(f"El Fibonacci de {decimal_input} es: {decimal_output}")
    
if __name__ == "__main__":
    main()
