import unittest
import sys
import os

# Ajouter le répertoire parent au chemin de recherche de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.example import add_numbers


class TestExample(unittest.TestCase):
    def test_add_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)


if __name__ == '__main__':
    unittest.main()