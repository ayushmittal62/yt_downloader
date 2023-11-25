import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube

TOKEN = "6933069021:AAFUVL1Tj00nNasQTmlZcZKovrZfoP7yqEI"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please send a YouTube video URL.')

def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        download_youtube_video(url)
        update.message.reply_text(f"Downloaded video from {url}")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def download_youtube_video(url):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    if video is None:
        print("Cannot find a suitable video.")
        return
    print(f"Downloading video '{video.title}' from '{yt.title}'")
    video.download(output_path="videos")
    print(f"Downloaded video '{video.title}'")

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()