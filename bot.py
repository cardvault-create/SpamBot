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
{self.bi('Owner: @' + self.owner_username)}
"""
    
    async def get_chat_info(self, context, chat_id):
        try:
            chat = await context.bot.get_chat(chat_id)
            return chat.title if chat.title else str(chat_id)
        except:
            return str(chat_id)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_owner(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id in user_states:
            del user_states[user_id]
        
        keyboard = [
            [InlineKeyboardButton("START SPAMMING", callback_data="start_spam")],
            [InlineKeyboardButton("GET GROUP ID", callback_data="get_id_info"),
             InlineKeyboardButton("HELP", callback_data="help_menu")],
            [InlineKeyboardButton("STATS", callback_data="my_stats"),
             InlineKeyboardButton("OWNER PANEL", callback_data="owner_panel")],
            [InlineKeyboardButton("OWNER CHANNEL", url=f"https://t.me/{self.owner_username}")]
        ]
        
        msg = f"""
{self.bi('EXCLUSIVE PREMIUM SPAM BOT')}
{self.bi('WELCOME BACK MASTER')}

{self.bi('PREMIUM FEATURES')}
{self.bi('All Media Types Working')}
{self.bi('Group Name Detection')}
{self.bi('Built-in ID System')}
{self.bi('No Admin Rights Needed')}
{self.bi('Custom Speed Control')}

{self.bi('SELECT AN OPTION')}
"""
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def id_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /id command in groups"""
        chat_id = update.effective_chat.id
        chat_title = update.effective_chat.title if update.effective_chat.title else "Private Chat"
        user_id = update.effective_user.id
        
        if update.effective_chat.type in ["group", "supergroup"]:
            msg = f"""
{self.bi('GROUP INFORMATION')}
{self.bi('--------------------')}
{self.bi('Name: ' + chat_title)}
{self.bi('ID: ' + str(chat_id))}
{self.bi('--------------------')}
{self.bi('Copy this ID for spam')}
"""
            if update.message.reply_to_message:
                replied_user = update.message.reply_to_message.from_user
                msg += f"""
{self.bi('REPLIED USER')}
{self.bi('Name: ' + (replied_user.first_name or ''))}
{self.bi('ID: ' + str(replied_user.id))}
"""
        else:
            msg = f"""
{self.bi('CHAT INFORMATION')}
{self.bi('--------------------')}
{self.bi('Name: ' + chat_title)}
{self.bi('ID: ' + str(chat_id))}
"""
        
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        if not self.is_owner(user_id):
            await query.edit_message_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        data = query.data
        
        if data == "main_menu":
            if user_id in user_states:
                del user_states[user_id]
            keyboard = [
                [InlineKeyboardButton("START SPAMMING", callback_data="start_spam")],
                [InlineKeyboardButton("GET GROUP ID", callback_data="get_id_info"),
                 InlineKeyboardButton("HELP", callback_data="help_menu")],
                [InlineKeyboardButton("STATS", callback_data="my_stats"),
                 InlineKeyboardButton("OWNER PANEL", callback_data="owner_panel")],
                [InlineKeyboardButton("OWNER CHANNEL", url=f"https://t.me/{self.owner_username}")]
            ]
            msg = f"""
{self.bi('EXCLUSIVE PREMIUM SPAM BOT')}
{self.bi('WELCOME BACK MASTER')}

{self.bi('SELECT AN OPTION')}
"""
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if data == "get_id_info":
            keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('HOW TO GET GROUP ID')}
{self.bi('--------------------')}

{self.bi('METHOD 1 - Using This Bot:')}
{self.bi('1. Add this bot to group as ADMIN')}
{self.bi('2. Send /id in the group')}
{self.bi('3. Bot will show Group ID')}

{self.bi('METHOD 2 - Using @getidsbot:')}
{self.bi('1. Add @getidsbot to group')}
{self.bi('2. Send /id in group')}
{self.bi('3. Copy the ID')}

{self.bi('METHOD 3 - Forward Message:')}
{self.bi('1. Forward any group message to @getidsbot')}
{self.bi('2. It will show the Group ID')}

{self.bi('The ID looks like: -1001234567890')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "start_spam":
            user_states[user_id] = {"step": "waiting_for_group"}
            keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('SEND GROUP ID OR USERNAME')}

{self.bi('Get Group ID:')}
{self.bi('Add bot to group as ADMIN')}
{self.bi('Send /id in group')}
{self.bi('Copy the ID number')}

{self.bi('Format: -1001234567890')}
{self.bi('Or send @username')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "my_stats":
            keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('OWNER STATISTICS')}
{self.bi('--------------------')}
{self.bi('Status: Active Online')}
{self.bi('Plan: Exclusive Owner')}
{self.bi('Limits: Unlimited')}
{self.bi('All Media: Working')}
{self.bi('ID System: Active')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "help_menu":
            keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('HOW TO USE')}
{self.bi('--------------------')}

{self.bi('STEP 1:')}
{self.bi('Add bot to group as ADMIN')}
{self.bi('Give ALL permissions to bot')}

{self.bi('STEP 2:')}
{self.bi('Send /id in group to get ID')}

{self.bi('STEP 3:')}
{self.bi('Click START SPAMMING')}

{self.bi('STEP 4:')}
{self.bi('Send Group ID to bot')}

{self.bi('STEP 5:')}
{self.bi('Select content type')}

{self.bi('STEP 6:')}
{self.bi('Send content and set count')}

{self.bi('IMPORTANT:')}
{self.bi('Bot must have SEND permissions')}
{self.bi('For stickers: Send Stickers ON')}
{self.bi('For photos: Send Photos ON')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "owner_panel":
            keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('OWNER PANEL')}
{self.bi('--------------------')}
{self.bi('Owner ID: ' + str(self.owner_id))}
{self.bi('Username: @' + self.owner_username)}
{self.bi('Access: Exclusive')}
{self.bi('All Features Working')}
{self.bi('ID System: Built-in')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data.startswith("type_"):
            msg_type = data.replace("type_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            
            keyboard = [[InlineKeyboardButton("BACK TO TYPE SELECTION", callback_data="show_types")]]
            
            msgs = {
                "text": f"{self.bi('SEND YOUR TEXT MESSAGE')}",
                "sticker": f"{self.bi('SEND YOUR STICKER')}",
                "photo": f"{self.bi('SEND YOUR PHOTO')}",
                "video": f"{self.bi('SEND YOUR VIDEO')}",
                "document": f"{self.bi('SEND YOUR DOCUMENT')}",
                "audio": f"{self.bi('SEND YOUR AUDIO')}",
                "voice": f"{self.bi('SEND YOUR VOICE MESSAGE')}",
                "video_note": f"{self.bi('SEND YOUR VIDEO NOTE')}"
            }
            await query.edit_message_text(
                msgs.get(msg_type, self.bi('SEND YOUR CONTENT')),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "show_types":
            chat_id = user_states[user_id].get("chat_id", "N/A")
            user_states[user_id]["step"] = "waiting_for_type"
            
            keyboard = [
                [InlineKeyboardButton("TEXT", callback_data="type_text"),
                 InlineKeyboardButton("STICKER", callback_data="type_sticker")],
                [InlineKeyboardButton("PHOTO", callback_data="type_photo"),
                 InlineKeyboardButton("VIDEO", callback_data="type_video")],
                [InlineKeyboardButton("DOCUMENT", callback_data="type_document"),
                 InlineKeyboardButton("AUDIO", callback_data="type_audio")],
                [InlineKeyboardButton("VOICE", callback_data="type_voice"),
                 InlineKeyboardButton("VIDEO NOTE", callback_data="type_video_note")],
                [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]
            ]
            
            await query.edit_message_text(
                f"""
{self.bi('SELECT CONTENT TYPE')}
{self.bi('Target: ' + str(chat_id))}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "show_count":
            user_states[user_id]["step"] = "waiting_for_count"
            keyboard = [[InlineKeyboardButton("BACK TO TYPE SELECTION", callback_data="show_types")]]
            await query.edit_message_text(
                f"""
{self.bi('HOW MANY TIMES')}
{self.bi('Send a number from 1 to 1000')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data.startswith("speed_"):
            speed_map = {
                "speed_ultra": 0.5,
                "speed_fast": 1,
                "speed_normal": 2,
                "speed_slow": 5
            }
            user_states[user_id]["delay"] = speed_map.get(data, 1)
            await self.execute_spam(query, user_id, context)
            return
        
        if data == "resend_same":
            if user_id in user_states and "chat_id" in user_states[user_id]:
                await self.execute_spam(query, user_id, context)
            else:
                keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"{self.bi('NO DATA FOUND')}\n{self.bi('Start new spam')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        if data == "new_spam":
            chat_id = user_states.get(user_id, {}).get("chat_id")
            if chat_id:
                user_states[user_id] = {"chat_id": chat_id, "step": "waiting_for_type"}
                keyboard = [
                    [InlineKeyboardButton("TEXT", callback_data="type_text"),
                     InlineKeyboardButton("STICKER", callback_data="type_sticker")],
                    [InlineKeyboardButton("PHOTO", callback_data="type_photo"),
                     InlineKeyboardButton("VIDEO", callback_data="type_video")],
                    [InlineKeyboardButton("DOCUMENT", callback_data="type_document"),
                     InlineKeyboardButton("AUDIO", callback_data="type_audio")],
                    [InlineKeyboardButton("VOICE", callback_data="type_voice"),
                     InlineKeyboardButton("VIDEO NOTE", callback_data="type_video_note")],
                    [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]
                ]
                await query.edit_message_text(
                    f"{self.bi('SELECT CONTENT TYPE')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                user_states[user_id] = {"step": "waiting_for_group"}
                keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"{self.bi('SEND GROUP ID OR USERNAME')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        if data == "change_type":
            user_states[user_id]["step"] = "waiting_for_type"
            keyboard = [
                [InlineKeyboardButton("TEXT", callback_data="type_text"),
                 InlineKeyboardButton("STICKER", callback_data="type_sticker")],
                [InlineKeyboardButton("PHOTO", callback_data="type_photo"),
                 InlineKeyboardButton("VIDEO", callback_data="type_video")],
                [InlineKeyboardButton("DOCUMENT", callback_data="type_document"),
                 InlineKeyboardButton("AUDIO", callback_data="type_audio")],
                [InlineKeyboardButton("VOICE", callback_data="type_voice"),
                 InlineKeyboardButton("VIDEO NOTE", callback_data="type_video_note")],
                [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"{self.bi('SELECT NEW CONTENT TYPE')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
    
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
            chat_id = self.parse_chat_id(text)
            
            if chat_id:
                try:
                    group_name = await self.get_chat_info(context, chat_id)
                except:
                    group_name = str(chat_id)
                
                user_states[user_id]["chat_id"] = chat_id
                user_states[user_id]["group_name"] = group_name
                user_states[user_id]["step"] = "waiting_for_type"
                
                keyboard = [
                    [InlineKeyboardButton("TEXT", callback_data="type_text"),
                     InlineKeyboardButton("STICKER", callback_data="type_sticker")],
                    [InlineKeyboardButton("PHOTO", callback_data="type_photo"),
                     InlineKeyboardButton("VIDEO", callback_data="type_video")],
                    [InlineKeyboardButton("DOCUMENT", callback_data="type_document"),
                     InlineKeyboardButton("AUDIO", callback_data="type_audio")],
                    [InlineKeyboardButton("VOICE", callback_data="type_voice"),
                     InlineKeyboardButton("VIDEO NOTE", callback_data="type_video_note")],
                    [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('GROUP FOUND SUCCESSFULLY')}
{self.bi('--------------------')}
{self.bi('Name: ' + group_name)}
{self.bi('ID: ' + str(chat_id))}
{self.bi('--------------------')}

{self.bi('NOW SELECT CONTENT TYPE')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                keyboard = [[InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]]
                await update.message.reply_text(
                    f"""
{self.bi('INVALID GROUP ID')}
{self.bi('Send /id in group to get ID')}
{self.bi('Format: -1001234567890')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        if step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            
            keyboard = [[InlineKeyboardButton("BACK TO TYPE SELECTION", callback_data="show_types")]]
            
            await update.message.reply_text(
                f"""
{self.bi('CONTENT RECEIVED')}
{self.bi('HOW MANY TIMES')}
{self.bi('Send a number from 1 to 1000')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if step == "waiting_for_count":
            try:
                count = int(update.message.text)
                count = max(1, min(count, 1000))
                
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "waiting_for_speed"
                
                keyboard = [
                    [InlineKeyboardButton("ULTRA (0.5s)", callback_data="speed_ultra"),
                     InlineKeyboardButton("FAST (1s)", callback_data="speed_fast")],
                    [InlineKeyboardButton("NORMAL (2s)", callback_data="speed_normal"),
                     InlineKeyboardButton("SLOW (5s)", callback_data="speed_slow")],
                    [InlineKeyboardButton("BACK TO COUNT INPUT", callback_data="show_count")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('CHOOSE SPEED')}
{self.bi('Count: ' + str(count))}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                keyboard = [[InlineKeyboardButton("BACK TO TYPE SELECTION", callback_data="show_types")]]
                await update.message.reply_text(
                    f"{self.bi('INVALID NUMBER')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
    
    def parse_chat_id(self, text):
        if not text:
            return None
        text = text.strip()
        
        if re.match(r'^-?\d{10,}$', text):
            return int(text)
        
        match = re.search(r'@([a-zA-Z0-9_]+)', text)
        if match:
            return f"@{match.group(1)}"
        
        match = re.search(r'(?:https?://)?t\.me/([a-zA-Z0-9_]+)', text)
        if match:
            return f"@{match.group(1)}"
        
        if re.match(r'^[a-zA-Z0-9_]{4,}$', text):
            return f"@{text}"
        
        return None
    
    async def execute_spam(self, query, user_id, context):
        data = user_states.get(user_id, {})
        chat_id = data.get("chat_id", "")
        group_name = data.get("group_name", str(chat_id))
        count = data.get("count", 1)
        delay = data.get("delay", 1.0)
        msg_type = data.get("msg_type", "text")
        content = data.get("content")
        
        await query.edit_message_text(
            f"""
{self.bi('SPAM ATTACK STARTED')}
{self.bi('--------------------')}
{self.bi('Group: ' + group_name)}
{self.bi('Type: ' + msg_type)}
{self.bi('Count: ' + str(count))}
{self.bi('Speed: ' + str(delay) + 's')}
{self.bi('SENDING NOW')}
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        error_msg = None
        
        for i in range(count):
            try:
                if msg_type == "text":
                    msg_text = content.text if content and content.text else "Premium Spam Bot"
                    await context.bot.send_message(chat_id=chat_id, text=msg_text)
                    success += 1
                
                elif msg_type == "sticker":
                    if content and content.sticker:
                        await context.bot.send_sticker(chat_id=chat_id, sticker=content.sticker.file_id)
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No sticker found. Send a valid sticker."
                        break
                
                elif msg_type == "photo":
                    if content and content.photo:
                        await context.bot.send_photo(
                            chat_id=chat_id,
                            photo=content.photo[-1].file_id,
                            caption=content.caption or ""
                        )
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No photo found"
                        break
                
                elif msg_type == "video":
                    if content and content.video:
                        await context.bot.send_video(
                            chat_id=chat_id,
                            video=content.video.file_id,
                            caption=content.caption or ""
                        )
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No video found"
                        break
                
                elif msg_type == "document":
                    if content and content.document:
                        await context.bot.send_document(
                            chat_id=chat_id,
                            document=content.document.file_id,
                            caption=content.caption or ""
                        )
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No document found"
                        break
                
                elif msg_type == "audio":
                    if content and content.audio:
                        await context.bot.send_audio(
                            chat_id=chat_id,
                            audio=content.audio.file_id,
                            caption=content.caption or ""
                        )
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No audio found"
                        break
                
                elif msg_type == "voice":
                    if content and content.voice:
                        await context.bot.send_voice(
                            chat_id=chat_id,
                            voice=content.voice.file_id,
                            caption=content.caption or ""
                        )
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No voice message found"
                        break
                
                elif msg_type == "video_note":
                    if content and content.video_note:
                        await context.bot.send_video_note(
                            chat_id=chat_id,
                            video_note=content.video_note.file_id
                        )
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No video note found"
                        break
                
                else:
                    failed += 1
                    error_msg = "Unknown content type"
                    break
                
                if success > 0 and success % 5 == 0:
                    try:
                        await query.edit_message_text(
                            f"""
{self.bi('SPAMMING IN PROGRESS')}
{self.bi('Group: ' + group_name)}
{self.bi('Sent: ' + str(success) + '/' + str(count))}
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
                
                if "not enough rights" in error_str:
                    error_msg = f"Bot needs ADMIN rights with {msg_type} permission ON"
                    break
                elif "forbidden" in error_str or "blocked" in error_str:
                    error_msg = "Bot is not in group or blocked"
                    break
                elif "not found" in error_str:
                    error_msg = "Group not found. Check ID"
                    break
                elif "sticker" in error_str:
                    error_msg = "Cannot send sticker. Give bot sticker permission"
                    break
                else:
                    error_msg = str(e)[:200]
                
                if failed > 2:
                    break
        
        user_states[user_id]["last_success"] = success
        user_states[user_id]["last_failed"] = failed
        
        result = f"""
{self.bi('MISSION COMPLETED')}
{self.bi('--------------------')}
{self.bi('Group: ' + group_name)}
{self.bi('Success: ' + str(success))}
{self.bi('Failed: ' + str(failed))}
{self.bi('Type: ' + msg_type)}
{self.bi('Speed: ' + str(delay) + 's')}
"""
        
        if error_msg and success == 0:
            result += f"""
{self.bi('--------------------')}
{self.bi('ERROR: ' + error_msg)}
{self.bi('--------------------')}

{self.bi('SOLUTION:')}
{self.bi('1. Make bot ADMIN in group')}
{self.bi('2. Enable ALL permissions')}
{self.bi('3. Try again')}
"""
        
        result += f"""
{self.bi('--------------------')}

{self.bi('WHAT DO YOU WANT TO DO')}
"""
        
        keyboard = [
            [InlineKeyboardButton("RESEND SAME", callback_data="resend_same"),
             InlineKeyboardButton("NEW SPAM", callback_data="new_spam")],
            [InlineKeyboardButton("CHANGE TYPE", callback_data="change_type"),
             InlineKeyboardButton("CHANGE COUNT", callback_data="show_count")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="main_menu")]
        ]
        
        try:
            await query.message.reply_text(
                result,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error sending result: {e}")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("BOT_TOKEN not set")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    bot = PremiumGroupSpamBot()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("id", bot.id_command))
    app.add_handler(CallbackQueryHandler(bot.handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.message_handler))
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE |
        filters.Document.ALL | filters.Sticker.ALL | filters.VIDEO_NOTE,
        bot.message_handler
    ))
    
    print(f"PREMIUM GROUP SPAM BOT STARTED")
    print(f"Owner: @{OWNER_USERNAME}")
    print("Features: /id command, ALL media types")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
