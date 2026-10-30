"""Настройки проекта."""
COMPANY_NAME = "Мир Света"
APP_TITLE = f"Система продаж — {COMPANY_NAME}"

# PostgreSQL
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "init_db"
DB_USER = "postgres"
DB_PASSWORD = "123"

def get_dsn():
    return (f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} "
            f"user={DB_USER} password={DB_PASSWORD}")