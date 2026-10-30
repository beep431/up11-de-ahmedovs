"""Каталог товаров — Мир Света."""
import tkinter as tk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product, refresh=None):
    """Создаёт карточку товара."""
    qty = product[6]
    bg_color = _get_card_color(qty)
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty, refresh)
    return card


def _get_card_color(qty):
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)
    photo = get_product_image(product[7], size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty, refresh):
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True,
                    padx=10, pady=10)
    
    name = product[1] or "[Без названия]"
    production = product[3] or "[Без производителя]"
    category = product[2] or "[Без категории]"
    characteristics = product[4] or "[Не указаны]"
    price = product[5] if product[5] is not None else 0
    
    _add_label(text_frame, f"{production} | {name}", bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color)
    _add_label(text_frame, f"Характеристики: {characteristics}", bg_color)
    _add_label(text_frame, f"{price} руб.", bg_color, bold=True, size=FONT_SIZE_HEADER)

    # Добавляем кнопку "Добавить в заказ"
    btn = tk.Button(text_frame, text="Добавить в заказ", 
                    bg=COLOR_ACCENT, fg="white",
                    font=font(FONT_SIZE_NORMAL),
                    command=lambda: _open_view(card, product, refresh))
    btn.pack(anchor="w", pady=5)


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    return "Много" if qty > 5 else "Мало"


def _open_view(parent, product, refresh=None):
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)