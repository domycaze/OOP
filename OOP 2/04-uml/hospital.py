"""Implementation of the Task 3 Hospital Management design (UML exo 1).

Run: python3 hospital.py
"""
from __future__ import annotations

import hashlib
import itertools
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

_ids = itertools.count(1)


def new_id(prefix: str) -> str:
    return f"{prefix}-{next(_ids):03d}"


# ----------------------------------------------------------------- users ---
class User(ABC):
    def __init__(self, name: str, password: str) -> None:
        self.user_id = new_id(type(self).__name__[:3].upper())
        self.name = name
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.logged_in = False

    def login(self, password: str) -> bool:
        self.logged_in = hashlib.sha256(password.encode()).hexdigest() == self._password_hash
        return self.logged_in

    def logout(self) -> None:
        self.logged_in = False


class Patient(User):
    def __init__(self, name: str, password: str) -> None:
        super().__init__(name, password)
        self.problems: list[HealthProblem] = []

    def post_problem(self, description: str) -> HealthProblem:
        problem = HealthProblem(self, description)
        self.problems.append(problem)
        return problem

    def past_prescriptions(self) -> list[Prescription]:
        return [p.prescription for p in self.problems if p.prescription]

    def pay(self, prescription: Prescription, method: PaymentMethod) -> Payment:
        payment = Payment(prescription, method)
        payment.execute()
        return payment


class Doctor(User):
    def __init__(self, name: str, password: str, speciality: str) -> None:
        super().__init__(name, password)
        self.speciality = speciality
        self.balance = 0.0

    def write_prescription(self, problem: HealthProblem, content: str, fee: float,
                           based_on: Prescription | None = None) -> Prescription:
        if problem.doctor is not self:
            raise PermissionError("this problem is not assigned to this doctor")
        problem.prescription = Prescription(self, problem, content, fee, based_on)
        return problem.prescription


class Organizer(User):
    def register_member(self, role: str, name: str, password: str, **extra) -> User:
        roles = {"patient": Patient, "doctor": Doctor}
        return roles[role](name, password, **extra)

    def assign(self, problem: HealthProblem, doctor: Doctor) -> None:
        problem.doctor = doctor
        problem.set_status(ProblemStatus.IN_REVIEW)

    def deliver(self, prescription: Prescription) -> None:
        prescription.problem.set_status(ProblemStatus.RESOLVED)

    def forward_payment(self, payment: Payment) -> None:
        if payment.status != "PAID":
            raise ValueError("only a PAID payment can be forwarded")
        payment.prescription.doctor.balance += payment.amount
        payment.status = "FORWARDED"


# ---------------------------------------------------------- domain model ---
class ProblemStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in-review"
    RESOLVED = "resolved"


class HealthProblem:
    def __init__(self, patient: Patient, description: str) -> None:
        self.problem_id = new_id("PB")
        self.patient = patient
        self.description = description
        self.status = ProblemStatus.PENDING
        self.created_at = self.updated_at = datetime.now()
        self.doctor: Doctor | None = None
        self.prescription: Prescription | None = None

    def set_status(self, status: ProblemStatus) -> None:
        self.status = status
        self.updated_at = datetime.now()


class Prescription:
    def __init__(self, doctor: Doctor, problem: HealthProblem, content: str,
                 fee: float, based_on: Prescription | None = None) -> None:
        self.prescription_id = new_id("RX")
        self.doctor = doctor
        self.problem = problem
        self.content = content
        self.fee = fee
        self.issued_at = datetime.now()
        self.based_on = based_on          # reference to a past prescription (renewal)
        self.payment: Payment | None = None


# ------------------------------------------------ payment strategy pattern ---
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool: ...


class CashMethod(PaymentMethod):
    def pay(self, amount: float) -> bool:
        print(f"  cash received: {amount:.2f}€")
        return True


class CheckMethod(PaymentMethod):
    def __init__(self, check_number: str) -> None:
        self.check_number = check_number

    def pay(self, amount: float) -> bool:
        print(f"  check #{self.check_number} deposited: {amount:.2f}€")
        return True


class CreditCardMethod(PaymentMethod):
    def __init__(self, card_number: str) -> None:
        self.card_last4 = card_number[-4:]     # never store the full number

    def pay(self, amount: float) -> bool:
        print(f"  card ****{self.card_last4} charged: {amount:.2f}€")
        return True


class Payment:
    def __init__(self, prescription: Prescription, method: PaymentMethod) -> None:
        if prescription.payment is not None:
            raise ValueError("this prescription is already paid")
        self.payment_id = new_id("PAY")
        self.prescription = prescription
        self.method = method
        self.amount = prescription.fee
        self.status = "PENDING"
        self.paid_at: datetime | None = None

    def execute(self) -> bool:
        if self.method.pay(self.amount):
            self.status = "PAID"
            self.paid_at = datetime.now()
            self.prescription.payment = self
            return True
        self.status = "FAILED"
        return False


if __name__ == "__main__":
    admin = Organizer("Admin", "admin-pass")
    alice = admin.register_member("patient", "Alice", "alice-pass")
    house = admin.register_member("doctor", "Dr House", "doc-pass", speciality="General")

    assert alice.login("alice-pass")
    problem = alice.post_problem("Headache for 3 days")
    print("1. posted:", problem.problem_id, problem.status.value)

    admin.assign(problem, house)
    print("2. assigned to", house.name, "->", problem.status.value)

    rx = house.write_prescription(problem, "Rest + paracetamol 1g", fee=30.0)
    admin.deliver(rx)
    print("3. prescription", rx.prescription_id, "->", problem.status.value)

    print("4. payment:")
    payment = alice.pay(rx, CreditCardMethod("4970101234567890"))
    admin.forward_payment(payment)
    print("5.", payment.status, "| doctor balance:", house.balance)

    renewal_problem = alice.post_problem("Headache again")
    admin.assign(renewal_problem, house)
    renewal = house.write_prescription(renewal_problem, "Same treatment", 15.0, based_on=rx)
    print("6. renewal based on", renewal.based_on.prescription_id,
          "| past prescriptions:", [p.prescription_id for p in alice.past_prescriptions()])
