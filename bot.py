import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import re

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8887965375:AAEwf6UR5F0oFSTqS5KTCmNxIVDyysyx4s8")
OWNER_ID = int(os.getenv("OWNER_ID", "7614459746"))
OWNER_USERNAME = "BeStChEaT_OwNeR"

user_states = {}

class PremiumSpamBot:
    def __init__(self):
        self.owner_id = OWNER_ID
        self.owner_username = OWNER_USERNAME
    
    def is_owner(self, user_id):
        return user_id == self.owner_id
    
    def bi(self, text):
        """BOLD + ITALIC formatting for EVERYTHING"""
        return f"***{text}***"
    
    def block_msg(self):
        return f"""
{self.bi('🔥 EXCLUSIVE PREMIUM BOT 🔥')}

{self.bi('🔐 ACCESS DENIED 🔐')}

{self.bi('♛ This bot is strictly private')}
{self.bi('and operates for owner only!')}

{self.bi('⭐ Owner: @' + self.owner_username)}

{self.bi('❌ Unauthorized access blocked!')}
{self.bi('Your attempt has been recorded.')}
"""
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        keyboard = [
            [InlineKeyboardButton(self.bi('🔥 START SPAMMING 🔥'), callback_data="start_spam")],
            [InlineKeyboardButton(self.bi('⭐ STATS ⭐'), callback_data="my_stats"),
             InlineKeyboardButton(self.bi('ℹ️ HELP ℹ️'), callback_data="help_menu")],
            [InlineKeyboardButton(self.bi('👥 GROUP SPAM 👥'), callback_data="target_group"),
             InlineKeyboardButton(self.bi('💬 PRIVATE SPAM 💬'), callback_data="target_private")],
            [InlineKeyboardButton(self.bi('🔐 OWNER PANEL 🔐'), callback_data="owner_panel")],
            [InlineKeyboardButton(self.bi('♛ OWNER CHANNEL ♛'), url=f"https://t.me/{self.owner_username}")]
        ]
        
        await update.message.reply_text(
            f"""
{self.bi('🔥🔥 EXCLUSIVE PREMIUM SPAM BOT 🔥🔥')}

{self.bi('♛ WELCOME BACK MASTER! ♛')}

{self.bi('⭐ PREMIUM FEATURES ⭐')}
{self.bi('• Ultra Fast Spamming')}
{self.bi('• Multi-Media Support')}
{self.bi('• Anti-Ban Protection')}
{self.bi('• Group & Private Mode')}
{self.bi('• Custom Speed Control')}
{self.bi('• Unlimited Messages')}
{self.bi('• 24/7 Running')}

{self.bi('🔐 STATUS: Private Mode')}
{self.bi('👑 ACCESS: Owner Only')}
{self.bi('🔥 PLAN: Exclusive Premium')}

{self.bi('SELECT AN OPTION BELOW 👇')}
""",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        if not self.is_owner(user_id):
            await query.edit_message_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        data = query.data
        
        if data == "start_spam":
            keyboard = [
                [InlineKeyboardButton(self.bi('👥 GROUP 👥'), callback_data="target_group"),
                 InlineKeyboardButton(self.bi('💬 PRIVATE 💬'), callback_data="target_private")],
                [InlineKeyboardButton(self.bi('🔙 MAIN MENU 🔙'), callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"{self.bi('♛ CHOOSE TARGET TYPE ♛')}\n\n{self.bi('Select where to send messages 👇')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data in ["target_group", "target_private"]:
            target_type = "group" if data == "target_group" else "private"
            user_states[user_id] = {"step": "waiting_for_username", "target_type": target_type}
            
            msg = f"""
{self.bi('📎 SEND GROUP LINK OR USERNAME')}

{self.bi('Examples:')}
{self.bi('• https://t.me/username')}
{self.bi('• @username')}
{self.bi('• username')}

{self.bi('⭐ Send now to continue ⭐')}
"""
            await query.edit_message_text(msg, parse_mode=ParseMode.MARKDOWN)
        
        elif data == "my_stats":
            await query.edit_message_text(
                f"""
{self.bi('🔥 OWNER STATISTICS 🔥')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('♛ Status: Active & Online')}
{self.bi('👑 Plan: Exclusive Owner')}
{self.bi('🔐 Access: Private Mode')}
{self.bi('🔥 Limits: Unlimited')}
{self.bi('⚡ Speed: Ultra Max')}
{self.bi('⏰ Uptime: 24/7')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('♛ NO ONE ELSE CAN USE THIS BOT!')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "help_menu":
            await query.edit_message_text(
                f"""
{self.bi('📚 HOW TO USE 📚')}
{self.bi('━━━━━━━━━━')}
{self.bi('1️⃣ Click Start Spamming')}
{self.bi('2️⃣ Choose Group or Private')}
{self.bi('3️⃣ Send Username/Link')}
{self.bi('4️⃣ Select Content Type')}
{self.bi('5️⃣ Set Count & Speed')}
{self.bi('6️⃣ Watch Magic! ✨')}
{self.bi('👑 Owner Exclusive Access')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "owner_panel":
            await query.edit_message_text(
                f"""
{self.bi('🔐 OWNER PANEL 🔐')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('♛ Owner ID: ' + str(self.owner_id))}
{self.bi('👑 Username: @' + self.owner_username)}
{self.bi('🔐 Access: Exclusive')}
{self.bi('🔥 Protection: Maximum')}
{self.bi('⚡ Speed: Unlimited')}
{self.bi('Bot is 100% Secure!')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "main_menu":
            if user_id in user_states:
                del user_states[user_id]
            await self.start(update, context)
        
        elif data.startswith("type_"):
            msg_type = data.replace("type_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            
            msgs = {
                "text": self.bi('💬 SEND YOUR TEXT MESSAGE 💬'),
                "photo": self.bi('🖼 SEND YOUR PHOTO 🖼'),
                "video": self.bi('🎥 SEND YOUR VIDEO 🎥'),
                "document": self.bi('📄 SEND YOUR DOCUMENT 📄'),
                "audio": self.bi('🎵 SEND YOUR AUDIO 🎵'),
                "sticker": self.bi('🏷 SEND YOUR STICKER 🏷')
            }
            await query.edit_message_text(msgs.get(msg_type, self.bi('SEND YOUR CONTENT')), parse_mode=ParseMode.MARKDOWN)
        
        elif data.startswith("speed_"):
            speed_map = {"speed_ultra": 0.1, "speed_fast": 0.5, "speed_normal": 1.0, "speed_slow": 3.0}
            user_states[user_id]["delay"] = speed_map.get(data, 1.0)
            await self.execute_spam(query, user_id, context)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id not in user_states:
            return
        
        state = user_states[user_id]
        step = state.get("step")
        
        if step == "waiting_for_username":
            text = update.message.text
            username = self.extract_username(text)
            
            if username:
                user_states[user_id]["username"] = username
                user_states[user_id]["step"] = "waiting_for_type"
                
                keyboard = [
                    [InlineKeyboardButton(self.bi('💬 TEXT 💬'), callback_data="type_text"),
                     InlineKeyboardButton(self.bi('🖼 PHOTO 🖼'), callback_data="type_photo")],
                    [InlineKeyboardButton(self.bi('🎥 VIDEO 🎥'), callback_data="type_video"),
                     InlineKeyboardButton(self.bi('📄 DOCUMENT 📄'), callback_data="type_document")],
                    [InlineKeyboardButton(self.bi('🎵 AUDIO 🎵'), callback_data="type_audio"),
                     InlineKeyboardButton(self.bi('🏷 STICKER 🏷'), callback_data="type_sticker")],
                    [InlineKeyboardButton(self.bi('🔙 CANCEL 🔙'), callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('✅ TARGET SET SUCCESSFULLY ✅')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('⭐ Target: @' + username)}
{self.bi('👥 Type: ' + state.get('target_type', 'N/A'))}

{self.bi('NOW SELECT CONTENT TYPE 👇')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    f"""
{self.bi('❌ INVALID USERNAME! ❌')}

{self.bi('Please send a valid format:')}
{self.bi('• https://t.me/username')}
{self.bi('• @username')}
{self.bi('• username')}
""",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        elif step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            
            await update.message.reply_text(
                f"""
{self.bi('🔢 HOW MANY TIMES? 🔢')}

{self.bi('Send a number (1-1000)')}
{self.bi('⭐ Recommended: 10-50 for testing')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif step == "waiting_for_count":
            try:
                count = int(update.message.text)
                count = max(1, min(count, 1000))
                
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "waiting_for_speed"
                
                keyboard = [
                    [InlineKeyboardButton(self.bi('⚡ ULTRA ⚡ (0.1s)'), callback_data="speed_ultra"),
                     InlineKeyboardButton(self.bi('🚀 FAST 🚀 (0.5s)'), callback_data="speed_fast")],
                    [InlineKeyboardButton(self.bi('🐢 NORMAL 🐢 (1s)'), callback_data="speed_normal"),
                     InlineKeyboardButton(self.bi('🦥 SLOW 🦥 (3s)'), callback_data="speed_slow")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('⚙️ CHOOSE SPEED ⚙️')}
{self.bi('━━━━━━━━━━')}
{self.bi('🔢 Count: ' + str(count))}

{self.bi('Select speed now 👇')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                await update.message.reply_text(
                    f"""
{self.bi('❌ INVALID NUMBER! ❌')}

{self.bi('Please send a valid number (1-1000)')}
""",
                    parse_mode=ParseMode.MARKDOWN
                )
    
    async def execute_spam(self, query, user_id, context):
        data = user_states.get(user_id, {})
        username = data.get("username", "")
        count = data.get("count", 1)
        delay = data.get("delay", 1.0)
        msg_type = data.get("msg_type", "text")
        content = data.get("content")
        
        await query.edit_message_text(
            f"""
{self.bi('⚡ SPAM ATTACK STARTED ⚡')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('👑 Target: @' + username)}
{self.bi('📝 Type: ' + msg_type)}
{self.bi('🔢 Count: ' + str(count))}
{self.bi('⚡ Speed: ' + str(delay) + 's')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('🔥 EXECUTING... 🔥')}
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        chat_id = f"@{username}"
        
        for i in range(count):
            try:
                if msg_type == "text":
                    msg_text = content.text if content and content.text else self.bi("🔥 Premium Spam Bot Message 🔥")
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=msg_text,
                        parse_mode=ParseMode.MARKDOWN
                    )
                
                elif msg_type == "photo" and content and content.photo:
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=content.photo[-1].file_id,
                        caption=content.caption if content.caption else ""
                    )
                
                elif msg_type == "video" and content and content.video:
                    await context.bot.send_video(
                        chat_id=chat_id,
                        video=content.video.file_id,
                        caption=content.caption if content.caption else ""
                    )
                
                elif msg_type == "document" and content and content.document:
                    await context.bot.send_document(
                        chat_id=chat_id,
                        document=content.document.file_id,
                        caption=content.caption if content.caption else ""
                    )
                
                elif msg_type == "audio" and content and content.audio:
                    await context.bot.send_audio(
                        chat_id=chat_id,
                        audio=content.audio.file_id,
                        caption=content.caption if content.caption else ""
                    )
                
                elif msg_type == "sticker" and content and content.sticker:
                    await context.bot.send_sticker(
                        chat_id=chat_id,
                        sticker=content.sticker.file_id
                    )
                
                else:
                    failed += 1
                    continue
                
                success += 1
                
                if success % 5 == 0:
                    try:
                        await query.edit_message_text(
                            f"""
{self.bi('⚡ SPAMMING IN PROGRESS ⚡')}
{self.bi('━━━━━━━━━━')}
{self.bi('✅ Sent: ' + str(success) + '/' + str(count))}
{self.bi('👑 Target: @' + username)}
""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                error_msg = str(e).lower()
                
                if "bot was blocked" in error_msg or "can't initiate" in error_msg or "bot can't send" in error_msg:
                    await query.edit_message_text(
                        f"""
{self.bi('❌ BLOCKED OR CANNOT SEND! ❌')}
{self.bi('━━━━━━━━━━')}
{self.bi('✅ Sent before block: ' + str(success))}
{self.bi('Make sure bot can message this user/group!')}
""",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                
                if "chat not found" in error_msg or "not found" in error_msg:
                    await query.edit_message_text(
                        f"""
{self.bi('❌ USER/GROUP NOT FOUND! ❌')}
{self.bi('━━━━━━━━━━')}
{self.bi('Make sure:')}
{self.bi('• Username is correct')}
{self.bi('• Group is public')}
{self.bi('• Bot is member of group')}
""",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                
                if failed > 10:
                    break
        
        # FINAL REPORT
        try:
            await query.message.reply_text(
                f"""
{self.bi('🔥 MISSION COMPLETED! 🔥')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('✅ Success: ' + str(success))}
{self.bi('❌ Failed: ' + str(failed))}
{self.bi('👑 Target: @' + username)}
{self.bi('⚡ Speed: ' + str(delay) + 's')}
{self.bi('📝 Type: ' + msg_type)}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('♛ BOT REMAINS PRIVATE! ♛')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
        
        if user_id in user_states:
            del user_states[user_id]
    
    def extract_username(self, text):
        if not text:
            return ""
        text = text.strip()
        
        # t.me/username
        match = re.search(r'(?:https?://)?t\.me/([a-zA-Z0-9_]+)', text)
        if match:
            return match.group(1)
        
        # @username
        match = re.search(r'@([a-zA-Z0-9_]+)', text)
        if match:
            return match.group(1)
        
        # direct username
        if re.match(r'^[a-zA-Z0-9_]{4,}$', text):
            return text
        
        return ""

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ BOT_TOKEN not set!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    bot = PremiumSpamBot()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message_handler))
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.Document.ALL | filters.Sticker.ALL,
        bot.message_handler
    ))
    
    print(f"""
╔══════════════════════════════════════╗
║   🔥 EXCLUSIVE PREMIUM BOT 🔥       ║
║   🔐 PRIVATE MODE ACTIVE 🔐         ║
║   👑 Owner: @{OWNER_USERNAME}      ║
║   ⚡ Status: Online                 ║
╚══════════════════════════════════════╝
    """)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
