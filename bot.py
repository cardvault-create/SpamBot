import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import re
import time

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8887965375:AAEwf6UR5F0oFSTqS5KTCmNxIVDyysyx4s8")
OWNER_ID = int(os.getenv("OWNER_ID", "7614459746"))
OWNER_USERNAME = "BeStChEaT_OwNeR"  # Aapka username

# User states storage
user_states = {}

class PremiumSpamBot:
    def __init__(self):
        self.owner_id = OWNER_ID
        self.owner_username = OWNER_USERNAME
    
    def is_owner(self, user_id: int) -> bool:
        return user_id == self.owner_id
    
    def bold_italic(self, text: str) -> str:
        """Sab kuch BOLD + ITALIC"""
        return f"***{text}***"
    
    def block_msg(self) -> str:
        """Non-owner block message"""
        return f"""
🔥 {self.bold_italic('EXCLUSIVE PREMIUM BOT')} 🔥

🔐 {self.bold_italic('ACCESS DENIED')} 🔐

♛ {self.bold_italic('This bot is strictly private')}
{self.bold_italic('and operates for owner only!')}

⭐ {self.bold_italic('Owner')}: {self.bold_italic('@' + self.owner_username)}

❌ {self.bold_italic('Unauthorized access blocked!')}
{self.bold_italic('Your attempt has been recorded.')}
"""
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(
                self.block_msg(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        keyboard = [
            [InlineKeyboardButton(f"🔥 {self.bold_italic('START SPAMMING')} 🔥", callback_data="start_spam")],
            [
                InlineKeyboardButton(f"⭐ {self.bold_italic('STATS')} ⭐", callback_data="my_stats"),
                InlineKeyboardButton(f"ℹ️ {self.bold_italic('HELP')} ℹ️", callback_data="help_menu")
            ],
            [
                InlineKeyboardButton(f"👥 {self.bold_italic('GROUP SPAM')} 👥", callback_data="target_group"),
                InlineKeyboardButton(f"💬 {self.bold_italic('PRIVATE SPAM')} 💬", callback_data="target_private")
            ],
            [InlineKeyboardButton(f"🔐 {self.bold_italic('OWNER PANEL')} 🔐", callback_data="owner_panel")],
            [InlineKeyboardButton(f"♛ {self.bold_italic('OWNER CHANNEL')} ♛", url=f"https://t.me/{self.owner_username}")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = f"""
🔥🔥 {self.bold_italic('EXCLUSIVE PREMIUM SPAM BOT')} 🔥🔥

♛ {self.bold_italic('WELCOME BACK MASTER!')} ♛

⭐ {self.bold_italic('PREMIUM FEATURES')} ⭐
{self.bold_italic('• Ultra Fast Spamming')}
{self.bold_italic('• Multi-Media Support')}
{self.bold_italic('• Anti-Ban Protection')}
{self.bold_italic('• Group & Private Mode')}
{self.bold_italic('• Custom Speed Control')}
{self.bold_italic('• Unlimited Messages')}
{self.bold_italic('• 24/7 Running')}

🔐 {self.bold_italic('STATUS')}: {self.bold_italic('Private Mode')}
👑 {self.bold_italic('ACCESS')}: {self.bold_italic('Owner Only')}
🔥 {self.bold_italic('PLAN')}: {self.bold_italic('Exclusive Premium')}

{self.bold_italic('SELECT AN OPTION BELOW')} 👇
"""
        
        await update.message.reply_text(
            welcome_msg,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_owner(user_id):
            await query.edit_message_text(
                self.block_msg(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        data = query.data
        
        if data == "start_spam":
            keyboard = [
                [
                    InlineKeyboardButton(f"👥 {self.bold_italic('GROUP')} 👥", callback_data="target_group"),
                    InlineKeyboardButton(f"💬 {self.bold_italic('PRIVATE')} 💬", callback_data="target_private")
                ],
                [InlineKeyboardButton(f"🔙 {self.bold_italic('MAIN MENU')} 🔙", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"""
♛ {self.bold_italic('CHOOSE TARGET TYPE')} ♛

{self.bold_italic('Select where to send messages')} 👇
""",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "target_group":
            user_states[user_id] = {"step": "waiting_for_username", "target_type": "group"}
            
            await query.edit_message_text(
                f"""
📎 {self.bold_italic('SEND GROUP LINK OR USERNAME')}

{self.bold_italic('Examples')}:
• {self.bold_italic('https://t.me/username')}
• {self.bold_italic('@username')}
• {self.bold_italic('username')}

⭐ {self.bold_italic('Only public groups supported')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "target_private":
            user_states[user_id] = {"step": "waiting_for_username", "target_type": "private"}
            
            await query.edit_message_text(
                f"""
📱 {self.bold_italic('SEND USERNAME')}

{self.bold_italic('Examples')}:
• {self.bold_italic('@username')}
• {self.bold_italic('username')}

⭐ {self.bold_italic('User must be accessible')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "my_stats":
            await query.edit_message_text(
                f"""
🔥 {self.bold_italic('OWNER STATISTICS')} 🔥
{self.bold_italic('━━━━━━━━━━━━━━')}

♛ {self.bold_italic('Status')}: {self.bold_italic('Active & Online')}
👑 {self.bold_italic('Plan')}: {self.bold_italic('Exclusive Owner')}
🔐 {self.bold_italic('Access')}: {self.bold_italic('Private Mode')}
🔥 {self.bold_italic('Limits')}: {self.bold_italic('Unlimited')}
⚡ {self.bold_italic('Speed')}: {self.bold_italic('Ultra Max')}
⏰ {self.bold_italic('Uptime')}: {self.bold_italic('24/7')}

{self.bold_italic('━━━━━━━━━━━━━━')}
♛ {self.bold_italic('NO ONE ELSE CAN USE THIS BOT!')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "help_menu":
            await query.edit_message_text(
                f"""
📚 {self.bold_italic('HOW TO USE')} 📚
{self.bold_italic('━━━━━━━━━━')}

1️⃣ {self.bold_italic('Click Start Spamming')}
2️⃣ {self.bold_italic('Choose Group or Private')}
3️⃣ {self.bold_italic('Send Username/Link')}
4️⃣ {self.bold_italic('Select Content Type')}
5️⃣ {self.bold_italic('Set Count & Speed')}
6️⃣ {self.bold_italic('Watch Magic!')} ✨

👑 {self.bold_italic('Owner Exclusive Access')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "owner_panel":
            await query.edit_message_text(
                f"""
🔐 {self.bold_italic('OWNER PANEL')} 🔐
{self.bold_italic('━━━━━━━━━━━━━━')}

♛ {self.bold_italic('Owner ID')}: {self.bold_italic(str(self.owner_id))}
👑 {self.bold_italic('Username')}: {self.bold_italic('@' + self.owner_username)}
🔐 {self.bold_italic('Access')}: {self.bold_italic('Exclusive')}
🔥 {self.bold_italic('Protection')}: {self.bold_italic('Maximum')}
⚡ {self.bold_italic('Speed')}: {self.bold_italic('Unlimited')}

{self.bold_italic('Bot is 100% Secure!')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "main_menu":
            # Clear state
            if user_id in user_states:
                del user_states[user_id]
            # Create fake update for start
            await self.start(update, context)
        
        elif data.startswith("type_"):
            msg_type = data.replace("type_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            
            messages = {
                "text": f"💬 {self.bold_italic('SEND YOUR TEXT MESSAGE')}",
                "photo": f"🖼 {self.bold_italic('SEND YOUR PHOTO')}",
                "video": f"🎥 {self.bold_italic('SEND YOUR VIDEO')}",
                "document": f"📄 {self.bold_italic('SEND YOUR DOCUMENT')}",
                "audio": f"🎵 {self.bold_italic('SEND YOUR AUDIO')}",
                "sticker": f"🏷 {self.bold_italic('SEND YOUR STICKER')}"
            }
            
            await query.edit_message_text(
                messages.get(msg_type, f"{self.bold_italic('SEND YOUR CONTENT')}"),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data.startswith("speed_"):
            speed_map = {
                "speed_ultra": 0.1,
                "speed_fast": 0.5,
                "speed_normal": 1.0,
                "speed_slow": 3.0
            }
            
            delay = speed_map.get(data, 1.0)
            user_states[user_id]["delay"] = delay
            
            # Start spamming
            await self.execute_spam(query, user_id, context)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(
                self.block_msg(),
                parse_mode=ParseMode.MARKDOWN
            )
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
                    [
                        InlineKeyboardButton(f"💬 {self.bold_italic('TEXT')} 💬", callback_data="type_text"),
                        InlineKeyboardButton(f"🖼 {self.bold_italic('PHOTO')} 🖼", callback_data="type_photo")
                    ],
                    [
                        InlineKeyboardButton(f"🎥 {self.bold_italic('VIDEO')} 🎥", callback_data="type_video"),
                        InlineKeyboardButton(f"📄 {self.bold_italic('DOCUMENT')} 📄", callback_data="type_document")
                    ],
                    [
                        InlineKeyboardButton(f"🎵 {self.bold_italic('AUDIO')} 🎵", callback_data="type_audio"),
                        InlineKeyboardButton(f"🏷 {self.bold_italic('STICKER')} 🏷", callback_data="type_sticker")
                    ],
                    [InlineKeyboardButton(f"🔙 {self.bold_italic('CANCEL')} 🔙", callback_data="main_menu")]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"""
✅ {self.bold_italic('TARGET SET SUCCESSFULLY')} ✅
{self.bold_italic('━━━━━━━━━━━━━━')}
⭐ {self.bold_italic('Target')}: {self.bold_italic('@' + username)}
👥 {self.bold_italic('Type')}: {self.bold_italic(state.get('target_type', 'N/A'))}

{self.bold_italic('NOW SELECT CONTENT TYPE')} 👇
""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    f"""
❌ {self.bold_italic('INVALID USERNAME!')} ❌

{self.bold_italic('Please send a valid format:')}
• {self.bold_italic('https://t.me/username')}
• {self.bold_italic('@username')}
• {self.bold_italic('username')}
""",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        elif step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            
            await update.message.reply_text(
                f"""
🔢 {self.bold_italic('HOW MANY TIMES?')} 🔢

{self.bold_italic('Send a number (1-1000)')}

⭐ {self.bold_italic('Recommended: 10-50 for testing')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif step == "waiting_for_count":
            try:
                count = int(update.message.text)
                if count > 1000:
                    count = 1000
                elif count < 1:
                    count = 1
                
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "waiting_for_speed"
                
                keyboard = [
                    [
                        InlineKeyboardButton(f"⚡ {self.bold_italic('ULTRA')} ⚡ (0.1s)", callback_data="speed_ultra"),
                        InlineKeyboardButton(f"🚀 {self.bold_italic('FAST')} 🚀 (0.5s)", callback_data="speed_fast")
                    ],
                    [
                        InlineKeyboardButton(f"🐢 {self.bold_italic('NORMAL')} 🐢 (1s)", callback_data="speed_normal"),
                        InlineKeyboardButton(f"🦥 {self.bold_italic('SLOW')} 🦥 (3s)", callback_data="speed_slow")
                    ]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"""
⚙️ {self.bold_italic('CHOOSE SPEED')} ⚙️
{self.bold_italic('━━━━━━━━━━')}
🔢 {self.bold_italic('Count')}: {self.bold_italic(str(count))}

{self.bold_italic('Select speed now')} 👇
""",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                await update.message.reply_text(
                    f"""
❌ {self.bold_italic('INVALID NUMBER!')} ❌

{self.bold_italic('Please send a valid number (1-1000)')}
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
        target_type = data.get("target_type", "group")
        
        await query.edit_message_text(
            f"""
⚡ {self.bold_italic('SPAM ATTACK STARTED')} ⚡
{self.bold_italic('━━━━━━━━━━━━━━')}

👑 {self.bold_italic('Target')}: {self.bold_italic('@' + username)}
📝 {self.bold_italic('Type')}: {self.bold_italic(msg_type)}
🔢 {self.bold_italic('Count')}: {self.bold_italic(str(count))}
⚡ {self.bold_italic('Speed')}: {self.bold_italic(f'{delay}s')}

{self.bold_italic('━━━━━━━━━━━━━━')}
🔥 {self.bold_italic('EXECUTING...')} 🔥
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        chat_id = f"@{username}"
        
        for i in range(count):
            try:
                if msg_type == "text":
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=content.text if content.text else "🔥 Premium Spam Bot 🔥"
                    )
                
                elif msg_type == "photo":
                    if content.photo:
                        await context.bot.send_photo(
                            chat_id=chat_id,
                            photo=content.photo[-1].file_id,
                            caption=content.caption if content.caption else ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "video":
                    if content.video:
                        await context.bot.send_video(
                            chat_id=chat_id,
                            video=content.video.file_id,
                            caption=content.caption if content.caption else ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "document":
                    if content.document:
                        await context.bot.send_document(
                            chat_id=chat_id,
                            document=content.document.file_id,
                            caption=content.caption if content.caption else ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "audio":
                    if content.audio:
                        await context.bot.send_audio(
                            chat_id=chat_id,
                            audio=content.audio.file_id,
                            caption=content.caption if content.caption else ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "sticker":
                    if content.sticker:
                        await context.bot.send_sticker(
                            chat_id=chat_id,
                            sticker=content.sticker.file_id
                        )
                    else:
                        failed += 1
                        continue
                
                success += 1
                
                # Progress update har 5 messages pe
                if success % 5 == 0:
                    try:
                        await query.edit_message_text(
                            f"""
⚡ {self.bold_italic('SPAMMING IN PROGRESS')} ⚡
{self.bold_italic('━━━━━━━━━━')}
✅ {self.bold_italic('Sent')}: {self.bold_italic(f'{success}/{count}')}
👑 {self.bold_italic('Target')}: {self.bold_italic('@' + username)}
""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                error_msg = str(e)
                
                if "bot was blocked" in error_msg.lower() or "bot can't initiate" in error_msg.lower():
                    await query.edit_message_text(
                        f"""
❌ {self.bold_italic('BLOCKED BY USER/GROUP!')} ❌
{self.bold_italic('━━━━━━━━━━')}
✅ {self.bold_italic('Sent before block')}: {self.bold_italic(str(success))}

{self.bold_italic('Cannot send more messages.')}
""",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                
                if "chat not found" in error_msg.lower():
                    await query.edit_message_text(
                        f"""
❌ {self.bold_italic('USER/GROUP NOT FOUND!')} ❌

{self.bold_italic('Make sure:')}
• {self.bold_italic('Username is correct')}
• {self.bold_italic('Group is public')}
• {self.bold_italic('Bot is not banned')}
""",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                
                if failed > 10:
                    await query.edit_message_text(
                        f"""
⚠️ {self.bold_italic('TOO MANY ERRORS!')} ⚠️
{self.bold_italic('━━━━━━━━━━')}
✅ {self.bold_italic('Sent')}: {self.bold_italic(str(success))}
❌ {self.bold_italic('Failed')}: {self.bold_italic(str(failed))}

{self.bold_italic('Stopping for safety.')}
""",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
        
        # Final completion report
        try:
            await query.message.reply_text(
                f"""
🔥 {self.bold_italic('MISSION COMPLETED!')} 🔥
{self.bold_italic('━━━━━━━━━━━━━━')}

✅ {self.bold_italic('Success')}: {self.bold_italic(str(success))}
❌ {self.bold_italic('Failed')}: {self.bold_italic(str(failed))}
👑 {self.bold_italic('Target')}: {self.bold_italic('@' + username)}
⚡ {self.bold_italic('Speed')}: {self.bold_italic(f'{delay}s')}
📝 {self.bold_italic('Type')}: {self.bold_italic(msg_type)}

{self.bold_italic('━━━━━━━━━━━━━━')}
♛ {self.bold_italic('BOT REMAINS PRIVATE!')} ♛
""",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
        
        # Clear state
        if user_id in user_states:
            del user_states[user_id]
    
    def extract_username(self, text: str) -> str:
        """Extract username from various formats"""
        if not text:
            return ""
        
        # t.me/username or https://t.me/username
        match = re.search(r'(?:https?://)?t\.me/([a-zA-Z0-9_]+)', text)
        if match:
            return match.group(1)
        
        # @username
        match = re.search(r'@([a-zA-Z0-9_]+)', text)
        if match:
            return match.group(1)
        
        # Direct username (at least 5 chars)
        text = text.strip()
        if re.match(r'^[a-zA-Z0-9_]{5,}$', text):
            return text
        
        return ""

def main():
    """Start the bot"""
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ Error: BOT_TOKEN not set!")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Create bot instance
    bot = PremiumSpamBot()
    
    # Add handlers
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("help", bot.start))
    app.add_handler(CallbackQueryHandler(bot.handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.AUDIO | filters.Sticker.ALL | filters.Document.ALL, bot.message_handler))
    
    # Start bot
    print(f"""
╔══════════════════════════════════════╗
║                                      ║
║   🔥 EXCLUSIVE PREMIUM BOT 🔥       ║
║   🔐 PRIVATE MODE ACTIVE 🔐         ║
║   👑 Owner: @{OWNER_USERNAME}      ║
║   ⚡ Status: Online                 ║
║                                      ║
╚══════════════════════════════════════╝
    """)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
