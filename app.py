import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# جلب المتغيرات من إعدادات Koyeb
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")

# إعداد Gemini
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # إرسال النص إلى Gemini
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، واجهت مشكلة في الاتصال بـ Gemini.")

if __name__ == '__main__':
    # التأكد من وجود التوكن قبل البدء
    if not TELEGRAM_TOKEN:
        print("خطأ: TELEGRAM_TOKEN غير موجود في إعدادات البيئة!")
    else:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("جاري تشغيل البوت...")
        app.run_polling()
