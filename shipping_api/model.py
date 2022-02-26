# NOTE: This allows us to use the type hint of the enclosing
#       class when writing functions within that class.
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Optional

from .exceptions import OutOfStock


@dataclass(unsafe_hash=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: Optional[date],
    ):
        self.reference = reference
        self.sku = sku
        self.eta = eta

        self._purchased_quantity = quantity
        self._allocations: set[OrderLine] = set()

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Batch):
            return False

        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: Batch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True

        return self.eta > other.eta


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)

        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for SKU: {line.sku}")
