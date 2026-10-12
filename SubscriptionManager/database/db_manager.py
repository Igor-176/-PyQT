import sqlite3

DB_NAME = "subscriptions.db"

def init_db():
    """Инициализация базы данных и создание необходимых таблиц."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица категорий
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    # Таблица подписок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            billing_day INTEGER NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    
    # Заполнение базовых категорий по умолчанию
    default_categories = ["Стриминги", "Работа", "Игры", "Софт", "Прочее"]
    for cat in default_categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
        
    conn.commit()
    conn.close()

def get_all_categories():
    """Возвращает список всех категорий."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_subscriptions():
    """Возвращает список всех подписок вместе с их категориями."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, s.price, s.billing_day, c.name, s.category_id
        FROM subscriptions s
        JOIN categories c ON s.category_id = c.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_subscription(category_id, name, price, billing_day):
    """Добавляет новую подписку в базу данных."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO subscriptions (category_id, name, price, billing_day)
        VALUES (?, ?, ?, ?)
    """, (category_id, name, price, billing_day))
    conn.commit()
    conn.close()

def update_subscription(sub_id, category_id, name, price, billing_day):
    """Обновляет существующую подписку."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE subscriptions
        SET category_id = ?, name = ?, price = ?, billing_day = ?
        WHERE id = ?
    """, (category_id, name, price, billing_day, sub_id))
    conn.commit()
    conn.close()

def delete_subscription(sub_id):
    """Удаляет подписку по её ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()