import asyncio
from database import load_json
from config import USERS_FILE, ADMIN_ID

BROADCAST_MODE = {}


# =====================================================
# /broadcast COMMAND
# =====================================================

async def broadcast_command(update, context):

    if update.effective_user.id != ADMIN_ID:
        return

    BROADCAST_MODE[ADMIN_ID] = True

    await update.message.reply_text(
        "📢 Broadcast rejimi yoqildi.\n\n"
        "Endi yuboradigan xabaringizni jo‘nating.\n"
        "Text / rasm / video / gif / document mumkin."
    )


# =====================================================
# BROADCAST MESSAGE HANDLER
# =====================================================

async def broadcast_handler(update, context):

    # Kanal post yoki boshqa update bo‘lsa chiqadi
    if not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:
        return

    if not BROADCAST_MODE.get(ADMIN_ID):
        return

    users = load_json(USERS_FILE, {})

    success = 0
    failed = 0

    for user_id in users.keys():
        try:
            await context.bot.copy_message(
                chat_id=int(user_id),
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )

            success += 1
            await asyncio.sleep(0.05)  # Flood protection

        except:
            failed += 1

    BROADCAST_MODE[ADMIN_ID] = False

    await update.message.reply_text(
        f"✅ Yuborildi: {success}\n"
        f"❌ Xatolik: {failed}"
    )
