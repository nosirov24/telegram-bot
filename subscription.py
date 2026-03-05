import time
from database import load_json, save_json
from config import VIP_FILE, CHANNELS_FILE


# =====================================================
# LOAD CHANNELS
# =====================================================

def load_channels():
    return load_json(CHANNELS_FILE, [])


# =====================================================
# VIP CHECK
# =====================================================

def is_vip(user_id):

    vip_users = load_json(VIP_FILE, {})

    user_id = str(user_id)

    if user_id not in vip_users:
        return False

    expire_time = vip_users[user_id]

    if time.time() > expire_time:
        # VIP expired
        del vip_users[user_id]
        save_json(VIP_FILE, vip_users)
        return False

    return True


# =====================================================
# ADD VIP
# =====================================================

def add_vip(user_id, days):

    vip_users = load_json(VIP_FILE, {})

    expire_time = time.time() + (days * 86400)

    vip_users[str(user_id)] = expire_time

    save_json(VIP_FILE, vip_users)


# =====================================================
# REMOVE EXPIRED VIP (MANUAL CLEANER)
# =====================================================

def remove_expired_vip():

    vip_users = load_json(VIP_FILE, {})
    changed = False

    for user_id in list(vip_users.keys()):
        if time.time() > vip_users[user_id]:
            del vip_users[user_id]
            changed = True

    if changed:
        save_json(VIP_FILE, vip_users)
        # ===============================
# CHANNEL MANAGEMENT
# ===============================

def add_channel(channel_username: str):
    channels = load_channels()

    if channel_username not in channels:
        channels.append(channel_username)
        save_json(CHANNELS_FILE, channels)


def remove_channel(channel_username: str):
    channels = load_channels()

    if channel_username in channels:
        channels.remove(channel_username)
        save_json(CHANNELS_FILE, channels)
