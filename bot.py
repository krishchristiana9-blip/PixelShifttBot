import os
import asyncio
import logging
from io import BytesIO
from PIL import Image

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
TARGET_CHANNEL = "https://t.me/FOREXPIPSWORLDFX"

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

    if GLOBAL_BOT_MODE == "REDIRECT":
        welcome_text = (
            "📈 *Welcome to Forex Pips World!*\n\n"
            "In the world of economic uncertainty, having a passive income is crucial.\n"
            "Join our community for daily signals, expert analysis, and profitable trades!\n\n"
            "🔹 *Free Trading Signals*\n"
            "🔹 *Expert Analysis*\n"
            "🔹 *Passive Income Strategies*\n\n"
            "Click the button below to join now! 🚀"
        )
        await update.message.reply_text(welcome_text, parse_mode="Markdown")

        await asyncio.sleep(1)

        keyboard = [
            [InlineKeyboardButton("🚀 Join Forex Pips World", url=TARGET_CHANNEL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👇 *Click here to join our channel:*",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
        return

    # NORMAL mode - Image Resizer
    welcome = (
        "🖼️ *Welcome to Image Resizer Bot!*\n\n"
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
            "The bot will now redirect all users to Forex Pips World.",
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

    # Ignore text if in redirect mode
    if GLOBAL_BOT_MODE == "REDIRECT":
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
        await update.message.reply_text(
            "📈 Join Forex Pips World for daily signals and profits!\n"
            f"{TARGET_CHANNEL}"
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
            "Channel is in redirect mode. Please join our channel!",
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
        await update.message.reply_text(
            f"📈 Join our channel for daily signals and profits!\n{TARGET_CHANNEL}"
        )
        return

    help_text = (
        "🖼️ *Image Resizer Bot Help*\n\n"
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
            f"📈 Join Forex Pips World for daily signals!\n{TARGET_CHANNEL}"
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

    # Start bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
