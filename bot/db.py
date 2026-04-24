import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


# =========================
# 🔥 ИНИЦИАЛИЗАЦИЯ
# =========================

def init_db():
    # 👤 пользователи
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        name TEXT,
        age INT,
        city TEXT,
        gender TEXT,
        looking TEXT,
        bio TEXT,
        photo TEXT,

        balance INT DEFAULT 0,
        is_premium BOOLEAN DEFAULT FALSE,

        invites INT DEFAULT 0,
        referrer BIGINT,

        views INT DEFAULT 0,
        likes INT DEFAULT 0,
        reputation INT DEFAULT 0
    )
    """)

    # ❤️ лайки
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        id SERIAL PRIMARY KEY,
        from_user BIGINT,
        to_user BIGINT,
        UNIQUE (from_user, to_user)
    )
    """)

    # 🎁 промо
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promos (
        id SERIAL PRIMARY KEY,
        code TEXT UNIQUE,
        reward INT,
        uses INT DEFAULT 0
    )
    """)

    # 🛡 модераторы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS moderators (
        user_id BIGINT UNIQUE
    )
    """)

    conn.commit()


# =========================
# 👤 ПОЛЬЗОВАТЕЛИ
# =========================

def create_user(user_id, name, age, city, gender, looking, bio, photo, referrer=None):
    cursor.execute("""
        INSERT INTO users (
            user_id, name, age, city, gender, looking, bio, photo, referrer
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id, name, age, city, gender, looking, bio, photo, referrer))
    conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


def get_users_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]


# =========================
# ❤️ ЛАЙКИ
# =========================

def add_like_user(from_user, to_user):
    cursor.execute("""
        INSERT INTO likes (from_user, to_user)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (from_user, to_user))
    conn.commit()


def get_incoming_likes(user_id):
    cursor.execute(
        "SELECT from_user FROM likes WHERE to_user = %s",
        (user_id,)
    )
    return cursor.fetchall()


def get_outgoing_likes(user_id):
    cursor.execute(
        "SELECT to_user FROM likes WHERE from_user = %s",
        (user_id,)
    )
    return cursor.fetchall()


def check_match(user1, user2):
    cursor.execute("""
        SELECT 1 FROM likes 
        WHERE from_user = %s AND to_user = %s
    """, (user1, user2))
    a = cursor.fetchone()

    cursor.execute("""
        SELECT 1 FROM likes 
        WHERE from_user = %s AND to_user = %s
    """, (user2, user1))
    b = cursor.fetchone()

    return a and b


# =========================
# ⭐ ПРЕМИУМ
# =========================

def set_premium(user_id, status=True):
    cursor.execute(
        "UPDATE users SET is_premium = %s WHERE user_id = %s",
        (status, user_id)
    )
    conn.commit()


# =========================
# 🎁 ПРОМО
# =========================

def create_promo(code, reward):
    cursor.execute("""
        INSERT INTO promos (code, reward)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (code, reward))
    conn.commit()


def get_promo(code):
    cursor.execute("SELECT * FROM promos WHERE code = %s", (code,))
    return cursor.fetchone()


# =========================
# 🛡 МОДЕРАТОРЫ
# =========================

def add_moderator(user_id):
    cursor.execute("""
        INSERT INTO moderators (user_id)
        VALUES (%s)
        ON CONFLICT DO NOTHING
    """, (user_id,))
    conn.commit()


def is_moderator(user_id):
    cursor.execute(
        "SELECT 1 FROM moderators WHERE user_id = %s",
        (user_id,)
    )
    return cursor.fetchone() is not None


# =========================
# 📊 СТАТИСТИКА
# =========================

def add_view(user_id):
    cursor.execute(
        "UPDATE users SET views = views + 1 WHERE user_id = %s",
        (user_id,)
    )
    conn.commit()


def add_like_stat(user_id):
    cursor.execute(
        "UPDATE users SET likes = likes + 1 WHERE user_id = %s",
        (user_id,)
    )
    conn.commit()


def add_invite(user_id):
    cursor.execute(
        "UPDATE users SET invites = invites + 1 WHERE user_id = %s",
        (user_id,)
    )
    conn.commit()


def update_balance(user_id, amount):
    cursor.execute(
        "UPDATE users SET balance = balance + %s WHERE user_id = %s",
        (amount, user_id)
    )
    conn.commit()


# =========================
# 💣 СБРОС БД
# =========================

def reset_db():
    cursor.execute("""
        TRUNCATE users, likes, promos, moderators
        RESTART IDENTITY CASCADE
    """)
    conn.commit()
