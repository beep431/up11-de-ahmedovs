"""Работа с ресурсами — Мир Света."""
import os
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Указываем, что картинки лежат в папке Images в корне проекта
PRODUCTS_DIR = os.path.join(BASE_DIR, "Images")

# Логотип и заглушка (они у вас тоже есть в корне, судя по скриншотам)
PATH_PICTURE = os.path.join(BASE_DIR, "picture.png")
PATH_LOGO = os.path.join(BASE_DIR, "logo.png")

def load_image(path, size=(100, 100)):
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None

def load_image_proportional(path, max_size=(100, 100)):
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path)
        img.thumbnail(max_size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None

def get_product_image(image_path, size=(100, 100)):
    """Ищет картинку в папке Images."""
    if image_path:
        # Берем только имя файла (IMG_05_001.png) и ищем в папке Images
        full_path = os.path.join(PRODUCTS_DIR, os.path.basename(image_path))
        if os.path.exists(full_path):
            return load_image(full_path, size)

    return load_image(PATH_PICTURE, size)