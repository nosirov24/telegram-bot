from database import load_json, save_json
from config import MOVIES_FILE, MULTFILMS_FILE


# =====================================================
# AUTO CLEAN ENGINE
# =====================================================

async def safe_send_video(update, context, file_id, caption, code, content_type):

    try:
        await update.message.reply_video(
            file_id,
            caption=caption,
            parse_mode="HTML"
        )
        return True

    except Exception:

        # Agar video mavjud bo‘lmasa JSONdan o‘chiradi
        if content_type == "movie":
            movies = load_json(MOVIES_FILE, {})
            if code in movies:
                del movies[code]
                save_json(MOVIES_FILE, movies)

        if content_type == "mult":
            mult = load_json(MULTFILMS_FILE, {})
            if code in mult:
                del mult[code]
                save_json(MULTFILMS_FILE, mult)

        await update.message.reply_text(
            "❌ Kontent mavjud emas yoki o‘chirilgan."
        )

        return False
