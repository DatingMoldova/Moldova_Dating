import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    database=os.getenv("PGDATABASE")
)

cursor = conn.cursor()


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
        username TEXT,
        referrer_id BIGINT,
        invites INTEGER DEFAULT 0,
        balance INTEGER DEFAULT 0,
        is_counted BOOLEAN DEFAULT FALSE
    )
    """)
    conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


def save_user(user_id, name, age, city, gender, search, about, photo, username, referrer_id):
    cursor.execute("""
    INSERT INTO users (user_id, name, age, city, gender, search, about, photo, username, referrer_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, name, age, city, gender, search, about, photo, username, referrer_id))
    conn.commit()


def add_referral(referrer_id, new_user_id):
    # уже засчитан?
    cursor.execute("SELECT is_counted FROM users WHERE user_id = %s", (new_user_id,))
    res = cursor.fetchone()

    if res and res[0]:
        return

    # начисление
    cursor.execute("""
    UPDATE users
    SET invites = invites + 1,
        balance = balance + 10
    WHERE user_id = %s
    """, (referrer_id,))

    # помечаем
    cursor.execute("""
    UPDATE users
    SET is_counted = TRUE
    WHERE user_id = %s
    """, (new_user_id,))

    conn.commit()
