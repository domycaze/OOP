"""OOP Problems - Operator Overloading (slide 67).

Statement: https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc
Run: python3 operator_overloading.py
"""
from __future__ import annotations

import math
from functools import total_ordering


# ---------------------------------------------------------------------------
# Problem 1 - Complex numbers: overload + and -
# ---------------------------------------------------------------------------
class Complex:
    def __init__(self, real: float, imag: float) -> None:
        self.real = real
        self.imag = imag

    def __add__(self, other: Complex) -> Complex:
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: Complex) -> Complex:
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Complex):
            return NotImplemented
        return self.real == other.real and self.imag == other.imag

    def __repr__(self) -> str:
        sign = "+" if self.imag >= 0 else "-"
        return f"({self.real} {sign} {abs(self.imag)}i)"


# ---------------------------------------------------------------------------
# Problem 2 - Person compared by age with >
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name: str, age: int, gender: str) -> None:
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other: Person) -> bool:
        return self.age > other.age

    def __repr__(self) -> str:
        return f"Person({self.name!r}, {self.age}, {self.gender!r})"


# ---------------------------------------------------------------------------
# Problem 4 - Vector: * returns the dot product
# (the statement has no Problem 3)
# ---------------------------------------------------------------------------
class Vector:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"


# ---------------------------------------------------------------------------
# Problem 5 - Circle: all six comparison operators, based on radius
# ---------------------------------------------------------------------------
class Circle:
    def __init__(self, radius: float) -> None:
        if radius < 0:
            raise ValueError("radius cannot be negative")
        self.radius = radius

    def __lt__(self, other: Circle) -> bool:
        return self.radius < other.radius

    def __le__(self, other: Circle) -> bool:
        return self.radius <= other.radius

    def __gt__(self, other: Circle) -> bool:
        return self.radius > other.radius

    def __ge__(self, other: Circle) -> bool:
        return self.radius >= other.radius

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius != other.radius

    def __repr__(self) -> str:
        return f"Circle(r={self.radius})"


# ---------------------------------------------------------------------------
# Problem 6 - 2D point compared by Euclidean distance from the origin
# @total_ordering builds <=, >, >= from __eq__ and __lt__
# ---------------------------------------------------------------------------
@total_ordering
class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_from_origin(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return math.isclose(self.distance_from_origin(), other.distance_from_origin())

    def __lt__(self, other: Point2D) -> bool:
        return (not self == other) and self.distance_from_origin() < other.distance_from_origin()

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"


# ---------------------------------------------------------------------------
# Problem 7 - Matrix multiplication with *
# ---------------------------------------------------------------------------
class Matrix:
    def __init__(self, rows: list[list[float]]) -> None:
        if not rows or any(len(r) != len(rows[0]) for r in rows):
            raise ValueError("all rows must have the same, non-zero length")
        self.rows = rows
        self.n_rows = len(rows)
        self.n_cols = len(rows[0])

    def __mul__(self, other: Matrix) -> Matrix:
        if self.n_cols != other.n_rows:
            raise ValueError(
                f"cannot multiply {self.n_rows}x{self.n_cols} by {other.n_rows}x{other.n_cols}"
            )
        result = [
            [
                sum(self.rows[i][k] * other.rows[k][j] for k in range(self.n_cols))
                for j in range(other.n_cols)
            ]
            for i in range(self.n_rows)
        ]
        return Matrix(result)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __repr__(self) -> str:
        return "Matrix(" + ", ".join(str(r) for r in self.rows) + ")"


if __name__ == "__main__":
    print("Problem 1:", Complex(3, 2) + Complex(1, 7), Complex(3, 2) - Complex(1, 7))

    alice, bob = Person("Alice", 30, "F"), Person("Bob", 25, "M")
    print("Problem 2: alice > bob ->", alice > bob, "| bob > alice ->", bob > alice)

    print("Problem 4:", Vector(1, 2, 3) * Vector(4, 5, 6))  # 32

    small, big = Circle(2), Circle(5)
    print("Problem 5:", small < big, small <= big, small > big,
          small >= big, small == Circle(2), small != big)

    p, q = Point2D(3, 4), Point2D(1, 1)
    print("Problem 6:", p > q, p == Point2D(5, 0), q <= p)

    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    print("Problem 7:", a * b)  # [[19, 22], [43, 50]]
