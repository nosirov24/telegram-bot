from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_ID, ADMIN_USERNAME
from subscription import add_vip
from languages import LANG
from database import load_json
from config import USERS_FILE


# =====================================================
# VIP MENU
# =====================================================

def vip_menu(t):
    keyboard = [
        [
            InlineKeyboardButton(t["vip_15"], callback_data="vip_buy_15"),
            InlineKeyboardButton(t["vip_30"], callback_data="vip_buy_30"),
        ],
        [
            InlineKeyboardButton(t["back"], callback_data="back")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def vip_admin_approve(user_id, days):
    keyboard = [
        [
            InlineKeyboardButton(
                f"✅ {days} kun berish",
                callback_data=f"vip_confirm_{days}_{user_id}"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# =====================================================
# VIP CALLBACK ROUTER
# =====================================================

async def vip_callback_handler(update, context):

    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    users = load_json(USERS_FILE, {})
    lang = users.get(str(user_id), {}).get("lang", "uz")
    t = LANG[lang]

    # ================= VIP MENU =================
    if data == "menu_vip":

        text = (
            f"💎 <b>{t['vip']}</b>\n\n"
            f"{t['vip_info']}\n\n"
            "Tarifni tanlang:"
        )

        await query.edit_message_text(
            text,
            reply_markup=vip_menu(t),
            parse_mode="HTML"
        )
        return

    # ================= USER PLAN SELECT =================
    if data in ["vip_buy_15", "vip_buy_30"]:

        days = 15 if data == "vip_buy_15" else 30

        payment_text = (
            f"{t['vip_payment']}\n\n"
            f"Tanlangan muddat: {days} kun"
        )

        # Admin ga so‘rov yuboriladi
        await context.bot.send_message(
            ADMIN_ID,
            f"💎 VIP so‘rov\n\nUser ID: {user_id}\nMuddat: {days} kun",
            reply_markup=vip_admin_approve(user_id, days)
        )

        await query.edit_message_text(
            payment_text,
            parse_mode="HTML"
        )
        return

    # ================= ADMIN CONFIRM =================
    if data.startswith("vip_confirm_"):

        # Faqat admin tasdiqlashi mumkin
        if user_id != ADMIN_ID:
            return

        parts = data.split("_")
        days = int(parts[2])
        target_user = int(parts[3])

        add_vip(target_user, days)

        await query.edit_message_text(
            f"✅ {target_user} ga {days} kunlik VIP berildi"
        )

        await context.bot.send_message(
            target_user,
            f"🎉 Sizga {days} kunlik VIP berildi!\nEndi reklamasiz foydalanishingiz mumkin."
        )
        return
