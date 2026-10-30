"""Работа с заказами (PostgreSQL) — под 6-табличную схему."""
from datetime import datetime
from database import get_connection
from discount import calculate_price_with_discount


def get_all_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_by_id(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ WHERE id = %s",
                (order_id,))
    row = cur.fetchone()
    conn.close()
    return row


def get_order_items(order_id):
    """Состав заказа: id, товар, производитель, вариант, кол-во, цена, сумма."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT so.id, t.название, t.производитель,
               so.вариант, so.количество, so.цена,
               so.количество * so.цена AS сумма
        FROM Состав_заказа so
        JOIN Товар t ON so.товар_id = t.id
        WHERE so.заказ_id = %s
        ORDER BY so.id
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_total(order_id, date=None):
    """Итоговая сумма заказа с учётом скидки 25% по каждой позиции."""
    if date is None:
        date = datetime.now().date()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT so.товар_id, so.количество, so.цена
        FROM Состав_заказа so
        WHERE so.заказ_id = %s
    """, (order_id,))
    items = cur.fetchall()
    conn.close()

    total = 0.0
    for product_id, qty, price in items:
        final_price = calculate_price_with_discount(product_id, price, date)
        total += qty * final_price
    return total


def create_order(client, items, date=None):
    """
    items = [(product_id, variant, quantity, price), ...]
    variant — строка: 'Белый' | 'Чёрный' | 'Серебристый'
    """
    if date is None:
        date = datetime.now().date()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (%s, %s) RETURNING id",
            (date, client)
        )
        order_id = cur.fetchone()[0]

        # карта колонок остатков по варианту
        col_qty = {
            "Белый":       "кол_белый",
            "Чёрный":      "кол_чёрный",
            "Серебристый": "кол_серебристый",
        }

        for product_id, variant, quantity, price in items:
            if variant not in col_qty:
                raise ValueError(f"Неизвестный вариант: {variant}")

            # проверка остатка по выбранному варианту
            cur.execute(
                f"SELECT {col_qty[variant]} FROM Товар WHERE id = %s",
                (product_id,)
            )
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(
                    f"Недостаточно товара id={product_id} ({variant})"
                )

            cur.execute("""
                INSERT INTO Состав_заказа
                (заказ_id, товар_id, вариант, количество, цена)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, product_id, variant, quantity, price))

            cur.execute(
                f"UPDATE Товар SET {col_qty[variant]} = {col_qty[variant]} - %s "
                f"WHERE id = %s",
                (quantity, product_id)
            )

        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None
    finally:
        conn.close()


def delete_order(order_id):
    """Удаляет заказ и восстанавливает остатки по вариантам."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT товар_id, вариант, количество
            FROM Состав_заказа WHERE заказ_id = %s
        """, (order_id,))
        rows = cur.fetchall()

        col_qty = {
            "Белый":       "кол_белый",
            "Чёрный":      "кол_чёрный",
            "Серебристый": "кол_серебристый",
        }
        for product_id, variant, quantity in rows:
            col = col_qty.get(variant)
            if col:
                cur.execute(
                    f"UPDATE Товар SET {col} = {col} + %s WHERE id = %s",
                    (quantity, product_id)
                )

        cur.execute("DELETE FROM Состав_заказа WHERE заказ_id = %s",
                    (order_id,))
        cur.execute("DELETE FROM Заказ WHERE id = %s", (order_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def update_order_date(order_id, new_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Заказ SET дата = %s WHERE id = %s",
                (new_date, order_id))
    conn.commit()
    conn.close()
    return True


def delete_order_item(item_id):
    """Удаляет позицию и восстанавливает остаток по варианту."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT товар_id, вариант, количество
            FROM Состав_заказа WHERE id = %s
        """, (item_id,))
        product_id, variant, quantity = cur.fetchone()

        col_qty = {
            "Белый":       "кол_белый",
            "Чёрный":      "кол_чёрный",
            "Серебристый": "кол_серебристый",
        }
        col = col_qty.get(variant)
        if col:
            cur.execute(
                f"UPDATE Товар SET {col} = {col} + %s WHERE id = %s",
                (quantity, product_id)
            )

        cur.execute("DELETE FROM Состав_заказа WHERE id = %s", (item_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()