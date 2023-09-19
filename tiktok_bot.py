import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from tiktokpy import TikTokPy

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        fr"Hi {user.mention_html()}!",
        reply_markup=None,
    )

# Define the receive TikTok link function
def receive_tiktok_link(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    logger.info(f"Received TikTok link: {url}")
    
    if "tiktok.com" in url:
        try:
            # Use TikTokPy to fetch the TikTok video
            tiktok = TikTokPy(url)
            video_url = tiktok.get_download_url()
            
            logger.info(f"Downloaded TikTok video: {video_url}")

            # Send the video URL back to the user
            update.message.reply_text(f"Download TikTok video: {video_url}")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            update.message.reply_text("An error occurred while fetching the TikTok video.")
    else:
        update.message.reply_text("Please send a valid TikTok link.")

# Define the main function to start the bot
def main() -> None:
    # Initialize the Telegram Updater with your bot's token
    updater = Updater(token="6289957656:AAEfhteomUsA0WqQQDM5LucCrB18Ah_Hmrw", use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Register a command handler for the /start command
    dp.add_handler(CommandHandler("start", start))
    
    # Register a message handler for all messages
    dp.add_handler(MessageHandler(Filters.text, receive_tiktok_link))
    
    # Start the bot
    updater.start_polling()
    
    # Run the bot until you send a signal to stop (e.g., Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()

