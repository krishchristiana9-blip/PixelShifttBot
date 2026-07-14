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
GLOBAL_BOT_MODE = "NORMAL"

# URLs
REGISTER_LINK = "https://tinyurl.com/mstcrbzj"
DM_LINK = "https://t.me/Glucky878"
WEBSITE_LINK = "ald6655.com"

# Store user IDs for reminders
active_users = set()

# Video Configuration - Your video file ID
PROMO_VIDEO_ID = "BAACAgUAAxkBAAIFNmpWmo_kHIyKg1057DT7yG4gwPtiAAInIQACIEGxVlEpmY4R49eNPQQ"
USE_VIDEO_ID = True

# ============= CUSTOM EMOJI IDs FROM YOUR VIDEO =============
# Smiley faces
EMOJI_SMILE1 = "6077849430780810472"
EMOJI_SMILE2 = "6077681879811624990"
EMOJI_SMILE3 = "6077782399226220921"

# Cool faces
EMOJI_COOL1 = "6078046763053223669"
EMOJI_COOL2 = "6077950383987101548"
EMOJI_COOL3 = "6077713898792815927"

# Other emojis
EMOJI_CHECK = "5215492745900077682"
EMOJI_SLOT = "5384509325429463744"
EMOJI_CROWN = "6109498606698367901"
EMOJI_CROWN2 = "5940649513713669684"
EMOJI_WRITE = "5037286044458812218"
EMOJI_FIRE = "5037585712916988616"
EMOJI_FIRE2 = "5472326412901817384"
EMOJI_BULB = "5778639327219159639"
EMOJI_LIGHTNING = "5472350516258283380"
EMOJI_DICE = "5472016041385138963"
EMOJI_SLOT2 = "5472374142873378039"
EMOJI_GIFT = "5841276284155467413"

# Tech emojis
EMOJI_LAPTOP = "5474665842933244236"
EMOJI_DESKTOP = "5471949529521593965"
EMOJI_PHONE = "5472326412901817384"
EMOJI_PHONE2 = "5422747651193980920"
EMOJI_CARD = "5472059734087442438"
EMOJI_BANK = "5287292843763713628"

# Question/Email
EMOJI_QUESTION = "6048888058281988304"
EMOJI_EMAIL = "6048818870653816953"

# Gift
EMOJI_GIFT2 = "5203996991054432397"

# Money
EMOJI_MONEY = "5409048419211682843"
EMOJI_MONEY2 = "5249483078425923131"

# Food emojis
EMOJI_BURGER = "5395706614407766408"
EMOJI_FRIES = "5395366032091127062"
EMOJI_CHICKEN = "5395826890671926072"
EMOJI_PIZZA = "5463364976523621351"
EMOJI_DRINK = "5463053870567536260"
EMOJI_BURGER2 = "5395804062920745463"
EMOJI_FRIES2 = "5395839277357605843"
EMOJI_CHICKEN2 = "5395377796006552826"
EMOJI_PIZZA2 = "5395453572114555649"

# More drinks
EMOJI_DRINK2 = "6077833204394364808"
EMOJI_DRINK3 = "6080169288646266931"
EMOJI_DRINK4 = "6080025832443612782"
EMOJI_DRINK5 = "6078135050400960606"
EMOJI_DRINK6 = "6077861065847214572"
EMOJI_DRINK7 = "6078137240834280478"
EMOJI_DRINK8 = "6078138288806301352"
EMOJI_DRINK9 = "6077898870149353029"
EMOJI_DRINK10 = "6078075131312212932"

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

VIDEO_FILE_NAME = "promo.mp4"


async def send_promo_video(update: Update):
    """Send the promotional video with exact custom emojis."""
    global PROMO_VIDEO_ID, USE_VIDEO_ID
    
    try:
        if USE_VIDEO_ID and PROMO_VIDEO_ID:
            # This is the exact caption from your video with custom emojis
            caption = (
                f'<tg-emoji emoji-id="{EMOJI_SMILE1}">😀</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_SMILE2}">😀</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_SMILE3}">😀</tg-emoji>'
                f' GLUCKY87 '
                f'<tg-emoji emoji-id="{EMOJI_COOL1}">😎</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_COOL2}">😎</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_COOL3}">😎</tg-emoji>\n\n'
                f'BET RM3.60 WIN RM12,873'
                f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>\n'
                f'ALADDIN99 '
                f'<tg-emoji emoji-id="{EMOJI_SLOT}">🎰</tg-emoji>\n'
                f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>: Gates Of Olympus 1000\n\n'
                f'<tg-emoji emoji-id="{EMOJI_WRITE}">✍️</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_FIRE}">🔥</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_BULB}">💡</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡️</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DICE}">🎲</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_SLOT2}">🎰</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_CROWN2}">👑</tg-emoji>: {REGISTER_LINK}\n'
                f'{REGISTER_LINK}\n\n'
                f'<tg-emoji emoji-id="{EMOJI_LAPTOP}">💻</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DESKTOP}">🖥️</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_PHONE}">📱</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_PHONE2}">📲</tg-emoji>: {WEBSITE_LINK}\n\n'
                f'Any Questions '
                f'<tg-emoji emoji-id="{EMOJI_QUESTION}">❓</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_EMAIL}">✉️</tg-emoji>: @Glucky878\n\n'
                f'<tg-emoji emoji-id="{EMOJI_GIFT2}">🎁</tg-emoji> Welcome Bonus 300%\n'
                f'<tg-emoji emoji-id="{EMOJI_GIFT2}">🎁</tg-emoji> Affiliate System 5%\n'
                f'<tg-emoji emoji-id="{EMOJI_GIFT2}">🎁</tg-emoji> Daily Rebate 1%\n\n'
                f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_MONEY2}">💰</tg-emoji> Online Transfer / FPX / E-Wallet '
                f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_MONEY2}">💰</tg-emoji>\n'
                f'<tg-emoji emoji-id="{EMOJI_BURGER}">🍔</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_FRIES}">🍟</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_CHICKEN}">🍗</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_PIZZA}">🍕</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK2}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK3}">🥤</tg-emoji>\n'
                f'<tg-emoji emoji-id="{EMOJI_DRINK4}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK5}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK6}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK7}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK8}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK9}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_DRINK10}">🥤</tg-emoji>'
                f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>'
            )
            
            await update.message.reply_video(
                video=PROMO_VIDEO_ID,
                caption=caption,
                parse_mode="HTML"
            )
            logger.info("Video sent using file_id")
            return True
        
        if os.path.exists(VIDEO_FILE_NAME):
            with open(VIDEO_FILE_NAME, 'rb') as video:
                await update.message.reply_video(
                    video=video,
                    caption="GLUCKY87",
                    parse_mode="HTML"
                )
            logger.info("Video sent from local file")
            return True
        
        logger.warning(f"No video found")
        return False
        
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        return False


async def send_promo_content(update: Update):
    """Send the promotion text with exact custom emojis."""
    
    promo_text = (
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji> <b>EVOLUTION</b> <tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>\n'
        f'<b>GLUCKY87</b>\n'
        f'<b>PRAGMATIC</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FIRE}">🔥</tg-emoji> <b>BET RM3.60 WIN RM12,873</b> <tg-emoji emoji-id="{EMOJI_FIRE2}">🔥</tg-emoji>\n'
        f'<b>ALADDIN99</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>\n\n'
        f'<b>Gates Of Olympus 1000</b> <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡️</tg-emoji>\n\n'
        f'📝 <b>REGISTER</b>\n'
        f'ID : <a href="{REGISTER_LINK}">{REGISTER_LINK}</a>\n'
        f'<a href="{REGISTER_LINK}">{REGISTER_LINK}</a>\n\n'
        f'🔐 <b>LOGIN</b>\n'
        f'{WEBSITE_LINK}\n\n'
        f'❓ <b>Any Questions</b>\n'
        f'DM : <a href="{DM_LINK}">@Glucky878</a>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_GIFT}">🎁</tg-emoji> <b>Welcome Bonus 300%</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_GIFT}">🎁</tg-emoji> <b>Affiliate System 5%</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_GIFT}">🎁</tg-emoji> <b>Daily Rebate 1%</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_CARD}">💳</tg-emoji> <b>Online Transfer / FPX / E-Wallet</b>'
    )
    
    await update.message.reply_text(
        promo_text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    
    # Send buttons - Using the exact button texts from your video
    keyboard = [
        [InlineKeyboardButton("Register & Get 300% Welcome Bonus .", url=REGISTER_LINK)],
        [InlineKeyboardButton("DM ADMIN TO CLAIM 300% BONUS !", url=DM_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👇 Click below to claim your bonus:",
        reply_markup=reply_markup
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video uploads - Get video file_id."""
    global PROMO_VIDEO_ID, USE_VIDEO_ID
    
    try:
        video = update.message.video
        file_id = video.file_id
        
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        
        PROMO_VIDEO_ID = file_id
        USE_VIDEO_ID = True
        
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
    
    if not context.args:
        await update.message.reply_text(
            "📹 *Set Promo Video*\n\n"
            "Usage: `/setvideo VIDEO_ID`\n\n"
            "To get a video ID, send me a video and I'll give you the ID.\n\n"
            "Example:\n"
            "`/setvideo BAACAgUAAxk...`",
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
    
    if user.id not in active_users:
        active_users.add(user.id)
        logger.info(f"New user added: {user.id}")

    if GLOBAL_BOT_MODE == "REDIRECT":
        # Step 1: Send video first with custom emojis
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

    if GLOBAL_BOT_MODE == "REDIRECT":
        await send_promo_video(update)
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    await update.message.reply_text(
        "📸 Please send me an image to resize. "
        "You can also use /help for more information."
    )


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image uploads."""
    global GLOBAL_BOT_MODE

    if GLOBAL_BOT_MODE == "REDIRECT":
        await send_promo_video(update)
        await asyncio.sleep(1)
        await send_promo_content(update)
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    context.user_data["image_file"] = file
    context.user_data["image_id"] = photo.file_id

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
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji> <b>DAILY REMINDER - GLUCKY87</b> <tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FIRE}">🔥</tg-emoji> <b>BET RM3.60 WIN RM12,873</b> <tg-emoji emoji-id="{EMOJI_FIRE2}">🔥</tg-emoji>\n'
        f'<b>ALADDIN99</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>'
        f'<tg-emoji emoji-id="{EMOJI_CROWN}">👑</tg-emoji>\n\n'
        f'<b>Gates Of Olympus 1000</b> <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡️</tg-emoji>\n\n'
        f'📝 <b>REGISTER NOW!</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_GIFT}">🎁</tg-emoji> <b>Welcome Bonus 300%</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_GIFT}">🎁</tg-emoji> <b>Affiliate System 5%</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_GIFT}">🎁</tg-emoji> <b>Daily Rebate 1%</b>'
    )
    
    keyboard = [
        [InlineKeyboardButton("Register & Get 300% Welcome Bonus .", url=REGISTER_LINK)],
        [InlineKeyboardButton("DM ADMIN TO CLAIM 300% BONUS !", url=DM_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    sent_count = 0
    for user_id in list(active_users):
        try:
            await app.bot.send_message(
                chat_id=user_id,
                text=reminder_text,
                reply_markup=reply_markup,
                parse_mode="HTML"
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

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    application.add_handler(CommandHandler("setvideo", set_video_command))
    application.add_handler(CommandHandler("getvideo", get_video_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    application.add_handler(CallbackQueryHandler(size_callback, pattern="size_"))

    application.add_error_handler(error_handler)

    start_scheduler(application)

    logger.info("PixelShift Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
