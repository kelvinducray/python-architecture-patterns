from sqlalchemy import text
from sqlalchemy.orm.session import Session

from shipping_api import model


def test_orderline_mapper_can_load_lines(session: Session) -> None:
    session.execute(
        text(
            """
            INSERT INTO order_lines (order_id, sku, quantity)
            VALUES
                ('order-1', 'RED-CHAR', 12),
                ('order-1', 'RED-TABLE', 13),
                ('order-2', 'BLUE-LIPSTICK', 14)
            """,
        )
    )

    expected = [
        model.OrderLine("order-1", "RED-CHAR", 12),
        model.OrderLine("order-1", "RED-TABLE", 13),
        model.OrderLine("order-2", "BLUE-LIPSTICK", 14),
    ]

    actual = session.query(model.OrderLine).all()

    assert actual == expected


def test_orderline_mapper_can_save_lines(session: Session) -> None:
    new_line = model.OrderLine("order-1", "DECORATIVE-WIDGET", 12)

    session.add(new_line)
    session.commit()

    actual = session.execute("SELECT order_id, sku, quantity FROM order_lines").all()

    expected = [("order-1", "DECORATIVE-WIDGET", 12)]

    assert actual == expected
