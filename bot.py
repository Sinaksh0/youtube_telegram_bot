import os 
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🎉 *سلام دوست عزیز!* خوش اومدی به ربات دانلود مستقیم از یوتیوب 🎥\n\n"
        "من اینجام تا هر ویدیویی که داخل یوتیوب هست رو با کیفیت دلخواه برات دانلود کنم، از *1080p* تا *144p*، سریع و بی‌دردسر! ⚡️\n\n"
        "📌 فقط کافیه لینک ویدیوی یوتیوب رو برام بفرستی، من بقیه‌ش رو هندل می‌کنم 😎\n\n"
        "برای شروع، لینک رو بفرست یا از دکمه‌های پایین استفاده کن 👇"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

    
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    URL = update.message.text
    
    if "youtube.com" in URL or "youtu.be" in URL:
        context.user_data["video_url"] = URL
        
        Keyboard = [
            [InlineKeyboardButton("🎥 1080p", callback_data="1080p")],
            [InlineKeyboardButton("🎥 720p", callback_data="720p")],
            [InlineKeyboardButton("🎥 480p", callback_data="480p")],
            [InlineKeyboardButton("🎥 360p", callback_data="360p")],
            [InlineKeyboardButton("🎧 فقط صدا (MP3)", callback_data="audio")]
            ]
        reply_markup = InlineKeyboardMarkup(Keyboard)
        await update.message.reply_text("لطفاً کیفیت مورد نظر رو انتخاب کن:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("ل⚠️ این لینک یوتیوب نیست! لطفاً یه لینک معتبر بفرست.")
        
async def handle_qulity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    URL = context.user_data.get("video_url")
    if not URL:
        await query.edit_message_text("❌ لینک پیدا نشد. لطفاً دوباره لینک رو بفرست.")
        return
    
    await query.edit_message_text("⏳ در حال دانلود با کیفیت انتخابی... لطفاً صبر کن.")
    
    try:
        choice = query.data
        if choice == "1080p":
            format_code = "bestvideo[height<=1080]+bestaudio/best"
        elif choice == "720p":
               format_code = "bestvideo[height<=720]+bestaudio/best"
        elif choice == "480p":
            format_code = "bestvideo[height<=480]+bestaudio/best"
        elif choice == "360p":
            format_code = "bestvideo[height<=360]+bestaudio/best"
        elif choice == "audio":
            format_code = "bestaudio"
        else:
            format_code = "best"
        
        filepath = download_youtube(URL, format_code)
        await query.message.reply_text(f"📁 فایل آماده شد: {filepath}")
        await query.message.reply_document(document=open(filepath, "rb"))
    except Exception as e:
        await query.message.reply_text(f"❌ خطا در دانلود یا ارسال فایل: {e}")
    
    
def download_youtube(URL,format_code='best'):
    you_form = {
        'format': format_code,
        'ffmpeg_location': r'C:\Users\shrqy\Downloads\ABDM\Compressed\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe',
        'outtmpl': 'download_video.%(ext)s',
        'quiet': True
        }
    with YoutubeDL(you_form) as ydl:
        info = ydl.extract_info(URL, download=True)
        filename = ydl.prepare_filename(info)
        return filename

TOKEN = os.getenv("TELEGRAM_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(handle_qulity))

app.run_polling()
