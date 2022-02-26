from sqlalchemy.orm import Session

from shipping_api.model import Batch, OrderLine
from shipping_api.repository import SQLAlchemyRepository


def test_repository_can_save_a_batch(session: Session) -> None:
    batch = Batch("batch1", "RUSTY-SOAPDISH", quantity=100, eta=None)

    repo = SQLAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    actual = session.execute(
        """
            SELECT
                reference,
                sku,
                _purchased_quantity,
                eta
            FROM batches
        """
    ).all()

    expected = [("batch1", "RUSTY-SOAPDISH", 100, None)]

    assert actual == expected


# NOTE: This is a helper function for subsequent test
def insert_order_line(session: Session) -> str:
    session.execute(
        """
            INSERT INTO order_lines (orderid, sku, quantity)
            VALUES ('order1', 'GENERIC-SOFA', 12)
        """
    )

    (orderline_id,) = session.execute(
        """
            SELECT id
            FROM order_lines
            WHERE
                orderid=:orderid
                AND sku=:sku
        """,
        dict(orderid="order1", sku="GENERIC-SOFA"),
    ).all()

    return orderline_id


# NOTE: This is a helper function for subsequent test
def insert_batch(session: Session, batch_id: str) -> str:
    session.execute(
        """
            INSERT INTO batches (reference, sku, _purchased_quantity, eta)
            VALUES (:batch_id, 'GENERIC-SOFA', 100, null)
        """,
        dict(batch_id=batch_id),
    )

    (batch_id,) = session.execute(
        """
            SELECT id
            FROM batches
            WHERE
                reference=:batch_id
                AND sku="GENERIC-SOFA
        """,
        dict(batch_id=batch_id),
    ).all()

    return batch_id


# NOTE: This is a helper function for subsequent test
def insert_allocation(
    session: Session,
    orderline_id: str,
    batch_id: str,
) -> None:
    session.execute(
        """
            INSERT INTO allocations (orderline_id, batch_id)
            VALUES (:orderline_id, :batch_id)
        """,
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


def test_repository_can_retrieve_a_batch_with_allocations(
    session: Session,
) -> None:
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SQLAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)

    assert retrieved == expected  # Batch.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }
