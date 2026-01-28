import os
import logging
from datetime import datetime
from pathlib import Path
import random
import string
from dotenv import load_dotenv
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = json.loads(os.getenv("ADMIN_IDS", "[7221952061]"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create necessary directories
Path("photos").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)

# ===== PHOTO GENERATION FUNCTIONS =====
def generate_front_camera_photo(user_info=None):
    """Generate a simulated front camera photo"""
    # Create a new image
    img = Image.new('RGB', (1080, 1920), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw camera UI elements
    # Top status bar
    draw.rectangle([0, 0, 1080, 100], fill=(20, 24, 32))
    draw.text((50, 20), "📱 Front Camera", font=font, fill=(255, 255, 255))
    draw.text((850, 20), "12:00", font=font, fill=(255, 255, 255))
    
    # Camera preview
    draw.rectangle([40, 150, 1040, 1770], fill=(60, 64, 72), outline=(100, 200, 255), width=5)
    
    # Add some random "face detection" boxes
    for _ in range(3):
        x = random.randint(100, 900)
        y = random.randint(300, 1400)
        draw.rectangle([x, y, x+200, y+200], outline=(0, 255, 100), width=3)
        draw.text((x+10, y+10), "👤", font=font)
    
    # Add user info if provided
    if user_info:
        info_y = 1800
        info_text = f"User: {user_info}"
        draw.text((50, info_y), info_text, font=small_font, fill=(200, 200, 255))
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((50, 1850), f"📅 {timestamp}", font=small_font, fill=(200, 200, 200))
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes

def generate_back_camera_photo(user_info=None):
    """Generate a simulated back camera photo"""
    img = Image.new('RGB', (1920, 1080), color=(50, 54, 62))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Camera UI
    draw.rectangle([0, 0, 1920, 80], fill=(25, 29, 37))
    draw.text((50, 10), "📷 Back Camera", font=font, fill=(255, 255, 255))
    
    # Grid lines (simulating camera grid)
    for i in range(1, 4):
        x = i * 480
        draw.line([(x, 100), (x, 1000)], fill=(100, 100, 100, 100), width=2)
    for i in range(1, 3):
        y = 100 + i * 300
        draw.line([(50, y), (1870, y)], fill=(100, 100, 100, 100), width=2)
    
    # Add some objects
    objects = ["🏢 Building", "🌳 Tree", "🚗 Car", "👥 People", "☁️ Sky"]
    for i, obj in enumerate(objects):
        x = 100 + i * 350
        y = 400
        draw.text((x, y), obj, font=font, fill=(255, 255, 200))
    
    # Add focus point
    draw.ellipse([900, 400, 1020, 520], outline=(0, 255, 0), width=4)
    draw.text((930, 450), "⚫", font=font)
    
    if user_info:
        draw.text((50, 1020), f"📸 By: {user_info}", font=small_font, fill=(200, 200, 255))
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((1500, 1020), f"🕒 {timestamp}", font=small_font, fill=(200, 200, 200))
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes

def generate_selfie_photo(user_info=None):
    """Generate a simulated selfie photo"""
    img = Image.new('RGB', (1080, 1920), color=(45, 49, 57))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 70)
        small_font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Selfie-specific elements
    draw.rectangle([0, 0, 1080, 120], fill=(30, 34, 42))
    draw.text((50, 20), "🤳 SELFIE MODE", font=font, fill=(255, 200, 100))
    
    # Mirror-like effect
    draw.ellipse([340, 300, 740, 700], outline=(100, 200, 255), width=8)
    draw.text((480, 450), "👤", font=font)
    
    # Add some effects
    effects = ["✨", "🌟", "💫", "❤️", "🔥"]
    for i, effect in enumerate(effects):
        x = 100 + i * 180
        y = 800
        draw.text((x, y), effect, font=font)
    
    # User info
    if user_info:
        draw.text((50, 1700), f"User: {user_info}", font=small_font, fill=(255, 200, 100))
    
    # Camera info
    camera_info = "f/2.2 • 1/30s • ISO 400"
    draw.text((50, 1800), f"📷 {camera_info}", font=small_font, fill=(200, 200, 200))
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes

def generate_random_photo(photo_type="front", user_info=None):
    """Generate random photo based on type"""
    if photo_type == "front":
        return generate_front_camera_photo(user_info)
    elif photo_type == "back":
        return generate_back_camera_photo(user_info)
    elif photo_type == "selfie":
        return generate_selfie_photo(user_info)
    else:
        return generate_front_camera_photo(user_info)

# ===== KEYBOARDS =====
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📱 Auto Front Camera", callback_data="auto_front"),
        InlineKeyboardButton("📷 Auto Back Camera", callback_data="auto_back"),
        InlineKeyboardButton("🤳 Auto Selfie", callback_data="auto_selfie"),
        InlineKeyboardButton("🔄 Auto All Photos", callback_data="auto_all"),
        InlineKeyboardButton("📍 Auto Location", callback_data="auto_location"),
        InlineKeyboardButton("📞 Auto Contact", callback_data="auto_contact"),
        InlineKeyboardButton("📊 Auto Device Info", callback_data="auto_device"),
        InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
        InlineKeyboardButton("🆘 Help", callback_data="help"),
    )
    if ADMIN_IDS:
        keyboard.add(InlineKeyboardButton("👑 Auto Admin Panel", callback_data="admin_panel"))
    return keyboard

def settings_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔢 Set Photo Count", callback_data="set_count"),
        InlineKeyboardButton("⏱️ Set Delay", callback_data="set_delay"),
        InlineKeyboardButton("🔄 Auto Mode", callback_data="auto_mode"),
        InlineKeyboardButton("📤 Auto Send to Admin", callback_data="auto_send_admin"),
        InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
    )
    return keyboard

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    user_info = f"{user.first_name} (@{user.username})" if user.username else user.first_name
    
    welcome_text = (
        f"🤖 *Auto Bot Activated!*\n\n"
        f"👋 Welcome *{user.first_name}*\n\n"
        "🚀 *AUTO FEATURES:*\n"
        "• 📱 Auto Front Camera Photos\n"
        "• 📷 Auto Back Camera Photos\n"
        "• 🤳 Auto Selfie Photos\n"
        "• 🔄 Auto All Photos (Sequence)\n"
        "• 📍 Auto Location Share\n"
        "• 📞 Auto Contact Share\n"
        "• 📊 Auto Device Info\n\n"
        "⚡ *Click any button for automatic action!*\n"
        "No manual uploads needed!"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
    
    # Send immediate auto-welcome photo
    try:
        photo_bytes = generate_front_camera_photo(user_info)
        bot.send_photo(
            message.chat.id,
            photo_bytes,
            caption="📸 *Auto Welcome Photo Generated!*\nFront camera simulation",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error generating welcome photo: {e}")

# ===== AUTO PHOTO HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('auto_'))
def handle_auto_actions(call):
    user = call.from_user
    user_info = f"{user.first_name} (@{user.username})" if user.username else user.first_name
    
    if call.data == "auto_front":
        # Auto generate and send front camera photo
        bot.answer_callback_query(call.id, "📱 Generating front camera photo...")
        
        try:
            photo_bytes = generate_front_camera_photo(user_info)
            bot.send_photo(
                call.message.chat.id,
                photo_bytes,
                caption="📱 *Auto Front Camera Photo*\nSimulated using Pillow",
                parse_mode="Markdown"
            )
            
            # Auto notify admin
            for admin_id in ADMIN_IDS:
                try:
                    bot.send_photo(
                        admin_id,
                        photo_bytes,
                        caption=f"📱 Auto Front Camera\n👤 From: {user_info}\n🆔 ID: {user.id}",
                        parse_mode="Markdown"
                    )
                except:
                    pass
                    
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")
    
    elif call.data == "auto_back":
        # Auto generate and send back camera photo
        bot.answer_callback_query(call.id, "📷 Generating back camera photo...")
        
        try:
            photo_bytes = generate_back_camera_photo(user_info)
            bot.send_photo(
                call.message.chat.id,
                photo_bytes,
                caption="📷 *Auto Back Camera Photo*\nSimulated outdoor scene",
                parse_mode="Markdown"
            )
            
            # Auto notify admin
            for admin_id in ADMIN_IDS:
                try:
                    bot.send_photo(
                        admin_id,
                        photo_bytes,
                        caption=f"📷 Auto Back Camera\n👤 From: {user_info}\n🆔 ID: {user.id}",
                        parse_mode="Markdown"
                    )
                except:
                    pass
                    
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")
    
    elif call.data == "auto_selfie":
        # Auto generate and send selfie photo
        bot.answer_callback_query(call.id, "🤳 Generating selfie photo...")
        
        try:
            photo_bytes = generate_selfie_photo(user_info)
            bot.send_photo(
                call.message.chat.id,
                photo_bytes,
                caption="🤳 *Auto Selfie Photo*\nWith special effects",
                parse_mode="Markdown"
            )
            
            # Auto notify admin
            for admin_id in ADMIN_IDS:
                try:
                    bot.send_photo(
                        admin_id,
                        photo_bytes,
                        caption=f"🤳 Auto Selfie\n👤 From: {user_info}\n🆔 ID: {user.id}",
                        parse_mode="Markdown"
                    )
                except:
                    pass
                    
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")
    
    elif call.data == "auto_all":
        # Auto generate ALL photos in sequence
        bot.answer_callback_query(call.id, "🔄 Generating all photos...")
        
        try:
            # Send typing action
            bot.send_chat_action(call.message.chat.id, 'upload_photo')
            
            # Generate and send all photos
            photo_types = [
                ("front", "📱 Front Camera"),
                ("back", "📷 Back Camera"), 
                ("selfie", "🤳 Selfie")
            ]
            
            for photo_type, caption in photo_types:
                photo_bytes = generate_random_photo(photo_type, user_info)
                bot.send_photo(
                    call.message.chat.id,
                    photo_bytes,
                    caption=f"*{caption}*\nAuto-generated sequence",
                    parse_mode="Markdown"
                )
                
                # Small delay between photos
                import time
                time.sleep(1)
            
            bot.send_message(
                call.message.chat.id,
                "✅ *Auto Sequence Complete!*\nAll photos generated automatically!",
                parse_mode="Markdown"
            )
            
            # Auto notify admin
            for admin_id in ADMIN_IDS:
                try:
                    summary_text = (
                        f"🔄 Auto All Photos Completed\n"
                        f"👤 User: {user_info}\n"
                        f"🆔 ID: {user.id}\n"
                        f"📊 Generated: 3 photos\n"
                        f"🕒 Time: {datetime.now().strftime('%H:%M:%S')}"
                    )
                    bot.send_message(admin_id, summary_text, parse_mode="Markdown")
                except:
                    pass
                    
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")
    
    elif call.data == "auto_location":
        # Auto simulate location sharing
        bot.answer_callback_query(call.id, "📍 Generating random location...")
        
        # Generate random coordinates
        lat = round(random.uniform(-90, 90), 6)
        lon = round(random.uniform(-180, 180), 6)
        maps_link = f"https://maps.google.com/?q={lat},{lon}"
        
        # Create location message
        location_msg = (
            f"📍 *Auto Location Generated!*\n\n"
            f"🌍 *Coordinates:*\n"
            f"• Latitude: `{lat}`\n"
            f"• Longitude: `{lon}`\n\n"
            f"🗺️ [Open in Google Maps]({maps_link})\n\n"
            f"🕒 Time: {datetime.now().strftime('%H:%M:%S')}"
        )
        
        bot.send_message(
            call.message.chat.id,
            location_msg,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    
    elif call.data == "auto_contact":
        # Auto generate contact info
        bot.answer_callback_query(call.id, "📞 Generating contact info...")
        
        # Generate fake contact data
        phone_number = f"+1{random.randint(200, 999)}{random.randint(1000000, 9999999)}"
        email = f"user{random.randint(1000, 9999)}@example.com"
        
        contact_msg = (
            f"📞 *Auto Contact Information*\n\n"
            f"👤 *Name:* {user.first_name}\n"
            f"📱 *Phone:* `{phone_number}`\n"
            f"📧 *Email:* `{email}`\n"
            f"🆔 *User ID:* `{user.id}`\n\n"
            f"⚠️ *Note:* This is simulated data"
        )
        
        bot.send_message(
            call.message.chat.id,
            contact_msg,
            parse_mode="Markdown"
        )
    
    elif call.data == "auto_device":
        # Auto generate device info
        bot.answer_callback_query(call.id, "📊 Generating device info...")
        
        # Simulated device data
        devices = ["iPhone 15 Pro", "Samsung Galaxy S24", "Google Pixel 8", "OnePlus 12"]
        os_versions = ["iOS 17.2", "Android 14", "HarmonyOS 4.0"]
        
        device_info = (
            f"📱 *Auto Device Information*\n\n"
            f"📲 *Device:* {random.choice(devices)}\n"
            f"⚙️ *OS:* {random.choice(os_versions)}\n"
            f"🔋 *Battery:* {random.randint(20, 100)}%\n"
            f"📶 *Signal:* {random.randint(1, 5)}/5 bars\n"
            f"💾 *Storage:* {random.randint(32, 512)}GB\n\n"
            f"👤 *User:* {user_info}\n"
            f"🆔 *Telegram ID:* `{user.id}`\n\n"
            f"⚠️ *Simulated data for demo*"
        )
        
        bot.send_message(
            call.message.chat.id,
            device_info,
            parse_mode="Markdown"
        )
    
    elif call.data == "settings":
        bot.edit_message_text(
            "⚙️ *Auto Bot Settings*\nConfigure automatic actions:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=settings_menu()
        )
    
    elif call.data == "help":
        help_text = (
            "🆘 *Auto Bot Help*\n\n"
            "🔘 *How to use:*\n"
            "1. Click any 'Auto' button\n"
            "2. Bot will automatically generate content\n"
            "3. No manual uploads required!\n\n"
            "📸 *Photo Types:*\n"
            "• Front Camera: Simulated front camera\n"
            "• Back Camera: Simulated outdoor\n"
            "• Selfie: With effects\n\n"
            "⚡ *All actions are automatic!*"
        )
        
        bot.edit_message_text(
            help_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    
    elif call.data == "admin_panel" and is_admin(call.from_user.id):
        admin_text = (
            "👑 *Admin Panel*\n\n"
            "🔧 *Auto Admin Features:*\n"
            "• View all users\n"
            "• Auto broadcast messages\n"
            "• Monitor auto activities\n"
            "• Download all auto-generated content\n\n"
            "*Coming soon with database integration*"
        )
        
        bot.edit_message_text(
            admin_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

# ===== SETTINGS HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data in ["set_count", "set_delay", "auto_mode", "auto_send_admin"])
def handle_settings(call):
    if call.data == "set_count":
        bot.send_message(
            call.message.chat.id,
            "🔢 *Set Auto Photo Count*\n\n"
            "Enter number of photos to auto-generate (1-10):\n"
            "Example: `3`",
            parse_mode="Markdown"
        )
    elif call.data == "set_delay":
        bot.send_message(
            call.message.chat.id,
            "⏱️ *Set Auto Delay*\n\n"
            "Enter delay between auto-actions in seconds (1-60):\n"
            "Example: `5`",
            parse_mode="Markdown"
        )
    elif call.data == "auto_mode":
        bot.send_message(
            call.message.chat.id,
            "🔄 *Auto Mode Settings*\n\n"
            "Configure continuous auto-generation:\n"
            "• Interval between actions\n"
            "• Types of content\n"
            "• Number of iterations",
            parse_mode="Markdown"
        )
    elif call.data == "auto_send_admin":
        bot.send_message(
            call.message.chat.id,
            "📤 *Auto Send to Admin*\n\n"
            "Toggle automatic sending to admin:\n"
            "✅ Currently: Enabled\n"
            "All auto-generated content is sent to admin",
            parse_mode="Markdown"
        )

# ===== ADDITIONAL COMMANDS =====
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🤖 *Auto Bot Commands*\n\n"
        "*/start* - Start bot with auto menu\n"
        "*/auto_front* - Auto front camera photo\n"
        "*/auto_back* - Auto back camera photo\n"
        "*/auto_selfie* - Auto selfie photo\n"
        "*/auto_all* - Auto all photos sequence\n"
        "*/auto_location* - Auto generate location\n"
        "*/auto_contact* - Auto generate contact\n"
        "*/auto_device* - Auto device info\n"
        "*/help* - Show this help\n\n"
        "⚡ *Everything is automatic!*"
    )
    
    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['auto_front', 'auto_back', 'auto_selfie', 'auto_all', 'auto_location', 'auto_contact', 'auto_device'])
def handle_auto_commands(message):
    # Map commands to callback data
    command_map = {
        '/auto_front': 'auto_front',
        '/auto_back': 'auto_back',
        '/auto_selfie': 'auto_selfie',
        '/auto_all': 'auto_all',
        '/auto_location': 'auto_location',
        '/auto_contact': 'auto_contact',
        '/auto_device': 'auto_device',
    }
    
    # Create a fake callback object
    class FakeCallback:
        def __init__(self, message, callback_data):
            self.message = message
            self.data = callback_data
            self.id = "cmd"
            self.from_user = message.from_user
    
    # Trigger the auto handler
    callback_data = command_map.get(message.text)
    if callback_data:
        fake_call = FakeCallback(message, callback_data)
        handle_auto_actions(fake_call)

# ===== RUN BOT =====
if __name__ == "__main__":
    print("🤖 Auto Bot is running...")
    print("🚀 Features: Auto photos, location, contact, device info")
    print("⚡ Everything is automatic!")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"❌ Error: {e}")