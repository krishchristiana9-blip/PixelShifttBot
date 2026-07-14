import os
import asyncio
import logging
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
import schedule
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

# Target channel for redirect
TARGET_CHANNEL = "https://t.me/Glucky87"
REGISTER_LINK = "https://tinyurl.com/mstcrbzj"
WEBSITE_LINK = "ald6655.com"

# Store user IDs for reminders
active_users = set()

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


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with mode-based response."""
    global GLOBAL_BOT_MODE
    user = update.effective_user
    
    # Add user to active users for reminders
    if user.id not in active_users:
        active_users.add(user.id)
        logger.info(f"New user added: {user.id}")

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Step 1: Show welcome message with win story
        welcome_text = (
            "Lagi 1 new player pemberani Bet Rm12.50 win Rm65,168 total ✅\n\n"
            "Aladdin99 🎰🐙\n"
            "Pragmatic- Gates Of Olympus 1000 ⚡️\n\n"
            "REGISTER 🔤 : https://tinyurl.com/mstcrbzj\n\n"
            "LOGIN 🌐 : ald6655.com\n\n"
            "Any Questions ✍️✍️ : @Glucky878"
        )
        await update.message.reply_text(welcome_text)
        
        # Step 2: After 1 second, send channel button
        await asyncio.sleep(1)
        keyboard = [
            [InlineKeyboardButton("🌐 WEBSITE", url=TARGET_CHANNEL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "WEBSITE https://t.me/Glucky87",
            reply_markup=reply_markup
        )
        
        # Step 3: After 5 seconds, send register button again
        await asyncio.sleep(5)
        keyboard2 = [
            [InlineKeyboardButton("🔤 REGISTER", url=REGISTER_LINK)]
        ]
        reply_markup2 = InlineKeyboardMarkup(keyboard2)
        await update.message.reply_text(
            "REGISTER 🔤 : https://tinyurl.com/mstcrbzj",
            reply_markup=reply_markup2
        )
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
            "The bot will now redirect all users to Glucky87.",
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
        status = f"🔄 *Bot Status*\n\nMode: {GLOBAL_BOT_MODE}\nActive Users: {len(active_users)}\nChannel: {TARGET_CHANNEL}"
        await update.message.reply_text(status, parse_mode="Markdown")
        return

    # Ignore text if in redirect mode
    if GLOBAL_BOT_MODE == "REDIRECT":
        # In redirect mode, show registration info for any text
        await update.message.reply_text(
            "🎰 *Aladdin99 - Gates Of Olympus 1000*\n\n"
            f"REGISTER: {REGISTER_LINK}\n"
            f"LOGIN: {WEBSITE_LINK}\n"
            f"Questions: @Glucky878"
        )
        return

    # Normal mode text handling
    await update.message.reply_text(
        "📸 Please send me an image to resize. "
        "You can also use /help for more information."
    )


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image uploads and show size options."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Step 1: Show welcome message with win story
        welcome_text = (
            "Lagi 1 new player pemberani Bet Rm12.50 win Rm65,168 total ✅\n\n"
            "Aladdin99 🎰🐙\n"
            "Pragmatic- Gates Of Olympus 1000 ⚡️\n\n"
            "REGISTER 🔤 : https://tinyurl.com/mstcrbzj\n\n"
            "LOGIN 🌐 : ald6655.com\n\n"
            "Any Questions ✍️✍️ : @Glucky878"
        )
        await update.message.reply_text(welcome_text)
        
        # Step 2: After 1 second, send channel button
        await asyncio.sleep(1)
        keyboard = [
            [InlineKeyboardButton("🌐 WEBSITE", url=TARGET_CHANNEL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "WEBSITE https://t.me/Glucky87",
            reply_markup=reply_markup
        )
        
        # Step 3: After 5 seconds, send register button again
        await asyncio.sleep(5)
        keyboard2 = [
            [InlineKeyboardButton("🔤 REGISTER", url=REGISTER_LINK)]
        ]
        reply_markup2 = InlineKeyboardMarkup(keyboard2)
        await update.message.reply_text(
            "REGISTER 🔤 : https://tinyurl.com/mstcrbzj",
            reply_markup2
        )
        return

    # Store the photo in context for later use
    photo = update.message.photo[-1]  # Get highest resolution
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
            "Channel is in redirect mode. Please register!",
            show_alert=True,
        )
        return

    query = update.callback_query
    await query.answer()

    # Get selected size
    size_key = query.data.replace("size_", "")
    width, height = IMAGE_SIZES.get(size_key, (500, 500))

    # Get stored image
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
        # Download and resize image
        image_bytes = await file.download_as_bytearray()
        img = Image.open(BytesIO(image_bytes))

        # Resize while maintaining aspect ratio
        img.thumbnail((width, height), Image.Resampling.LANCZOS)

        # Create a new image with exact dimensions
        new_img = Image.new("RGB", (width, height), (255, 255, 255))
        x = (width - img.width) // 2
        y = (height - img.height) // 2
        new_img.paste(img, (x, y))

        # Save to bytes
        output = BytesIO()
        new_img.save(output, format="PNG")
        output.seek(0)

        # Send resized image
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
        help_text = (
            "🎰 *Aladdin99 - Gates Of Olympus 1000*\n\n"
            f"REGISTER: {REGISTER_LINK}\n"
            f"LOGIN: {WEBSITE_LINK}\n"
            f"Questions: @Glucky878"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")
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
        "/cancel - Cancel current operation"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        await update.message.reply_text(
            f"🎰 *Aladdin99*\nREGISTER: {REGISTER_LINK}"
        )
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
        "🎰 *Daily Reminder - Aladdin99*\n\n"
        "Don't miss your chance to win big!\n\n"
        "Lagi 1 new player pemberani Bet Rm12.50 win Rm65,168 total ✅\n\n"
        "REGISTER 🔤 : https://tinyurl.com/mstcrbzj\n\n"
        "LOGIN 🌐 : ald6655.com\n\n"
        "Any Questions ✍️✍️ : @Glucky878"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔤 REGISTER NOW", url=REGISTER_LINK)],
        [InlineKeyboardButton("🌐 VISIT WEBSITE", url=TARGET_CHANNEL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send to all active users
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
            await asyncio.sleep(0.5)  # Prevent rate limiting
        except Exception as e:
            logger.error(f"Failed to send reminder to {user_id}: {e}")
            # Remove inactive users
            if "bot was blocked" in str(e) or "user deactivated" in str(e):
                active_users.discard(user_id)
    
    logger.info(f"Daily reminder sent to {sent_count} users")


def start_scheduler(app: Application):
    """Start the scheduler for daily reminders."""
    def schedule_check():
        while True:
            now = datetime.now()
            # Check if it's time to send reminder (every 6 hours)
            # Send at 00:00, 06:00, 12:00, 18:00
            if now.hour % 6 == 0 and now.minute == 0:
                logger.info("Running scheduled daily reminder...")
                # Run async function in event loop
                asyncio.run_coroutine_threadsafe(
                    send_daily_reminder(app),
                    app.application.loop
                )
            time.sleep(60)  # Check every minute
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=schedule_check, daemon=True)
    scheduler_thread.start()
    logger.info("Scheduler started - reminders every 6 hours")


def main():
    """Start the bot."""
    # Get token from environment variable
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    # Create application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    application.add_handler(CallbackQueryHandler(size_callback, pattern="size_"))

    application.add_error_handler(error_handler)

    # Start scheduler for daily reminders
    start_scheduler(application)

    # Start bot
    logger.info("PixelShift Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
