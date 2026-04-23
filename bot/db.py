import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не найден")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


# 🔥 СОЗДАНИЕ ТАБЛИЦЫ
def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,

            name TEXT,
            age INT,
            city TEXT,

            gender TEXT,
            search TEXT,
            about TEXT,

            photo TEXT,
            username TEXT,

            referrer INT,

            invites INT DEFAULT 0,
            balance INT DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            likes INT DEFAULT 0,
            views INT DEFAULT 0,

            is_premium BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    conn.commit()


# 💾 СОХРАНЕНИЕ ПОЛЬЗОВАТЕЛЯ
def save_user(user_id, name, age, city, gender, search, about, photo, username, referrer):
    cursor.execute("""
        INSERT INTO users 
        (user_id, name, age, city, gender, search, about, photo, username, referrer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            name = EXCLUDED.name,
            age = EXCLUDED.age,
            city = EXCLUDED.city,
            gender = EXCLUDED.gender,
            search = EXCLUDED.search,
            about = EXCLUDED.about,
            photo = EXCLUDED.photo
    """, (user_id, name, age, city, gender, search, about, photo, username, referrer))

    conn.commit()


# 👤 ПОЛУЧИТЬ ПОЛЬЗОВАТЕЛЯ
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


# 🔄 ВКЛ / ВЫКЛ АНКЕТЫ
def toggle_active(user_id, status: bool):
    cursor.execute(
        "UPDATE users SET is_active = %s WHERE user_id = %s",
        (status, user_id)
    )
    conn.commit()


# 📊 КОЛ-ВО ПОЛЬЗОВАТЕЛЕЙ
def get_users_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]


# 💣 СБРОС БД
def reset_db():
    cursor.execute("DELETE FROM users")
    conn.commit()
