"""Creational - Factory Method: refactor the payment system.

Statement: https://courses.dallard.tech/sys_design/creational_pattern/
Run: python3 factory_payment.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# 1. The interface: every processor promises validate() and process()
class PaymentProcessor(ABC):
    method_name: str = ""

    @abstractmethod
    def validate(self, details: dict) -> bool: ...

    @abstractmethod
    def compute_fee(self, amount: float) -> float: ...

    @property
    @abstractmethod
    def error_message(self) -> str: ...

    def process(self, amount: float, details: dict) -> dict:
        # Shared workflow written once; the specifics come from the subclass
        if not self.validate(details):
            return {"success": False, "error": self.error_message}
        fee = round(self.compute_fee(amount), 2)
        return {"success": True, "method": self.method_name,
                "amount": round(amount + fee, 2), "fee": fee}


# 2. Concrete implementations - each one owns its own rules and fee
class CreditCardProcessor(PaymentProcessor):
    method_name = "credit_card"
    _error = "Invalid card details"

    def validate(self, details: dict) -> bool:
        card, cvv = details.get("card_number"), details.get("cvv")
        if not card or len(card) != 16:
            self._error = "Invalid card number"
            return False
        if not cvv or len(cvv) != 3:
            self._error = "Invalid CVV"
            return False
        return True

    def compute_fee(self, amount: float) -> float:
        return amount * 0.029          # 2.9%

    @property
    def error_message(self) -> str:
        return self._error


class BankTransferProcessor(PaymentProcessor):
    method_name = "bank_transfer"

    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        return bool(iban) and len(iban) >= 15

    def compute_fee(self, amount: float) -> float:
        return 1.50                    # flat fee

    @property
    def error_message(self) -> str:
        return "Invalid IBAN"


class PayPalProcessor(PaymentProcessor):
    method_name = "paypal"

    def validate(self, details: dict) -> bool:
        email = details.get("email")
        return bool(email) and "@" in email

    def compute_fee(self, amount: float) -> float:
        return amount * 0.034 + 0.30   # 3.4% + 0.30€

    @property
    def error_message(self) -> str:
        return "Invalid PayPal email"


# 3. The factory: a dictionary maps names to classes, no if/elif chain.
#    Adding Apple Pay = write one class + one register() call (Open/Closed).
class PaymentFactory:
    _processors: dict[str, type[PaymentProcessor]] = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    @classmethod
    def register(cls, name: str, processor: type[PaymentProcessor]) -> None:
        cls._processors[name] = processor

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        try:
            return self._processors[payment_type]()
        except KeyError:
            raise ValueError(f"Unknown payment type: {payment_type}") from None


if __name__ == "__main__":
    factory = PaymentFactory()

    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    print(factory.get_processor("bank_transfer").process(
        100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))
    print(factory.get_processor("paypal").process(100.0, {"email": "me@shop.com"}))
    print(factory.get_processor("paypal").process(100.0, {"email": "wrong"}))

    # Extending without touching existing code
    class ApplePayProcessor(PaymentProcessor):
        method_name = "apple_pay"

        def validate(self, details: dict) -> bool:
            return "token" in details

        def compute_fee(self, amount: float) -> float:
            return amount * 0.015

        @property
        def error_message(self) -> str:
            return "Missing Apple Pay token"

    PaymentFactory.register("apple_pay", ApplePayProcessor)
    print(factory.get_processor("apple_pay").process(100.0, {"token": "tok_123"}))
