"""Форма просмотра товара — Мир Света."""
import tkinter as tk
from tkinter import messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from resources import get_product_image
from database import get_product_quantity
from order_manager import create_order
from error_handler import validate_positive_int


class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.qty_var = tk.StringVar(value="1")

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[1]}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=self.product[1],
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        img_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        img_frame.pack(pady=10)
        photo = get_product_image(self.product[7], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG,
                     width=20, height=10).pack()

        info_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        info_frame.pack(fill="x", padx=20, pady=10)
        self._add_field(info_frame, "Название", self.product[1])
        self._add_field(info_frame, "Категория", self.product[2])
        self._add_field(info_frame, "Производитель", self.product[3])
        self._add_field(info_frame, "Характеристики", self.product[4])
        self._add_field(info_frame, "Цена", f"{self.product[5]} руб.")
        self._add_field(info_frame, "Количество", self.product[6])

        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(qty_frame, text="Количество для заказа:",
                 font=font(bold=True), bg=COLOR_MAIN_BG).pack(side="left")
        tk.Entry(qty_frame, textvariable=self.qty_var,
                 width=10).pack(side="left", padx=5)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=20)
        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL)).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Закрыть",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL)).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{label}:", font=font(bold=True),
                 width=15, anchor="w").pack(side="left")
        tk.Label(row, text=str(value), font=font(),
                 anchor="w").pack(side="left")

    def add_to_order(self):
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showerror("Ошибка ввода", str(result))
            return

        qty = int(result)
        current_qty = get_product_quantity(self.product[0])
        if qty > current_qty:
            messagebox.showwarning("Ошибка",
                                   f"Доступно только {current_qty} шт.")
            return

        try:
            items = [(self.product[0], self.product[8], qty,
                      float(self.product[5]))]
            order_id = create_order("Клиент", items)
            if order_id:
                messagebox.showinfo("Успех", f"Заказ №{order_id} оформлен")
                if self.on_add_to_order:
                    self.on_add_to_order()
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка заказа:\n{e}")