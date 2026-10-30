"""Работа с БД PostgreSQL."""
import psycopg2
from config import get_dsn


def get_connection():
    """Соединение с PostgreSQL."""
    return psycopg2.connect(get_dsn())


def get_all_products():
    """Список товаров под 6-табличную схему.

    Возвращает строки в порядке, который ждёт catalog.py:
        id, название, категория, производитель, характеристики,
        цена, количество, изображение, модель
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id,
               название,
               категория,
               производитель,
               характеристики,
               цена_белый                                   AS цена,
               (кол_белый + кол_чёрный + кол_серебристый)  AS количество,
               изображение,
               NULL                                         AS модель
        FROM Товар
        ORDER BY id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_product_quantity(product_id):
    """Суммарный остаток по всем вариантам."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT кол_белый + кол_чёрный + кол_серебристый
        FROM Товар
        WHERE id = %s
    """, (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_user_by_login(login):
    """Пользователь по логину.
       Возвращает (id, фамилия, имя, отчество, логин, роль).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.фамилия, u.имя, u.отчество,
               u.логин, r.название
        FROM Пользователь u
        JOIN Роль r ON u.роль_id = r.id
        WHERE u.логин = %s
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row