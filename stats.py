from config import USERS_FILE, VIP_FILE, CHANNELS_FILE, ADMIN_ID
from database import load_json
import time


# =====================================================
# STATS COMMAND
# =====================================================

async def stats_command(update, context):

    if update.effective_user.id != ADMIN_ID:
        return

    users = load_json(USERS_FILE, {})
    vip_users = load_json(VIP_FILE, {})
    channels = load_json(CHANNELS_FILE, [])

    total_users = len(users)
    total_channels = len(channels)

    # Active VIP hisoblash
    active_vip = 0
    now = time.time()

    for expire_time in vip_users.values():
        if expire_time > now:
            active_vip += 1

    expired_vip = len(vip_users) - active_vip

    text = (
        "📊 <b>BOT STATISTIKASI</b>\n\n"
        f"👤 Umumiy foydalanuvchilar: <b>{total_users}</b>\n"
        f"💎 Aktiv VIP: <b>{active_vip}</b>\n"
        f"⌛ Tugagan VIP: <b>{expired_vip}</b>\n"
        f"📢 Majburiy kanallar: <b>{total_channels}</b>\n"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )
