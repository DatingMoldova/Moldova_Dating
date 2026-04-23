import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# ❌ если нет DATABASE_URL — сразу понятная ошибка
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не найден в переменных окружения")

# 🔥 фикс для Railway
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ БД подключена")
except Exception as e:
    print("❌ Ошибка подключения к БД:", e)
    raise


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE,

        name TEXT,
        age INTEGER,
        city TEXT,

        gender TEXT,
        search TEXT,
        about TEXT,

        photo TEXT,
        photos TEXT[],

        username TEXT,

        referrer_id BIGINT,

        invites INTEGER DEFAULT 0,
        balance INTEGER DEFAULT 0,

        is_counted BOOLEAN DEFAULT FALSE,

        likes INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0,

        is_active BOOLEAN DEFAULT TRUE
    )
    """)
    conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


def save_user(user_id, name, age, city, gender, search, about, photo, username, referrer_id):
    cursor.execute("""
    INSERT INTO users (
        user_id, name, age, city, gender, search, about,
        photo, username, referrer_id
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (user_id) DO NOTHING
    """, (user_id,name,age,city,gender,search,about,photo,username,referrer_id))
    conn.commit()


def toggle_active(user_id, status):
    cursor.execute(
        "UPDATE users SET is_active = %s WHERE user_id = %s",
        (status, user_id)
    )
    conn.commit()
