from unittest import TestCase
from dependency.main import Dependency

class DependencyTest(TestCase):
    def test_input_1(self):
        with open("tests/test_input.txt", "r") as file:
            data = file.read()
        lines = data.split("\n")
        response = Dependency(lines)

        with open("tests/test_output.txt", "r") as file:
            _data = file.read()
        