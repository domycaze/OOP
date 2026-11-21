"""Tests for the OOP exercises. Run: python3 -m pytest (or python3 test_oop.py)."""
import unittest

from inheritance import BankAccount, Bicycle, Car, Employee, SavingsAccount, Student, Vehicle
from operator_overloading import Circle, Complex, Matrix, Person, Point2D, Vector


class TestOperatorOverloading(unittest.TestCase):
    def test_complex(self):
        self.assertEqual(Complex(3, 2) + Complex(1, 7), Complex(4, 9))
        self.assertEqual(Complex(3, 2) - Complex(1, 7), Complex(2, -5))

    def test_person_gt(self):
        self.assertTrue(Person("A", 30, "F") > Person("B", 25, "M"))
        self.assertFalse(Person("A", 20, "F") > Person("B", 25, "M"))

    def test_vector_dot(self):
        self.assertEqual(Vector(1, 2, 3) * Vector(4, 5, 6), 32)

    def test_circle(self):
        a, b = Circle(2), Circle(5)
        self.assertTrue(a < b and a <= b and b > a and b >= a and a != b)
        self.assertTrue(a == Circle(2))

    def test_point(self):
        self.assertTrue(Point2D(3, 4) == Point2D(5, 0))
        self.assertTrue(Point2D(1, 1) < Point2D(3, 4))
        self.assertTrue(Point2D(3, 4) >= Point2D(0, 5))

    def test_matrix(self):
        product = Matrix([[1, 2], [3, 4]]) * Matrix([[5, 6], [7, 8]])
        self.assertEqual(product, Matrix([[19, 22], [43, 50]]))
        with self.assertRaises(ValueError):
            Matrix([[1, 2]]) * Matrix([[1, 2]])


class TestInheritance(unittest.TestCase):
    def test_vehicles(self):
        self.assertEqual(Vehicle().drive(), "Driving a vehicle")
        self.assertEqual(Car().drive(), "Driving a car")
        self.assertEqual(Bicycle().drive(), "Riding a bicycle")

    def test_people(self):
        self.assertIn("Data", Student("L", 19, "Cergy", "Data").introduce())
        self.assertIn("Airbus", Employee("P", 35, "Lyon", "Airbus").introduce())

    def test_bank(self):
        src, dst = BankAccount("1", 100), SavingsAccount("2", 0, 0.1)
        self.assertTrue(src.transfer(dst, 60))
        self.assertFalse(src.transfer(dst, 60))
        self.assertEqual((src.balance, dst.check_balance()), (40, 60))
        dst.add_interest()
        self.assertAlmostEqual(dst.check_balance(), 66)


if __name__ == "__main__":
    unittest.main()
