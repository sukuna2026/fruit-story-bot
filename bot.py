import telebot

TOKEN = "8855216335:AAGSXKbO-ORrVjgdc31z-QudEqrHPptolgM"
ADMIN_ID = 6023326430

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("🎬 طلب فيديو AI")
    markup.row("🖼 إنشاء صورة AI")
    markup.row("💰 الأسعار")
    markup.row("📁 معرض الأعمال")
    markup.row("📞 التواصل مع الإدارة")

    bot.send_message(
        message.chat.id,
        "مرحباً بك في متجر خدمات الذكاء الاصطناعي 🤖",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "💰 الأسعار")
def prices(message):

    bot.send_message(
        message.chat.id,
        """
💰 الأسعار

🎬 فيديو قصير: 5$

🎬 فيديو احترافي 15$

🖼 صورة AI: 1$

✨ تحسين Prompt: 1$
"""
    )

@bot.message_handler(func=lambda m: m.text == "📁 معرض الأعمال")
def gallery(message):

    bot.send_message(
        message.chat.id,
        """
📁 معرض الأعمال

✅ الطلبات المنجزة: 125

👥 العملاء: 78

⭐ التقييم: 4.9/5
"""
    )

@bot.message_handler(func=lambda m: m.text == "🎬 طلب فيديو AI")
def order_video(message):

    msg = bot.send_message(
        message.chat.id,
        "اكتب فكرة الفيديو أو القصة:"
    )

    bot.register_next_step_handler(
        msg,
        get_video_story
    )

def get_video_story(message):

    user_data[message.chat.id] = {
        "story": message.text
    }

    msg = bot.send_message(
        message.chat.id,
        "اكتب مدة الفيديو المطلوبة:"
    )

    bot.register_next_step_handler(
        msg,
        get_video_duration
    )

def get_video_duration(message):

    story = user_data[message.chat.id]["story"]

    duration = message.text

    bot.send_message(
        ADMIN_ID,
        f"""
📥 طلب فيديو جديد

👤 المستخدم:
{message.from_user.first_name}

🆔:
{message.from_user.id}

📝 القصة:
{story}

⏱ المدة:
{duration}
"""
    )

    bot.send_message(
        message.chat.id,
        "✅ تم إرسال طلبك للإدارة بنجاح."
    )

@bot.message_handler(func=lambda m: m.text == "🖼 إنشاء صورة AI")
def image_request(message):

    msg = bot.send_message(
        message.chat.id,
        "اكتب وصف الصورة:"
    )

    bot.register_next_step_handler(
        msg,
        get_image_prompt
    )

def get_image_prompt(message):

    bot.send_message(
        ADMIN_ID,
        f"""
🖼 طلب صورة جديد

👤 {message.from_user.first_name}

📝 الوصف:

{message.text}
"""
    )

    bot.send_message(
        message.chat.id,
        "✅ تم إرسال طلب الصورة."
    )

@bot.message_handler(func=lambda m: m.text == "📞 التواصل مع الإدارة")
def support(message):

    msg = bot.send_message(
        message.chat.id,
        "اكتب رسالتك للإدارة:"
    )

    bot.register_next_step_handler(
        msg,
        send_to_admin
    )

def send_to_admin(message):

    bot.send_message(
        ADMIN_ID,
        f"""
📨 رسالة جديدة

👤 {message.from_user.first_name}

🆔 {message.from_user.id}

{message.text}
"""
    )

    bot.send_message(
        message.chat.id,
        "✅ تم إرسال الرسالة."
    )

print("Bot Started...")

bot.infinity_polling()


def get_characters(message):

    user_data[message.chat.id]["characters"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "🎬 كم عدد الأجزاء؟"
    )

    bot.register_next_step_handler(
        msg,
        get_parts
    )


def get_parts(message):

    user_data[message.chat.id]["parts"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "⏱ كم ثانية لكل جزء؟"
    )

    bot.register_next_step_handler(
        msg,
        get_duration
    )


def get_duration(message):

    user_data[message.chat.id]["duration"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "📖 اكتب القصة أو الفكرة كاملة:"
    )

    bot.register_next_step_handler(
        msg,
        finish_order
    )


def finish_order(message):

    user_data[message.chat.id]["story"] = message.text

    data = user_data[message.chat.id]

    has_discount = (
        message.from_user.id
        in discount_users
    )

    price = calculate_price(
        data["parts"],
        has_discount
    )

    username = message.from_user.username

    if username:
        username = "@" + username
    else:
        username = "لا يوجد"

    order_text = f"""
📥 طلب جديد

👤 العميل:
{message.from_user.first_name}

🔗 اليوزر:
{username}

🆔 ID:
{message.from_user.id}

🎬 العنوان:
{data['title']}

🎭 النوع:
{data['type']}

👥 الشخصيات:
{data['characters']}

🎞 عدد الأجزاء:
{data['parts']}

⏱ مدة الجزء:
{data['duration']}

📖 القصة:
{data['story']}

💰 السعر:
{price}$
"""

    bot.send_message(
        ADMIN_ID,
        order_text
    )

    bot.send_message(
        message.chat.id,
        f"""
✅ تم إرسال الطلب بنجاح

💰 السعر النهائي:
{price}$

📞 للتواصل:
@MohamedAminAi
"""
    )

print("Bot Started...")
bot.infinity_polling()