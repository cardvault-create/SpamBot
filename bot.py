import os
import asyncio
import logging
import json
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
saved_groups = {}
admin_list = set()

GROUPS_FILE = "saved_groups.json"
ADMIN_FILE = "admin_list.json"

class PremiumGroupSpamBot:
    def __init__(self):
        self.owner_id = OWNER_ID
        self.owner_username = OWNER_USERNAME
        self.load_data()
    
    def load_data(self):
        global saved_groups, admin_list
        try:
            with open(GROUPS_FILE, 'r') as f:
                saved_groups = json.load(f)
        except:
            saved_groups = {}
        try:
            with open(ADMIN_FILE, 'r') as f:
                admin_list = set(json.load(f))
        except:
            admin_list = set()
        admin_list.add(self.owner_id)
    
    def save_groups(self):
        with open(GROUPS_FILE, 'w') as f:
            json.dump(saved_groups, f)
    
    def save_admins(self):
        with open(ADMIN_FILE, 'w') as f:
            json.dump(list(admin_list), f)
    
    def is_authorized(self, user_id):
        return user_id == self.owner_id or user_id in admin_list
    
    def bi(self, text):
        return f"***{text}***"
    
    def block_msg(self):
        return f"""
{self.bi('🔐 EXCLUSIVE PREMIUM BOT 🔐')}
{self.bi('⛔ ACCESS DENIED ⛔')}
{self.bi('👑 Owner: @' + self.owner_username)}
"""
    
    async def get_chat_info(self, context, chat_id):
        try:
            chat = await context.bot.get_chat(chat_id)
            return chat.title if chat.title else str(chat_id)
        except:
            return str(chat_id)
    
    async def show_main_menu(self, query):
        user_id = query.from_user.id
        
        if not self.is_authorized(user_id):
            await query.edit_message_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id in user_states:
            del user_states[user_id]
        
        keyboard = [
            [InlineKeyboardButton("🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥", callback_data="start_spam")],
            [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", callback_data="saved_groups_menu"),
             InlineKeyboardButton("➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 ➕", callback_data="add_group_manual")],
            [InlineKeyboardButton("🆔 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔", callback_data="get_id_info"),
             InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣 ❓", callback_data="help_menu")],
            [InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦 📊", callback_data="my_stats"),
             InlineKeyboardButton("🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐", callback_data="owner_panel")],
            [InlineKeyboardButton("👑 𝗢𝗪𝗡𝗘𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 👑", url=f"https://t.me/{self.owner_username}")]
        ]
        
        msg = f"""
{self.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{self.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{self.bi('⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 ⭐')}
{self.bi('• 𝗔𝗹𝗹 𝗠𝗲𝗱𝗶𝗮 𝗧𝘆𝗽𝗲𝘀 𝗪𝗼𝗿𝗸𝗶𝗻𝗴')}
{self.bi('• 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝘆𝘀𝘁𝗲𝗺')}
{self.bi('• 𝗢𝗻𝗲-𝗖𝗹𝗶𝗰𝗸 𝗚𝗿𝗼𝘂𝗽 𝗦𝗲𝗹𝗲𝗰𝘁')}
{self.bi('• 𝗔𝗱𝗺𝗶𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁')}
{self.bi('• 𝗖𝘂𝘀𝘁𝗼𝗺 𝗦𝗽𝗲𝗲𝗱 𝗖𝗼𝗻𝘁𝗿𝗼𝗹')}
{self.bi('• 𝟮𝟰/𝟳 𝗥𝘂𝗻𝗻𝗶𝗻𝗴')}

{self.bi('🔒 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗠𝗼𝗱𝗲')}
{self.bi('👑 𝗔𝗖𝗖𝗘𝗦𝗦: 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗢𝗻𝗹𝘆')}
{self.bi('💎 𝗣𝗟𝗔𝗡: 𝗘𝘅𝗰𝗹𝘂𝘀𝗶𝘃𝗲 𝗣𝗿𝗲𝗺𝗶𝘂𝗺')}

{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 📌')}
"""
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id in user_states:
            del user_states[user_id]
        
        keyboard = [
            [InlineKeyboardButton("🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥", callback_data="start_spam")],
            [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", callback_data="saved_groups_menu"),
             InlineKeyboardButton("➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 ➕", callback_data="add_group_manual")],
            [InlineKeyboardButton("🆔 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔", callback_data="get_id_info"),
             InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣 ❓", callback_data="help_menu")],
            [InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦 📊", callback_data="my_stats"),
             InlineKeyboardButton("🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐", callback_data="owner_panel")],
            [InlineKeyboardButton("👑 𝗢𝗪𝗡𝗘𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 👑", url=f"https://t.me/{self.owner_username}")]
        ]
        
        msg = f"""
{self.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{self.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{self.bi('⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 ⭐')}
{self.bi('• 𝗔𝗹𝗹 𝗠𝗲𝗱𝗶𝗮 𝗧𝘆𝗽𝗲𝘀 𝗪𝗼𝗿𝗸𝗶𝗻𝗴')}
{self.bi('• 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝘆𝘀𝘁𝗲𝗺')}
{self.bi('• 𝗢𝗻𝗲-𝗖𝗹𝗶𝗰𝗸 𝗚𝗿𝗼𝘂𝗽 𝗦𝗲𝗹𝗲𝗰𝘁')}
{self.bi('• 𝗔𝗱𝗺𝗶𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁')}
{self.bi('• 𝗖𝘂𝘀𝘁𝗼𝗺 𝗦𝗽𝗲𝗲𝗱 𝗖𝗼𝗻𝘁𝗿𝗼𝗹')}
{self.bi('• 𝟮𝟰/𝟳 𝗥𝘂𝗻𝗻𝗶𝗻𝗴')}

{self.bi('🔒 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗠𝗼𝗱𝗲')}
{self.bi('👑 𝗔𝗖𝗖𝗘𝗦𝗦: 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗢𝗻𝗹𝘆')}
{self.bi('💎 𝗣𝗟𝗔𝗡: 𝗘𝘅𝗰𝗹𝘂𝘀𝗶𝘃𝗲 𝗣𝗿𝗲𝗺𝗶𝘂𝗺')}

{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 📌')}
"""
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def id_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        chat_title = update.effective_chat.title if update.effective_chat.title else "Private Chat"
        chat_type = update.effective_chat.type
        
        if chat_type in ["group", "supergroup"]:
            saved_groups[str(chat_id)] = {
                "name": chat_title,
                "type": chat_type,
                "id": str(chat_id)
            }
            self.save_groups()
            
            msg = f"""
{self.bi('📋 𝗚𝗥𝗢𝗨𝗣 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + chat_title)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('📂 𝗧𝘆𝗽𝗲: ' + chat_type)}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('✅ 𝗚𝗿𝗼𝘂𝗽 𝗔𝘂𝘁𝗼-𝗦𝗮𝘃𝗲𝗱')}
{self.bi('📋 𝗨𝘀𝗲 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 𝗯𝘂𝘁𝘁𝗼𝗻')}
"""
        else:
            msg = f"""
{self.bi('💬 𝗖𝗛𝗔𝗧 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 💬')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + chat_title)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
"""
        
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        if not self.is_authorized(user_id):
            await query.edit_message_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        data = query.data
        
        # MAIN MENU - BACK BUTTON
        if data == "main_menu":
            await self.show_main_menu(query)
            return
        
        # GET ID INFO
        if data == "get_id_info":
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('🆔 𝗛𝗢𝗪 𝗧𝗢 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔')}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('📌 𝗠𝗘𝗧𝗛𝗢𝗗 𝟭 - 𝗨𝘀𝗶𝗻𝗴 𝗧𝗵𝗶𝘀 𝗕𝗼𝘁:')}
{self.bi('𝟭️ 𝗔𝗱𝗱 𝗯𝗼𝘁 𝘁𝗼 𝗴𝗿𝗼𝘂𝗽 𝗮𝘀 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('𝟮️ 𝗦𝗲𝗻𝗱 /𝗶𝗱 𝗶𝗻 𝘁𝗵𝗲 𝗴𝗿𝗼𝘂𝗽')}
{self.bi('𝟯️ 𝗕𝗼𝘁 𝘀𝗵𝗼𝘄𝘀 𝗜𝗗 & 𝗔𝗨𝗧𝗢-𝗦𝗔𝗩𝗘𝗦')}

{self.bi('📌 𝗠𝗘𝗧𝗛𝗢𝗗 𝟮 - 𝗨𝘀𝗶𝗻𝗴 @𝗴𝗲𝘁𝗶𝗱𝘀𝗯𝗼𝘁:')}
{self.bi('𝟭️ 𝗔𝗱𝗱 @𝗴𝗲𝘁𝗶𝗱𝘀𝗯𝗼𝘁 𝘁𝗼 𝗴𝗿𝗼𝘂𝗽')}
{self.bi('𝟮️ 𝗦𝗲𝗻𝗱 /𝗶𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}

{self.bi('💡 𝗧𝗜𝗣: 𝗚𝗿𝗼𝘂𝗽𝘀 𝗮𝗿𝗲 𝗮𝘂𝘁𝗼-𝘀𝗮𝘃𝗲𝗱')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # SAVED GROUPS MENU
        if data == "saved_groups_menu":
            if not saved_groups:
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"""
{self.bi('📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('❌ 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽𝘀 𝘀𝗮𝘃𝗲𝗱 𝘆𝗲𝘁!')}

{self.bi('💡 𝗛𝗼𝘄 𝘁𝗼 𝘀𝗮𝘃𝗲:')}
{self.bi('𝟭️ 𝗔𝗱𝗱 𝗯𝗼𝘁 𝘁𝗼 𝗴𝗿𝗼𝘂𝗽')}
{self.bi('𝟮️ 𝗦𝗲𝗻𝗱 /𝗶𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            keyboard = []
            for group_id, group_info in list(saved_groups.items())[:20]:
                name = group_info.get("name", group_id)[:35]
                keyboard.append([InlineKeyboardButton(f"📌 {name}", callback_data=f"select_group_{group_id}")])
            
            keyboard.append([InlineKeyboardButton("🗑 𝗖𝗟𝗘𝗔𝗥 𝗔𝗟𝗟 𝗚𝗥𝗢𝗨𝗣𝗦 🗑", callback_data="clear_groups")])
            keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")])
            
            await query.edit_message_text(
                f"""
{self.bi('📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 𝗟𝗜𝗦𝗧 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗧𝗼𝘁𝗮𝗹: ' + str(len(saved_groups)) + ' 𝗴𝗿𝗼𝘂𝗽𝘀')}

{self.bi('👇 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔 𝗚𝗥𝗢𝗨𝗣 👇')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # SELECT GROUP FROM SAVED
        if data.startswith("select_group_"):
            group_id = data.replace("select_group_", "")
            group_info = saved_groups.get(group_id, {})
            group_name = group_info.get("name", group_id)
            
            try:
                chat_id = int(group_id)
            except:
                chat_id = group_id
            
            user_states[user_id] = {
                "step": "waiting_for_type",
                "chat_id": chat_id,
                "group_name": group_name
            }
            
            keyboard = [
                [InlineKeyboardButton("💬 𝗧𝗘𝗫𝗧 💬", callback_data="type_text"),
                 InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯", callback_data="type_sticker")],
                [InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢 🖼", callback_data="type_photo"),
                 InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢 🎥", callback_data="type_video")],
                [InlineKeyboardButton("📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄", callback_data="type_document"),
                 InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢 🎵", callback_data="type_audio")],
                [InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘 🎤", callback_data="type_voice"),
                 InlineKeyboardButton("📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹", callback_data="type_video_note")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗚𝗥𝗢𝗨𝗣𝗦 🔙", callback_data="saved_groups_menu")]
            ]
            
            await query.edit_message_text(
                f"""
{self.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + group_name)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('🎯 𝗡𝗢𝗪 𝗦𝗘𝗟𝗘𝗖𝗧 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗧𝗬𝗣𝗘 🎯')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # CLEAR GROUPS
        if data == "clear_groups":
            saved_groups.clear()
            self.save_groups()
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('🗑 𝗚𝗥𝗢𝗨𝗣𝗦 𝗖𝗟𝗘𝗔𝗥𝗘𝗗 🗑')}
{self.bi('✅ 𝗔𝗹𝗹 𝘀𝗮𝘃𝗲𝗱 𝗴𝗿𝗼𝘂𝗽𝘀 𝗱𝗲𝗹𝗲𝘁𝗲𝗱')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # ADD GROUP MANUALLY
        if data == "add_group_manual":
            user_states[user_id] = {"step": "waiting_for_group_manual"}
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 𝗠𝗔𝗡𝗨𝗔𝗟𝗟𝗬 ➕')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗 𝗼𝗿 @𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲')}
{self.bi('📌 𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}
{self.bi('📌 𝗢𝗿: @𝗴𝗿𝗼𝘂𝗽𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # START SPAM
        if data == "start_spam":
            user_states[user_id] = {"step": "waiting_for_group"}
            keyboard = [
                [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", callback_data="saved_groups_menu")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"""
{self.bi('🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}
{self.bi('📌 𝗢𝗿 𝘀𝗲𝗹𝗲𝗰𝘁 𝗳𝗿𝗼𝗺 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦')}
{self.bi('📌 𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # STATS
        if data == "my_stats":
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('📊 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦 📊')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('👑 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗔𝗰𝘁𝗶𝘃𝗲 & 𝗢𝗻𝗹𝗶𝗻𝗲')}
{self.bi('💎 𝗣𝗹𝗮𝗻: 𝗘𝘅𝗰𝗹𝘂𝘀𝗶𝘃𝗲 𝗣𝗿𝗲𝗺𝗶𝘂𝗺')}
{self.bi('🔒 𝗔𝗰𝗰𝗲𝘀𝘀: 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗠𝗼𝗱𝗲')}
{self.bi('♾ 𝗟𝗶𝗺𝗶𝘁𝘀: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱')}
{self.bi('⚡ 𝗦𝗽𝗲𝗲𝗱: 𝗨𝗹𝘁𝗿𝗮 𝗠𝗮𝘅')}
{self.bi('📋 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀: ' + str(len(saved_groups)))}
{self.bi('👥 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(len(admin_list)))}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🔐 𝗡𝗢 𝗢𝗡𝗘 𝗘𝗟𝗦𝗘 𝗖𝗔𝗡 𝗨𝗦𝗘')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # HELP
        if data == "help_menu":
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('❓ 𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 ❓')}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟭:')}
{self.bi('𝗔𝗱𝗱 𝗯𝗼𝘁 𝘁𝗼 𝗴𝗿𝗼𝘂𝗽 𝗮𝘀 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('𝗚𝗶𝘃𝗲 𝗔𝗟𝗟 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻𝘀')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟮:')}
{self.bi('𝗦𝗲𝗻𝗱 /𝗶𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟯:')}
{self.bi('𝗖𝗹𝗶𝗰𝗸 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟰:')}
{self.bi('𝗦𝗲𝗹𝗲𝗰𝘁 𝗰𝗼𝗻𝘁𝗲𝗻𝘁 𝘁𝘆𝗽𝗲')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟱:')}
{self.bi('𝗦𝗲𝗻𝗱 𝗰𝗼𝗻𝘁𝗲𝗻𝘁 + 𝗰𝗼𝘂𝗻𝘁 + 𝘀𝗽𝗲𝗲𝗱')}

{self.bi('⚠ 𝗜𝗠𝗣𝗢𝗥𝗧𝗔𝗡𝗧:')}
{self.bi('𝗕𝗼𝘁 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗔𝗗𝗠𝗜𝗡')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # OWNER PANEL
        if data == "owner_panel":
            keyboard = [
                [InlineKeyboardButton("👥 𝗠𝗔𝗡𝗔𝗚𝗘 𝗔𝗗𝗠𝗜𝗡𝗦 👥", callback_data="manage_admins")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"""
{self.bi('🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('👑 𝗢𝘄𝗻𝗲𝗿 𝗜𝗗: ' + str(self.owner_id))}
{self.bi('📌 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @' + self.owner_username)}
{self.bi('👥 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(len(admin_list)))}
{self.bi('📋 𝗚𝗿𝗼𝘂𝗽𝘀: ' + str(len(saved_groups)))}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('✅ 𝗔𝗹𝗹 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀 𝗪𝗼𝗿𝗸𝗶𝗻𝗴')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # MANAGE ADMINS
        if data == "manage_admins":
            if user_id != self.owner_id:
                await query.answer("Only Owner can manage admins!", show_alert=True)
                return
            
            admin_text = f"""
{self.bi('👥 𝗔𝗗𝗠𝗜𝗡 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧 👥')}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👑 𝗢𝘄𝗻𝗲𝗿: @' + self.owner_username + ' (' + str(self.owner_id) + ')')}

{self.bi('👥 𝗔𝗱𝗺𝗶𝗻 𝗟𝗶𝘀𝘁:')}
"""
            for aid in admin_list:
                if aid != self.owner_id:
                    admin_text += f"{self.bi('• ' + str(aid))}\n"
            
            if len(admin_list) <= 1:
                admin_text += f"{self.bi('• 𝗡𝗼 𝗼𝘁𝗵𝗲𝗿 𝗮𝗱𝗺𝗶𝗻𝘀')}\n"
            
            admin_text += f"""
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👇 𝗦𝗲𝗻𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗮𝗱𝗱 𝗼𝗿 𝗿𝗲𝗺𝗼𝘃𝗲:')}
"""
            
            user_states[user_id] = {"step": "waiting_for_admin_id"}
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔙", callback_data="owner_panel")]]
            await query.edit_message_text(
                admin_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # TYPE SELECTION
        if data.startswith("type_"):
            msg_type = data.replace("type_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗧𝗬𝗣𝗘 𝗦𝗘𝗟𝗘𝗖𝗧𝗜𝗢𝗡 🔙", callback_data="show_types")]]
            
            msgs = {
                "text": f"{self.bi('💬 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗧𝗘𝗫𝗧 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 💬')}",
                "sticker": f"{self.bi('🎯 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯')}",
                "photo": f"{self.bi('🖼 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗣𝗛𝗢𝗧𝗢 🖼')}",
                "video": f"{self.bi('🎥 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗩𝗜𝗗𝗘𝗢 🎥')}",
                "document": f"{self.bi('📄 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄')}",
                "audio": f"{self.bi('🎵 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗔𝗨𝗗𝗜𝗢 🎵')}",
                "voice": f"{self.bi('🎤 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗩𝗢𝗜𝗖𝗘 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 🎤')}",
                "video_note": f"{self.bi('📹 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹')}"
            }
            await query.edit_message_text(
                msgs.get(msg_type, self.bi('📤 𝗦𝗘𝗡𝗗 𝗬𝗢𝗨𝗥 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 📤')),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # SHOW TYPES - BACK BUTTON FROM CONTENT
        if data == "show_types":
            chat_id = user_states[user_id].get("chat_id", "N/A")
            group_name = user_states[user_id].get("group_name", str(chat_id))
            user_states[user_id]["step"] = "waiting_for_type"
            
            keyboard = [
                [InlineKeyboardButton("💬 𝗧𝗘𝗫𝗧 💬", callback_data="type_text"),
                 InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯", callback_data="type_sticker")],
                [InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢 🖼", callback_data="type_photo"),
                 InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢 🎥", callback_data="type_video")],
                [InlineKeyboardButton("📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄", callback_data="type_document"),
                 InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢 🎵", callback_data="type_audio")],
                [InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘 🎤", callback_data="type_voice"),
                 InlineKeyboardButton("📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹", callback_data="type_video_note")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
            ]
            
            await query.edit_message_text(
                f"""
{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗧𝗬𝗣𝗘 🎯')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + group_name)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # SHOW COUNT - BACK BUTTON FROM SPEED
        if data == "show_count":
            user_states[user_id]["step"] = "waiting_for_count"
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗧𝗬𝗣𝗘 🔙", callback_data="show_types")]]
            await query.edit_message_text(
                f"""
{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬 𝗧𝗜𝗠𝗘𝗦? 🔢')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗮 𝗻𝘂𝗺𝗯𝗲𝗿 (𝟭-𝟭𝟬𝟬𝟬)')}
{self.bi('💡 𝗥𝗲𝗰𝗼𝗺𝗺𝗲𝗻𝗱𝗲𝗱: 𝟭𝟬')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # SPEED SELECTION
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
        
        # RESEND SAME
        if data == "resend_same":
            if user_id in user_states and "chat_id" in user_states[user_id]:
                await self.execute_spam(query, user_id, context)
            else:
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"{self.bi('❌ 𝗡𝗢 𝗣𝗥𝗘𝗩𝗜𝗢𝗨𝗦 𝗗𝗔𝗧𝗔')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        # NEW SPAM
        if data == "new_spam":
            chat_id = user_states.get(user_id, {}).get("chat_id")
            group_name = user_states.get(user_id, {}).get("group_name", str(chat_id))
            if chat_id:
                user_states[user_id] = {
                    "chat_id": chat_id,
                    "group_name": group_name,
                    "step": "waiting_for_type"
                }
                keyboard = [
                    [InlineKeyboardButton("💬 𝗧𝗘𝗫𝗧 💬", callback_data="type_text"),
                     InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯", callback_data="type_sticker")],
                    [InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢 🖼", callback_data="type_photo"),
                     InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢 🎥", callback_data="type_video")],
                    [InlineKeyboardButton("📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄", callback_data="type_document"),
                     InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢 🎵", callback_data="type_audio")],
                    [InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘 🎤", callback_data="type_voice"),
                     InlineKeyboardButton("📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹", callback_data="type_video_note")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
                ]
                await query.edit_message_text(
                    f"{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗧𝗬𝗣𝗘 🎯')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                user_states[user_id] = {"step": "waiting_for_group"}
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"{self.bi('📌 𝗦𝗘𝗡𝗗 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 𝗢𝗥 @𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 📌')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        # CHANGE TYPE
        if data == "change_type":
            user_states[user_id]["step"] = "waiting_for_type"
            keyboard = [
                [InlineKeyboardButton("💬 𝗧𝗘𝗫𝗧 💬", callback_data="type_text"),
                 InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯", callback_data="type_sticker")],
                [InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢 🖼", callback_data="type_photo"),
                 InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢 🎥", callback_data="type_video")],
                [InlineKeyboardButton("📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄", callback_data="type_document"),
                 InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢 🎵", callback_data="type_audio")],
                [InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘 🎤", callback_data="type_voice"),
                 InlineKeyboardButton("📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹", callback_data="type_video_note")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 🔙", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"{self.bi('🔄 𝗦𝗘𝗟𝗘𝗖𝗧 𝗡𝗘𝗪 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗧𝗬𝗣𝗘 🔄')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text(self.block_msg(), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id not in user_states:
            return
        
        state = user_states[user_id]
        step = state.get("step")
        
        # WAITING FOR ADMIN ID
        if step == "waiting_for_admin_id":
            if user_id != self.owner_id:
                await update.message.reply_text(
                    f"{self.bi('❌ Only Owner can manage admins!')}",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            text = update.message.text.strip()
            try:
                target_id = int(text)
                if target_id in admin_list:
                    admin_list.remove(target_id)
                    self.save_admins()
                    await update.message.reply_text(
                        f"{self.bi('✅ 𝗔𝗱𝗺𝗶𝗻 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: ' + str(target_id))}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    admin_list.add(target_id)
                    self.save_admins()
                    await update.message.reply_text(
                        f"{self.bi('✅ 𝗔𝗱𝗺𝗶𝗻 𝗔𝗱𝗱𝗲𝗱: ' + str(target_id))}",
                        parse_mode=ParseMode.MARKDOWN
                    )
            except:
                await update.message.reply_text(
                    f"{self.bi('❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗜𝗗! 𝗦𝗲𝗻𝗱 𝗻𝘂𝗺𝗲𝗿𝗶𝗰 𝗨𝘀𝗲𝗿 𝗜𝗗')}",
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        # WAITING FOR GROUP MANUAL
        if step == "waiting_for_group_manual":
            text = update.message.text
            chat_id = self.parse_chat_id(text)
            
            if chat_id:
                try:
                    group_name = await self.get_chat_info(context, chat_id)
                except:
                    group_name = str(chat_id)
                
                saved_groups[str(chat_id)] = {
                    "name": group_name,
                    "id": str(chat_id)
                }
                self.save_groups()
                
                user_states[user_id] = {
                    "chat_id": chat_id,
                    "group_name": group_name,
                    "step": "waiting_for_type"
                }
                
                keyboard = [
                    [InlineKeyboardButton("💬 𝗧𝗘𝗫𝗧 💬", callback_data="type_text"),
                     InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯", callback_data="type_sticker")],
                    [InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢 🖼", callback_data="type_photo"),
                     InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢 🎥", callback_data="type_video")],
                    [InlineKeyboardButton("📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄", callback_data="type_document"),
                     InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢 🎵", callback_data="type_audio")],
                    [InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘 🎤", callback_data="type_voice"),
                     InlineKeyboardButton("📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹", callback_data="type_video_note")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗔𝗗𝗗𝗘𝗗 & 𝗦𝗔𝗩𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + group_name)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('🎯 𝗡𝗢𝗪 𝗦𝗘𝗟𝗘𝗖𝗧 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗧𝗬𝗣𝗘 🎯')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]]
                await update.message.reply_text(
                    f"""
{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 ❌')}
{self.bi('𝗦𝗲𝗻𝗱 /𝗶𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}
{self.bi('𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        # WAITING FOR GROUP
        if step == "waiting_for_group":
            text = update.message.text
            chat_id = self.parse_chat_id(text)
            
            if chat_id:
                try:
                    group_name = await self.get_chat_info(context, chat_id)
                except:
                    group_name = str(chat_id)
                
                saved_groups[str(chat_id)] = {
                    "name": group_name,
                    "id": str(chat_id)
                }
                self.save_groups()
                
                user_states[user_id]["chat_id"] = chat_id
                user_states[user_id]["group_name"] = group_name
                user_states[user_id]["step"] = "waiting_for_type"
                
                keyboard = [
                    [InlineKeyboardButton("💬 𝗧𝗘𝗫𝗧 💬", callback_data="type_text"),
                     InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯", callback_data="type_sticker")],
                    [InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢 🖼", callback_data="type_photo"),
                     InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢 🎥", callback_data="type_video")],
                    [InlineKeyboardButton("📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧 📄", callback_data="type_document"),
                     InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢 🎵", callback_data="type_audio")],
                    [InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘 🎤", callback_data="type_voice"),
                     InlineKeyboardButton("📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘 📹", callback_data="type_video_note")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗙𝗢𝗨𝗡𝗗 & 𝗦𝗔𝗩𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + group_name)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('🎯 𝗡𝗢𝗪 𝗦𝗘𝗟𝗘𝗖𝗧 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗧𝗬𝗣𝗘 🎯')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                keyboard = [
                    [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", callback_data="saved_groups_menu")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
                ]
                await update.message.reply_text(
                    f"""
{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 ❌')}
{self.bi('𝗨𝘀𝗲 /𝗶𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}
{self.bi('𝗢𝗿 𝘀𝗲𝗹𝗲𝗰𝘁 𝗳𝗿𝗼𝗺 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        # WAITING FOR CONTENT
        if step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗧𝗬𝗣𝗘 🔙", callback_data="show_types")]]
            
            await update.message.reply_text(
                f"""
{self.bi('✅ 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗥𝗘𝗖𝗘𝗜𝗩𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬 𝗧𝗜𝗠𝗘𝗦? 🔢')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗮 𝗻𝘂𝗺𝗯𝗲𝗿 (𝟭-𝟭𝟬𝟬𝟬)')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # WAITING FOR COUNT
        if step == "waiting_for_count":
            try:
                count = int(update.message.text)
                count = max(1, min(count, 1000))
                
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "waiting_for_speed"
                
                keyboard = [
                    [InlineKeyboardButton("⚡ 𝗨𝗟𝗧𝗥𝗔 ⚡ (𝟬.𝟱𝘀)", callback_data="speed_ultra"),
                     InlineKeyboardButton("🚀 𝗙𝗔𝗦𝗧 🚀 (𝟭𝘀)", callback_data="speed_fast")],
                    [InlineKeyboardButton("🐢 𝗡𝗢𝗥𝗠𝗔𝗟 🐢 (𝟮𝘀)", callback_data="speed_normal"),
                     InlineKeyboardButton("🦥 𝗦𝗟𝗢𝗪 🦥 (𝟱𝘀)", callback_data="speed_slow")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗖𝗢𝗨𝗡𝗧 🔙", callback_data="show_count")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('⚡ 𝗖𝗛𝗢𝗢𝗦𝗘 𝗦𝗣𝗘𝗘𝗗 ⚡')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🔢 𝗖𝗼𝘂𝗻𝘁: ' + str(count))}

{self.bi('👇 𝗦𝗲𝗹𝗲𝗰𝘁 𝘀𝗽𝗲𝗲𝗱 𝗯𝗲𝗹𝗼𝘄 👇')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗧𝗬𝗣𝗘 🔙", callback_data="show_types")]]
                await update.message.reply_text(
                    f"{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗡𝗨𝗠𝗕𝗘𝗥 ❌')}",
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
{self.bi('🔥 𝗦𝗣𝗔𝗠 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 🔥')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + group_name)}
{self.bi('🎯 𝗧𝘆𝗽𝗲: ' + msg_type)}
{self.bi('🔢 𝗖𝗼𝘂𝗻𝘁: ' + str(count))}
{self.bi('⚡ 𝗦𝗽𝗲𝗲𝗱: ' + str(delay) + '𝘀')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🚀 𝗦𝗘𝗡𝗗𝗜𝗡𝗚 𝗠𝗘𝗦𝗦𝗔𝗚𝗘𝗦 𝗡𝗢𝗪 🚀')}
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        error_msg = None
        
        for i in range(count):
            try:
                if msg_type == "text":
                    msg_text = content.text if content and content.text else "🔥 Premium Spam Bot 🔥"
                    await context.bot.send_message(chat_id=chat_id, text=msg_text)
                    success += 1
                
                elif msg_type == "sticker":
                    if content and content.sticker:
                        await context.bot.send_sticker(chat_id=chat_id, sticker=content.sticker.file_id)
                        success += 1
                    else:
                        failed += 1
                        error_msg = "No sticker found"
                        break
                
                elif msg_type == "photo":
                    if content and content.photo:
                        await context.bot.send_photo(chat_id=chat_id, photo=content.photo[-1].file_id, caption=content.caption or "")
                        success += 1
                    else:
                        failed += 1
                        break
                
                elif msg_type == "video":
                    if content and content.video:
                        await context.bot.send_video(chat_id=chat_id, video=content.video.file_id, caption=content.caption or "")
                        success += 1
                    else:
                        failed += 1
                        break
                
                elif msg_type == "document":
                    if content and content.document:
                        await context.bot.send_document(chat_id=chat_id, document=content.document.file_id, caption=content.caption or "")
                        success += 1
                    else:
                        failed += 1
                        break
                
                elif msg_type == "audio":
                    if content and content.audio:
                        await context.bot.send_audio(chat_id=chat_id, audio=content.audio.file_id, caption=content.caption or "")
                        success += 1
                    else:
                        failed += 1
                        break
                
                elif msg_type == "voice":
                    if content and content.voice:
                        await context.bot.send_voice(chat_id=chat_id, voice=content.voice.file_id, caption=content.caption or "")
                        success += 1
                    else:
                        failed += 1
                        break
                
                elif msg_type == "video_note":
                    if content and content.video_note:
                        await context.bot.send_video_note(chat_id=chat_id, video_note=content.video_note.file_id)
                        success += 1
                    else:
                        failed += 1
                        break
                
                else:
                    failed += 1
                    break
                
                if success > 0 and success % 5 == 0:
                    try:
                        await query.edit_message_text(
                            f"""
{self.bi('⚡ 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 𝗜𝗡 𝗣𝗥𝗢𝗚𝗥𝗘𝗦𝗦 ⚡')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + group_name)}
{self.bi('✅ 𝗦𝗲𝗻𝘁: ' + str(success) + '/' + str(count))}
""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                error_str = str(e).lower()
                
                if "not enough rights" in error_str:
                    error_msg = f"Bot needs ADMIN with {msg_type} permission ON"
                    break
                elif "forbidden" in error_str or "blocked" in error_str:
                    error_msg = "Bot not in group or blocked"
                    break
                elif "not found" in error_str:
                    error_msg = "Group not found"
                    break
                else:
                    error_msg = str(e)[:150]
                
                if failed > 2:
                    break
        
        result = f"""
{self.bi('✅ 𝗠𝗜𝗦𝗦𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + group_name)}
{self.bi('✅ 𝗦𝘂𝗰𝗰𝗲𝘀𝘀: ' + str(success))}
{self.bi('❌ 𝗙𝗮𝗶𝗹𝗲𝗱: ' + str(failed))}
{self.bi('🎯 𝗧𝘆𝗽𝗲: ' + msg_type)}
{self.bi('⚡ 𝗦𝗽𝗲𝗲𝗱: ' + str(delay) + '𝘀')}
"""
        
        if error_msg and success == 0:
            result += f"""
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('⚠ 𝗘𝗥𝗥𝗢𝗥: ' + error_msg)}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('💡 𝗦𝗢𝗟𝗨𝗧𝗜𝗢𝗡:')}
{self.bi('𝟭️ 𝗠𝗮𝗸𝗲 𝗯𝗼𝘁 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('𝟮️ 𝗘𝗻𝗮𝗯𝗹𝗲 𝗔𝗟𝗟 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻𝘀')}
"""
        
        result += f"""
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👇 𝗪𝗛𝗔𝗧 𝗡𝗘𝗫𝗧? 👇')}
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 𝗥𝗘𝗦𝗘𝗡𝗗 𝗦𝗔𝗠𝗘 🔄", callback_data="resend_same"),
             InlineKeyboardButton("🆕 𝗡𝗘𝗪 𝗦𝗣𝗔𝗠 🆕", callback_data="new_spam")],
            [InlineKeyboardButton("🔀 𝗖𝗛𝗔𝗡𝗚𝗘 𝗧𝗬𝗣𝗘 🔀", callback_data="change_type"),
             InlineKeyboardButton("🔢 𝗖𝗛𝗔𝗡𝗚𝗘 𝗖𝗢𝗨𝗡𝗧 🔢", callback_data="show_count")],
            [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨 🔙", callback_data="main_menu")]
        ]
        
        try:
            await query.message.reply_text(
                result,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Result error: {e}")

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
    
    print(f"""
╔══════════════════════════════════════╗
║   👑 PREMIUM SPAM BOT STARTED 👑   ║
║   🔒 PRIVATE MODE ACTIVE 🔒        ║
║   📋 Groups Auto-Save Active       ║
║   👥 Admin System Active           ║
║   👤 Owner: @{OWNER_USERNAME}     ║
╚══════════════════════════════════════╝
    """)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
