"""OOP Problems - Inheritance (slide 67).

Statement: https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc
Run: python3 inheritance.py
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Problem 1 - Vehicle / Car / Bicycle
# ---------------------------------------------------------------------------
class Vehicle:
    def drive(self) -> str:
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self) -> str:
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self) -> str:
        return "Riding a bicycle"


# ---------------------------------------------------------------------------
# Problem 2 - Person / Student / Employee
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name: str, age: int, address: str) -> None:
        self.name = name
        self.age = age
        self.address = address

    def introduce(self) -> str:
        return f"Hi, I'm {self.name}, I'm {self.age} and I live in {self.address}."


class Student(Person):
    def __init__(self, name: str, age: int, address: str, field_of_study: str) -> None:
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self) -> str:
        return super().introduce() + f" I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name: str, age: int, address: str, company: str) -> None:
        super().__init__(name, age, address)
        self.company = company

    def introduce(self) -> str:
        return super().introduce() + f" I work at {self.company}."


# ---------------------------------------------------------------------------
# Problem 3 - BankAccount / SavingsAccount
# ---------------------------------------------------------------------------
class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0) -> None:
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("withdraw amount must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination: BankAccount, amount: float) -> bool:
        """Move money to another account. False if the balance is too low."""
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.account_number}, balance={self.balance:.2f})"


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, balance: float = 0.0,
                 interest_rate: float = 0.02) -> None:
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self) -> float:
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self) -> float:
        return self.balance


if __name__ == "__main__":
    for v in (Vehicle(), Car(), Bicycle()):
        print("Problem 1:", v.drive())

    for p in (Person("Domitille", 19, "Paris"),
              Student("Lina", 19, "Cergy", "AI & Data Science"),
              Employee("Paul", 35, "Lyon", "Airbus")):
        print("Problem 2:", p.introduce())

    current = BankAccount("FR-001", 500)
    savings = SavingsAccount("FR-002", 1000, interest_rate=0.03)
    print("Problem 3: transfer 200 ->", current.transfer(savings, 200), current, savings)
    print("Problem 3: transfer 1000 ->", current.transfer(savings, 1000), "(insufficient)")
    print("Problem 3: interest added ->", savings.add_interest(),
          "| balance:", savings.check_balance())
