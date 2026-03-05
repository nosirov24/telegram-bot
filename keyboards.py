from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from subscription import load_channels

def subscription_menu(t):
    channels = load_channels()

    keyboard = []

    for ch in channels:
        url = f"https://t.me/{ch.replace('@','')}"
        keyboard.append([InlineKeyboardButton(ch, url=url)])

    keyboard.append([InlineKeyboardButton("✅ A'zolikni tekshirish", callback_data="check_sub")])
    keyboard.append([InlineKeyboardButton("⬅ Orqaga", callback_data="back")])

    return InlineKeyboardMarkup(keyboard)


# =====================================================
# MAIN MENU
# =====================================================

def main_menu(t):

    keyboard = [
        [
            InlineKeyboardButton(t["kino"], callback_data="menu_movie"),
            InlineKeyboardButton(t["mult"], callback_data="menu_mult"),
        ],
        [
            InlineKeyboardButton(t["vip"], callback_data="menu_vip"),
        ],
        [
            InlineKeyboardButton(t["lang"], callback_data="menu_lang"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =====================================================
# LANGUAGE MENU
# =====================================================

def language_menu():

    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 Uzbek", callback_data="set_lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru"),
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =====================================================
# VIP MENU
# =====================================================

def vip_menu(t):

    keyboard = [
        [
            InlineKeyboardButton(t["vip_15"], callback_data="vip_15"),
            InlineKeyboardButton(t["vip_30"], callback_data="vip_30"),
        ],
        [
            InlineKeyboardButton(t["back"], callback_data="back")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =====================================================
# BACK BUTTON ONLY
# =====================================================

def back_button(t):

    keyboard = [
        [
            InlineKeyboardButton(t["back"], callback_data="back")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
