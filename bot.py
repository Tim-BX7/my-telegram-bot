import os
import json
import asyncio
import logging
import sqlite3
from datetime import datetime
from functools import wraps
 
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import TelegramError
 
# ========= إعداد اللوغ =========
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
 
# ========= إعدادات البوت =========
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7554028181
DEVELOPER_USERNAME = "Oday2_4"
CHANNEL_USERNAME = "@It_2028"  # ← غيّر هذا لاسم قناتك
 
# ========= قاعدة بيانات SQLite =========
def init_db():
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TEXT,
            last_seen TEXT,
            request_count INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
 
def add_or_update_user(uid: int, username: str, first_name: str):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO users (uid, username, first_name, joined_at, last_seen)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(uid) DO UPDATE SET
            username=excluded.username,
            first_name=excluded.first_name,
            last_seen=excluded.last_seen,
            request_count = request_count + 1
    """, (uid, username, first_name, now, now))
    conn.commit()
    conn.close()
 
def get_user_count() -> int:
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count
 
def is_banned(uid: int) -> bool:
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT is_banned FROM users WHERE uid=?", (uid,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == 1
 
def ban_user(uid: int):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned=1 WHERE uid=?", (uid,))
    conn.commit()
    conn.close()
 
def unban_user(uid: int):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned=0 WHERE uid=?", (uid,))
    conn.commit()
    conn.close()
 
def get_all_users() -> list:
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT uid FROM users WHERE is_banned=0")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users
 
def get_top_users(limit=10) -> list:
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("""
        SELECT uid, first_name, username, request_count
        FROM users ORDER BY request_count DESC LIMIT ?
    """, (limit,))
    users = c.fetchall()
    conn.close()
    return users
 
# ========= تحميل البيانات =========
def load_data() -> dict:
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("data.json غير موجود!")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"خطأ في data.json: {e}")
        return {}
 
DATA = load_data()
 
# ========= مسار المستخدم =========
user_path = {}
 
# ========= Decorator للأمان =========
def secure_handler(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user or not update.message:
            return
        uid = update.effective_user.id
        if is_banned(uid):
            await update.message.reply_text("🚫 أنت محظور من استخدام البوت.")
            return
        return await func(update, context)
    return wrapper
 
# ========= دوال مساعدة =========
def kb(options, back=True, is_main=False):
    opts = list(options)
    rows = [opts[i:i+2] for i in range(0, len(opts), 2)]
    if back and not is_main:
        rows.append(["⬅️ رجوع", "🏠 الرئيسية"])
    elif is_main:
        rows.append(["🏠 الرئيسية"])
    rows.append(["📞 تواصل مع المطور"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)
 
def get_node(path):
    node = DATA
    for p in path:
        if isinstance(node, dict) and p in node:
            node = node[p]
        else:
            return DATA
    return node
 
# ========= التواصل مع المطور =========
async def contact_developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or "لا يوجد"
    first_name = update.effective_user.first_name or ""
 
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 مراسلة المطور", url=f"https://t.me/{DEVELOPER_USERNAME}")],
        [InlineKeyboardButton("💬 إرسال رسالة مباشرة", url=f"tg://user?id={ADMIN_ID}")]
    ])
 
    await update.message.reply_text(
        "👨‍💻 *للتواصل مع المطور:*\n\n"
        "• الإبلاغ عن مشكلة\n"
        "• الاقتراحات والتطوير\n"
        "• الاستفسارات\n\n"
        "اضغط على الزر أدناه 📩",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
 
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📢 *طلب تواصل جديد*\n\n"
                 f"👤 الاسم: {first_name}\n"
                 f"🆔 ID: `{uid}`\n"
                 f"📝 اليوزر: @{username}\n"
                 f"🕐 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode="Markdown"
        )
    except TelegramError:
        pass
 
# ========= /start =========
@secure_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or ""
    first_name = update.effective_user.first_name or ""
 
    add_or_update_user(uid, username, first_name)
    user_path[uid] = []
 
    await update.message.reply_text(
        f"🔥 أهلاً *{first_name}* في بوت الملخصات!\nاختر السنة:",
        reply_markup=kb(list(DATA.keys()), False, True),
        parse_mode="Markdown"
    )
 
# ========= /search =========
@secure_handler
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).strip()
    if not query:
        await update.message.reply_text(
            "🔍 الاستخدام: `/search اسم_الملف`\nمثال: `/search رياضيات`",
            parse_mode="Markdown"
        )
        return
 
    results = []
 
    def search_in_node(node, path=""):
        if isinstance(node, list):
            for name, _ in node:
                if query.lower() in name.lower():
                    results.append((path, name))
        elif isinstance(node, dict):
            for k, v in node.items():
                search_in_node(v, f"{path} ← {k}" if path else k)
 
    search_in_node(DATA)
 
    if results:
        msg = f"🔍 نتائج البحث عن *{query}*:\n\n"
        for path, name in results[:10]:
            msg += f"📁 `{path}` → {name}\n"
        if len(results) > 10:
            msg += f"\n_...و {len(results)-10} نتيجة أخرى_"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ لا توجد نتائج لـ *{query}*", parse_mode="Markdown")
 
# ========= /stats (أدمن) =========
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
 
    def count_files(node):
        if isinstance(node, list):
            return len(node)
        elif isinstance(node, dict):
            return sum(count_files(v) for v in node.values())
        return 0
 
    top_users = get_top_users(5)
    top_text = "\n".join([
        f"  {i+1}. {u[1]} (@{u[2] or 'N/A'}) — {u[3]} طلب"
        for i, u in enumerate(top_users)
    ])
 
    await update.message.reply_text(
        f"📊 *إحصائيات البوت:*\n\n"
        f"👥 المستخدمون: `{get_user_count()}`\n"
        f"📁 الملفات: `{count_files(DATA)}`\n"
        f"📂 التصنيفات: `{len(DATA)}`\n\n"
        f"🏆 *الأكثر نشاطاً:*\n{top_text}",
        parse_mode="Markdown"
    )
 
# ========= /ban و /unban (أدمن) =========
async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("الاستخدام: `/ban USER_ID`", parse_mode="Markdown")
        return
    try:
        target = int(context.args[0])
        ban_user(target)
        await update.message.reply_text(f"✅ تم حظر المستخدم `{target}`", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ ID غير صالح")
 
async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("الاستخدام: `/unban USER_ID`", parse_mode="Markdown")
        return
    try:
        target = int(context.args[0])
        unban_user(target)
        await update.message.reply_text(f"✅ تم رفع الحظر عن `{target}`", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ ID غير صالح")
 
# ========= /broadcast (أدمن) =========
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
 
    custom_text = " ".join(context.args) if context.args else None
    text = custom_text or (
        "📚 *مرحباً بالجميع!*\n\n"
        "جرّبوا البوت وشوفوا شو عنا من ملفات 🎓\n\n"
        "📌 البوت فيه ملفات المكاتب، وقريباً رح نضيف كمان ملفات الدكاترة!\n\n"
        "📢 متابعين قناتنا؟ كل جديد بينزل عليها أولاً:\n"
        f"{CHANNEL_USERNAME}\n\n"
        "إذا واجهتوا أي مشكلة أو عندكم اقتراح، تواصلوا مع الأدمن مباشرة من داخل البوت 👇\n"
        "اضغطوا على 📞 *تواصل مع المطور*"
    )
 
    users = get_all_users()
    total = len(users)
    sent = failed = 0
 
    msg = await update.message.reply_text(f"📡 بدء الإذاعة...\n0 / {total}")
 
    for i, uid in enumerate(users, start=1):
        try:
            await context.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown")
            sent += 1
        except TelegramError:
            failed += 1
 
        if i % 10 == 0 or i == total:
            try:
                await msg.edit_text(
                    f"📡 *الإذاعة جارية...*\n"
                    f"✅ تم: {sent}\n❌ فشل: {failed}\n📊 {i}/{total}",
                    parse_mode="Markdown"
                )
            except TelegramError:
                pass
 
        await asyncio.sleep(0.05)
 
    await msg.edit_text(
        f"✅ *انتهت الإذاعة*\n\n"
        f"📤 تم الإرسال: {sent}\n"
        f"🚫 فشل: {failed}\n"
        f"👥 الكلي: {total}",
        parse_mode="Markdown"
    )
 
# ========= /backup (أدمن) =========
async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.json"
 
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(DATA, f, ensure_ascii=False, indent=2)
 
    with open(backup_file, "rb") as f:
        await update.message.reply_document(f, filename=backup_file, caption="✅ نسخة احتياطية من data.json")
 
    os.remove(backup_file)
 
    if os.path.exists("bot.db"):
        with open("bot.db", "rb") as f:
            await update.message.reply_document(
                f,
                filename=f"backup_db_{timestamp}.db",
                caption="✅ نسخة احتياطية من قاعدة البيانات"
            )
 
# ========= معالج الملفات =========
async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
 
    # ===== أدمن: احصل على file_id =====
    if uid == ADMIN_ID:
        if update.effective_chat.type != "private":
            return
 
        msg = update.message
        file_id = caption = None
 
        if msg.document:
            file_id = msg.document.file_id
            caption = f"📄 *{msg.document.file_name}*"
        elif msg.photo:
            file_id = msg.photo[-1].file_id
            caption = "🖼 صورة"
        elif msg.video:
            file_id = msg.video.file_id
            caption = "🎥 فيديو"
        elif msg.audio:
            file_id = msg.audio.file_id
            caption = "🎵 صوت"
 
        if file_id:
            await msg.reply_text(
                f"{caption}\n\n*file\\_id:*\n`{file_id}`\n\n✅ انسخه لـ data.json",
                parse_mode="Markdown"
            )
 
    # ===== مستخدم عادي: رفض الملف =====
    else:
        await update.message.reply_text(
            "❌ *لا يمكن رفع ملفات.*\n\n"
            "البوت مخصص فقط لتحميل الملفات الموجودة.\n"
            "إذا عندك اقتراح أو طلب، تواصل مع الأدمن 👇",
            parse_mode="Markdown"
        )
 
# ========= المعالج الرئيسي =========
@secure_handler
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or ""
    first_name = update.effective_user.first_name or ""
    text = update.message.text
 
    add_or_update_user(uid, username, first_name)
 
    if uid not in user_path:
        user_path[uid] = []
 
    path = user_path[uid]
 
    if text == "📞 تواصل مع المطور":
        await contact_developer(update, context)
        return
 
    if text == "🏠 الرئيسية":
        user_path[uid] = []
        await update.message.reply_text(
            "🏠 *الصفحة الرئيسية* — اختر السنة:",
            reply_markup=kb(list(DATA.keys()), False, True),
            parse_mode="Markdown"
        )
        return
 
    if text == "⬅️ رجوع":
        if path:
            path.pop()
        node = get_node(path)
        is_main = len(path) == 0
        if is_main:
            await update.message.reply_text(
                "🏠 *الصفحة الرئيسية* — اختر السنة:",
                reply_markup=kb(list(DATA.keys()), False, True),
                parse_mode="Markdown"
            )
        else:
            keys = node.keys() if isinstance(node, dict) else [n for n, _ in node]
            await update.message.reply_text("⬅️ رجوع:", reply_markup=kb(keys))
        return
 
    node = get_node(path)
 
    if isinstance(node, dict):
        if text in node:
            path.append(text)
            new_node = node[text]
            if isinstance(new_node, list):
                await update.message.reply_text(
                    f"📂 *{text}* — اختر الملف:",
                    reply_markup=kb([n for n, _ in new_node]),
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    f"📂 *{text}* — اختر:",
                    reply_markup=kb(new_node.keys()),
                    parse_mode="Markdown"
                )
        else:
            await update.message.reply_text("⚠️ يرجى الاختيار من الأزرار.")
 
    elif isinstance(node, list):
        file_id = next((f for n, f in node if text == n), None)
        if file_id:
            await update.message.reply_document(
                file_id,
                caption=f"📄 *{text}*",
                parse_mode="Markdown"
            )
            logger.info(f"User {uid} downloaded: {text}")
        else:
            await update.message.reply_text("❌ الملف غير موجود، اختر من القائمة.")
 
    user_path[uid] = path
 
# ========= تشغيل البوت =========
if __name__ == "__main__":
    if not TOKEN:
        logger.error("TOKEN غير موجود! أضفه في متغيرات البيئة.")
    else:
        init_db()
        logger.info("تم تهيئة قاعدة البيانات ✅")
 
        app = ApplicationBuilder().token(TOKEN).build()
 
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("bc", broadcast))
        app.add_handler(CommandHandler("stats", stats))
        app.add_handler(CommandHandler("search", search))
        app.add_handler(CommandHandler("backup", backup))
        app.add_handler(CommandHandler("ban", ban_cmd))
        app.add_handler(CommandHandler("unban", unban_cmd))
 
        # معالج موحد للملفات (أدمن → file_id | مستخدم → رفض)
        app.add_handler(MessageHandler(
            filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO,
            handle_files
        ))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
 
        logger.info("--- BOT IS RUNNING ---")
        app.run_polling()
