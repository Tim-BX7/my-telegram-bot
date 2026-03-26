import os
import json
import asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import BadRequest

# ========= إعدادات البوت =========
TOKEN = os.getenv("TOKEN")

CHANNEL_ID = "@It_2028"
CHANNEL_LINK = "https://t.me/It_2028"

ADMIN_ID = 7554028181
USER_FILE = "users.txt"

# ========= قراءة قاعدة البيانات =========
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

# ========= مسار المستخدم داخل القوائم =========
user_path = {}
def kb(options, back=True):
    opts = list(options)
    # ترتيب الأزرار في صفوف (كل صف فيه زرين)
    rows = [opts[i:i+2] for i in range(0, len(opts), 2)]
    if back:
        rows.append(["⬅️ رجوع", "🏠 الرئيسية"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def get_node(path):
    node = DATA
    for p in path:
        # التأكد أن المفتاح موجود لتجنب انهيار البوت
        if isinstance(node, dict) and p in node:
            node = node[p]
        else:
            return DATA # العودة للبداية في حال حدوث خطأ
    return node

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_path[uid] = []

    # تسجيل المستخدم للإذاعة
    try:
        with open(USER_FILE, "a+") as f:
            f.seek(0)
            users = f.read().splitlines()
            if str(uid) not in users:
                f.write(str(uid) + "\n")
    except:
        pass

    await update.message.reply_text(
        "🔥 تم تحديث البوت\n"
        "الرجاء الضغط على القوائم من جديد ❤️",
        reply_markup=kb(DATA.keys(), False)
    )
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = "🔥 تم تطوير البوت\n\nالرجاء الضغط على /start من جديد لتحديث القوائم ❤️"

    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()

    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()

    total = len(users)
    sent = 0
    failed = 0

    msg = await update.message.reply_text(f"📡 بدء الإذاعة...\n0 / {total}")

    for i, user in enumerate(users, start=1):
        try:
            await context.bot.send_message(
                chat_id=int(user),
                text=text
            )
            sent += 1
        except:
            failed += 1

        # تحديث العداد كل 10 مستخدمين
        if i % 10 == 0 or i == total:
            try:
                await msg.edit_text(
                    f"📡 الإذاعة قيد الإرسال...\n"
                    f"✅ تم الإرسال: {sent}\n"
                    f"❌ فشل: {failed}\n"
                    f"📊 التقدم: {i} / {total}"
                )
            except:
                pass

        await asyncio.sleep(0.06)

    await msg.edit_text(
        f"✅ انتهت الإذاعة بنجاح\n\n"
        f"📤 تم الإرسال: {sent}\n"
        f"🚫 فشل: {failed}\n"
        f"👥 العدد الكلي: {total}"
    )

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    
    # التأكد أن المستخدم مسجل في الذاكرة، وإلا نبدأ من البداية
    if uid not in user_path:
        user_path[uid] = []
    
    path = user_path[uid]

    # العودة للرئيسية
    if text == "🏠 الرئيسية":
        user_path[uid] = []
        await update.message.reply_text("الرئيسية", reply_markup=kb(DATA.keys(), False))
        return

    # العودة للخلف
    if text == "⬅️ رجوع":
        if path:
            path.pop()
        node = get_node(path)
        is_main = len(path) == 0
        await update.message.reply_text("رجوع", reply_markup=kb(node.keys(), not is_main))
        return

    node = get_node(path)

    # إذا كانت القائمة الحالية عبارة عن تصنيفات (أزرار)
    if isinstance(node, dict):
        if text in node:
            path.append(text)
            new_node = node[text]

            if isinstance(new_node, list): # إذا وصلنا لقائمة الملفات
                await update.message.reply_text("اختر الملف لتحميله:", reply_markup=kb([n for n, _ in new_node]))
            else: # إذا دخلنا في تصنيف فرعي آخر
                await update.message.reply_text(f"تم اختيار {text}:", reply_markup=kb(new_node.keys()))
        else:
            await update.message.reply_text("يرجى اختيار أحد الأزرار الظاهرة.")

    # إذا كانت القائمة الحالية عبارة عن ملفات (إرسال مستند)
    elif isinstance(node, list):
        file_id = None
        for n, f in node:
            if text == n:
                file_id = f
                break
        
        if file_id:
            await update.message.reply_document(file_id)
        else:
            await update.message.reply_text("الملف غير موجود، يرجى الاختيار من القائمة.")

    user_path[uid] = path

if __name__ == "__main__":
    if not TOKEN:
        print("خطأ: لم يتم العثور على TOKEN! أضفه في متغيرات البيئة.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("bc", broadcast))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
        print("--- BOT IS RUNNING ---")
        app.run_polling()
