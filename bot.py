import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8887965375:AAEwf6UR5F0oFSTqS5KTCmNxIVDyysyx4s8")
OWNER_ID = int(os.getenv("OWNER_ID", "7614459746"))
OWNER_USERNAME = "BeStChEaT_OwNeR"

user_states = {}

class PremiumGroupSpamBot:
    def __init__(self):
        self.owner_id = OWNER_ID
        self.owner_username = OWNER_USERNAME
    
    def is_owner(self, user_id):
        return user_id == self.owner_id
    
    def bi(self, text):
        return f"***{text}***"
    
    def block_msg(self):
        return f"""
{self.bi('EXCLUSIVE PREMIUM BOT')}

{self.bi('ACCESS DENIED')}

{self.bi('This bot is strictly private')}
{self.bi('and operates for owner only')}

{self.bi('Owner: @' + self.owner_username)}

{self.bi('Unauthorized access blocked')}
"""
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        keyboard = [
            [InlineKeyboardButton("START SPAMMING", callback_data="start_spam")],
            [InlineKeyboardButton("STATS", callback_data="my_stats"),
             InlineKeyboardButton("HELP", callback_data="help_menu")],
            [InlineKeyboardButton("OWNER PANEL", callback_data="owner_panel")],
            [InlineKeyboardButton("OWNER CHANNEL", url=f"https://t.me/{self.owner_username}")]
        ]
        
        welcome = f"""
{self.bi('EXCLUSIVE PREMIUM SPAM BOT')}

{self.bi('WELCOME BACK MASTER')}

{self.bi('PREMIUM FEATURES')}
{self.bi('Ultra Fast Group Spamming')}
{self.bi('Private Group Link Support')}
{self.bi('Multi-Media Support')}
{self.bi('Anti-Ban Protection')}
{self.bi('Custom Speed Control')}
{self.bi('Unlimited Messages')}
{self.bi('24/7 Running')}

{self.bi('STATUS: Private Mode')}
{self.bi('ACCESS: Owner Only')}
{self.bi('PLAN: Exclusive Premium')}

{self.bi('SELECT AN OPTION BELOW')}
"""
        await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        if not self.is_owner(user_id):
            await query.edit_message_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        data = query.data
        
        if data == "start_spam":
            user_states[user_id] = {"step": "waiting_for_group"}
            keyboard = [[InlineKeyboardButton("BACK", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('SEND GROUP LINK OR USERNAME')}

{self.bi('Examples:')}
{self.bi('@groupusername')}
{self.bi('https://t.me/groupusername')}
{self.bi('https://t.me/+invite_hash')}
{self.bi('groupusername')}

{self.bi('IMPORTANT:')}
{self.bi('Bot must be added to group as ADMIN')}
{self.bi('Group must be PUBLIC or bot in group')}

{self.bi('Send group link or username now')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "my_stats":
            keyboard = [[InlineKeyboardButton("BACK", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('OWNER STATISTICS')}
{self.bi('--------------------')}
{self.bi('Status: Active and Online')}
{self.bi('Plan: Exclusive Owner')}
{self.bi('Access: Private Mode')}
{self.bi('Limits: Unlimited')}
{self.bi('Speed: Ultra Max')}
{self.bi('Uptime: 24/7')}
{self.bi('--------------------')}
{self.bi('NO ONE ELSE CAN USE THIS BOT')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "help_menu":
            keyboard = [[InlineKeyboardButton("BACK", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('HOW TO USE')}
{self.bi('--------------------')}

{self.bi('STEP 1:')}
{self.bi('Add bot to your group as ADMIN')}

{self.bi('STEP 2:')}
{self.bi('Make sure bot has all permissions')}

{self.bi('STEP 3:')}
{self.bi('Click START SPAMMING')}

{self.bi('STEP 4:')}
{self.bi('Send group link or @username')}

{self.bi('STEP 5:')}
{self.bi('Select message type')}

{self.bi('STEP 6:')}
{self.bi('Send content and set count')}

{self.bi('STEP 7:')}
{self.bi('Choose speed')}

{self.bi('STEP 8:')}
{self.bi('Bot will spam in group')}

{self.bi('Owner Exclusive Access')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "owner_panel":
            keyboard = [[InlineKeyboardButton("BACK", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('OWNER PANEL')}
{self.bi('--------------------')}
{self.bi('Owner ID: ' + str(self.owner_id))}
{self.bi('Username: @' + self.owner_username)}
{self.bi('Access: Exclusive')}
{self.bi('Protection: Maximum')}
{self.bi('Speed: Unlimited')}
{self.bi('Bot is 100 Percent Secure')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
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
            
            keyboard = [[InlineKeyboardButton("BACK", callback_data="back_to_type")]]
            
            msgs = {
                "text": f"{self.bi('SEND YOUR TEXT MESSAGE')}",
                "photo": f"{self.bi('SEND YOUR PHOTO')}",
                "video": f"{self.bi('SEND YOUR VIDEO')}",
                "document": f"{self.bi('SEND YOUR DOCUMENT')}",
                "audio": f"{self.bi('SEND YOUR AUDIO')}",
                "sticker": f"{self.bi('SEND YOUR STICKER')}",
                "voice": f"{self.bi('SEND YOUR VOICE MESSAGE')}",
                "video_note": f"{self.bi('SEND YOUR VIDEO NOTE')}"
            }
            await query.edit_message_text(
                msgs.get(msg_type, self.bi('SEND YOUR CONTENT')),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "back_to_type":
            user_states[user_id]["step"] = "waiting_for_type"
            keyboard = [
                [InlineKeyboardButton("TEXT", callback_data="type_text"),
                 InlineKeyboardButton("PHOTO", callback_data="type_photo")],
                [InlineKeyboardButton("VIDEO", callback_data="type_video"),
                 InlineKeyboardButton("DOCUMENT", callback_data="type_document")],
                [InlineKeyboardButton("AUDIO", callback_data="type_audio"),
                 InlineKeyboardButton("STICKER", callback_data="type_sticker")],
                [InlineKeyboardButton("VOICE", callback_data="type_voice"),
                 InlineKeyboardButton("VIDEO NOTE", callback_data="type_video_note")],
                [InlineKeyboardButton("BACK", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"""
{self.bi('SELECT CONTENT TYPE')}
{self.bi('Target: @' + user_states[user_id].get('username', 'N/A'))}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data.startswith("speed_"):
            speed_map = {
                "speed_ultra": 0.3,
                "speed_fast": 0.7,
                "speed_normal": 1.5,
                "speed_slow": 4
            }
            user_states[user_id]["delay"] = speed_map.get(data, 1)
            await self.execute_spam(query, user_id, context)
        
        elif data == "back_to_speed":
            user_states[user_id]["step"] = "waiting_for_speed"
            keyboard = [
                [InlineKeyboardButton("ULTRA (0.3s)", callback_data="speed_ultra"),
                 InlineKeyboardButton("FAST (0.7s)", callback_data="speed_fast")],
                [InlineKeyboardButton("NORMAL (1.5s)", callback_data="speed_normal"),
                 InlineKeyboardButton("SLOW (4s)", callback_data="speed_slow")],
                [InlineKeyboardButton("BACK", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"""
{self.bi('CHOOSE SPEED')}
{self.bi('Count: ' + str(user_states[user_id].get('count', 0)))}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "back_to_count":
            user_states[user_id]["step"] = "waiting_for_count"
            keyboard = [[InlineKeyboardButton("BACK", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('HOW MANY TIMES')}

{self.bi('Send a number from 1 to 1000')}
{self.bi('Recommended: 10 for testing')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id not in user_states:
            return
        
        state = user_states[user_id]
        step = state.get("step")
        
        if step == "waiting_for_group":
            text = update.message.text
            
            # Try to extract group info from any format
            group_id = self.extract_group_info(text)
            
            if group_id:
                user_states[user_id]["group_id"] = group_id
                user_states[user_id]["username"] = group_id.replace("@", "").replace("https://t.me/", "").replace("https://t.me/+", "")
                user_states[user_id]["step"] = "waiting_for_type"
                
                keyboard = [
                    [InlineKeyboardButton("TEXT", callback_data="type_text"),
                     InlineKeyboardButton("PHOTO", callback_data="type_photo")],
                    [InlineKeyboardButton("VIDEO", callback_data="type_video"),
                     InlineKeyboardButton("DOCUMENT", callback_data="type_document")],
                    [InlineKeyboardButton("AUDIO", callback_data="type_audio"),
                     InlineKeyboardButton("STICKER", callback_data="type_sticker")],
                    [InlineKeyboardButton("VOICE", callback_data="type_voice"),
                     InlineKeyboardButton("VIDEO NOTE", callback_data="type_video_note")],
                    [InlineKeyboardButton("BACK", callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('GROUP SET SUCCESSFULLY')}
{self.bi('--------------------')}
{self.bi('Group: ' + group_id)}

{self.bi('NOW SELECT CONTENT TYPE')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                keyboard = [[InlineKeyboardButton("BACK", callback_data="main_menu")]]
                await update.message.reply_text(
                    f"""
{self.bi('INVALID GROUP LINK OR USERNAME')}

{self.bi('Please send a valid format:')}
{self.bi('@groupusername')}
{self.bi('https://t.me/groupusername')}
{self.bi('https://t.me/+invite_hash')}
{self.bi('groupusername')}

{self.bi('Make sure bot is ADMIN in the group')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
        
        elif step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            
            keyboard = [[InlineKeyboardButton("BACK", callback_data="back_to_type")]]
            
            await update.message.reply_text(
                f"""
{self.bi('HOW MANY TIMES')}

{self.bi('Send a number from 1 to 1000')}
{self.bi('Recommended: 10 for testing')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif step == "waiting_for_count":
            try:
                count = int(update.message.text)
                count = max(1, min(count, 1000))
                
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "waiting_for_speed"
                
                keyboard = [
                    [InlineKeyboardButton("ULTRA (0.3s)", callback_data="speed_ultra"),
                     InlineKeyboardButton("FAST (0.7s)", callback_data="speed_fast")],
                    [InlineKeyboardButton("NORMAL (1.5s)", callback_data="speed_normal"),
                     InlineKeyboardButton("SLOW (4s)", callback_data="speed_slow")],
                    [InlineKeyboardButton("BACK", callback_data="back_to_count")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('CHOOSE SPEED')}
{self.bi('--------------------')}
{self.bi('Count: ' + str(count))}

{self.bi('Select speed now')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                keyboard = [[InlineKeyboardButton("BACK", callback_data="back_to_type")]]
                await update.message.reply_text(
                    f"""
{self.bi('INVALID NUMBER')}

{self.bi('Please send a valid number from 1 to 1000')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
    
    async def execute_spam(self, query, user_id, context):
        data = user_states.get(user_id, {})
        group_id = data.get("group_id", "")
        count = data.get("count", 1)
        delay = data.get("delay", 1.0)
        msg_type = data.get("msg_type", "text")
        content = data.get("content")
        
        # Try multiple formats for private groups
        chat_id = group_id
        
        await query.edit_message_text(
            f"""
{self.bi('SPAM ATTACK STARTED')}
{self.bi('--------------------')}
{self.bi('Target: ' + group_id)}
{self.bi('Type: ' + msg_type)}
{self.bi('Count: ' + str(count))}
{self.bi('Speed: ' + str(delay) + 's')}
{self.bi('--------------------')}
{self.bi('SENDING MESSAGES NOW')}
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        
        for i in range(count):
            try:
                if msg_type == "text":
                    msg_text = content.text if content and content.text else "Premium Spam Bot Message"
                    await context.bot.send_message(chat_id=chat_id, text=msg_text)
                
                elif msg_type == "photo":
                    if content and content.photo:
                        await context.bot.send_photo(
                            chat_id=chat_id,
                            photo=content.photo[-1].file_id,
                            caption=content.caption or ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "video":
                    if content and content.video:
                        await context.bot.send_video(
                            chat_id=chat_id,
                            video=content.video.file_id,
                            caption=content.caption or ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "document":
                    if content and content.document:
                        await context.bot.send_document(
                            chat_id=chat_id,
                            document=content.document.file_id,
                            caption=content.caption or ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "audio":
                    if content and content.audio:
                        await context.bot.send_audio(
                            chat_id=chat_id,
                            audio=content.audio.file_id,
                            caption=content.caption or ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "sticker":
                    if content and content.sticker:
                        await context.bot.send_sticker(
                            chat_id=chat_id,
                            sticker=content.sticker.file_id
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "voice":
                    if content and content.voice:
                        await context.bot.send_voice(
                            chat_id=chat_id,
                            voice=content.voice.file_id,
                            caption=content.caption or ""
                        )
                    else:
                        failed += 1
                        continue
                
                elif msg_type == "video_note":
                    if content and content.video_note:
                        await context.bot.send_video_note(
                            chat_id=chat_id,
                            video_note=content.video_note.file_id
                        )
                    else:
                        failed += 1
                        continue
                
                else:
                    failed += 1
                    continue
                
                success += 1
                logger.info(f"Message {success}/{count} sent to {group_id}")
                
                if success % 10 == 0:
                    try:
                        await query.edit_message_text(
                            f"""
{self.bi('SPAMMING IN PROGRESS')}
{self.bi('--------------------')}
{self.bi('Sent: ' + str(success) + '/' + str(count))}
{self.bi('Target: ' + group_id)}
""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                error_str = str(e).lower()
                logger.error(f"Error: {e}")
                
                if "forbidden" in error_str or "blocked" in error_str or "not enough rights" in error_str:
                    try:
                        await query.edit_message_text(
                            f"""
{self.bi('CANNOT SEND MESSAGES')}
{self.bi('--------------------')}
{self.bi('Sent: ' + str(success))}
{self.bi('Reason: Bot needs ADMIN rights')}

{self.bi('SOLUTION:')}
{self.bi('Make bot ADMIN in the group')}
{self.bi('Enable all permissions')}
""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                    break
                
                if "not found" in error_str or "chat not found" in error_str:
                    try:
                        await query.edit_message_text(
                            f"""
{self.bi('GROUP NOT FOUND')}
{self.bi('--------------------')}
{self.bi('Group: ' + group_id)}
{self.bi('Sent: ' + str(success))}

{self.bi('CHECK:')}
{self.bi('Is link or username correct')}
{self.bi('Is bot ADMIN in the group')}
{self.bi('Try using @username format')}
""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                    break
                
                if failed > 5:
                    break
        
        try:
            await query.message.reply_text(
                f"""
{self.bi('MISSION COMPLETED')}
{self.bi('--------------------')}
{self.bi('Success: ' + str(success))}
{self.bi('Failed: ' + str(failed))}
{self.bi('Target: ' + group_id)}
{self.bi('Speed: ' + str(delay) + 's')}
{self.bi('Type: ' + msg_type)}
{self.bi('--------------------')}
{self.bi('BOT REMAINS PRIVATE')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
        
        if user_id in user_states:
            del user_states[user_id]
    
    def extract_group_info(self, text):
        """Extract group info from any format"""
        if not text:
            return None
        
        text = text.strip()
        
        # Private group invite link: https://t.me/+hash
        match = re.search(r'(?:https?://)?t\.me/\+([a-zA-Z0-9_-]+)', text)
        if match:
            return f"https://t.me/+{match.group(1)}"
        
        # Public group link: https://t.me/username
        match = re.search(r'(?:https?://)?t\.me/([a-zA-Z0-9_]+)', text)
        if match:
            username = match.group(1)
            if username != '+':
                return f"@{username}"
        
        # @username format
        match = re.search(r'@([a-zA-Z0-9_]+)', text)
        if match:
            return f"@{match.group(1)}"
        
        # Direct username
        if re.match(r'^[a-zA-Z0-9_]{4,}$', text):
            return f"@{text}"
        
        return None

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("BOT_TOKEN not set")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    bot = PremiumGroupSpamBot()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message_handler))
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE |
        filters.Document.ALL | filters.Sticker.ALL | filters.VIDEO_NOTE,
        bot.message_handler
    ))
    
    print(f"PREMIUM GROUP SPAM BOT STARTED - Owner: @{OWNER_USERNAME}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
