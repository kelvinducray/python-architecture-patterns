from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self,
        ref: str,
        sku: str,
        quantity: int,
        eta: Optional[date],
    ):
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = quantity

    def allocate(self, order_line: OrderLine):
        self.available_quantity -= order_line.quantity
