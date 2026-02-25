import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# إعداد السجلات (Logs)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إعداد إعدادات Gemini
# تأكد من إضافة API_KEY في إعدادات Koyeb
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# دالة التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # إرسال النص إلى Gemini والحصول على رد
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك.")

if __name__ == '__main__':
    # الحصول على التوكن من بيئة التشغيل
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة معالج الرسائل
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("البوت يعمل الآن...")
    application.run_polling()
