"""Авторизация пользователей."""
import tkinter as tk
from tkinter import messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from database import get_user_by_login


class AuthWindow:
    """Окно авторизации."""

    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        self.window = tk.Toplevel(root)
        self.window.title("Авторизация — Мир Света")
        self.window.geometry("400x350") # Немного увеличили высоту для пароля
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.grab_set()

        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="ВХОД В «МИР СВЕТА»",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        form = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        form.pack(pady=20)

        # Поле логина
        tk.Label(form, text="Логин:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w")

        self.login_var = tk.StringVar()
        tk.Entry(form, textvariable=self.login_var, width=30,
                 font=font(FONT_SIZE_NORMAL)).pack(pady=5)

        # Поле пароля
        tk.Label(form, text="Пароль:", font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(anchor="w", pady=(5, 0))

        self.password_var = tk.StringVar()
        tk.Entry(form, textvariable=self.password_var, width=30, show="*",
                 font=font(FONT_SIZE_NORMAL)).pack(pady=5)

        tk.Button(form, text="Войти", command=self.login,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=20, pady=5).pack(pady=15)

        # Правильная подсказка!
        tk.Label(form, text="Пример: client01, manager1, admin",
                 font=font(FONT_SIZE_NORMAL),
                 fg="gray", bg=COLOR_MAIN_BG).pack()

    def login(self):
        login = self.login_var.get().strip()
        password = self.password_var.get().strip()

        if not login:
            messagebox.showwarning("Ошибка", "Введите логин")
            return

        user = get_user_by_login(login)
        
        if not user:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return
            
        # (Опционально) Проверка пароля, если вы захотите её добавить позже.
        # Сейчас в БД у всех пароль '1234'.
        # if password != '1234':
        #     messagebox.showerror("Ошибка", "Неверный пароль")
        #     return

        messagebox.showinfo("Успех", f"Добро пожаловать, {user[1]}!")
        self.window.destroy()
        self.on_success(user)