users = {}


def create_user(user_id, name, age, city, gender, looking, bio, photo):
    users[user_id] = [
        user_id, name, age, city, gender, looking, bio, photo,
        0, 0, 0, 0, 0, 0, 0, 0
    ]


def get_user(user_id):
    return users.get(user_id)


def add_view(user_id):
    if user_id in users:
        users[user_id][13] += 1


# ---- admin заглушки ----

def set_premium(user_id, status):
    if user_id in users:
        users[user_id][9] = int(status)


def create_promo(code, reward):
    pass


def add_moderator(user_id):
    pass


def get_users_count():
    return len(users)


cursor = None
conn = None
