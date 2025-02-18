import unittest
from controller.turingMachine import TuringMachine

class TestTuringMachine(unittest.TestCase):
    def setUp(self):
        """Inicializar la máquina de Turing antes de cada prueba."""
        self.machine = TuringMachine("./assets/fibonacci_json.json")

    def test_case_0(self):
        self.machine.set_input('0')
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "0")

    def test_case_1(self):
        self.machine.set_input('1')
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "1")

    def test_case_2(self):
        self.machine.set_input('10')
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "1")

    def test_case_3(self):
        self.machine.set_input('11')  # 3 en binario
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "10")  # Fibonacci(3) = 2

    def test_case_5(self):
        self.machine.set_input('101')  # 5 en binario
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "101")  # Fibonacci(5) = 5

    def test_case_10(self):
        self.machine.set_input('1010')  # 10 en binario
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "110111")  # Fibonacci(10) = 55

    def test_case_15(self):
        self.machine.set_input('1111')  # 15 en binario
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "1001100010")  # Fibonacci(15) = 610

    def test_case_50(self):
        self.machine.set_input('110010')  # 50 en binario
        self.machine.run()
        self.assertEqual(self.machine.get_last_value(), "1011101110001100110011100101100001")  # Fibonacci(50) = 12586269025

if __name__ == '__main__':
    unittest.main()