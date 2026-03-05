from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_ID
from subscription import load_channels, add_channel, remove_channel

ADMIN_STATE = {}


# =====================================================
# ADMIN MENU
# =====================================================

def admin_menu():
    keyboard = [
        [InlineKeyboardButton("➕ Kanal qo‘shish", callback_data="admin_add_channel")],
        [InlineKeyboardButton("➖ Kanal o‘chirish", callback_data="admin_remove_channel")],
        [InlineKeyboardButton("📋 Kanal ro‘yxati", callback_data="admin_list_channel")]
    ]
    return InlineKeyboardMarkup(keyboard)


# =====================================================
# /admin COMMAND
# =====================================================

async def admin_command(update, context):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "⚙️ ADMIN PANEL",
        reply_markup=admin_menu()
    )


# =====================================================
# ADMIN CALLBACK
# =====================================================

async def admin_callback(update, context):

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data

    if data == "admin_add_channel":
        ADMIN_STATE[query.from_user.id] = "add_channel"
        await query.edit_message_text("Kanal username yuboring (masalan: @kanal)")

    elif data == "admin_remove_channel":
        ADMIN_STATE[query.from_user.id] = "remove_channel"
        await query.edit_message_text("O‘chiriladigan kanal username yuboring")

    elif data == "admin_list_channel":

        channels = load_channels()

        if not channels:
            text = "❌ Kanal mavjud emas"
        else:
            text = "📋 Majburiy kanallar:\n\n" + "\n".join(channels)

        await query.edit_message_text(text)


# =====================================================
# ADMIN TEXT HANDLER
# =====================================================

async def admin_text_handler(update, context):

    if update.effective_user.id != ADMIN_ID:
        return

    state = ADMIN_STATE.get(update.effective_user.id)
    if not state:
        return

    channel = update.message.text.strip()

    if not channel.startswith("@"):
        await update.message.reply_text("❌ Username @ bilan boshlanishi kerak")
        return

    if state == "add_channel":
        add_channel(channel)
        await update.message.reply_text(f"✅ Qo‘shildi: {channel}")

    elif state == "remove_channel":
        remove_channel(channel)
        await update.message.reply_text(f"❌ O‘chirildi: {channel}")

    ADMIN_STATE.pop(update.effective_user.id, None)
