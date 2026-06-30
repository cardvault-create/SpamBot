import os
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import re

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - SIRF BOT TOKEN CHAHIYE
BOT_TOKEN = os.getenv("BOT_TOKEN", "8887965375:AAEwf6UR5F0oFSTqS5KTCmNxIVDyysyx4s8")
OWNER_ID = int(os.getenv("OWNER_ID", "7614459746"))  # Apna Telegram User ID

# User states storage
user_states = {}

# Premium Symbols
PREMIUM_BADGE = "👑"
LOCK_ICON = "🔐"
VERIFIED_ICON = "✅"
PREMIUM_STAR = "⭐"
LIGHTNING = "⚡"
FIRE = "🔥"
CROWN = "♛"

class OwnerOnlyBot:
    def __init__(self):
        self.owner_id = OWNER_ID
    
    def is_owner(self, user_id: int) -> bool:
        """Check if user is owner"""
        return user_id == self.owner_id
    
    def format_bold_italic(self, text: str) -> str:
        """BOLD + ITALIC formatting"""
        return f"__**{text}**__"
    
    def format_bold(self, text: str) -> str:
        """BOLD only"""
        return f"**{text}**"
    
    def format_italic(self, text: str) -> str:
        """ITALIC only"""
        return f"__{text}__"
    
    def owner_only_block(self) -> str:
        """Block message for non-owners"""
        return f"""
{FIRE} {self.format_bold_italic('EXCLUSIVE PREMIUM BOT')} {FIRE}

{LOCK_ICON} {self.format_bold_italic('ACCESS DENIED')} {LOCK_ICON}

{CROWN} This bot is {self.format_bold_italic('strictly private')}
{self.format_bold_italic('and operates for owner only!')}

{PREMIUM_STAR} {self.format_italic('Owner')}: {self.format_bold_italic('@ExclusiveOwner')}

{self.format_bold_italic('❌ Unauthorized access blocked!')}
{self.format_italic('Your attempt has been recorded.')}
"""
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(
                self.owner_only_block(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        keyboard = [
            [InlineKeyboardButton(f"{FIRE} Start Spamming {FIRE}", callback_data="start_spam")],
            [
                InlineKeyboardButton(f"{PREMIUM_STAR} My Stats", callback_data="my_stats"),
                InlineKeyboardButton("ℹ️ Help", callback_data="help_menu")
            ],
            [
                InlineKeyboardButton("👥 Group Spam", callback_data="target_group"),
                InlineKeyboardButton("💬 Private Spam", callback_data="target_private")
            ],
            [InlineKeyboardButton(f"{LOCK_ICON} Owner Panel {LOCK_ICON}", callback_data="owner_panel")],
            [InlineKeyboardButton(f"{CROWN} Owner Channel", url="https://t.me/your_channel")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = f"""
{FIRE}{FIRE} {self.format_bold_italic('EXCLUSIVE SPAM BOT')} {FIRE}{FIRE}

{CROWN} {self.format_bold_italic('Welcome Back, Master!')}

{PREMIUM_STAR} {self.format_bold_italic('PREMIUM FEATURES:')}
{self.format_italic('• Ultra Fast Spamming')}
{self.format_italic('• Multi-Media Support')}
{self.format_italic('• Anti-Ban Protection')}
{self.format_italic('• Group & Private Mode')}
{self.format_italic('• Custom Speed Control')}
{self.format_italic('• Unlimited Messages')}

{LOCK_ICON} {self.format_bold_italic('STATUS')}: {self.format_italic('Private Mode')}
{PREMIUM_BADGE} {self.format_bold_italic('ACCESS')}: {self.format_italic('Owner Only')}
{FIRE} {self.format_bold_italic('PLAN')}: {self.format_italic('Exclusive Premium')}

{self.format_bold_italic('Choose an option:')}
        """
        
        await update.message.reply_text(
            welcome_msg,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all button clicks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Non-owner block
        if not self.is_owner(user_id):
            await query.edit_message_text(
                self.owner_only_block(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        data = query.data
        
        if data == "start_spam":
            keyboard = [
                [
                    InlineKeyboardButton("👥 Group", callback_data="target_group"),
                    InlineKeyboardButton("💬 Private", callback_data="target_private")
                ],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"""
{CROWN} {self.format_bold_italic('CHOOSE TARGET')}

{self.format_italic('Select target type:')}
                """,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "target_group":
            user_states[user_id] = {"step": "group_link", "target_type": "group"}
            
            await query.edit_message_text(
                f"""
{self.format_bold_italic('📎 SEND GROUP LINK')}

{self.format_italic('Formats accepted:')}
• {self.format_bold_italic('https://t.me/username')}
• {self.format_bold_italic('@username')}
• {self.format_bold_italic('username')}

{PREMIUM_STAR} {self.format_italic('Only public groups')}
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "target_private":
            user_states[user_id] = {"step": "private_user", "target_type": "private"}
            
            await query.edit_message_text(
                f"""
{self.format_bold_italic('📱 SEND USERNAME')}

{self.format_italic('Formats:')}
• {self.format_bold_italic('@username')}
• {self.format_bold_italic('username')}

{PREMIUM_STAR} {self.format_italic('User must be accessible')}
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "my_stats":
            await query.edit_message_text(
                f"""
{FIRE} {self.format_bold_italic('OWNER STATISTICS')} {FIRE}
{self.format_bold_italic('━━━━━━━━━━━━━━')}

{CROWN} {self.format_bold_italic('Status')}: {self.format_italic('Active & Online')}
{PREMIUM_BADGE} {self.format_bold_italic('Plan')}: {self.format_italic('Exclusive Owner')}
{LOCK_ICON} {self.format_bold_italic('Access')}: {self.format_italic('Private Mode')}
{FIRE} {self.format_bold_italic('Limits')}: {self.format_italic('Unlimited')}
{LIGHTNING} {self.format_bold_italic('Speed')}: {self.format_italic('Ultra Max')}

{self.format_bold_italic('━━━━━━━━━━━━━━')}
{CROWN} {self.format_bold_italic('NO ONE ELSE CAN USE!')}
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "help_menu":
            await query.edit_message_text(
                f"""
{self.format_bold_italic('📚 HOW TO USE')}
{self.format_bold_italic('━━━━━━━━━━')}

1️⃣ {self.format_italic('Start Spamming')}
2️⃣ {self.format_italic('Choose Target')}
3️⃣ {self.format_italic('Send Link/Username')}
4️⃣ {self.format_italic('Select Content Type')}
5️⃣ {self.format_italic('Set Count & Speed')}
6️⃣ {self.format_italic('Execute!')} {FIRE}

{PREMIUM_BADGE} {self.format_italic('Owner Exclusive Access')}
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "owner_panel":
            await query.edit_message_text(
                f"""
{LOCK_ICON} {self.format_bold_italic('OWNER PANEL')} {LOCK_ICON}
{self.format_bold_italic('━━━━━━━━━━━━━━')}

{CROWN} {self.format_bold_italic('Owner ID')}: {self.format_italic(str(self.owner_id))}
{PREMIUM_BADGE} {self.format_bold_italic('Access')}: {self.format_italic('Exclusive')}
{FIRE} {self.format_bold_italic('Protection')}: {self.format_italic('Maximum')}
{LOCK_ICON} {self.format_bold_italic('Mode')}: {self.format_italic('Private Only')}

{self.format_bold_italic('Bot is 100% secure!')}
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "main_menu":
            await self.start(update, context)
        
        elif data.startswith("type_"):
            msg_type = data.replace("type_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "content"
            
            type_messages = {
                "text": f"💬 {self.format_italic('Send your text message:')}",
                "photo": f"🖼 {self.format_italic('Send your photo:')}",
                "video": f"🎥 {self.format_italic('Send your video:')}",
                "document": f"📄 {self.format_italic('Send your document:')}",
                "audio": f"🎵 {self.format_italic('Send your audio:')}",
                "sticker": f"🏷 {self.format_italic('Send your sticker:')}"
            }
            
            await query.edit_message_text(
                type_messages.get(msg_type, "Send content:"),
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
            
            await self.start_spam_process(query, user_id)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all incoming messages"""
        user_id = update.effective_user.id
        
        # Non-owner block
        if not self.is_owner(user_id):
            await update.message.reply_text(
                self.owner_only_block(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if user_id not in user_states:
            return
        
        state = user_states[user_id]
        step = state.get("step")
        
        if step in ["group_link", "private_user"]:
            username = self.extract_username(update.message.text)
            
            if username:
                user_states[user_id]["username"] = username
                user_states[user_id]["step"] = "choose_type"
                
                keyboard = [
                    [
                        InlineKeyboardButton("💬 Text", callback_data="type_text"),
                        InlineKeyboardButton("🖼 Photo", callback_data="type_photo")
                    ],
                    [
                        InlineKeyboardButton("🎥 Video", callback_data="type_video"),
                        InlineKeyboardButton("📄 Document", callback_data="type_document")
                    ],
                    [
                        InlineKeyboardButton("🎵 Audio", callback_data="type_audio"),
                        InlineKeyboardButton("🏷 Sticker", callback_data="type_sticker")
                    ],
                    [InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"""
{VERIFIED_ICON} {self.format_bold_italic('TARGET SET')}
{self.format_bold_italic('━━━━━━━━━━')}
{PREMIUM_STAR} {self.format_italic('Target')}: {self.format_bold_italic(f'@{username}')}

{self.format_italic('Now choose content type:')}
                    """,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    f"❌ {self.format_bold_italic('Invalid!')} Please send valid username/link.",
                    parse_mode=ParseMode.MARKDOWN
                )
        
        elif step == "content":
            # Store the message content
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "count"
            
            await update.message.reply_text(
                f"""
{self.format_bold_italic('🔢 HOW MANY TIMES?')}
{self.format_italic('Send a number (1-1000)')}

{PREMIUM_BADGE} {self.format_italic('Unlimited for Owner')}
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif step == "count":
            try:
                count = int(update.message.text)
                if count > 1000:
                    count = 1000
                elif count < 1:
                    count = 1
                
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "choose_speed"
                
                keyboard = [
                    [
                        InlineKeyboardButton(f"{LIGHTNING} Ultra (0.1s)", callback_data="speed_ultra"),
                        InlineKeyboardButton("🚀 Fast (0.5s)", callback_data="speed_fast")
                    ],
                    [
                        InlineKeyboardButton("🐢 Normal (1s)", callback_data="speed_normal"),
                        InlineKeyboardButton("🦥 Slow (3s)", callback_data="speed_slow")
                    ]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"""
{self.format_bold_italic('⚙️ CHOOSE SPEED')}
{self.format_italic(f'Messages to send')}: {self.format_bold_italic(str(count))}

{self.format_italic('Select speed:')}
                    """,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                await update.message.reply_text(
                    f"❌ {self.format_bold_italic('Invalid!')} Send a valid number.",
                    parse_mode=ParseMode.MARKDOWN
                )
    
    async def start_spam_process(self, query, user_id):
        """Execute the spam process"""
        data = user_states.get(user_id, {})
        username = data.get("username", "")
        count = data.get("count", 1)
        delay = data.get("delay", 1.0)
        msg_type = data.get("msg_type", "text")
        content = data.get("content")
        
        await query.edit_message_text(
            f"""
{FIRE} {self.format_bold_italic('ATTACK LAUNCHED')} {FIRE}
{self.format_bold_italic('━━━━━━━━━━━━━━')}

{PREMIUM_BADGE} {self.format_italic('Target')}: {self.format_bold_italic(f'@{username}')}
📝 {self.format_italic('Type')}: {self.format_bold_italic(msg_type)}
🔢 {self.format_italic('Count')}: {self.format_bold_italic(str(count))}
{LIGHTNING} {self.format_italic('Speed')}: {self.format_bold_italic(f'{delay}s')}

{self.format_bold_italic('━━━━━━━━━━━━━━')}
{self.format_italic('Spamming in progress...')}
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        
        for i in range(count):
            try:
                if msg_type == "text":
                    await context.bot.send_message(
                        chat_id=f"@{username}",
                        text=content.text
                    )
                elif msg_type == "photo" and content.photo:
                    await context.bot.send_photo(
                        chat_id=f"@{username}",
                        photo=content.photo[-1].file_id,
                        caption=content.caption
                    )
                elif msg_type == "video" and content.video:
                    await context.bot.send_video(
                        chat_id=f"@{username}",
                        video=content.video.file_id,
                        caption=content.caption
                    )
                elif msg_type == "document" and content.document:
                    await context.bot.send_document(
                        chat_id=f"@{username}",
                        document=content.document.file_id,
                        caption=content.caption
                    )
                elif msg_type == "audio" and content.audio:
                    await context.bot.send_audio(
                        chat_id=f"@{username}",
                        audio=content.audio.file_id,
                        caption=content.caption
                    )
                elif msg_type == "sticker" and content.sticker:
                    await context.bot.send_sticker(
                        chat_id=f"@{username}",
                        sticker=content.sticker.file_id
                    )
                
                success += 1
                
                if success % 10 == 0:
                    await query.edit_message_text(
                        f"""
{LIGHTNING} {self.format_bold_italic('SPAMMING...')}
{self.format_bold_italic('━━━━━━━━━━')}
✅ {self.format_italic('Sent')}: {self.format_bold_italic(f'{success}/{count}')}
                        """,
                        parse_mode=ParseMode.MARKDOWN
                    )
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                logger.error(f"Error: {e}")
                
                if "bot was blocked" in str(e).lower():
                    await query.message.reply_text(
                        f"❌ {self.format_bold_italic('Blocked by user/group!')}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
                
                if failed > 10:
                    await query.message.reply_text(
                        f"⚠️ {self.format_bold_italic('Too many failures. Stopping.')}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    break
        
        # Final report
        await query.message.reply_text(
            f"""
{FIRE} {self.format_bold_italic('MISSION COMPLETE')} {FIRE}
{self.format_bold_italic('━━━━━━━━━━━━━━')}

✅ {self.format_italic('Success')}: {self.format_bold_italic(str(success))}
❌ {self.format_italic('Failed')}: {self.format_bold_italic(str(failed))}
👤 {self.format_italic('Target')}: {self.format_bold_italic(f'@{username}')}
{LIGHTNING} {self.format_italic('Speed')}: {self.format_bold_italic(f'{delay}s')}

{self.format_bold_italic('━━━━━━━━━━━━━━')}
{CROWN} {self.format_italic('Bot remains private!')}
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Clear state
        if user_id in user_states:
            del user_states[user_id]
    
    def extract_username(self, text: str) -> str:
        """Extract username from various formats"""
        # t.me/username
        match = re.search(r'(?:https?://)?t\.me/([a-zA-Z0-9_]+)', text)
        if match:
            return match.group(1)
        
        # @username
        match = re.search(r'@([a-zA-Z0-9_]+)', text)
        if match:
            return match.group(1)
        
        # Direct username
        if re.match(r'^[a-zA-Z0-9_]{5,}$', text):
            return text
        
        return ""

# Initialize bot
owner_bot = OwnerOnlyBot()

def main():
    """Start the bot"""
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", owner_bot.start))
    app.add_handler(CommandHandler("owner", owner_bot.start))
    app.add_handler(CallbackQueryHandler(owner_bot.button_handler))
    app.add_handler(MessageHandler(filters.ALL, owner_bot.message_handler))
    
    # Start bot
    print(f"""
{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}
{CROWN} EXCLUSIVE OWNER BOT {CROWN}
{LOCK_ICON} PRIVATE MODE ACTIVE {LOCK_ICON}
{PREMIUM_BADGE} Owner Access Only {PREMIUM_BADGE}
{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}{FIRE}
    """)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
