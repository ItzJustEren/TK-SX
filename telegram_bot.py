# telegram_bot.py
# Cyrus Bot - ربات فروش کامل TK-SX
# شامل: جوین کانال، ثبت کارت، کیف پول، معرفی، تخفیف، قرعه‌کشی، پرداخت‌ها، رد با دلیل

import asyncio
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from main import (
    LINKS, LINKS_LOCK, SUBS, SUBS_LOCK,
    PRODUCTS, PRODUCTS_LOCK, ORDERS, ORDERS_LOCK,
    CARD_NUMBER, CARD_OWNER_NAME, PRICE_PER_GB, ADMIN_IDS, OWNER_ID,
    TEST_USERS, USER_CODES, REYMIT_LINKS, FEEDBACKS, TUTORIAL_CHANNEL, ADMIN_GROUP_ID,
    WALLETS, WALLETS_LOCK, TRANSACTIONS,
    USER_CARDS, CARDS_LOCK,
    REFERRALS, REFERRALS_LOCK,
    DISCOUNT_CODES, DISCOUNT_LOCK,
    LOTTERY, LOTTERY_LOCK,
    make_link, generate_user_code, calculate_user_level,
    get_balance, add_balance, deduct_balance,
    register_card, get_card_status,
    generate_referral_code, get_referral_info, add_referral_earning,
    use_discount_code, create_discount_code,
    log_activity, save_state, logger,
    generate_link_url, get_host, CONFIG,
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    logger.warning("TELEGRAM_BOT_TOKEN not set")
    raise RuntimeError("Bot token missing")

REQUIRED_CHANNEL = os.environ.get("REQUIRED_CHANNEL", "@TaaKaaOrg").strip()
if not REQUIRED_CHANNEL.startswith("@"):
    REQUIRED_CHANNEL = "@" + REQUIRED_CHANNEL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ── FSM States ──────────────────────────────────────────────────────────────
class BuyStates(StatesGroup):
    waiting_receipt = State()
    waiting_volume = State()
    waiting_renew_receipt = State()
    waiting_card_registration = State()
    waiting_gift_receipt = State()
    waiting_discount_code = State()

class FeedbackStates(StatesGroup):
    waiting_feedback = State()

class AdminStates(StatesGroup):
    waiting_reject_reason = State()
    waiting_reject_reason_other = State()

# ── Helper functions ────────────────────────────────────────────────────────
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def check_channel_membership(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

async def is_card_registered(user_id: int) -> bool:
    card = await get_card_status(user_id)
    return card is not None and card.get("status") == "approved"

# ── Keyboard builders ──────────────────────────────────────────────────────
def get_main_menu_keyboard(is_admin_user: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🛍️ خرید اشتراک", callback_data="buy"))
    builder.row(InlineKeyboardButton(text="💰 کیف پول", callback_data="wallet"), InlineKeyboardButton(text="📂 اشتراک‌ها", callback_data="my_subscriptions"))
    builder.row(InlineKeyboardButton(text="💡 آموزش", callback_data="tutorials"), InlineKeyboardButton(text="👤 حساب", callback_data="my_account"))
    builder.row(InlineKeyboardButton(text="🧪 تست رایگان", callback_data="test_service"), InlineKeyboardButton(text="📞 پشتیبانی", callback_data="support"))
    builder.row(InlineKeyboardButton(text="🔗 معرفی", callback_data="referral"), InlineKeyboardButton(text="🎁 قرعه‌کشی", callback_data="lottery"))
    builder.row(InlineKeyboardButton(text="✍️ بازخورد", callback_data="send_feedback"), InlineKeyboardButton(text="💬 بازخوردها", callback_data="view_feedbacks"))
    if is_admin_user:
        builder.row(InlineKeyboardButton(text="⚙️ پنل ادمین", callback_data="admin_panel"))
    return builder.as_markup()

def get_payment_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💳 کارت به کارت", callback_data="pay_card"), InlineKeyboardButton(text="🌐 ریمیت", callback_data="pay_reymit"))
    builder.row(InlineKeyboardButton(text="⭐ استارز", callback_data="pay_stars"), InlineKeyboardButton(text="🎁 گیفت", callback_data="pay_gift"))
    builder.row(InlineKeyboardButton(text="🔙 بازگشت", callback_data="main_menu"))
    return builder.as_markup()

def get_reject_reason_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⏰ بعد از ساعت معین", callback_data="reject_reason:late"), InlineKeyboardButton(text="🖼 رسید فیک", callback_data="reject_reason:fake"))
    builder.row(InlineKeyboardButton(text="📝 دلیل دیگر", callback_data="reject_reason:other"))
    return builder.as_markup()

def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📦 محصولات", callback_data="admin_products"), InlineKeyboardButton(text="📋 سفارشات", callback_data="admin_orders:0"))
    builder.row(InlineKeyboardButton(text="👥 ادمین‌ها", callback_data="admin_admins"), InlineKeyboardButton(text="💳 کارت‌ها", callback_data="admin_cards"))
    builder.row(InlineKeyboardButton(text="🎟️ تخفیف‌ها", callback_data="admin_discounts"), InlineKeyboardButton(text="💰 تنظیمات", callback_data="admin_settings"))
    builder.row(InlineKeyboardButton(text="📊 آمار", callback_data="admin_stats"), InlineKeyboardButton(text="🎁 قرعه‌کشی", callback_data="admin_lottery"))
    builder.row(InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu"))
    return builder.as_markup()

# ── Start Command ──────────────────────────────────────────────────────────
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id

    # Check channel membership
    if not await check_channel_membership(user_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 عضویت", url=f"https://t.me/{REQUIRED_CHANNEL.lstrip('@')}")],
            [InlineKeyboardButton(text="✅ بررسی", callback_data="check_membership")]
        ])
        await message.answer(f"👋 لطفاً در کانال {REQUIRED_CHANNEL} عضو شوید.", reply_markup=keyboard)
        return

    # Check card registration
    if not await is_card_registered(user_id):
        await state.set_state(BuyStates.waiting_card_registration)
        await message.answer(
            "📝 **ثبت اطلاعات کارت**\n\n"
            "لطفاً به صورت زیر ارسال کنید:\n"
            "`شماره کارت | نام و نام خانوادگی`\n\n"
            "مثال: `6037-9910-1234-5678 | علی محمدی`\n\n"
            "⚠️ با ثبت این اطلاعات، قوانین TK-SX را می‌پذیرید.",
            parse_mode="Markdown"
        )
        return

    await show_main_menu(message)

@dp.callback_query(F.data == "check_membership")
async def callback_check_membership(callback: CallbackQuery):
    if await check_channel_membership(callback.from_user.id):
        await callback.answer("✅ عضویت تأیید شد!", show_alert=True)
        await cmd_start(callback.message, None)
    else:
        await callback.answer("❌ عضو نشده‌اید.", show_alert=True)

@dp.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await show_main_menu(callback.message)

async def show_main_menu(message: types.Message):
    keyboard = get_main_menu_keyboard(is_admin(message.from_user.id))
    await message.answer("👋 **به Cyrus Bot خوش آمدید!**", reply_markup=keyboard, parse_mode="Markdown")

# ── Card Registration ──────────────────────────────────────────────────────
@dp.message(BuyStates.waiting_card_registration)
async def handle_card_registration(message: types.Message, state: FSMContext):
    try:
        parts = [p.strip() for p in message.text.split("|")]
        if len(parts) != 2:
            raise ValueError("فرمت صحیح نیست")
        card_number, full_name = parts
        await register_card(message.from_user.id, card_number, full_name)
        await save_state()
        await send_card_to_admins(message.from_user.id, card_number, full_name)
        await message.answer("✅ کارت ثبت شد. در انتظار تأیید ادمین...")
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ خطا: {e}\nفرمت: `شماره کارت | نام و نام خانوادگی`")

async def send_card_to_admins(user_id: int, card_number: str, full_name: str):
    user = await bot.get_chat(user_id)
    text = f"💳 **ثبت کارت جدید**\n\n👤 {user.full_name} (@{user.username or 'ندارد'})\n🆔 {user_id}\n💳 {card_number}\n📝 {full_name}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ تایید", callback_data=f"approve_card:{user_id}"),
         InlineKeyboardButton(text="❌ رد", callback_data=f"reject_card:{user_id}")]
    ])
    if ADMIN_GROUP_ID:
        try:
            topic = await bot.create_forum_topic(chat_id=ADMIN_GROUP_ID, name="💳 ثبت کارت‌ها")
            await bot.send_message(ADMIN_GROUP_ID, text, reply_markup=keyboard, message_thread_id=topic.message_thread_id)
            return
        except:
            pass
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, reply_markup=keyboard)
        except:
            pass

@dp.callback_query(F.data.startswith("approve_card:"))
async def approve_card(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    user_id = int(callback.data.split(":")[1])
    async with CARDS_LOCK:
        if user_id not in USER_CARDS:
            await callback.answer("کارت یافت نشد.", show_alert=True)
            return
        USER_CARDS[user_id]["status"] = "approved"
        USER_CARDS[user_id]["approved_at"] = datetime.now().isoformat()
    await save_state()
    try:
        await bot.send_message(user_id, "✅ کارت شما تأیید شد! 🎉\nدستور /start را ارسال کنید.")
    except:
        pass
    await callback.message.edit_text(f"✅ کارت کاربر {user_id} تأیید شد.")
    await callback.answer()

@dp.callback_query(F.data.startswith("reject_card:"))
async def reject_card(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    user_id = int(callback.data.split(":")[1])
    async with CARDS_LOCK:
        if user_id not in USER_CARDS:
            await callback.answer("کارت یافت نشد.", show_alert=True)
            return
        USER_CARDS[user_id]["status"] = "rejected"
    await save_state()
    try:
        await bot.send_message(user_id, "❌ کارت شما رد شد. با پشتیبانی تماس بگیرید @ItzJustEren")
    except:
        pass
    await callback.message.edit_text(f"❌ کارت کاربر {user_id} رد شد.")
    await callback.answer()

# ── Buy Flow ────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "buy")
async def callback_buy(callback: CallbackQuery):
    if not await is_card_registered(callback.from_user.id):
        await callback.answer("❌ ابتدا کارت خود را ثبت کنید!", show_alert=True)
        return
    if not PRODUCTS:
        await callback.answer("❌ محصولی موجود نیست.", show_alert=True)
        return
    builder = InlineKeyboardBuilder()
    for pid, prod in PRODUCTS.items():
        builder.button(text=f"{prod['name']} — {prod['volume_gb']}GB / {prod['duration_days']} روز — {prod['price']:,} تومان", callback_data=f"buy:{pid}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu"))
    await callback.message.edit_text("🛒 **محصولات:**", reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("buy:"))
async def callback_product_select(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":")[1]
    product = PRODUCTS.get(product_id)
    if not product:
        await callback.answer("❌ محصول یافت نشد.", show_alert=True)
        return
    await state.update_data(product_id=product_id, product_price=product['price'])
    await callback.message.edit_text(f"📦 **{product['name']}**\n💰 {product['price']:,} تومان\n\nروش پرداخت را انتخاب کنید:", reply_markup=get_payment_keyboard(), parse_mode="Markdown")
    await callback.answer()

# ── Payment Methods ────────────────────────────────────────────────────────
@dp.callback_query(F.data == "pay_card")
async def pay_card(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = PRODUCTS.get(data.get("product_id"))
    if not product:
        await callback.answer("❌ محصول یافت نشد.", show_alert=True)
        return
    user_code = generate_user_code()
    USER_CODES[callback.from_user.id] = {"code": user_code, "created_at": datetime.now()}
    order_id = secrets.token_hex(8).upper()
    order = {"order_id": order_id, "user_id": callback.from_user.id, "product_id": product['product_id'], "volume": product['volume_gb'], "duration": product['duration_days'], "speed": product['speed_mbps'], "price": product['price'], "status": "pending", "created_at": datetime.now().isoformat(), "user_code": user_code, "payment_method": "card"}
    async with ORDERS_LOCK:
        ORDERS[order_id] = order
    await save_state()
    text = f"💳 **کارت به کارت**\n💰 {product['price']:,} تومان\n🔑 کد: `{user_code}`\n💳 شماره کارت: `{CARD_NUMBER}`\n👤 {CARD_OWNER_NAME}\n⏳ مهلت ۱ ساعت"
    await callback.message.edit_text(text, parse_mode="Markdown")
    await state.set_state(BuyStates.waiting_receipt)
    await state.update_data(order_id=order_id, order_time=datetime.now(), user_code=user_code, is_renew=False)
    await callback.answer()

@dp.callback_query(F.data == "pay_reymit")
async def pay_reymit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = PRODUCTS.get(data.get("product_id"))
    if not product:
        await callback.answer("❌ محصول یافت نشد.", show_alert=True)
        return
    user_code = generate_user_code()
    USER_CODES[callback.from_user.id] = {"code": user_code, "created_at": datetime.now()}
    order_id = secrets.token_hex(8).upper()
    order = {"order_id": order_id, "user_id": callback.from_user.id, "product_id": product['product_id'], "volume": product['volume_gb'], "duration": product['duration_days'], "speed": product['speed_mbps'], "price": product['price'], "status": "pending", "created_at": datetime.now().isoformat(), "user_code": user_code, "payment_method": "reymit"}
    async with ORDERS_LOCK:
        ORDERS[order_id] = order
    await save_state()
    reymit_link = REYMIT_LINKS[0] if REYMIT_LINKS else "https://reymit.ir/itzjusteren"
    text = f"🌐 **ریمیت**\n💰 {product['price']:,} تومان\n🔑 کد: `{user_code}`\n🔗 لینک: `{reymit_link}`\n⚠️ نام خود را **کد کاربری** وارد کنید."
    await callback.message.edit_text(text, parse_mode="Markdown")
    await state.set_state(BuyStates.waiting_receipt)
    await state.update_data(order_id=order_id, order_time=datetime.now(), user_code=user_code, is_renew=False)
    await callback.answer()

@dp.callback_query(F.data == "pay_stars")
async def pay_stars(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = PRODUCTS.get(data.get("product_id"))
    if not product:
        await callback.answer("❌ محصول یافت نشد.", show_alert=True)
        return
    stars_required = int(product['price'] / CONFIG["stars_rate"]) + 1
    await callback.message.edit_text(f"⭐ **استارز**\n💰 {product['price']:,} تومان\n⭐ {stars_required} استارز\n(هر استارز = {CONFIG['stars_rate']} تومان)\nاز @PremiumBot خریداری کنید.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ پرداخت کردم", callback_data=f"confirm_stars:{product['product_id']}")]]), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("confirm_stars:"))
async def confirm_stars(callback: CallbackQuery):
    await callback.message.edit_text("⭐ پرداخت با استارز انجام شد. سفارش شما در حال پردازش است...")
    await callback.answer()

@dp.callback_query(F.data == "pay_gift")
async def pay_gift(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = PRODUCTS.get(data.get("product_id"))
    if not product:
        await callback.answer("❌ محصول یافت نشد.", show_alert=True)
        return
    user_code = generate_user_code()
    USER_CODES[callback.from_user.id] = {"code": user_code, "created_at": datetime.now()}
    order_id = secrets.token_hex(8).upper()
    order = {"order_id": order_id, "user_id": callback.from_user.id, "product_id": product['product_id'], "volume": product['volume_gb'], "duration": product['duration_days'], "speed": product['speed_mbps'], "price": product['price'], "status": "pending", "created_at": datetime.now().isoformat(), "user_code": user_code, "payment_method": "gift"}
    async with ORDERS_LOCK:
        ORDERS[order_id] = order
    await save_state()
    text = f"🎁 **گیفت**\n🔑 کد: `{user_code}`\n📱 ارسال به @ItzJustEren\n⚠️ **حالت ناشناس را فعال نکنید**\nپس از ارسال، رسید را بفرستید."
    await callback.message.edit_text(text, parse_mode="Markdown")
    await state.set_state(BuyStates.waiting_gift_receipt)
    await state.update_data(order_id=order_id, order_time=datetime.now(), user_code=user_code, is_renew=False)
    await callback.answer()

# ── Receipt Handling ────────────────────────────────────────────────────────
@dp.message(BuyStates.waiting_receipt, F.photo)
async def handle_receipt(message: types.Message, state: FSMContext):
    await handle_receipt_common(message, state, is_gift=False)

@dp.message(BuyStates.waiting_gift_receipt, F.photo)
async def handle_gift_receipt(message: types.Message, state: FSMContext):
    await handle_receipt_common(message, state, is_gift=True)

async def handle_receipt_common(message: types.Message, state: FSMContext, is_gift: bool = False):
    data = await state.get_data()
    order_id = data.get("order_id")
    order_time = data.get("order_time")
    user_code = data.get("user_code")
    order = ORDERS.get(order_id)
    if not order:
        await message.answer("❌ سفارش یافت نشد.")
        await state.clear()
        return
    if order_time and (datetime.now() - order_time).total_seconds() > 3600:
        await message.answer("⛔ مهلت ۱ ساعته پایان یافت.")
        await state.clear()
        return
    product = PRODUCTS.get(order['product_id'])
    if product:
        await send_order_to_admins(order_id, order['user_id'], product, user_code, message, is_gift)
    await message.answer("✅ رسید دریافت شد. در انتظار تأیید...")
    await state.clear()

async def send_order_to_admins(order_id: str, user_id: int, product: dict, user_code: str, receipt_msg: types.Message, is_gift: bool = False):
    order = ORDERS.get(order_id)
    if not order:
        return
    user = await bot.get_chat(user_id)
    text = f"🆕 **{('گیفت' if is_gift else 'سفارش')} #{order_id}**\n\n👤 {user.full_name} (@{user.username or 'ندارد'})\n🆔 {user_id}\n🔑 `{user_code}`\n📦 {product['name']}\n📊 {product['volume_gb']}GB\n💰 {product['price']:,} تومان\n💳 {order.get('payment_method', 'نامشخص')}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ تایید", callback_data=f"approve:{order_id}"), InlineKeyboardButton(text="❌ رد", callback_data=f"reject:{order_id}")]])
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_photo(admin_id, photo=receipt_msg.photo[-1].file_id, caption=text, reply_markup=keyboard, parse_mode="Markdown")
        except:
            pass

# ── Approve / Reject Order ──────────────────────────────────────────────────
@dp.callback_query(F.data.startswith("approve:"))
async def approve_order(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    order_id = callback.data.split(":")[1]
    order = ORDERS.get(order_id)
    if not order or order["status"] != "pending":
        await callback.answer("سفارش یافت نشد یا بررسی شده.", show_alert=True)
        return
    product = PRODUCTS.get(order['product_id'])
    if not product:
        await callback.answer("❌ محصول حذف شده.", show_alert=True)
        return
    volume_bytes = product['volume_gb'] * 1024 * 1024 * 1024
    expires_at = (datetime.now() + timedelta(days=product['duration_days'])).isoformat()
    uid, link = await make_link(label=f"سفارش {order_id}", limit_bytes=volume_bytes, expires_at=expires_at, protocol="vless", port=443)
    sub_id = secrets.token_hex(8)
    async with SUBS_LOCK:
        SUBS[sub_id] = {"name": f"سفارش {order_id}", "uuid_key": sub_id, "created_at": datetime.now().isoformat(), "link_ids": [uid]}
    async with ORDERS_LOCK:
        ORDERS[order_id]["status"] = "confirmed"
        ORDERS[order_id]["config_uuid"] = uid
        ORDERS[order_id]["sub_id"] = sub_id
    await save_state()
    host = get_host()
    link_url = generate_link_url(uid, link, host)
    sub_url = f"https://{host}/p/{sub_id}"
    # Referral bonus
    ref_info = await get_referral_info(order['user_id'])
    if ref_info and ref_info.get("referred_by"):
        earnings = int(product['price'] * 0.1)
        await add_referral_earning(ref_info["referred_by"], earnings)
        try:
            await bot.send_message(ref_info["referred_by"], f"🎉 سود معرفی: {earnings} تومان به کیف پول اضافه شد.")
        except:
            pass
    await bot.send_message(order['user_id'], f"🎉 خرید شما انجام شد!\n🔗 لینک ساب: `{sub_url}`\n🔗 VLESS: `{link_url}`", parse_mode="Markdown")
    await callback.message.edit_text(f"✅ سفارش #{order_id} تأیید شد.")
    await callback.answer()

@dp.callback_query(F.data.startswith("reject:"))
async def reject_order(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    order_id = callback.data.split(":")[1]
    order = ORDERS.get(order_id)
    if not order or order["status"] != "pending":
        await callback.answer("سفارش یافت نشد.", show_alert=True)
        return
    await state.update_data(reject_order_id=order_id)
    await state.set_state(AdminStates.waiting_reject_reason)
    await callback.message.edit_text(f"❌ دلیل رد سفارش #{order_id}:", reply_markup=get_reject_reason_keyboard())
    await callback.answer()

@dp.callback_query(AdminStates.waiting_reject_reason, F.data.startswith("reject_reason:"))
async def reject_reason(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    reason_code = callback.data.split(":")[1]
    data = await state.get_data()
    order_id = data.get("reject_order_id")
    if reason_code == "other":
        await callback.message.edit_text("✏️ دلیل را بنویسید:")
        await state.set_state(AdminStates.waiting_reject_reason_other)
        await callback.answer()
        return
    reason_texts = {"fake": "🖼 رسید فیک", "late": "⏰ بعد از ساعت معین"}
    reason = reason_texts.get(reason_code, "دلیل نامشخص")
    await process_reject_order(order_id, reason, callback.message)
    await state.clear()
    await callback.answer()

@dp.message(AdminStates.waiting_reject_reason_other)
async def reject_reason_other(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ دسترسی ندارید.")
        return
    data = await state.get_data()
    order_id = data.get("reject_order_id")
    await process_reject_order(order_id, message.text, message)
    await state.clear()

async def process_reject_order(order_id: str, reason: str, msg_obj):
    order = ORDERS.get(order_id)
    if not order:
        await msg_obj.edit_text("❌ سفارش یافت نشد.")
        return
    async with ORDERS_LOCK:
        ORDERS[order_id]["status"] = "rejected"
        ORDERS[order_id]["reject_reason"] = reason
    await save_state()
    try:
        await bot.send_message(order['user_id'], f"❌ سفارش #{order_id} رد شد.\n📌 دلیل: {reason}\n💡 اگر خطاست به @ItzJustEren گزارش دهید.", parse_mode="Markdown")
    except:
        pass
    await msg_obj.edit_text(f"✅ سفارش #{order_id} رد شد.\nدلیل: {reason}")

# ── Wallet ──────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery):
    balance = await get_balance(callback.from_user.id)
    transactions = [t for t in TRANSACTIONS if t["user_id"] == callback.from_user.id][-10:]
    text = f"💰 موجودی: {balance:,} تومان\n\n"
    if transactions:
        text += "📋 تراکنش‌ها:\n" + "\n".join(f"{'+' if t['amount']>0 else ''}{t['amount']:,} - {t['description']}" for t in transactions)
    else:
        text += "تراکنشی وجود ندارد."
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💳 شارژ", callback_data="charge_wallet")], [InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "charge_wallet")
async def charge_wallet(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("💳 مبلغ شارژ را به تومان وارد کنید (حداقل ۱۰,۰۰۰):")
    await state.set_state("waiting_charge_amount")
    await callback.answer()

@dp.message(StateFilter("waiting_charge_amount"))
async def handle_charge_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text.replace(",", ""))
        if amount < 10000:
            await message.answer("❌ حداقل ۱۰,۰۰۰ تومان.")
            return
        await state.update_data(charge_amount=amount)
        for admin_id in ADMIN_IDS:
            await bot.send_message(admin_id, f"💳 درخواست شارژ {amount:,} تومان از {message.from_user.full_name} (@{message.from_user.username or 'ندارد'})\n🆔 {message.from_user.id}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ تایید", callback_data=f"approve_charge:{message.from_user.id}:{amount}")]]))
        await message.answer("✅ درخواست به ادمین ارسال شد.")
        await state.clear()
    except:
        await message.answer("❌ عدد معتبر وارد کنید.")

@dp.callback_query(F.data.startswith("approve_charge:"))
async def approve_charge(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    _, user_id, amount = callback.data.split(":")
    user_id, amount = int(user_id), int(amount)
    await add_balance(user_id, amount, f"شارژ توسط ادمین", callback.from_user.id)
    await bot.send_message(user_id, f"✅ {amount:,} تومان به کیف پول شما اضافه شد.")
    await callback.message.edit_text(f"✅ شارژ {amount:,} تومان کاربر {user_id} تایید شد.")
    await callback.answer()

# ── Referral ────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "referral")
async def referral(callback: CallbackQuery):
    info = await get_referral_info(callback.from_user.id)
    if not info:
        code = await generate_referral_code(callback.from_user.id)
    else:
        code = info["code"]
    link = f"https://t.me/{CONFIG['bot_username']}?start=ref_{code}"
    earnings = info.get("earnings", 0) if info else 0
    await callback.message.edit_text(f"🔗 لینک معرفی:\n`{link}`\n💰 درآمد: {earnings:,} تومان", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]), parse_mode="Markdown")
    await callback.answer()

# ── Lottery ──────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "lottery")
async def lottery(callback: CallbackQuery):
    async with LOTTERY_LOCK:
        lottery = dict(LOTTERY)
    if not lottery.get("active"):
        await callback.message.edit_text("🎁 قرعه‌کشی فعال نیست.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
        await callback.answer()
        return
    tickets = lottery.get("participants", {}).get(str(callback.from_user.id), 0)
    await callback.message.edit_text(f"🎁 **قرعه‌کشی**\n🏆 جایزه: {lottery.get('prize')}\n🎫 بلیت‌های شما: {tickets}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]), parse_mode="Markdown")
    await callback.answer()

# ── Test Service ──────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "test_service")
async def test_service(callback: CallbackQuery):
    user_id = callback.from_user.id
    test_data = TEST_USERS.get(user_id)
    if test_data and (datetime.now() - test_data["last_test"]).days < 7:
        remaining = 7 - (datetime.now() - test_data["last_test"]).days
        await callback.answer(f"⛔ {remaining} روز دیگر تلاش کنید.", show_alert=True)
        return
    uid, link = await make_link(label=f"تست {callback.from_user.full_name}", limit_bytes=50*1024*1024, expires_at=(datetime.now()+timedelta(days=1)).isoformat(), protocol="vless", port=443)
    TEST_USERS[user_id] = {"last_test": datetime.now(), "used": True}
    await save_state()
    host = get_host()
    link_url = generate_link_url(uid, link, host)
    await callback.message.edit_text(f"🧪 کانفیگ تست:\n`{link_url}`\n⏳ ۱ روز | ۵۰ مگابایت", parse_mode="Markdown")
    await callback.answer()

# ── My Account ──────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "my_account")
async def my_account(callback: CallbackQuery):
    user_orders = [o for o in ORDERS.values() if o["user_id"] == callback.from_user.id and o["status"] == "confirmed"]
    level = calculate_user_level(callback.from_user.id)
    balance = await get_balance(callback.from_user.id)
    text = f"👤 حساب کاربری\n🆔 {callback.from_user.id}\n📊 خرید: {len(user_orders)}\n⭐ سطح: {level}\n💰 موجودی: {balance:,} تومان"
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
    await callback.answer()

# ── My Subscriptions ──────────────────────────────────────────────────────────
@dp.callback_query(F.data == "my_subscriptions")
async def my_subscriptions(callback: CallbackQuery):
    user_orders = [o for o in ORDERS.values() if o["user_id"] == callback.from_user.id and o["status"] == "confirmed"]
    if not user_orders:
        await callback.message.edit_text("❌ اشتراکی ندارید.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
        await callback.answer()
        return
    text = "📂 اشتراک‌های شما:\n"
    for order in user_orders:
        sub_id = order.get("sub_id")
        sub_url = f"https://{get_host()}/p/{sub_id}" if sub_id else "نامشخص"
        product = PRODUCTS.get(order["product_id"])
        text += f"📦 {product['name'] if product else 'نامشخص'} - {order['volume']}GB\n🔗 `{sub_url}`\n"
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 تمدید", callback_data="renew_subscription")], [InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "renew_subscription")
async def renew_subscription(callback: CallbackQuery):
    user_orders = [o for o in ORDERS.values() if o["user_id"] == callback.from_user.id and o["status"] == "confirmed"]
    if not user_orders:
        await callback.answer("❌ اشتراکی برای تمدید ندارید.", show_alert=True)
        return
    builder = InlineKeyboardBuilder()
    for order in user_orders:
        product = PRODUCTS.get(order["product_id"])
        builder.button(text=f"{product['name'] if product else 'نامشخص'} - {order['volume']}GB", callback_data=f"renew:{order['order_id']}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 بازگشت", callback_data="my_subscriptions"))
    await callback.message.edit_text("🔄 اشتراک مورد نظر را انتخاب کنید:", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("renew:"))
async def renew_confirm(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.split(":")[1]
    order = ORDERS.get(order_id)
    if not order:
        await callback.answer("❌ اشتراک یافت نشد.", show_alert=True)
        return
    product = PRODUCTS.get(order["product_id"])
    if not product:
        await callback.answer("❌ محصول یافت نشد.", show_alert=True)
        return
    user_code = generate_user_code()
    USER_CODES[callback.from_user.id] = {"code": user_code, "created_at": datetime.now()}
    new_order_id = secrets.token_hex(8).upper()
    new_order = {"order_id": new_order_id, "user_id": callback.from_user.id, "product_id": order["product_id"], "volume": product['volume_gb'], "duration": product['duration_days'], "speed": product['speed_mbps'], "price": product['price'], "status": "pending", "created_at": datetime.now().isoformat(), "user_code": user_code, "payment_method": "renew", "renew_of": order_id}
    async with ORDERS_LOCK:
        ORDERS[new_order_id] = new_order
    await save_state()
    await callback.message.edit_text(f"🔄 تمدید\n📦 {product['name']}\n💰 {product['price']:,} تومان\n🔑 کد: `{user_code}`\n💳 شماره کارت: `{CARD_NUMBER}`\n👤 {CARD_OWNER_NAME}", parse_mode="Markdown")
    await state.set_state(BuyStates.waiting_receipt)
    await state.update_data(order_id=new_order_id, order_time=datetime.now(), user_code=user_code, is_renew=True)
    await callback.answer()

# ── Tutorials ────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "tutorials")
async def tutorials(callback: CallbackQuery):
    await callback.message.edit_text(f"💡 آموزش‌ها در کانال {TUTORIAL_CHANNEL}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
    await callback.answer()

# ── Support ──────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.edit_text("📞 پشتیبانی: @ItzJustEren", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
    await callback.answer()

# ── Feedback ──────────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "send_feedback")
async def send_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✍️ متن بازخورد را ارسال کنید:")
    await state.set_state(FeedbackStates.waiting_feedback)
    await callback.answer()

@dp.message(FeedbackStates.waiting_feedback)
async def handle_feedback(message: types.Message, state: FSMContext):
    feedback_data = {"id": secrets.token_hex(8), "user_id": message.from_user.id, "username": message.from_user.username or "کاربر", "text": message.text, "created_at": datetime.now().isoformat(), "approved": False}
    FEEDBACKS.append(feedback_data)
    await save_state()
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, f"📝 بازخورد جدید:\n{message.text}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ تایید", callback_data=f"approve_fb:{feedback_data['id']}"), InlineKeyboardButton(text="❌ رد", callback_data=f"reject_fb:{feedback_data['id']}")]]))
    await message.answer("✅ بازخورد ثبت شد.")
    await state.clear()

@dp.callback_query(F.data.startswith("approve_fb:"))
async def approve_fb(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    fb_id = callback.data.split(":")[1]
    for fb in FEEDBACKS:
        if fb.get("id") == fb_id:
            fb["approved"] = True
            await save_state()
            await callback.message.edit_text("✅ بازخورد تایید شد.")
            await callback.answer()
            return

@dp.callback_query(F.data == "view_feedbacks")
async def view_feedbacks(callback: CallbackQuery):
    approved = [fb for fb in FEEDBACKS if fb.get("approved", False)]
    if not approved:
        await callback.message.edit_text("💬 بازخوردی وجود ندارد.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
        await callback.answer()
        return
    text = "💬 بازخوردها:\n" + "\n".join(f"👤 {fb['username']}: {fb['text']}" for fb in approved[-10:])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 منوی اصلی", callback_data="main_menu")]]))
    await callback.answer()

# ── Admin Panel ──────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    await callback.message.edit_text("⚙️ پنل ادمین:", reply_markup=get_admin_dashboard_keyboard())
    await callback.answer()

# ── Admin: Products ──────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_products")
async def admin_products(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    text = "📦 محصولات:\n" + "\n".join(f"{p['name']} - {p['volume_gb']}GB - {p['price']:,} تومان" for p in PRODUCTS.values())
    await callback.message.edit_text(text or "محصولی وجود ندارد.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ افزودن", callback_data="admin_add_product")], [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

@dp.callback_query(F.data == "admin_add_product")
async def admin_add_product(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    await callback.message.edit_text("فرمت: `نام | حجم(GB) | مدت(روز) | سرعت(Mbps) | قیمت(تومان)`\nمثال: `کانفیگ استاندارد | 50 | 30 | 100 | 150000`")
    await state.set_state("waiting_product_data")
    await callback.answer()

@dp.message(StateFilter("waiting_product_data"))
async def handle_add_product(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ دسترسی ندارید.")
        return
    try:
        name, volume, duration, speed, price = [p.strip() for p in message.text.split("|")]
        volume, duration, speed, price = float(volume), int(duration), float(speed), float(price)
        product_id = secrets.token_hex(8)
        async with PRODUCTS_LOCK:
            PRODUCTS[product_id] = {"product_id": product_id, "name": name, "volume_gb": volume, "duration_days": duration, "speed_mbps": speed, "price": price, "created_at": datetime.now().isoformat()}
        await save_state()
        await message.answer(f"✅ محصول {name} اضافه شد.")
    except:
        await message.answer("❌ فرمت اشتباه.")
    await state.clear()

# ── Admin: Orders ────────────────────────────────────────────────────────────
@dp.callback_query(F.data.startswith("admin_orders:"))
async def admin_orders(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    page = int(callback.data.split(":")[1])
    pending = [o for o in ORDERS.values() if o.get("status") == "pending"]
    start, end = page*5, min((page+1)*5, len(pending))
    text = "📋 سفارشات در انتظار:\n" + "\n".join(f"#{o['order_id']} - {o['user_id']} - {o.get('price',0):,} تومان" for o in pending[start:end]) or "هیچ سفارشی وجود ندارد."
    builder = InlineKeyboardBuilder()
    if start > 0:
        builder.button(text="◀ قبلی", callback_data=f"admin_orders:{page-1}")
    if end < len(pending):
        builder.button(text="بعدی ▶", callback_data=f"admin_orders:{page+1}")
    builder.row(InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()

# ── Admin: Admins ────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_admins")
async def admin_admins(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    text = "👥 ادمین‌ها:\n" + "\n".join(f"🆔 {uid}" for uid in ADMIN_IDS)
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ افزودن", callback_data="admin_add_admin")], [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

@dp.callback_query(F.data == "admin_add_admin")
async def admin_add_admin(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    await callback.message.edit_text("آیدی عددی ادمین جدید را وارد کنید:")
    await state.set_state("waiting_admin_id")
    await callback.answer()

@dp.message(StateFilter("waiting_admin_id"))
async def handle_add_admin(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ دسترسی ندارید.")
        return
    try:
        user_id = int(message.text.strip())
        ADMIN_IDS.add(user_id)
        await save_state()
        await message.answer(f"✅ ادمین {user_id} اضافه شد.")
    except:
        await message.answer("❌ آیدی عددی معتبر وارد کنید.")
    await state.clear()

# ── Admin: Cards ─────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_cards")
async def admin_cards(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    cards = [f"🆔 {uid} - {c['card_number']} - {c['full_name']} - {c['status']}" for uid, c in USER_CARDS.items() if c.get("status") == "pending"]
    await callback.message.edit_text("💳 کارت‌های در انتظار:\n" + "\n".join(cards) or "هیچ کارت در انتظاری نیست.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

# ── Admin: Discounts ──────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_discounts")
async def admin_discounts(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    text = "🎟️ کدهای تخفیف:\n" + "\n".join(f"{k} - {v['percent']}% - {v['used_count']}/{v['max_uses']}" for k,v in DISCOUNT_CODES.items()) or "کد تخفیفی وجود ندارد."
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ افزودن", callback_data="admin_add_discount")], [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

@dp.callback_query(F.data == "admin_add_discount")
async def admin_add_discount(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    await callback.message.edit_text("فرمت: `کد | درصد | حداکثر استفاده`\nمثال: `DISCOUNT10 | 10 | 100`")
    await state.set_state("waiting_discount_data")
    await callback.answer()

@dp.message(StateFilter("waiting_discount_data"))
async def handle_add_discount(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ دسترسی ندارید.")
        return
    try:
        code, percent, max_uses = [p.strip() for p in message.text.split("|")]
        code, percent, max_uses = code.upper(), int(percent), int(max_uses)
        expires_at = (datetime.now()+timedelta(days=30)).isoformat()
        await create_discount_code(code, percent, max_uses, expires_at, message.from_user.id)
        await message.answer(f"✅ کد {code} اضافه شد.")
    except:
        await message.answer("❌ فرمت اشتباه.")
    await state.clear()

# ── Admin: Settings ──────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_settings")
async def admin_settings(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    text = f"⚙️ تنظیمات:\n💳 شماره کارت: {CARD_NUMBER}\n👤 {CARD_OWNER_NAME}\n💰 هر گیگ: {PRICE_PER_GB} هزار تومان\n⭐ نرخ استارز: {CONFIG['stars_rate']} تومان"
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

# ── Admin: Stats ─────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    text = f"📊 آمار:\nسفارشات: {len(ORDERS)}\nدر انتظار: {len([o for o in ORDERS.values() if o.get('status')=='pending'])}\nمحصولات: {len(PRODUCTS)}\nکاربران: {len(WALLETS)}\nکارت‌ها: {len(USER_CARDS)}"
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

# ── Admin: Lottery ───────────────────────────────────────────────────────────
@dp.callback_query(F.data == "admin_lottery")
async def admin_lottery(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    async with LOTTERY_LOCK:
        lottery = dict(LOTTERY)
    status = "فعال" if lottery.get("active") else "غیرفعال"
    await callback.message.edit_text(f"🎁 قرعه‌کشی: {status}\n🏆 جایزه: {lottery.get('prize')}\n👥 شرکت‌کنندگان: {len(lottery.get('participants', {}))}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 شروع/توقف", callback_data="admin_toggle_lottery")], [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_panel")]]))
    await callback.answer()

@dp.callback_query(F.data == "admin_toggle_lottery")
async def admin_toggle_lottery(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ دسترسی ندارید.", show_alert=True)
        return
    async with LOTTERY_LOCK:
        LOTTERY["active"] = not LOTTERY.get("active", False)
        if LOTTERY["active"]:
            LOTTERY["started_at"] = datetime.now().isoformat()
        else:
            LOTTERY["ended_at"] = datetime.now().isoformat()
    await save_state()
    await callback.message.edit_text(f"✅ قرعه‌کشی {'فعال' if LOTTERY['active'] else 'غیرفعال'} شد.")
    await callback.answer()

# ── Start/Stop ──────────────────────────────────────────────────────────────
_poll_task: Optional[asyncio.Task] = None

async def start_bot():
    global _poll_task
    if not BOT_TOKEN:
        return
    logger.info("🤖 Starting Cyrus Bot...")
    _poll_task = asyncio.create_task(dp.start_polling(bot))

async def stop_bot():
    if _poll_task:
        _poll_task.cancel()
        try:
            await _poll_task
        except:
            pass
        await bot.session.close()
