"""Structural - Decorator: order pricing system.

Statement: https://courses.dallard.tech/sys_design/structural_pattern/
Run: python3 decorator_order.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float: ...

    @abstractmethod
    def get_description(self) -> str: ...


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float) -> None:
        self.base_price = base_price

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base price: {self.base_price:.2f}€"


class OrderDecorator(OrderComponent):
    """Holds the wrapped order and delegates to it by default."""

    def __init__(self, order: OrderComponent) -> None:
        self._order = order

    def get_cost(self) -> float:
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()

    def _base_price(self) -> float:
        # walk down the chain to find the original price (insurance needs it)
        inner = self._order
        while isinstance(inner, OrderDecorator):
            inner = inner._order
        return inner.get_cost()


class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00

    def get_cost(self) -> float:
        return super().get_cost() + self.COST

    def get_description(self) -> str:
        return super().get_description() + f"\nExpress shipping: +{self.COST:.2f}€"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05

    def _insurance(self) -> float:
        return self._base_price() * self.RATE

    def get_cost(self) -> float:
        return super().get_cost() + self._insurance()

    def get_description(self) -> str:
        return super().get_description() + f"\nInsurance (5%): +{self._insurance():.2f}€"


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def get_cost(self) -> float:
        return super().get_cost() + self.COST

    def get_description(self) -> str:
        return super().get_description() + f"\nGift wrap: +{self.COST:.2f}€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float) -> None:
        super().__init__(order)
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        self.percent = percent

    def _discount(self) -> float:
        return super().get_cost() * self.percent / 100

    def get_cost(self) -> float:
        return super().get_cost() - self._discount()

    def get_description(self) -> str:
        return super().get_description() + f"\nDiscount ({self.percent:g}%): -{self._discount():.2f}€"


class PremiumMemberDecorator(DiscountDecorator):
    def __init__(self, order: OrderComponent) -> None:
        super().__init__(order, percent=10)

    def get_description(self) -> str:
        return OrderDecorator.get_description(self) + f"\nPremium member (10%): -{self._discount():.2f}€"


if __name__ == "__main__":
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"Total: {simple.get_cost():.2f}€")

    print("\n---\n")

    # Order of decorators = order of operations, now explicit and readable
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")   # 95.625€, same result as the original code
