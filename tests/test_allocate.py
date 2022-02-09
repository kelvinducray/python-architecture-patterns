from datetime import date, timedelta

import pytest

from shipping_api import Batch, OrderLine, allocate
from shipping_api.exceptions import OutOfStock

# Initialise some variables for later...
today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments() -> None:
    in_stock_batch = Batch(
        "in-stock-batch",
        "RETRO-CLOCK",
        quantity=100,
        eta=None,
    )
    shipment_batch = Batch(
        "shipment-batch",
        "RETRO-CLOCK",
        quantity=100,
        eta=tomorrow,
    )

    line = OrderLine("oref", "RETRO-CLOCK", quantity=10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches() -> None:
    earliest = Batch(
        "speedy-batch",
        "MINIMALIST-SPOON",
        quantity=100,
        eta=today,
    )
    medium = Batch(
        "normal-batch",
        "MINIMALIST-SPOON",
        quantity=100,
        eta=tomorrow,
    )
    latest = Batch(
        "slow-batch",
        "MINIMALIST-SPOON",
        quantity=100,
        eta=later,
    )

    line = OrderLine("order1", "MINIMALIST-SPOON", quantity=10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref() -> None:
    in_stock_batch = Batch(
        "in-stock-batch",
        "HIGHBROW-POSTER",
        quantity=100,
        eta=None,
    )
    shipment_batch = Batch(
        "shipment-batch",
        "HIGHBROW-POSTER",
        quantity=100,
        eta=tomorrow,
    )

    line = OrderLine("oref", "HIGHBROW-POSTER", quantity=10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "SMALL-FORK", quantity=10, eta=today)
    line_1 = OrderLine("order1", "SMALL-FORK", quantity=10)
    line_2 = OrderLine("order2", "SMALL-FORK", quantity=1)

    allocate(line_1, [batch])  # First we allocate the whole batch

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        # Then try after the stock is already allocated
        allocate(line_2, [batch])
