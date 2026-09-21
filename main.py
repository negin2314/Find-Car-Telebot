import logging
import os
import sys
from typing import Optional
import telebot
from telebot import types

# Optional python-dotenv support
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from scraper import fetch_cars, save_cars_to_csv

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Retrieve bot token from environment variables
DUMMY_TOKEN = "000000000:AAA_placeholder_token_for_validation"
raw_token = os.getenv("BOT_TOKEN") or os.getenv("API_TOKEN")

if raw_token and raw_token.strip() and raw_token.strip() != "botfather TOKEN":
    API_TOKEN = raw_token.strip()
    IS_CONFIGURED = True
else:
    API_TOKEN = DUMMY_TOKEN
    IS_CONFIGURED = False

bot = telebot.TeleBot(API_TOKEN)

# Body type labels
BODY_TYPE_NAMES = {
    "sedan": "سدان",
    "suv": "شاسی بلند",
    "pickup": "وانت",
    "hatchback": "هاچبک",
    "van": "ون",
}

# Legacy mapping for backwards compatibility
LEGACY_BODY_MAP = {
    "1111": "sedan",
    "2222": "suv",
    "3333": "pickup",
    "4444": "hatchback",
    "5555": "van",
}

LEGACY_STATUS_MAP = {
    # Sedan
    "k1": ("sedan", 2),
    "s1": ("sedan", 3),
    # SUV
    "nn": ("suv", 2),
    "mm": ("suv", 3),
    # Pickup
    "k3": ("pickup", 2),
    "s3": ("pickup", 3),
    # Van
    "k5": ("van", 2),
    "s5": ("van", 3),
    # Hatchback
    "k4": ("hatchback", 2),
    "s4": ("hatchback", 3),
}

LEGACY_SEARCH_MAP = {
    # Sedan Used
    "5-10": ("sedan", 2, "500,1000"),
    "10-50": ("sedan", 2, "1000,5000"),
    "50-100": ("sedan", 2, "5000,10000"),
    # Sedan New
    "1": ("sedan", 3, "500,1000"),
    "2": ("sedan", 3, "1000,5000"),
    "3": ("sedan", 3, "500,10000"),
    # SUV Used
    "01": ("suv", 2, "500,1000"),
    "02": ("suv", 2, "1000,5000"),
    "03": ("suv", 2, "5000,10000"),
    # SUV New
    "022": ("suv", 3, "1000,5000"),
    "033": ("suv", 3, "5000,10000"),
    # Pickup Used
    "12": ("pickup", 2, "500,1000"),
    "13": ("pickup", 2, "1000,5000"),
    # Pickup New
    "14": ("pickup", 3, "500,1000"),
    "15": ("pickup", 3, "1000,5000"),
    # Van Used
    "17": ("van", 2, "1000,5000"),
    # Van New
    "900": ("van", 3, "1000,5000"),
    # Hatchback Used
    "04": ("hatchback", 2, "500,1000"),
    "05": ("hatchback", 2, "1000,5000"),
    # Hatchback New
    "07": ("hatchback", 3, "500,1000"),
    "08": ("hatchback", 3, "1000,5000"),
}


# ==================== Keyboards ====================

def get_main_keyboard() -> types.InlineKeyboardMarkup:
    """Build the vehicle body type selection keyboard."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("سدان", callback_data="body:sedan"),
        types.InlineKeyboardButton("شاسی بلند", callback_data="body:suv"),
        types.InlineKeyboardButton("وانت", callback_data="body:pickup"),
        types.InlineKeyboardButton("هاچبک", callback_data="body:hatchback"),
        types.InlineKeyboardButton("ون", callback_data="body:van"),
    ]
    markup.add(*buttons)
    return markup


def get_status_keyboard(body_type: str) -> types.InlineKeyboardMarkup:
    """Build the vehicle condition (used / new) selection keyboard."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_used = types.InlineKeyboardButton("کارکرده", callback_data=f"status:{body_type}:2")
    btn_new = types.InlineKeyboardButton("صفر", callback_data=f"status:{body_type}:3")
    btn_back = types.InlineKeyboardButton("برگشت⬅️", callback_data="back:main")
    markup.add(btn_used, btn_new, btn_back)
    return markup


def get_price_keyboard(body_type: str, km_status: int) -> types.InlineKeyboardMarkup:
    """Build the price range selection keyboard based on vehicle type and status."""
    markup = types.InlineKeyboardMarkup(row_width=1)

    # Van and Hatchback have fewer high-end filters, Sedan/SUV have up to 10B
    if body_type in ["sedan", "suv"]:
        btn1 = types.InlineKeyboardButton(
            "۵۰۰ میلیون تا ۱ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:500,1000"
        )
        btn2 = types.InlineKeyboardButton(
            "۱ میلیارد تا ۵ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:1000,5000"
        )
        btn3 = types.InlineKeyboardButton(
            "۵ میلیارد تا ۱۰ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:5000,10000"
        )
        markup.add(btn1, btn2, btn3)
    elif body_type == "pickup":
        btn1 = types.InlineKeyboardButton(
            "۵۰۰ میلیون تا ۱ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:500,1000"
        )
        btn2 = types.InlineKeyboardButton(
            "۱ میلیارد تا ۵ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:1000,5000"
        )
        markup.add(btn1, btn2)
    elif body_type == "van":
        btn1 = types.InlineKeyboardButton(
            "۱ میلیارد تا ۵ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:1000,5000"
        )
        markup.add(btn1)
    elif body_type == "hatchback":
        btn1 = types.InlineKeyboardButton(
            "۵۰۰ میلیون تا ۱ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:500,1000"
        )
        btn2 = types.InlineKeyboardButton(
            "۱ میلیارد تا ۵ میلیارد تومان",
            callback_data=f"search:{body_type}:{km_status}:1000,5000"
        )
        markup.add(btn1, btn2)

    btn_back = types.InlineKeyboardButton("برگشت⬅️", callback_data=f"body:{body_type}")
    markup.add(btn_back)
    return markup


def get_result_keyboard(body_type: str, km_status: int, search_url: str) -> types.InlineKeyboardMarkup:
    """Build inline keyboard shown beneath search results."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_search_again = types.InlineKeyboardButton("🔄 جستجوی دیگر", callback_data=f"status:{body_type}:{km_status}")
    btn_main = types.InlineKeyboardButton("🏠 منوی اصلی", callback_data="back:main")
    markup.add(btn_search_again, btn_main)
    if search_url:
        btn_web = types.InlineKeyboardButton("🌐 مشاهده در همراه مکانیک", url=search_url)
        markup.add(btn_web)
    return markup


# ==================== Command Handlers ====================

@bot.message_handler(commands=["start"])
def welcome(message: types.Message):
    """Handle /start command."""
    username = message.from_user.username
    markup = get_main_keyboard()

    if username:
        text = (
            f"کاربر @{username} عزیز، به ربات ماشین‌یاب همراه مکانیک خوش آمدید! 😊🚗\n\n"
            "لطفاً نوع خودروی مورد نظر خود را انتخاب کنید:"
        )
    else:
        text = (
            "کاربر عزیز، به ربات ماشین‌یاب همراه مکانیک خوش آمدید! 😊🚗\n\n"
            "لطفاً نوع خودروی مورد نظر خود را انتخاب کنید:"
        )

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_command(message: types.Message):
    """Handle /help command."""
    text = (
        "🤖 **راهنمای استفاده از ربات ماشین‌یاب همراه مکانیک**\n\n"
        "1. دستور /start را ارسال کنید.\n"
        "2. نوع شاسی خودرو (سدان، شاسی بلند، هاچبک، ...) را انتخاب نمایید.\n"
        "3. وضعیت کارکرد خودرو (کارکرده یا صفر) را مشخص کنید.\n"
        "4. بازه قیمتی دلخواه خود را تعیین کنید.\n"
        "5. اطلاعات آخرین آگهی‌ها به همراه قیمت، کارکرد و لینک مستقیم دریافت می‌شود."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# ==================== Callback Query Handlers ====================

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call: types.CallbackQuery):
    """Universal handler for all inline keyboard clicks."""
    data = call.data
    logger.info(f"Callback received: {data} from user {call.from_user.id}")

    # Acknowledge the callback query immediately to stop the loading animation
    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        logger.debug(f"Failed to answer callback query: {e}")

    # 1. Main navigation: Back to main menu
    if data in ["back", "back:main"]:
        markup = get_main_keyboard()
        try:
            bot.edit_message_text(
                "دوست داری اطلاعات مربوط به کدوم مدل ماشین رو ببینی؟",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
        except Exception:
            bot.send_message(call.message.chat.id, "انتخاب مدل ماشین:", reply_markup=markup)
        return

    # Handle legacy 'backk' (which was previously broken with non-existent 'kk'/'ss')
    if data == "backk":
        markup = get_main_keyboard()
        try:
            bot.edit_message_text(
                "لطفاً مدل ماشین مورد نظر خود را انتخاب کنید:",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
        except Exception:
            bot.send_message(call.message.chat.id, "انتخاب مدل ماشین:", reply_markup=markup)
        return

    # 2. Body type selection (Legacy or Modern)
    body_type = None
    if data.startswith("body:"):
        body_type = data.split(":")[1]
    elif data in LEGACY_BODY_MAP:
        body_type = LEGACY_BODY_MAP[data]

    if body_type:
        body_name = BODY_TYPE_NAMES.get(body_type, body_type)
        markup = get_status_keyboard(body_type)
        bot.edit_message_text(
            f"وضعیت خودرو ({body_name}) را انتخاب کنید:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
        return

    # 3. Status selection (Used / New) -> Show price ranges
    status_body = None
    status_val = None

    if data.startswith("status:"):
        parts = data.split(":")
        status_body = parts[1]
        status_val = int(parts[2])
    elif data in LEGACY_STATUS_MAP:
        status_body, status_val = LEGACY_STATUS_MAP[data]

    if status_body and status_val:
        body_name = BODY_TYPE_NAMES.get(status_body, status_body)
        status_name = "کارکرده" if status_val == 2 else "صفر"
        markup = get_price_keyboard(status_body, status_val)
        bot.edit_message_text(
            f"بازه قیمتی خودروی {body_name} ({status_name}) را انتخاب کنید:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
        return

    # 4. Search execution
    search_body = None
    search_status = None
    search_price = None

    if data.startswith("search:"):
        parts = data.split(":")
        search_body = parts[1]
        search_status = int(parts[2])
        search_price = parts[3]
    elif data in LEGACY_SEARCH_MAP:
        search_body, search_status, search_price = LEGACY_SEARCH_MAP[data]

    if search_body and search_status and search_price:
        perform_car_search(call, search_body, search_status, search_price)
        return

    logger.warning(f"Unhandled callback data: {data}")


def perform_car_search(call: types.CallbackQuery, body_type: str, km_status: int, price_range: str):
    """Execute car search on Hamrah Mechanic and return formatted results."""
    chat_id = call.message.chat.id
    body_name = BODY_TYPE_NAMES.get(body_type, body_type)
    status_name = "کارکرده" if km_status == 2 else "صفر"

    # Send temporary searching notice
    loading_msg = bot.send_message(
        chat_id,
        f"⏳ در حال جستجوی خودروهای {body_name} ({status_name}) از سایت همراه مکانیک..."
    )

    try:
        results = fetch_cars(body_type, km_status, price_range)
        cars = results.get("cars", [])
        search_url = results.get("search_url", "")
        total_count = results.get("total_count", len(cars))

        # Delete loading notice
        try:
            bot.delete_message(chat_id, loading_msg.message_id)
        except Exception:
            pass

        if not cars:
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn_again = types.InlineKeyboardButton("🔄 انتخاب بازه قیمتی دیگر", callback_data=f"status:{body_type}:{km_status}")
            btn_main = types.InlineKeyboardButton("🏠 بازگشت به منوی اصلی", callback_data="back:main")
            markup.add(btn_again, btn_main)

            bot.send_message(
                chat_id,
                f"🔍 متأسفانه در حال حاضر خودرویی برای **{body_name} ({status_name})** در این بازه قیمتی یافت نشد.",
                reply_markup=markup,
                parse_mode="Markdown"
            )
            return

        # Save to car.csv with proper UTF-8 BOM encoding
        save_cars_to_csv(cars)

        # Build formatted text messages
        # Limit to top 10 cars per message to stay well within Telegram's 4096 char limit
        header = (
            f"📋 **نتایج جستجوی خودروهای {body_name} ({status_name}):**\n"
            f"تعداد آگهی‌های یافت‌شده: {total_count} مورد\n"
            f"────────────────────\n\n"
        )

        cards_text = []
        for i, c in enumerate(cars[:10], start=1):
            card = (
                f"{i}. 🚗 **{c['name']}**\n"
                f"💰 **قیمت:** {c['price']}\n"
                f"📅 **سال ساخت:** {c['year']} | 🛣 **کارکرد:** {c['km']}\n"
            )
            if c.get("color") or c.get("gearbox"):
                specs = []
                if c.get("color"):
                    specs.append(f"رنگ: {c['color']}")
                if c.get("gearbox"):
                    specs.append(f"گیربکس: {c['gearbox']}")
                card += f"⚙️ { ' | '.join(specs) }\n"
            if c.get("location") and c.get("location") != "نامشخص":
                card += f"📍 **موقعیت:** {c['location']}\n"
            if c.get("url"):
                card += f"🔗 [مشاهده جزییات آگهی]({c['url']})\n"
            card += "────────────────────\n"
            cards_text.append(card)

        message_content = header + "\n".join(cards_text)
        markup = get_result_keyboard(body_type, km_status, search_url)

        bot.send_message(
            chat_id,
            message_content,
            reply_markup=markup,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error while searching cars: {e}", exc_info=True)
        # Remove loading msg if still present
        try:
            bot.delete_message(chat_id, loading_msg.message_id)
        except Exception:
            pass

        bot.send_message(
            chat_id,
            "❌ متأسفانه در ارتباط با سایت همراه مکانیک خطایی رخ داد. لطفاً چند لحظه بعد مجدداً امتحان کنید."
        )


# ==================== Main Runner ====================

def main():
    if not IS_CONFIGURED:
        print("=" * 60)
        print("❌ خطا: توکن ربات تلگرام تنظیم نشده است!")
        print("لطفاً فایل .env را در مسیر پروژه ایجاد کرده و توکن خود را در آن وارد کنید:")
        print("    BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        print("یا به عنوان متغیر محیطی ست کنید:")
        print("    $env:BOT_TOKEN=\"your_token_here\"  # PowerShell")
        print("=" * 60)
        logger.error("BOT_TOKEN is missing or not configured. Exiting.")
        sys.exit(1)

    logger.info("Bot is starting polling...")
    print("ربات با موفقیت راه‌اندازی شد. در حال گوش دادن به پیام‌ها...")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
