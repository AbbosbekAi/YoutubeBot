import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
import yt_dlp

TOKEN = "7512648492:AAHnbwJySnowJjFBos79duaeIk20ymL6Gq8"

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def send_welcome(message: types.Message):
    await message.reply("Salom! Men @TurboYTBot👋!\n"
                        "Mening imkoniyatlarim: Youtubedan videolar yuklab beraolaman📩\n"
                        "Mening hozirgi versiyam: 0.2 medium🤖")
    
@dp.message(F.text == "/help")
async def send_help(message: types.Message):
    await message.reply("Bot bo'yicha savollar bo'lsa!\n"
                        "Telegram orqali @zuPREDATOR👨‍💻\n"
                        "Kamchiliklar uchun uzr!❤️")
    
@dp.message(F.text == "/info")
async def send_info(message: types.Message):
    await message.reply("Botning hozirgi versiyasi: 0.2 medium\n"
                        "Sana: 2025.03.29\n"
                        "Bot 50mb yuqori videolarni yuklab beraolmaydi!")

# Chat uchun funksiyalar
@dp.message(F.text.lower().in_(["salom", "hi", "assalomu alaykum"]))
async def chat_greeting(message: types.Message):
    await message.reply("Salom! Men TuboYTBot man men sizga youtubedan video yuklashga yordam beraman!")

@dp.message(F.text.lower().in_(["qanday funksiyalaring bor?", "nimalar qila olasan", "nima qila olasan"]))
async def chat_functions(message: types.Message):
    await message.reply("Men quyidagi funksiyalarni bajara olaman:\n"
                        "1️⃣ YouTube videolarini yuklab berish. | versiya: 0.1 slow\n"
                        "2️⃣ MP3 formatda yuklab berish. | versiya: 0.3 high\n"
                        "3️⃣ Instagram va Tiktokdan video yuklab olish. | versiya: 0.4 medium")

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def download_youtube_video(message: types.Message):
    url = message.text
    status_message = await message.reply("⏳ Yuklab olinmoqda, biroz kuting...")

    video_filename = f"video_{random.randint(1000, 9999)}.mp4"
    ydl_opts = {
        "format": "best",  # YouTube video formatini eng yuqori sifatga o'rnatamiz
        "outtmpl": video_filename,  # Video nomini o'zgaruvchan qilish
        "cookies": "cookies.txt",  # COOKIE faylini ulash
        "logger": logger,  # Log yozish
        "progress_hooks": [lambda d: logger.info(f"Progress: {d['status']} {d.get('filename', '')}")]  # Progressni loglash
    }

    try:
        # yt-dlp bilan video yuklash
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = FSInputFile(video_filename)
        await bot.delete_message(chat_id=message.chat.id, message_id=status_message.message_id)
        await message.answer_video(video_file)

    except Exception as e:
        logger.error(f"Video yuklashda xatolik: {e}", exc_info=True)
        await message.reply(f"❌ Xatolik yuz berdi: {e}")

    finally:
        if os.path.exists(video_filename):
            os.remove(video_filename)  # Faylni avtomatik o‘chirish

# Botni ishga tushirish
async def main():
    try:
        logger.info("🚀 Bot ishga tushdi!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Xatolik yuz berdi: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("🔴 Bot o'chirildi.")

# Asosiy funksiyani ishga tushirish
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("🛑 Bot majburan to‘xtatildi.")
