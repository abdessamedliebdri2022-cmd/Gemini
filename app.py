import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# إعداد السجلات (Logs) لرؤية ما يحدث أثناء التشغيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- دمج المفاتيح مباشرة ---
GENAI_API_KEY = "AIzaSyBHZAflStHBjZE8CTHvj2m8ebWN1l3TVa0"
TELEGRAM_TOKEN = "7238817675:AAHLRkPXI9yyXimgiTCk-K1DSJYprVQCiGQ"

# إعداد إعدادات Gemini
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# دالة التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # إرسال النص إلى Gemini والحصول على رد
        response = model.generate_content(user_text)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("لم أتمكن من توليد رد، حاول مرة أخرى.")
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"حدث خطأ: {str(e)}")

if __name__ == '__main__':
    # بناء التطبيق باستخدام التوكن المدمج
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # إضافة معالج الرسائل (يستجيب للرسائل النصية فقط ولا يستجيب للأوامر)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("البوت يعمل الآن... اذهب إلى تلغرام وجربه!")
    application.run_polling()    # إضافة معالج الرسائل
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("البوت يعمل الآن...")
    application.run_polling()
