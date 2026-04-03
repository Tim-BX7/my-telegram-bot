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
DEVELOPER_USERNAME = "Oday2_4"  # اسم المستخدم حقك

# ========= قراءة قاعدة البيانات =========
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

# ========= إضافة زر التواصل مع المطور =========
# نضيف الزر الجديد للقائمة الرئيسية فقط
MAIN_MENU_BUTTONS = list(DATA.keys()) + ["📞 تواصل مع المطور"]

# ========= مسار المستخدم داخل القوائم =========
user_path = {}

# ========= دوال مساعدة =========
def kb(options, back=True, is_main=False):
    opts = list(options)
    rows = [opts[i:i+2] for i in range(0, len(opts), 2)]
    if back and not is_main:
        rows.append(["⬅️ رجوع", "🏠 الرئيسية"])
    elif back and is_main:
        rows.append(["🏠 الرئيسية"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

def get_node(path):
    node = DATA
    for p in path:
        if isinstance(node, dict) and p in node:
            node = node[p]
        else:
            return DATA
    return node

# ========= دالة التواصل مع المطور =========
async def contact_developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or "لا يوجد يوزر"
    first_name = update.effective_user.first_name or ""
    
    # إنشاء زر للتواصل
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 مراسلة المطور", url=f"https://t.me/{DEVELOPER_USERNAME}")],
        [InlineKeyboardButton("💬 إرسال رسالة مباشرة", url=f"tg://user?id={ADMIN_ID}")]
    ])
    
    await update.message.reply_text(
        f"👨‍💻 **للتواصل مع المطور:**\n\n"
        f"• للإبلاغ عن مشكلة\n"
        f"• للاقتراحات والتطوير\n"
        f"• للاستفسارات\n\n"
        f"اضغط على الزر أدناه للتواصل 📩",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    
    # إرسال إشعار للمطور أن أحد المستخدمين يريد التواصل
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📢 **طلب تواصل جديد**\n\n"
                 f"👤 المستخدم: {first_name}\n"
                 f"🆔 ID: `{uid}`\n"
                 f"📝 اليوزر: @{username}\n"
                 f"⏰ الوقت: {asyncio.get_event_loop().time()}",
            parse_mode="Markdown"
        )
    except:
        pass

# ========= دالة الإحصائيات =========
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    # عدد المستخدمين
    if not os.path.exists(USER_FILE):
        users_count = 0
    else:
        with open(USER_FILE, "r") as f:
            users_count = len(f.read().splitlines())
    
    # عدد الملفات في قاعدة البيانات
    def count_files(node):
        if isinstance(node, list):
            return len(node)
        elif isinstance(node, dict):
            return sum(count_files(v) for v in node.values())
        return 0
    
    files_count = count_files(DATA)
    
    await update.message.reply_text(
        f"📊 إحصائيات البوت:\n"
        f"👥 عدد المستخدمين: {users_count}\n"
        f"📁 عدد الملفات: {files_count}\n"
        f"📂 عدد التصنيفات: {len(DATA)}"
    )

# ========= دالة البحث =========
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joined = await force_join(update, context)
    if not joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 اشترك بالقناة", url=CHANNEL_LINK)]
        ])
        await update.message.reply_text("🚨 اشترك بالقناة أولاً", reply_markup=keyboard)
        return
    
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("🔍 استخدم: /search اسم_الملف\nمثال: /search رياضيات")
        return
    
    results = []
    def search_in_node(node, path=""):
        if isinstance(node, list):
            for name, _ in node:
                if query.lower() in name.lower():
                    results.append((path, name))
        elif isinstance(node, dict):
            for k, v in node.items():
                search_in_node(v, f"{path}/{k}" if path else k)
    
    search_in_node(DATA)
    
    if results:
        msg = "🔍 نتائج البحث:\n\n"
        for path, name in results[:10]:
            msg += f"📁 {path} → {name}\n"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ لا توجد نتائج مطابقة")

# ========= دالة النسخ الاحتياطي =========
async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    backup_file = f"backup_{int(asyncio.get_event_loop().time())}.json"
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(DATA, f, ensure_ascii=False, indent=2)
    
    with open(backup_file, "rb") as f:
        await update.message.reply_document(f, filename=backup_file)
    
    os.remove(backup_file)
    await update.message.reply_text("✅ تم إنشاء النسخة الاحتياطية")

# ========= دوال البوت الأساسية =========
async def force_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joined = await force_join(update, context)
    if not joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 اشترك بالقناة", url=CHANNEL_LINK)]
        ])
        await update.message.reply_text(
            "🚨 لازم تشترك بالقناة أولاً حتى تستخدم البوت",
            reply_markup=keyboard
        )
        return

    uid = update.effective_user.id
    user_path[uid] = []

    # تسجيل المستخدم
    try:
        with open(USER_FILE, "a+") as f:
            f.seek(0)
            users = f.read().splitlines()
            if str(uid) not in users:
                f.write(str(uid) + "\n")
                # ترحيب للمستخدم الجديد
                await update.message.reply_text(
                    "🎉 اهلاً بك في البوت!\n"
                    "يمكنك تصفح الملفات حسب التصنيفات\n"
                    "📞 يمكنك التواصل مع المطور من القائمة الرئيسية"
                )
    except:
        pass

    await update.message.reply_text(
        "🔥 أهلاً بك في بوت الملخصات\nاختر السنة:",
        reply_markup=kb(MAIN_MENU_BUTTONS, False, True)
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

    joined = await force_join(update, context)
    if not joined:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 اشترك بالقناة", url=CHANNEL_LINK)]
        ])
        await update.message.reply_text(
            "🚨 اشترك بالقناة حتى تستخدم البوت",
            reply_markup=keyboard
        )
        return
    
    if uid not in user_path:
        user_path[uid] = []
    
    path = user_path[uid]

    # 🔹 معالج زر التواصل مع المطور
    if text == "📞 تواصل مع المطور":
        await contact_developer(update, context)
        return

    if text == "🏠 الرئيسية":
        user_path[uid] = []
        await update.message.reply_text("الرئيسية", reply_markup=kb(MAIN_MENU_BUTTONS, False, True))
        return

    if text == "⬅️ رجوع":
        if path:
            path.pop()
        node = get_node(path)
        is_main = len(path) == 0
        if is_main:
            await update.message.reply_text("الرئيسية", reply_markup=kb(MAIN_MENU_BUTTONS, False, True))
        else:
            await update.message.reply_text("رجوع", reply_markup=kb(node.keys(), not is_main))
        return

    node = get_node(path)

    if isinstance(node, dict):
        if text in node:
            path.append(text)
            new_node = node[text]

            if isinstance(new_node, list):
                await update.message.reply_text("اختر الملف لتحميله:", reply_markup=kb([n for n, _ in new_node]))
            else:
                await update.message.reply_text(f"تم اختيار {text}:", reply_markup=kb(new_node.keys()))
        else:
            await update.message.reply_text("يرجى اختيار أحد الأزرار الظاهرة.")

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

# ========= دالة الحصول على file_id عن طريق الرد =========
async def get_file_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # فقط للأدمن
    if update.effective_user.id != ADMIN_ID:
        return
    
    # يتأكد أن المستخدم رد على رسالة
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ قم بالرد على الملف الذي تريد معرفة file_id خاص به\n\nالطريقة: /fileid ثم الرد على الملف")
        return
    
    replied_msg = update.message.reply_to_message
    
    if replied_msg.document:
        file_id = replied_msg.document.file_id
        await update.message.reply_text(f"📄 file_id:\n`{file_id}`", parse_mode="Markdown")
    elif replied_msg.photo:
        file_id = replied_msg.photo[-1].file_id
        await update.message.reply_text(f"🖼 file_id:\n`{file_id}`", parse_mode="Markdown")
    elif replied_msg.video:
        file_id = replied_msg.video.file_id
        await update.message.reply_text(f"🎥 file_id:\n`{file_id}`", parse_mode="Markdown")
    elif replied_msg.audio:
        file_id = replied_msg.audio.file_id
        await update.message.reply_text(f"🎵 file_id:\n`{file_id}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ هذا ليس ملفاً مدعوماً (الملفات المدعومة: مستند، صورة، فيديو، صوت)")

# ========= تشغيل البوت =========
if __name__ == "__main__":
    if not TOKEN:
        print("خطأ: لم يتم العثور على TOKEN! أضفه في متغيرات البيئة.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # أوامر البوت
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("bc", broadcast))
        app.add_handler(CommandHandler("stats", stats))
        app.add_handler(CommandHandler("search", search))
        app.add_handler(CommandHandler("backup", backup))
        app.add_handler(CommandHandler("fileid", get_file_id_command))

        # معالجات الرسائل
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
        
        print("--- BOT IS RUNNING ---")
        app.run_polling()
