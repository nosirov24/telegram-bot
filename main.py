from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import *
from database import load_json, save_json
from languages import LANG
from keyboards import *

from subscription import (
    is_vip,
    remove_expired_vip,
    load_channels
)

from broadcast import broadcast_command, broadcast_handler
from vip import vip_callback_handler
from utils import safe_send_video
from admin import admin_command, admin_callback, admin_text_handler

# =====================================================
# USER SYSTEM
# =====================================================

def get_users():
    return load_json(USERS_FILE, {})


def save_users(data):
    save_json(USERS_FILE, data)


def register_user(user):
    users = get_users()
    if str(user.id) not in users:
        users[str(user.id)] = {"lang": "uz"}
        save_users(users)


def get_lang(user_id):
    users = get_users()
    return users.get(str(user_id), {}).get("lang", "uz")


def set_lang(user_id, lang):
    users = get_users()
    users[str(user_id)] = {"lang": lang}
    save_users(users)


# =====================================================
# SUB CHECK
# =====================================================

async def check_subscription(user_id, context):

    if is_vip(user_id):
        return True

    channels = load_channels()

    for ch in channels:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False

    return True


# =====================================================
# START
# =====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    register_user(user)

    lang = get_lang(user.id)
    t = LANG[lang]

    await update.message.reply_text(
        t["welcome"],
        reply_markup=main_menu(t)
    )


# =====================================================
# CALLBACK
# =====================================================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = get_lang(user_id)
    t = LANG[lang]

    data = query.data

    # LANGUAGE
    if data.startswith("set_lang_"):
        new_lang = data.split("_")[-1]
        set_lang(user_id, new_lang)
        t = LANG[new_lang]

        await query.edit_message_text(
            t["welcome"],
            reply_markup=main_menu(t)
        )
        return

    # VIP
    if data.startswith("vip_") or data == "menu_vip":
        await vip_callback_handler(update, context)
        return

    # MOVIE
    if data == "menu_movie":

        if not await check_subscription(user_id, context):
            await query.edit_message_text(
                t["subscribe"],
                reply_markup=subscription_menu(t)
            )
            return

        await query.edit_message_text(
            t["send_code"],
            reply_markup=back_button(t)
        )
        return

    # MULT
    if data == "menu_mult":

        if not await check_subscription(user_id, context):
            await query.edit_message_text(
                t["subscribe"],
                reply_markup=subscription_menu(t)
            )
            return

        await query.edit_message_text(
            t["send_code"],
            reply_markup=back_button(t)
        )
        return

    # BACK
    if data == "back":
        await query.edit_message_text(
            t["welcome"],
            reply_markup=main_menu(t)
        )
        return


# =====================================================
# MESSAGE HANDLER (RAQAM ONLY - PROFESSIONAL)
# =====================================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("MESSAGE HANDLER ISHLADI")

    user_id = update.effective_user.id
    lang = get_lang(user_id)
    t = LANG[lang]

    remove_expired_vip()

    if not await check_subscription(user_id, context):
        await update.message.reply_text(
            t["subscribe"],
            reply_markup=subscription_menu(t)
        )
        return

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text(t["not_found"])
        return

    number = text

    movies = load_json(MOVIES_FILE, {})
    multfilms = load_json(MULTFILMS_FILE, {})

    # MOVIE SEARCH (case insensitive)
    for key, data in movies.items():
        if key.lower() == f"kino_{number}":
            await update.message.reply_video(
                data["file_id"],
                caption=data.get("caption", ""),
                parse_mode="HTML"
            )
            return

    # MULT SEARCH (case insensitive)
    for key, data in multfilms.items():
        if key.lower() == f"multik_{number}":
            await update.message.reply_video(
                data["file_id"],
                caption=data.get("caption", ""),
                parse_mode="HTML"
            )
            return

    await update.message.reply_text(t["not_found"])
    
    # ================= MOVIE SEARCH (CASE INSENSITIVE) =================
    found_movie_key = None
    for key in movies.keys():
        if key.lower() == movie_key_input:
            found_movie_key = key
            break

    if found_movie_key:
        data = movies[found_movie_key]
        await safe_send_video(
            update,
            context,
            data["file_id"],
            data.get("caption", ""),
            found_movie_key,
            "movie"
        )
        return

    # ================= MULT SEARCH (CASE INSENSITIVE) =================
    found_mult_key = None
    for key in multfilms.keys():
        if key.lower() == mult_key_input:
            found_mult_key = key
            break

    if found_mult_key:
        data = multfilms[found_mult_key]
        await safe_send_video(
            update,
            context,
            data["file_id"],
            data.get("caption", ""),
            found_mult_key,
            "mult"
        )
        return

    await update.message.reply_text(t["not_found"])
# =====================================================
# CHANNEL AUTO SAVE
# =====================================================

async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.channel_post:
        return

    post = update.channel_post

    if not post.caption or not post.video:
        return

    caption = post.caption.strip()
    code = caption.split()[0].lower()

    # MOVIE
    if code.startswith("kino_"):
        movies = load_json(MOVIES_FILE, {})
        movies[code] = {
            "file_id": post.video.file_id,
            "caption": caption
        }
        save_json(MOVIES_FILE, movies)

    # MULT
    if code.startswith("multik_") or code.startswith("mult_"):
        multfilms = load_json(MULTFILMS_FILE, {})
        multfilms[code] = {
            "file_id": post.video.file_id,
            "caption": caption
        }
        save_json(MULTFILMS_FILE, multfilms)


# =====================================================
# APP START
# =====================================================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast_command))
app.add_handler(CommandHandler("admin", admin_command))

app.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))
app.add_handler(CallbackQueryHandler(callback))

#app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, broadcast_handler))
app.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post_handler))

# Admin text handler OLDIN turadi
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text_handler))

# Oddiy user text handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
