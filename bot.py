import os
import asyncio
import logging
from io import BytesIO
from PIL import Image
from datetime import datetime
import threading
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global Bot Mode
GLOBAL_BOT_MODE = "NORMAL"  # Can be "NORMAL" or "REDIRECT"

# URLs
REGISTER_LINK = "https://tinyurl.com/mstcrbzj"
DM_LINK = "https://t.me/Glucky878"
LOGIN_LINK = "ald6655.com"

# Store user IDs for reminders
active_users = set()

# Video Configuration - Your video file ID
PROMO_VIDEO_ID = "BAACAgQAAxkBAAIE0GpWfmLkPc-4mP2W7PEaS3wYOthcAALoIQACYgiwUsRIo56wMoFLPQQ"
USE_VIDEO_ID = True  # Set to True to use video ID

# Supported image sizes
IMAGE_SIZES = {
    "square": (500, 500),
    "hd": (1920, 1080),
    "instagram": (1080, 1080),
    "facebook": (1200, 630),
    "twitter": (1200, 675),
    "linkedin": (1200, 627),
    "youtube": (1280, 720),
    "thumbnail": (800, 600),
}

# Video file path (fallback if no video ID)
VIDEO_FILE_NAME = "promo.mp4"


async def send_promo_video(update: Update):
    """Send the promotional video to the user."""
    global PROMO_VIDEO_ID, USE_VIDEO_ID
    
    try:
        # Try video ID first (most reliable)
        if USE_VIDEO_ID and PROMO_VIDEO_ID:
            await update.message.reply_video(
                video=PROMO_VIDEO_ID,
                caption="🎰 *GLUCKY87 - EVOLUTION - PRAGMATIC*",
                parse_mode="Markdown"
            )
            logger.info("Video sent using file_id")
            return True
        
        # Try local file
        if os.path.exists(VIDEO_FILE_NAME):
            with open(VIDEO_FILE_NAME, 'rb') as video:
                await update.message.reply_video(
                    video=video,
                    caption="🎰 *GLUCKY87 - EVOLUTION - PRAGMATIC*",
                    parse_mode="Markdown"
                )
            logger.info("Video sent from local file")
            return True
        
        # If neither works, log and continue
        logger.warning(f"No video found: file_id={PROMO_VIDEO_ID}, file={VIDEO_FILE_NAME}")
        return False
        
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        return False


async def send_promo_content(update: Update):
    """Send the promotion text and buttons."""
    promo_text = (
        "😀😀😀 GLUCKY87 😀😀😀\n"
        "BET RM3.60 WIN RM12,873✅\n"
        "ALADDIN99 🎰😎😎😎: Gates Of Olympus 1000💓💓✏️🔡✏️✏️✏️🔠 🔤 : https://tinyurl.com/mstcrbzj\n"
        "https://tinyurl.com/mstcrbzj✏️✏️✏️❤️✏️🌐 : ald6655.com\n"
        "Any Questions ✍️✍️ : @Glucky878\n"
        "🎁 Welcome Bonus 300%🎁 Affiliate System 5%🎁 Daily Rebate 1%\n"
        "💵💵 Online Transfer / FPX / E-Wallet 💵💵💰💰💰🤑🤑✅💰💰💰\n"
        "😀😀😀😀😀😀😀😀😀"
    )
    await update.message.reply_text(promo_text)
    
    # Send buttons
    keyboard = [
        [InlineKeyboardButton("🎰 REGISTER NOW", url=REGISTER_LINK)],
        [InlineKeyboardButton("📩 DM ADMIN", url=DM_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👇 *Click below to register or ask questions:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video uploads - Get video file_id."""
    global PROMO_VIDEO_ID, USE_VIDEO_ID
    
    try:
        video = update.message.video
        file_id = video.file_id
        
        # Get video details
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        
        # Store video ID in memory
        PROMO_VIDEO_ID = file_id
        USE_VIDEO_ID = True
        
        # Send the video ID to user
        response = (
            "✅ *Video Received Successfully!*\n\n"
            f"📹 *Video ID:*\n`{file_id}`\n\n"
            f"📏 *Dimensions:* {width}x{height}\n"
            f"⏱️ *Duration:* {duration} seconds\n"
            f"📦 *File Size:* {file_size / 1024:.2f} KB\n\n"
            "🔑 *To set this as promo video:*\n"
            "Type: `/setvideo` and paste the ID above\n\n"
            "Example:\n"
            f"`/setvideo {file_id}`"
        )
        await update.message.reply_text(
            response,
            parse_mode="Markdown"
        )
        
        # Reply with the video to confirm
        await update.message.reply_video(
            video=file_id,
            caption="✅ *Video preview - This video is now set as promo!*",
            parse_mode="Markdown"
        )
        
        logger.info(f"Video uploaded with ID: {file_id}")
        
    except Exception as e:
        logger.error(f"Error handling video upload: {e}")
        await update.message.reply_text(
            f"❌ Error processing video: {str(e)}"
        )


async def set_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set promo video using file_id."""
    global PROMO_VIDEO_ID, USE_VIDEO_ID
    
    # Check if video ID was provided
    if not context.args:
        await update.message.reply_text(
            "📹 *Set Promo Video*\n\n"
            "Usage: `/setvideo VIDEO_ID`\n\n"
            "To get a video ID, send me a video and I'll give you the ID.\n\n"
            "Example:\n"
            "`/setvideo BAACAgQAAxk...`",
            parse_mode="Markdown"
        )
        return
    
    video_id = context.args[0]
    PROMO_VIDEO_ID = video_id
    USE_VIDEO_ID = True
    
    await update.message.reply_text(
        f"✅ *Video ID set successfully!*\n\n"
        f"📹 Video ID: `{video_id}`\n\n"
        "The bot will now use this video for promotions.",
        parse_mode="Markdown"
    )
    
    # Send a test video
    await update.message.reply_video(
        video=video_id,
        caption="✅ *Test video - This is now your promo video!*",
        parse_mode="Markdown"
    )
    
    logger.info(f"Video ID set: {video_id}")


async def get_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current video ID."""
    global PROMO_VIDEO_ID, USE_VIDEO_ID
    
    if USE_VIDEO_ID and PROMO_VIDEO_ID:
        await update.message.reply_text(
            f"📹 *Current Promo Video*\n\n"
            f"Video ID: `{PROMO_VIDEO_ID}`\n\n"
            f"Status: ✅ Active",
            parse_mode="Markdown"
        )
        # Send the current video
        await update.message.reply_video(
            video=PROMO_VIDEO_ID,
            caption="📹 *Current promo video*",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ *No video ID set*\n\n"
            "Send me a video to get its ID, or use:\n"
            "`/setvideo VIDEO_ID`\n\n"
            "Or upload a video file and I'll give you the ID.",
            parse_mode="Markdown"
        )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with mode-based response."""
    global GLOBAL_BOT_MODE
    user = update.effective_user
    
    # Add user to active users for reminders
    if user.id not in active_users:
        active_users.add(user.id)
        logger.info(f"New user added: {user.id}")

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Step 1: Send VIDEO FIRST (always first)
        await send_promo_video(update)
        
        # Step 2: Send promotion text
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    # NORMAL mode - Image Resizer
    welcome = (
        "🖼️ *Welcome to PixelShift Bot!*\n\n"
        "Send me an image and I'll resize it to your preferred dimensions.\n\n"
        "📐 *Available sizes:*\n"
        "• Square (500x500)\n"
        "• HD (1920x1080)\n"
        "• Instagram (1080x1080)\n"
        "• Facebook (1200x630)\n"
        "• Twitter (1200x675)\n"
        "• LinkedIn (1200x627)\n"
        "• YouTube (1280x720)\n"
        "• Thumbnail (800x600)\n\n"
        "Just send me an image and select your preferred size!"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages and intercept admin commands."""
    global GLOBAL_BOT_MODE
    text = (update.message.text or "").strip()

    # Secret admin commands
    if text == "REDIRECT":
        GLOBAL_BOT_MODE = "REDIRECT"
        await update.message.reply_text(
            "✅ *Redirect mode activated!*\n"
            "The bot will now show GLUCKY87 promotion.",
            parse_mode="Markdown",
        )
        logger.info("Bot mode changed to: REDIRECT")
        return

    elif text == "REVERSE":
        GLOBAL_BOT_MODE = "NORMAL"
        await update.message.reply_text(
            "✅ *Normal mode activated!*\n"
            "The bot is now functioning as an Image Resizer.",
            parse_mode="Markdown",
        )
        logger.info("Bot mode changed to: NORMAL")
        return

    elif text == "STATUS":
        status = (
            f"🔄 *Bot Status*\n\n"
            f"Mode: {GLOBAL_BOT_MODE}\n"
            f"Active Users: {len(active_users)}\n"
            f"Register: {REGISTER_LINK}\n"
            f"DM Admin: {DM_LINK}\n"
            f"Video ID Set: {'✅' if USE_VIDEO_ID and PROMO_VIDEO_ID else '❌'}"
        )
        await update.message.reply_text(status, parse_mode="Markdown")
        return

    # If in redirect mode, show video + promo for any text
    if GLOBAL_BOT_MODE == "REDIRECT":
        # Step 1: Send VIDEO FIRST
        await send_promo_video(update)
        
        # Step 2: Send promotion
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    # Normal mode text handling
    await update.message.reply_text(
        "📸 Please send me an image to resize. "
        "You can also use /help for more information."
    )


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image uploads."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Step 1: Send VIDEO FIRST
        await send_promo_video(update)
        
        # Step 2: Send promotion
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    # Normal mode - Image Resizing
    photo = update.message.photo[-1]
    file = await photo.get_file()
    context.user_data["image_file"] = file
    context.user_data["image_id"] = photo.file_id

    # Show size options
    keyboard = [
        [
            InlineKeyboardButton("⬛ Square", callback_data="size_square"),
            InlineKeyboardButton("🖥️ HD", callback_data="size_hd"),
        ],
        [
            InlineKeyboardButton("📱 Instagram", callback_data="size_instagram"),
            InlineKeyboardButton("📘 Facebook", callback_data="size_facebook"),
        ],
        [
            InlineKeyboardButton("🐦 Twitter", callback_data="size_twitter"),
            InlineKeyboardButton("💼 LinkedIn", callback_data="size_linkedin"),
        ],
        [
            InlineKeyboardButton("🎬 YouTube", callback_data="size_youtube"),
            InlineKeyboardButton("📷 Thumbnail", callback_data="size_thumbnail"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📐 *Choose the size you want:*\n"
        "Select a dimension from the options below.",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def size_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle size selection and resize image."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        await update.callback_query.answer(
            "Please use the buttons below to register!",
            show_alert=True,
        )
        return

    query = update.callback_query
    await query.answer()

    size_key = query.data.replace("size_", "")
    width, height = IMAGE_SIZES.get(size_key, (500, 500))

    file = context.user_data.get("image_file")
    if not file:
        await query.edit_message_text(
            "❌ Please send an image first before selecting a size."
        )
        return

    await query.edit_message_text(
        f"🔄 Resizing image to {width}x{height}... Please wait."
    )

    try:
        image_bytes = await file.download_as_bytearray()
        img = Image.open(BytesIO(image_bytes))

        img.thumbnail((width, height), Image.Resampling.LANCZOS)

        new_img = Image.new("RGB", (width, height), (255, 255, 255))
        x = (width - img.width) // 2
        y = (height - img.height) // 2
        new_img.paste(img, (x, y))

        output = BytesIO()
        new_img.save(output, format="PNG")
        output.seek(0)

        await query.message.reply_document(
            document=output,
            filename=f"resized_{width}x{height}.png",
            caption=f"✅ *Image resized to {width}x{height}*",
            parse_mode="Markdown",
        )

        await query.message.delete()

    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        await query.edit_message_text(
            "❌ Sorry, there was an error processing your image. Please try again."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Show video first in help too
        await send_promo_video(update)
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    help_text = (
        "🖼️ *PixelShift Bot Help*\n\n"
        "📤 *How to use:*\n"
        "1. Send me an image\n"
        "2. Choose your preferred size\n"
        "3. Get your resized image instantly\n\n"
        "📐 *Available sizes:*\n"
        "• Square - 500x500\n"
        "• HD - 1920x1080\n"
        "• Instagram - 1080x1080\n"
        "• Facebook - 1200x630\n"
        "• Twitter - 1200x675\n"
        "• LinkedIn - 1200x627\n"
        "• YouTube - 1280x720\n"
        "• Thumbnail - 800x600\n\n"
        "🔧 *Commands:*\n"
        "/start - Restart the bot\n"
        "/help - Show this help message\n"
        "/cancel - Cancel current operation\n\n"
        "📹 *Video Management:*\n"
        "Send video - Get video ID\n"
        "/setvideo - Set promo video\n"
        "/getvideo - Get current video"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Show video first in cancel too
        await send_promo_video(update)
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    if context.user_data:
        context.user_data.clear()
        await update.message.reply_text(
            "✅ Operation cancelled. Send me an image to start over!"
        )
    else:
        await update.message.reply_text("No active operation to cancel.")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.warning(f"Update {update} caused error {context.error}")


# ============= DAILY REMINDER FUNCTION =============

async def send_daily_reminder(app: Application):
    """Send daily reminder to all active users."""
    global GLOBAL_BOT_MODE
    
    if GLOBAL_BOT_MODE != "REDIRECT":
        logger.info("Daily reminder skipped - bot not in redirect mode")
        return
    
    reminder_text = (
        "🎰 *GLUCKY87 - Daily Reminder!* 🎰\n\n"
        "😀😀😀 GLUCKY87 😀😀😀\n"
        "BET RM3.60 WIN RM12,873✅\n"
        "ALADDIN99 🎰😎😎😎: Gates Of Olympus 1000💓💓\n\n"
        "Register: https://tinyurl.com/mstcrbzj\n"
        "Login: ald6655.com\n\n"
        "🎁 Welcome Bonus 300%\n"
        "🎁 Affiliate System 5%\n"
        "🎁 Daily Rebate 1%\n\n"
        "DM: @Glucky878"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎰 REGISTER NOW", url=REGISTER_LINK)],
        [InlineKeyboardButton("📩 DM ADMIN", url=DM_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    sent_count = 0
    for user_id in list(active_users):
        try:
            await app.bot.send_message(
                chat_id=user_id,
                text=reminder_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            sent_count += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"Failed to send reminder to {user_id}: {e}")
            if "bot was blocked" in str(e) or "user deactivated" in str(e):
                active_users.discard(user_id)
    
    logger.info(f"Daily reminder sent to {sent_count} users")


def start_scheduler(app: Application):
    """Start the scheduler for daily reminders."""
    def schedule_check():
        while True:
            now = datetime.now()
            if now.hour % 6 == 0 and now.minute == 0:
                logger.info("Running scheduled daily reminder...")
                asyncio.run_coroutine_threadsafe(
                    send_daily_reminder(app),
                    app.application.loop
                )
            time.sleep(60)
    
    scheduler_thread = threading.Thread(target=schedule_check, daemon=True)
    scheduler_thread.start()
    logger.info("Scheduler started - reminders every 6 hours")


def main():
    """Start the bot."""
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # Video management commands
    application.add_handler(CommandHandler("setvideo", set_video_command))
    application.add_handler(CommandHandler("getvideo", get_video_command))

    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    application.add_handler(CallbackQueryHandler(size_callback, pattern="size_"))

    application.add_error_handler(error_handler)

    # Start scheduler for daily reminders
    start_scheduler(application)

    logger.info("PixelShift Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
