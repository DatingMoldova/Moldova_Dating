import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не найден")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


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

            referrer BIGINT,

            invites INT DEFAULT 0,
            balance INT DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            likes INT DEFAULT 0,
            views INT DEFAULT 0,
            reputation INT DEFAULT 0,

            is_premium BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    conn.commit()


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

    # 🎁 рефералка
    if referrer and referrer != user_id:
        cursor.execute(
            "UPDATE users SET balance = balance + 10, invites = invites + 1 WHERE user_id = %s",
            (referrer,)
        )
        conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


def add_like(user_id):
    cursor.execute(
        "UPDATE users SET likes = likes + 1, reputation = reputation + 1 WHERE user_id = %s",
        (user_id,)
    )
    conn.commit()


def add_view(user_id):
    cursor.execute(
        "UPDATE users SET views = views + 1 WHERE user_id = %s",
        (user_id,)
    )
    conn.commit()
