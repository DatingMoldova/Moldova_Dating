import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


# =========================
# 🧱 СОЗДАНИЕ ТАБЛИЦЫ
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE,

    name TEXT,
    age INT,
    city TEXT,

    gender TEXT,
    looking TEXT,
    bio TEXT,
    photo TEXT,

    balance INT DEFAULT 0,
    premium BOOLEAN DEFAULT FALSE,
    invites INT DEFAULT 0,

    referrer BIGINT,

    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    reputation INT DEFAULT 0
)
""")

conn.commit()


# =========================
# 👤 СОЗДАТЬ / ОБНОВИТЬ
# =========================

def create_user(user_id, name, age, city, gender, looking, bio, photo):
    cursor.execute("""
    INSERT INTO users (
        user_id, name, age, city,
        gender, looking, bio, photo
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (user_id) DO UPDATE SET
        name = EXCLUDED.name,
        age = EXCLUDED.age,
        city = EXCLUDED.city,
        bio = EXCLUDED.bio,
        photo = EXCLUDED.photo
    """, (user_id, name, age, city, gender, looking, bio, photo))

    conn.commit()


# =========================
# 🔍 ПОЛУЧИТЬ ЮЗЕРА
# =========================

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


# =========================
# 👀 ПРОСМОТРЫ
# =========================

def add_view(user_id):
    cursor.execute("""
    UPDATE users
    SET views = views + 1
    WHERE user_id = %s
    """, (user_id,))
    conn.commit()


# =========================
# ⭐ ПРЕМИУМ
# =========================

def set_premium(user_id, status):
    cursor.execute("""
    UPDATE users
    SET premium = %s
    WHERE user_id = %s
    """, (status, user_id))
    conn.commit()


# =========================
# 🎁 ПРОМО
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS promos (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE,
    reward INT
)
""")
conn.commit()


def create_promo(code, reward):
    cursor.execute("""
    INSERT INTO promos (code, reward)
    VALUES (%s, %s)
    """, (code, reward))
    conn.commit()


# =========================
# 🛡 МОДЕРАТОРЫ
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS moderators (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE
)
""")
conn.commit()


def add_moderator(user_id):
    cursor.execute("""
    INSERT INTO moderators (user_id)
    VALUES (%s)
    ON CONFLICT DO NOTHING
    """, (user_id,))
    conn.commit()


# =========================
# 📊 СТАТИСТИКА
# =========================

def get_users_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]
