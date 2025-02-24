import json
import time

class TuringMachine:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
        
        self.states = set(config["Q"])
        self.input_symbols = set(config["Σ"])
        self.blank_symbol = config["␣"]
        self.initial_state = config["q0"]
        self.accept_states = set(config["F"])
        self.transitions = config["p"]
        self.tape = [self.blank_symbol] * 1000  # Se puede ampliar dinámicamente
        self.head_position = 500
        self.current_state = self.initial_state
        self.term_count = 2  # Iniciamos con los dos primeros términos de Fibonacci
        self.target_terms = 0

    def ensure_tape_capacity(self, new_position):
        """Expande la cinta si el cabezal intenta moverse fuera de los límites."""
        if new_position >= len(self.tape):
            self.tape.extend([self.blank_symbol] * (new_position - len(self.tape) + 100))
        elif new_position < 0:
            # Expande la cinta hacia la izquierda
            extension = [self.blank_symbol] * 100
            self.tape = extension + self.tape
            self.head_position += 100  # Ajustar la posición del cabezal

    def set_input(self, input_bin):
        """Carga el número binario de entrada en la cinta y coloca los primeros términos de Fibonacci.
        Maneja los casos base: 0 -> 0, 1 -> 1, 2 -> 1.
        """
        self.target_terms = int(input_bin, 2)  # Convertir binario a decimal
         # Reinicio explícito de los atributos críticos
        self.current_state = self.initial_state
        self.term_count = 2
        self.tape = [self.blank_symbol] * 1000
        self.head_position = 500

        # Aplicar límite de 500 términos
        if self.target_terms > 500:
            print(f"Limite de 500 alcanzado. Se calculara Fibonacci de 500 en lugar de {self.target_terms}.")
            self.target_terms = 500  

        # Casos base
        if self.target_terms == 0:
            self.tape[self.head_position] = "0"
            print("Caso base detectado: 0")
            return
        elif self.target_terms == 1:
            self.tape[self.head_position] = "1"
            print("Caso base detectado: 1")
            return
        elif self.target_terms == 2:
            self.tape[self.head_position] = "1"
            print("Caso base detectado: 2 (10 en binario) → Devuelve 1")
            return

        # Inicializar la cinta con los primeros términos de Fibonacci
        self.tape = [self.blank_symbol] * 1000
        self.head_position = 500
        self.tape[self.head_position:self.head_position+3] = list("1#1")
        self.head_position += 3
        print("Estado inicial de la cinta:", self.get_output())

    def print_tape(self):
        """Muestra el estado actual de la cinta para depuración."""
        tape_str = "".join(self.tape).strip(self.blank_symbol)
        print(f"Cinta actual: {tape_str}  (Estado: {self.current_state})")

    def run(self):
        """Ejecuta la Máquina de Turing hasta que se generen suficientes términos de Fibonacci."""
        if self.target_terms in [0, 1, 2]:  
            return  

        while self.term_count < self.target_terms:
            if self.term_count >= 500:
                print("Limite de 500 terminos alcanzado. Se detiene la ejecucion.")
                break

            num1, num2 = self.find_last_two_numbers()
            new_fib = self.binary_addition(num1, num2)

            # Encontrar el último `#` en la cinta y posicionar el cabezal después
            try:
                self.head_position = "".join(self.tape).rfind("#") + 1
            except ValueError:
                self.head_position = len(self.tape) - self.tape[::-1].index("#")  # Buscar desde el final

            # Asegurar que la cinta tenga suficiente espacio
            self.ensure_tape_capacity(self.head_position + len(new_fib) + 1)

            # Escribir el nuevo número
            self.tape[self.head_position:self.head_position+len(new_fib)] = list(new_fib)
            self.head_position += len(new_fib)

            # Agregar el separador y verificar capacidad
            self.ensure_tape_capacity(self.head_position)
            self.tape[self.head_position] = "#"
            self.head_position += 1

            self.term_count += 1  # Incrementamos el contador de términos generados
            self.print_tape()

        # Remover el último `#` y reemplazarlo con `_`
        last_hash_index = "".join(self.tape).rfind("#")
        if last_hash_index != -1:
            self.tape[last_hash_index] = "_"

        self.current_state = "q_accept"

    def find_last_two_numbers(self):
        """Encuentra los dos últimos números en la cinta para sumarlos."""
        tape_str = "".join(self.tape).strip(self.blank_symbol)
        numbers = [num for num in tape_str.split("#") if num.isdigit() and len(num) > 0]

        if len(numbers) < 2:
            return "1", "1"
        return numbers[-2], numbers[-1]

    def binary_addition(self, num1, num2):
        """Realiza la suma binaria de dos números representados como cadenas."""
        try:
            result = bin(int(num1, 2) + int(num2, 2))[2:]  # Suma binaria
            return result
        except ValueError:
            return "0"

    def get_output(self):
        """Devuelve el contenido de la cinta como la secuencia de Fibonacci en binario."""
        return "".join(self.tape).strip(self.blank_symbol)

    def get_last_value(self):
        """Devuelve el último número Fibonacci en la cinta."""
        tape_str = "".join(self.tape).strip(self.blank_symbol)
        numbers = [num for num in tape_str.split("#") if num.isdigit() and len(num) > 0]
        return numbers[-1] if numbers else "0"
    
    def decimal_to_binary(self, decimal):
        """Convierte un número decimal en binario."""
        if decimal < 0:
            return "-" + TuringMachine.decimal_to_binary(-decimal)
        if decimal == 0:
            return "0"
        result = ""
        while decimal > 0:
            result = str(decimal % 2) + result
            decimal = decimal // 2
        return result
    
    def binary_to_decimal(self, binary):
        """Convierte un número binario en decimal."""   
        negative = False
        if binary[0] == "-":
            negative = True
            binary = binary[1:]
        decimal = 0
        for digit in binary:
            if digit not in "01":
                raise ValueError("No es un número binario válido")
            decimal = decimal * 2 + int(digit)
        return -decimal if negative else decimal
    
    def run_with_timer(self):
        """Ejecuta la máquina y mide el tiempo de ejecución."""
        start_time = time.time()
        self.run()
        elapsed_time = time.time() - start_time
        print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
        return elapsed_time