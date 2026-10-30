"""Окно состава заказа."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import database as db
from datetime import datetime


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id, current_user=None):
        self.order_id = order_id
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("900x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        return (self.current_user and
                self.current_user[5] == "Администратор")

    def build_ui(self):
        tk.Label(self.window, text=f"ЗАКАЗ №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(fill="x")

        info_frame = tk.Frame(self.window, bg=COLOR_SECONDARY_BG)
        info_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(info_frame, text="Дата:", font=font(bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left")
        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(info_frame, textvariable=self.date_var,
                                   width=15, state="readonly")
        self.date_entry.pack(side="left", padx=5)
        if self.is_admin():
            self.date_entry.config(state="normal")
            tk.Button(info_frame, text="Сохранить дату",
                      command=self.save_date, bg=COLOR_ACCENT,
                      fg="white").pack(side="left")
        tk.Label(info_frame, text="Клиент:", font=font(bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", padx=(20, 5))
        self.client_label = tk.Label(info_frame, text="",
                                     bg=COLOR_SECONDARY_BG)
        self.client_label.pack(side="left")

        columns = ("id", "name", "production", "model",
                   "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=12)
        self.tree.heading("id", text="№")
        self.tree.heading("name", text="Товар")
        self.tree.heading("production", text="Производитель")
        self.tree.heading("model", text="Модель")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.total_label = tk.Label(self.window