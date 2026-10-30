"""Алгоритм расчёта цены со скидкой 25%."""
from datetime import datetime, timedelta
from database import get_connection


def get_previous_month_range(date):
    """Возвращает (начало, конец) предыдущего месяца."""
    first_day = date.replace(day=1)
    last_day_prev = first_day - timedelta(days=1)
    first_day_prev = last_day_prev.replace(day=1)
    return (first_day_prev.strftime("%Y-%m-%d"),
            last_day_prev.strftime("%Y-%m-%d"))


def has_orders_in_previous_month(product_id, date):
    """Есть ли заказы товара в предыдущем месяце?"""
    start, end = get_previous_month_range(date)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM Состав_заказа so
        JOIN Заказ z ON so.заказ_id = z.id
        WHERE so.товар_id = %s AND z.дата BETWEEN %s AND %s
    """, (product_id, start, end))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def calculate_price_with_discount(product_id, price, date):
    """Цена со скидкой 25%, если в прошлом месяце не было заказов."""
    if has_orders_in_previous_month(product_id, date):
        return price
    return float(price) * 0.75