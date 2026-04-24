# =========================
# 📦 ПРОСТАЯ БД В ПАМЯТИ
# =========================

users = {}
promos = {}
moderators = set()


# =========================
# 👤 ПОЛЬЗОВАТЕЛИ
# =========================

def create_user(user_id, name, age, city, gender, looking, bio, photo):
    users[user_id] = [
        user_id,   # 0
        name,      # 1
        age,       # 2
        city,      # 3
        gender,    # 4
        looking,   # 5
        bio,       # 6
        photo,     # 7

        0,         # 8 balance
        0,         # 9 premium (0/1)
        0,         # 10 invites

        0,         # 11 reserved
        0,         # 12 reserved

        0,         # 13 views
        0,         # 14 likes
        0          # 15 rep
    ]


def get_user(user_id):
    return users.get(user_id)


def delete_user(user_id):
    users.pop(user_id, None)


# =========================
# 📊 АКТИВНОСТЬ
# =========================

def add_view(user_id):
    if user_id in users:
        users[user_id][13] += 1


def add_like(user_id):
    if user_id in users:
        users[user_id][14] += 1


def add_rep(user_id, value=1):
    if user_id in users:
        users[user_id][15] += value


# =========================
# 💰 БАЛАНС / ПРЕМИУМ
# =========================

def add_balance(user_id, amount):
    if user_id in users:
        users[user_id][8] += amount


def set_premium(user_id, status):
    if user_id in users:
        users[user_id][9] = 1 if status else 0


# =========================
# 👥 РЕФЕРАЛКА
# =========================

def add_invite(user_id):
    if user_id in users:
        users[user_id][10] += 1


# =========================
# 🎁 ПРОМОКОДЫ
# =========================

def create_promo(code, reward):
    promos[code] = reward


def use_promo(user_id, code):
    if code not in promos:
        return False

    reward = promos[code]
    add_balance(user_id, reward)

    return True


# =========================
# 🛡 МОДЕРАТОРЫ
# =========================

def add_moderator(user_id):
    moderators.add(user_id)


def is_moderator(user_id):
    return user_id in moderators


# =========================
# 📊 СТАТИСТИКА
# =========================

def get_users_count():
    return len(users)


def get_top_referrals(limit=10):
    sorted_users = sorted(users.values(), key=lambda x: x[10], reverse=True)
    return sorted_users[:limit]


def get_total_balance():
    return sum(u[8] for u in users.values())


def get_total_invites():
    return sum(u[10] for u in users.values())
