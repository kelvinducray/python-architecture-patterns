from datetime import date

import pytest
from shipping_api import Batch, OrderLine


def test_allocating_to_a_batch_reduces_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", quantity=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", quantity=2)

    batch.allocate(line)

    assert batch.available_quantity == 18
