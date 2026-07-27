import os
import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================
# 🔥 CONFIG - APNI DETAILS YAHAN DAALO
# ============================================

BOT_TOKEN = "7953489963:AAGkiKWjqIT4SlPfS_1EHxLzI6ZabgfuI4k"
ADMIN_IDS = [8603893462]
GROUP_USERNAME = "@CertifiedDeal"
POWERED_BY = "@cyber_amit"
BOT_NAME = "CYBER ESCROW BOT"

# ============================================
# DATABASE
# ============================================

DATA_FILE = "escrow_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "users": {},
        "global_stats": {
            "total_deals": 0,
            "total_volume": {"TON": 0, "USDT": 0, "INR": 0}
        }
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

data = load_data()

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ============================================
# HELPERS
# ============================================

def get_user_stats(user_id):
    user_id = str(user_id)
    if user_id not in data["users"]:
        data["users"][user_id] = {
            "rank": len(data["users"]) + 1,
            "active_deals": 0,
            "total_escrows": 0,
            "volume": {"TON": 0, "USDT": 0, "TR4": 0}
        }
        save_data(data)
    return data["users"][user_id]

# ============================================
# START COMMAND
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("📊 My Stats", callback_data="mystats")],
        [InlineKeyboardButton("📋 My Deals Info", callback_data="mydeals")],
        [InlineKeyboardButton("⏳ My Pending Deals", callback_data="mypending")],
        [InlineKeyboardButton("🌍 Escrow Global Stats", callback_data="globalstats")],
        [InlineKeyboardButton("👑 Admin Panel", callback_data="admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"🚀 **Welcome {user.upper()}!**\n\n"
        f"🔒 **Escrow Bot for {GROUP_USERNAME}**\n"
        f"⚡ Powered by {POWERED_BY}\n"
        f"🏦 **THE DIGITAL WORLD**\n"
        f"🎯 **FOCUS MUST WIN**\n\n"
        f"📌 **This is Your Personal Dashboard:**\n"
        f"Select the option below 👇"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ============================================
# BUTTON HANDLERS
# ============================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "mystats":
        stats = get_user_stats(user_id)
        text = (
            f"👤 **{query.from_user.first_name} Deal stats !**\n\n"
            f"🏆 **Rank** ➤ #{stats['rank']}\n"
            f"📌 **Active deals** ➤ {stats['active_deals']}\n"
            f"📦 **Total Escrow's** ➤ {stats['total_escrows']}\n"
            f"💰 **Total Volume** :\n"
            f"  • **TON** ➤ {stats['volume']['TON']}\n"
            f"  • **USDT** ➤ {stats['volume']['USDT']}\n"
            f"  • **TR4** ➤ {stats['volume']['TR4']}\n\n"
            f"🔒 **Escrow Bot for {GROUP_USERNAME}**\n"
            f"⚡ Provided by {POWERED_BY} !"
        )
        await query.edit_message_text(text, parse_mode="Markdown")
    
    elif query.data == "mydeals":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
        await query.edit_message_text(
            f"❌ **No deals found for you!**\n\n"
            f"🔒 Escrow Bot for {GROUP_USERNAME}\n"
            f"⚡ Provided by {POWERED_BY}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data == "mypending":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
        await query.edit_message_text(
            f"⏳ **You have no Pending deals!**\n\n"
            f"🔙 Press Back to return.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data == "globalstats":
        stats = data["global_stats"]
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="globalstats")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]
        text = (
            f"🌍 **Escrow Global Statistics**\n\n"
            f"📊 **Total Deals:** {stats['total_deals']}\n\n"
            f"💰 **Total Volume:**\n"
            f"  • {stats['total_volume']['TON']:.2f} TON\n"
            f"  • {stats['total_volume']['USDT']:.2f} USDT\n"
            f"  • {stats['total_volume']['INR']:.2f} INR\n\n"
            f"🔒 **Escrow Bot for {GROUP_USERNAME}**\n"
            f"⚡ Provided by {POWERED_BY}"
        )
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data == "admin_panel":
        if user_id not in ADMIN_IDS:
            await query.edit_message_text("❌ **Unauthorized!** You are not an admin.")
            return
        
        keyboard = [
            [InlineKeyboardButton("👥 Total Users", callback_data="admin_users")],
            [InlineKeyboardButton("💰 Total Volume", callback_data="admin_volume")],
            [InlineKeyboardButton("📝 Add Deal", callback_data="admin_add_deal")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]
        await query.edit_message_text(
            "👑 **Admin Panel**\n\nSelect an option:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    
    elif query.data == "admin_users":
        total_users = len(data["users"])
        await query.edit_message_text(
            f"👥 **Total Users:** {total_users}\n\n"
            f"🔒 {GROUP_USERNAME} Escrow Bot",
            parse_mode="Markdown"
        )
    
    elif query.data == "admin_volume":
        stats = data["global_stats"]
        await query.edit_message_text(
            f"💰 **Total Escrow Volume:**\n\n"
            f"• {stats['total_volume']['TON']:.2f} TON\n"
            f"• {stats['total_volume']['USDT']:.2f} USDT\n"
            f"• {stats['total_volume']['INR']:.2f} INR\n\n"
            f"📊 **Total Deals:** {stats['total_deals']}",
            parse_mode="Markdown"
        )
    
    elif query.data == "admin_add_deal":
        stats = data["global_stats"]
        stats["total_deals"] += 1
        stats["total_volume"]["TON"] += 10.5
        stats["total_volume"]["USDT"] += 250
        stats["total_volume"]["INR"] += 1500
        save_data(data)
        
        await query.edit_message_text(
            "✅ **Deal Added Successfully!**\n\n"
            f"📊 New Total Deals: {stats['total_deals']}\n"
            f"💰 New Total Volume: {stats['total_volume']['TON']:.2f} TON",
            parse_mode="Markdown"
        )
    
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📊 My Stats", callback_data="mystats")],
            [InlineKeyboardButton("📋 My Deals Info", callback_data="mydeals")],
            [InlineKeyboardButton("⏳ My Pending Deals", callback_data="mypending")],
            [InlineKeyboardButton("🌍 Escrow Global Stats", callback_data="globalstats")],
            [InlineKeyboardButton("👑 Admin Panel", callback_data="admin_panel")]
        ]
        await query.edit_message_text(
            f"🚀 **Welcome Back!**\n\n"
            f"🔒 **Escrow Bot for {GROUP_USERNAME}**\n"
            f"⚡ Powered by {POWERED_BY}\n\n"
            f"📌 **Dashboard:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

# ============================================
# MAIN
# ============================================

def main():
    print("🤖 Starting Escrow Bot...")
    print(f"🔒 Group: {GROUP_USERNAME}")
    print(f"⚡ Powered by: {POWERED_BY}")
    print(f"👑 Admin ID: {ADMIN_IDS}")
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
