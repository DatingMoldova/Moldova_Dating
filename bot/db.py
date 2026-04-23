import psycopg2
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()


# ================= СОЗДАНИЕ ТАБЛИЦЫ =================

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


# ================= ПОЛУЧИТЬ ПОЛЬЗОВАТЕЛЯ =================

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


# ================= СОХРАНИТЬ ПОЛЬЗОВАТЕЛЯ =================

def save_user(user_id, name, age, city, gender, search, about, photo, username, referrer_id):
    cursor.execute("""
    INSERT INTO users (
        user_id, name, age, city, gender, search, about,
        photo, username, referrer_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO NOTHING
    """, (
        user_id, name, age, city, gender, search, about,
        photo, username, referrer_id
    ))
    conn.commit()


# ================= РЕФЕРАЛКА =================

def add_referral(referrer_id, new_user_id):
    cursor.execute(
        "SELECT is_counted FROM users WHERE user_id = %s",
        (new_user_id,)
    )
    res = cursor.fetchone()

    if res and res[0]:
        return

    cursor.execute("""
    UPDATE users
    SET invites = invites + 1,
        balance = balance + 10
    WHERE user_id = %s
    """, (referrer_id,))

    cursor.execute("""
    UPDATE users
    SET is_counted = TRUE
    WHERE user_id = %s
    """, (new_user_id,))

    conn.commit()


# ================= ЛАЙКИ / ПРОСМОТРЫ =================

def add_like(user_id):
    cursor.execute("""
    UPDATE users
    SET likes = likes + 1
    WHERE user_id = %s
    """, (user_id,))
    conn.commit()


def add_view(user_id):
    cursor.execute("""
    UPDATE users
    SET views = views + 1
    WHERE user_id = %s
    """, (user_id,))
    conn.commit()


# ================= ФОТО =================

def update_photos(user_id, photos):
    cursor.execute(
        "UPDATE users SET photos = %s WHERE user_id = %s",
        (photos, user_id)
    )
    conn.commit()


def set_main_photo(user_id, photo):
    cursor.execute(
        "UPDATE users SET photo = %s WHERE user_id = %s",
        (photo, user_id)
    )
    conn.commit()


# ================= АНКЕТА =================

def update_about(user_id, about):
    cursor.execute(
        "UPDATE users SET about = %s WHERE user_id = %s",
        (about, user_id)
    )
    conn.commit()


def toggle_active(user_id, status):
    cursor.execute(
        "UPDATE users SET is_active = %s WHERE user_id = %s",
        (status, user_id)
    )
    conn.commit()
