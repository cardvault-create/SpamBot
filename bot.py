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
auto_delete_enabled = True
last_spam_messages = {}

GROUPS_FILE = "saved_groups.json"
ADMIN_FILE = "admin_list.json"
CONFIG_FILE = "config.json"

class PremiumGroupSpamBot:
    def __init__(self):
        self.owner_id = OWNER_ID
        self.owner_username = OWNER_USERNAME
        self.load_data()
    
    def load_data(self):
        global saved_groups, admin_list, auto_delete_enabled
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
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                auto_delete_enabled = config.get("auto_delete", True)
        except:
            auto_delete_enabled = True
    
    def save_groups(self):
        with open(GROUPS_FILE, 'w') as f:
            json.dump(saved_groups, f)
    
    def save_admins(self):
        with open(ADMIN_FILE, 'w') as f:
            json.dump(list(admin_list), f)
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"auto_delete": auto_delete_enabled}, f)
    
    def is_authorized(self, user_id):
        return user_id == self.owner_id or user_id in admin_list
    
    def bi(self, text):
        return f"***{text}***"
    
    def make_bold(self, text):
        if not text:
            return "𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗦𝗽𝗮𝗺"
        bold_map = {
            'a':'𝗮','b':'𝗯','c':'𝗰','d':'𝗱','e':'𝗲','f':'𝗳','g':'𝗴','h':'𝗵','i':'𝗶','j':'𝗷',
            'k':'𝗸','l':'𝗹','m':'𝗺','n':'𝗻','o':'𝗼','p':'𝗽','q':'𝗾','r':'𝗿','s':'𝘀','t':'𝘁',
            'u':'𝘂','v':'𝘃','w':'𝘄','x':'𝘅','y':'𝘆','z':'𝘇',
            'A':'𝗔','B':'𝗕','C':'𝗖','D':'𝗗','E':'𝗘','F':'𝗙','G':'𝗚','H':'𝗛','I':'𝗜','J':'𝗝',
            'K':'𝗞','L':'𝗟','M':'𝗠','N':'𝗡','O':'𝗢','P':'𝗣','Q':'𝗤','R':'𝗥','S':'𝗦','T':'𝗧',
            'U':'𝗨','V':'𝗩','W':'𝗪','X':'𝗫','Y':'𝗬','Z':'𝗭',
            '0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'
        }
        return ''.join(bold_map.get(c, c) for c in text)
    
    def make_italic(self, text):
        if not text:
            return "𝑃𝑟𝑒𝑚𝑖𝑢𝑚 𝑆𝑝𝑎𝑚"
        italic_map = {
            'a':'𝑎','b':'𝑏','c':'𝑐','d':'𝑑','e':'𝑒','f':'𝑓','g':'𝑔','h':'ℎ','i':'𝑖','j':'𝑗',
            'k':'𝑘','l':'𝑙','m':'𝑚','n':'𝑛','o':'𝑜','p':'𝑝','q':'𝑞','r':'𝑟','s':'𝑠','t':'𝑡',
            'u':'𝑢','v':'𝑣','w':'𝑤','x':'𝑥','y':'𝑦','z':'𝑧',
            'A':'𝐴','B':'𝐵','C':'𝐶','D':'𝐷','E':'𝐸','F':'𝐹','G':'𝐺','H':'𝐻','I':'𝐼','J':'𝐽',
            'K':'𝐾','L':'𝐿','M':'𝑀','N':'𝑁','O':'𝑂','P':'𝑃','Q':'𝑄','R':'𝑅','S':'𝑆','T':'𝑇',
            'U':'𝑈','V':'𝑉','W':'𝑊','X':'𝑋','Y':'𝑌','Z':'𝑍'
        }
        return ''.join(italic_map.get(c, c) for c in text)
    
    def make_bold_italic(self, text):
        if not text:
            return "𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑺𝒑𝒂𝒎"
        bi_map = {
            'a':'𝒂','b':'𝒃','c':'𝒄','d':'𝒅','e':'𝒆','f':'𝒇','g':'𝒈','h':'𝒉','i':'𝒊','j':'𝒋',
            'k':'𝒌','l':'𝒍','m':'𝒎','n':'𝒏','o':'𝒐','p':'𝒑','q':'𝒒','r':'𝒓','s':'𝒔','t':'𝒕',
            'u':'𝒖','v':'𝒗','w':'𝒘','x':'𝒙','y':'𝒚','z':'𝒛',
            'A':'𝑨','B':'𝑩','C':'𝑪','D':'𝑫','E':'𝑬','F':'𝑭','G':'𝑮','H':'𝑯','I':'𝑰','J':'𝑱',
            'K':'𝑲','L':'𝑳','M':'𝑴','N':'𝑵','O':'𝑶','P':'𝑷','Q':'𝑸','R':'𝑹','S':'𝑺','T':'𝑻',
            'U':'𝑼','V':'𝑽','W':'𝑾','X':'𝑿','Y':'𝒀','Z':'𝒁'
        }
        return ''.join(bi_map.get(c, c) for c in text)
    
    def make_monospace(self, text):
        if not text:
            return "𝙿𝚛𝚎𝚖𝚒𝚞𝚖 𝚂𝚙𝚊𝚖"
        mono_map = {
            'a':'𝚊','b':'𝚋','c':'𝚌','d':'𝚍','e':'𝚎','f':'𝚏','g':'𝚐','h':'𝚑','i':'𝚒','j':'𝚓',
            'k':'𝚔','l':'𝚕','m':'𝚖','n':'𝚗','o':'𝚘','p':'𝚙','q':'𝚚','r':'𝚛','s':'𝚜','t':'𝚝',
            'u':'𝚞','v':'𝚟','w':'𝚠','x':'𝚡','y':'𝚢','z':'𝚣',
            'A':'𝙰','B':'𝙱','C':'𝙲','D':'𝙳','E':'𝙴','F':'𝙵','G':'𝙶','H':'𝙷','I':'𝙸','J':'𝙹',
            'K':'𝙺','L':'𝙻','M':'𝙼','N':'𝙽','O':'𝙾','P':'𝙿','Q':'𝚀','R':'𝚁','S':'𝚂','T':'𝚃',
            'U':'𝚄','V':'𝚅','W':'𝚆','X':'𝚇','Y':'𝚈','Z':'𝚉'
        }
        return ''.join(mono_map.get(c, c) for c in text)
    
    def block_msg(self):
        return f"""
{self.bi('🔐 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🔐')}
{self.bi('⛔ 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗 ⛔')}
{self.bi('𝗧𝗵𝗶𝘀 𝗯𝗼𝘁 𝗶𝘀 𝘀𝘁𝗿𝗶𝗰𝘁𝗹𝘆 𝗽𝗿𝗶𝘃𝗮𝘁𝗲')}
{self.bi('𝗮𝗻𝗱 𝗼𝗽𝗲𝗿𝗮𝘁𝗲𝘀 𝗳𝗼𝗿 𝗼𝘄𝗻𝗲𝗿 𝗼𝗻𝗹𝘆')}
{self.bi('👑 𝗢𝘄𝗻𝗲𝗿: @' + self.owner_username)}
{self.bi('❌ 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗮𝗰𝗰𝗲𝘀𝘀 𝗯𝗹𝗼𝗰𝗸𝗲𝗱')}
"""
    
    async def get_chat_info(self, context, chat_id):
        try:
            chat = await context.bot.get_chat(chat_id)
            return chat.title if chat.title else str(chat_id)
        except:
            return str(chat_id)
    
    async def delete_spam_messages(self, context, chat_id, message_ids):
        """Delete spam messages from group"""
        deleted = 0
        for msg_id in message_ids:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                deleted += 1
                await asyncio.sleep(0.5)
            except:
                pass
        return deleted
    
    async def show_main_menu(self, query):
        user_id = query.from_user.id
        
        if not self.is_authorized(user_id):
            keyboard = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await query.edit_message_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id in user_states:
            del user_states[user_id]
        
        auto_status = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
        
        keyboard = [
            [InlineKeyboardButton("🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥", callback_data="start_spam")],
            [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", callback_data="saved_groups_menu"),
             InlineKeyboardButton("➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 ➕", callback_data="add_group_manual")],
            [InlineKeyboardButton("🆔 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔", callback_data="get_id_info"),
             InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣 ❓", callback_data="help_menu")],
            [InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦 📊", callback_data="my_stats"),
             InlineKeyboardButton("🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐", callback_data="owner_panel")],
            [InlineKeyboardButton(f"🔄 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘: {auto_status}", callback_data="toggle_auto_delete")],
            [InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]
        ]
        
        msg = f"""
{self.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{self.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{self.bi('⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 ⭐')}
{self.bi('• 𝟰 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀 (𝗕𝗼𝗹𝗱/𝗜𝘁𝗮𝗹𝗶𝗰/𝗕&𝗜/𝗠𝗼𝗻𝗼)')}
{self.bi('• 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝗲𝗻𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
{self.bi('• 𝗗𝗲𝗹𝗲𝘁𝗲 𝗔𝗹𝗹 𝗚𝗿𝗼𝘂𝗽 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
{self.bi('• 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝘆𝘀𝘁𝗲𝗺')}
{self.bi('• 𝗔𝗱𝗺𝗶𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁')}

{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 📌')}
"""
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            keyboard = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id in user_states:
            del user_states[user_id]
        
        auto_status = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
        
        keyboard = [
            [InlineKeyboardButton("🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥", callback_data="start_spam")],
            [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", callback_data="saved_groups_menu"),
             InlineKeyboardButton("➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 ➕", callback_data="add_group_manual")],
            [InlineKeyboardButton("🆔 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔", callback_data="get_id_info"),
             InlineKeyboardButton("❓ 𝗛𝗘𝗟𝗣 ❓", callback_data="help_menu")],
            [InlineKeyboardButton("📊 𝗦𝗧𝗔𝗧𝗦 📊", callback_data="my_stats"),
             InlineKeyboardButton("🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐", callback_data="owner_panel")],
            [InlineKeyboardButton(f"🔄 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘: {auto_status}", callback_data="toggle_auto_delete")],
            [InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]
        ]
        
        msg = f"""
{self.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{self.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{self.bi('⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 ⭐')}
{self.bi('• 𝟰 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀')}
{self.bi('• 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝗲𝗻𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
{self.bi('• 𝗗𝗲𝗹𝗲𝘁𝗲 𝗔𝗹𝗹 𝗚𝗿𝗼𝘂𝗽 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}

{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 📌')}
"""
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def getid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        chat_title = update.effective_chat.title if update.effective_chat.title else "Private Chat"
        chat_type = update.effective_chat.type
        
        if chat_type in ["group", "supergroup"]:
            saved_groups[str(chat_id)] = {"name": chat_title, "type": chat_type, "id": str(chat_id)}
            self.save_groups()
            
            msg = f"""
{self.bi('📋 𝗚𝗥𝗢𝗨𝗣 𝗜𝗡𝗙𝗢 📋')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + chat_title)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('✅ 𝗔𝘂𝘁𝗼-𝗦𝗮𝘃𝗲𝗱')}
"""
        else:
            msg = f"""
{self.bi('💬 𝗖𝗛𝗔𝗧 𝗜𝗡𝗙𝗢 💬')}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
"""
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    async def deleteall_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            keyboard = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        user_states[user_id] = {"step": "waiting_for_delete_group"}
        keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
        await update.message.reply_text(
            f"""
{self.bi('🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗔𝗟𝗟 𝗠𝗘𝗦𝗦𝗔𝗚𝗘𝗦 🗑')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}
{self.bi('⚠ 𝗕𝗼𝘁 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗔𝗗𝗠𝗜𝗡')}
""",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        if not self.is_authorized(user_id):
            keyboard = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await query.edit_message_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        data = query.data
        
        if data == "main_menu":
            await self.show_main_menu(query)
            return
        
        if data == "toggle_auto_delete":
            global auto_delete_enabled
            auto_delete_enabled = not auto_delete_enabled
            self.save_config()
            status = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
            await query.answer(f"Auto Delete {status}", show_alert=True)
            await self.show_main_menu(query)
            return
        
        if data == "delete_last_spam":
            if user_id in last_spam_messages:
                spam_data = last_spam_messages[user_id]
                chat_id = spam_data.get("chat_id")
                msg_ids = spam_data.get("message_ids", [])
                
                await query.edit_message_text(
                    f"{self.bi('🗑 𝗗𝗘𝗟𝗘𝗧𝗜𝗡𝗚 𝗠𝗘𝗦𝗦𝗔𝗚𝗘𝗦... 🗑')}",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                deleted = await self.delete_spam_messages(context, chat_id, msg_ids)
                
                keyboard = [[InlineKeyboardButton("🔙 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"""
{self.bi('✅ 𝗗𝗘𝗟𝗘𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━')}
{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗲𝗱: ' + str(deleted) + '/' + str(len(msg_ids)))}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + str(chat_id))}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
                del last_spam_messages[user_id]
            else:
                await query.answer("No messages to delete!", show_alert=True)
            return
        
        if data == "get_id_info":
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('🆔 𝗛𝗢𝗪 𝗧𝗢 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔')}

{self.bi('📌 𝗔𝗱𝗱 𝗯𝗼𝘁 𝘁𝗼 𝗴𝗿𝗼𝘂𝗽 𝗮𝘀 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('📌 𝗦𝗲𝗻𝗱 /𝗚𝗲𝘁𝗜𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}
{self.bi('📌 𝗕𝗼𝘁 𝘀𝗵𝗼𝘄𝘀 𝗜𝗗 & 𝗔𝗨𝗧𝗢-𝗦𝗔𝗩𝗘𝗦')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "saved_groups_menu":
            if not saved_groups:
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"{self.bi('📋 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽𝘀 𝘀𝗮𝘃𝗲𝗱')}\n{self.bi('𝗦𝗲𝗻𝗱 /𝗚𝗲𝘁𝗜𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            keyboard = []
            for gid, ginfo in list(saved_groups.items())[:20]:
                name = ginfo.get("name", gid)[:30]
                keyboard.append([InlineKeyboardButton(f"📌 {name}", callback_data=f"sg_{gid}")])
            
            keyboard.append([InlineKeyboardButton("🗑 𝗖𝗟𝗘𝗔𝗥 𝗔𝗟𝗟", callback_data="clear_groups")])
            keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")])
            
            await query.edit_message_text(
                f"{self.bi('📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 (' + str(len(saved_groups)) + ')')}\n{self.bi('👇 𝗦𝗘𝗟𝗘𝗖𝗧 👇')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data.startswith("sg_"):
            group_id = data.replace("sg_", "")
            ginfo = saved_groups.get(group_id, {})
            gname = ginfo.get("name", group_id)
            try:
                chat_id = int(group_id)
            except:
                chat_id = group_id
            
            user_states[user_id] = {"step": "waiting_for_type", "chat_id": chat_id, "group_name": gname}
            
            keyboard = [
                [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="type_text"),
                 InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="type_bold")],
                [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_italic"),
                 InlineKeyboardButton("𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_bold_italic")],
                [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢𝗦𝗣𝗔𝗖𝗘", callback_data="type_mono")],
                [InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", callback_data="type_sticker"),
                 InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢", callback_data="type_photo")],
                [InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢", callback_data="type_video"),
                 InlineKeyboardButton("📄 𝗗𝗢𝗖", callback_data="type_document")],
                [InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢", callback_data="type_audio"),
                 InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘", callback_data="type_voice")],
                [InlineKeyboardButton("📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘", callback_data="type_video_note")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="saved_groups_menu")]
            ]
            
            await query.edit_message_text(
                f"""
{self.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 ✅')}
{self.bi('📌 ' + gname)}
{self.bi('🆔 ' + str(chat_id))}

{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘/𝗧𝗬𝗣𝗘 🎯')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "clear_groups":
            saved_groups.clear()
            self.save_groups()
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(f"{self.bi('🗑 𝗖𝗟𝗘𝗔𝗥𝗘𝗗')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if data == "add_group_manual":
            user_states[user_id] = {"step": "waiting_for_group_manual"}
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"{self.bi('➕ 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}\n{self.bi('𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "start_spam":
            user_states[user_id] = {"step": "waiting_for_group"}
            keyboard = [
                [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦", callback_data="saved_groups_menu")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"{self.bi('🔥 𝗦𝗘𝗡𝗗 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗')}\n{self.bi('𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "my_stats":
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('📊 𝗦𝗧𝗔𝗧𝗦 📊')}
{self.bi('👑 𝗔𝗰𝘁𝗶𝘃𝗲')}
{self.bi('📋 𝗚𝗿𝗼𝘂𝗽𝘀: ' + str(len(saved_groups)))}
{self.bi('👥 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(len(admin_list)))}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "help_menu":
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('❓ 𝗛𝗘𝗟𝗣 ❓')}
{self.bi('📌 𝗔𝗱𝗱 𝗯𝗼𝘁 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('📌 /𝗚𝗲𝘁𝗜𝗱 𝗳𝗼𝗿 𝗜𝗗')}
{self.bi('📌 𝗖𝗵𝗼𝗼𝘀𝗲 𝘀𝘁𝘆𝗹𝗲')}
{self.bi('📌 𝗗𝗲𝗹𝗲𝘁𝗲 𝗮𝗳𝘁𝗲𝗿 𝘀𝗽𝗮𝗺')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "owner_panel":
            keyboard = [
                [InlineKeyboardButton("👥 𝗠𝗔𝗡𝗔𝗚𝗘 𝗔𝗗𝗠𝗜𝗡𝗦", callback_data="manage_admins")],
                [InlineKeyboardButton("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗔𝗟𝗟 𝗚𝗥𝗢𝗨𝗣 𝗠𝗦𝗚", callback_data="delete_all_group")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"""
{self.bi('🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐')}
{self.bi('👑 @' + self.owner_username)}
{self.bi('👥 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(len(admin_list)))}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "delete_all_group":
            user_states[user_id] = {"step": "waiting_for_delete_group"}
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")]]
            await query.edit_message_text(
                f"{self.bi('🗑 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "manage_admins":
            if user_id != self.owner_id:
                await query.answer("Only Owner!", show_alert=True)
                return
            
            atext = f"{self.bi('👥 𝗔𝗗𝗠𝗜𝗡𝗦 👥')}\n"
            for aid in admin_list:
                if aid != self.owner_id:
                    atext += f"{self.bi('• ' + str(aid))}\n"
            if len(admin_list) <= 1:
                atext += f"{self.bi('• 𝗡𝗼𝗻𝗲')}\n"
            atext += f"\n{self.bi('👇 𝗦𝗲𝗻𝗱 𝗜𝗗:')}"
            
            user_states[user_id] = {"step": "waiting_for_admin_id"}
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")]]
            await query.edit_message_text(atext, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if data.startswith("type_"):
            msg_type = data.replace("type_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_types")]]
            
            msgs = {
                "text": f"{self.bi('💬 𝗦𝗘𝗡𝗗 𝗡𝗢𝗥𝗠𝗔𝗟 𝗧𝗘𝗫𝗧 💬')}",
                "bold": f"{self.bi('𝗕 𝗦𝗘𝗡𝗗 𝗧𝗘𝗫𝗧 𝗙𝗢𝗥 𝗕𝗢𝗟𝗗 𝗕')}",
                "italic": f"{self.bi('𝑰 𝗦𝗘𝗡𝗗 𝗧𝗘𝗫𝗧 𝗙𝗢𝗥 𝗜𝗧𝗔𝗟𝗜𝗖 𝑰')}",
                "bold_italic": f"{self.bi('𝑩𝑰 𝗦𝗘𝗡𝗗 𝗧𝗘𝗫𝗧 𝗙𝗢𝗥 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖 𝑩𝑰')}",
                "mono": f"{self.bi('𝙼 𝗦𝗘𝗡𝗗 𝗧𝗘𝗫𝗧 𝗙𝗢𝗥 𝗠𝗢𝗡𝗢 𝙼')}",
                "sticker": f"{self.bi('🎯 𝗦𝗘𝗡𝗗 𝗦𝗧𝗜𝗖𝗞𝗘𝗥 🎯')}",
                "photo": f"{self.bi('🖼 𝗦𝗘𝗡𝗗 𝗣𝗛𝗢𝗧𝗢 🖼')}",
                "video": f"{self.bi('🎥 𝗦𝗘𝗡𝗗 𝗩𝗜𝗗𝗘𝗢 🎥')}",
                "document": f"{self.bi('📄 𝗦𝗘𝗡𝗗 𝗗𝗢𝗖 📄')}",
                "audio": f"{self.bi('🎵 𝗦𝗘𝗡𝗗 𝗔𝗨𝗗𝗜𝗢 🎵')}",
                "voice": f"{self.bi('🎤 𝗦𝗘𝗡𝗗 𝗩𝗢𝗜𝗖𝗘 🎤')}",
                "video_note": f"{self.bi('📹 𝗦𝗘𝗡𝗗 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘 📹')}"
            }
            await query.edit_message_text(msgs.get(msg_type, self.bi('📤 𝗦𝗘𝗡𝗗')), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if data == "show_types":
            chat_id = user_states[user_id].get("chat_id", "N/A")
            gname = user_states[user_id].get("group_name", str(chat_id))
            user_states[user_id]["step"] = "waiting_for_type"
            
            keyboard = [
                [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="type_text"),
                 InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="type_bold")],
                [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_italic"),
                 InlineKeyboardButton("𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_bold_italic")],
                [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢", callback_data="type_mono")],
                [InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", callback_data="type_sticker"),
                 InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢", callback_data="type_photo")],
                [InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢", callback_data="type_video"),
                 InlineKeyboardButton("📄 𝗗𝗢𝗖", callback_data="type_document")],
                [InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢", callback_data="type_audio"),
                 InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘", callback_data="type_voice")],
                [InlineKeyboardButton("📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘", callback_data="type_video_note")],
                [InlineKeyboardButton("🔙 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
            ]
            
            await query.edit_message_text(
                f"{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘')}\n{self.bi('📌 ' + gname)}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if data == "show_count":
            user_states[user_id]["step"] = "waiting_for_count"
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_types")]]
            await query.edit_message_text(f"{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬?')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if data.startswith("speed_"):
            speed_map = {"speed_ultra": 0.5, "speed_fast": 1, "speed_normal": 2, "speed_slow": 5}
            user_states[user_id]["delay"] = speed_map.get(data, 1)
            await self.execute_spam(query, user_id, context)
            return
        
        if data == "resend_same":
            if user_id in user_states and "chat_id" in user_states[user_id]:
                await self.execute_spam(query, user_id, context)
            return
        
        if data == "new_spam":
            chat_id = user_states.get(user_id, {}).get("chat_id")
            gname = user_states.get(user_id, {}).get("group_name", str(chat_id))
            if chat_id:
                user_states[user_id] = {"chat_id": chat_id, "group_name": gname, "step": "waiting_for_type"}
                keyboard = [
                    [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="type_text"),
                     InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="type_bold")],
                    [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_italic"),
                     InlineKeyboardButton("𝑩𝑰 𝗕&𝗜", callback_data="type_bold_italic")],
                    [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢", callback_data="type_mono")],
                    [InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", callback_data="type_sticker"),
                     InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢", callback_data="type_photo")],
                    [InlineKeyboardButton("🔙 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
                ]
                await query.edit_message_text(f"{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if data == "change_type":
            user_states[user_id]["step"] = "waiting_for_type"
            keyboard = [
                [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="type_text"),
                 InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="type_bold")],
                [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_italic"),
                 InlineKeyboardButton("𝑩𝑰 𝗕&𝗜", callback_data="type_bold_italic")],
                [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢", callback_data="type_mono")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]
            ]
            await query.edit_message_text(f"{self.bi('🔄 𝗡𝗘𝗪 𝗦𝗧𝗬𝗟𝗘')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            keyboard = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if user_id not in user_states:
            return
        
        state = user_states[user_id]
        step = state.get("step")
        
        if step == "waiting_for_admin_id":
            if user_id != self.owner_id:
                return
            text = update.message.text.strip()
            try:
                tid = int(text)
                if tid in admin_list:
                    admin_list.remove(tid)
                    self.save_admins()
                    await update.message.reply_text(f"{self.bi('✅ 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: ' + str(tid))}", parse_mode=ParseMode.MARKDOWN)
                else:
                    admin_list.add(tid)
                    self.save_admins()
                    await update.message.reply_text(f"{self.bi('✅ 𝗔𝗱𝗱𝗲𝗱: ' + str(tid))}", parse_mode=ParseMode.MARKDOWN)
            except:
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱')}", parse_mode=ParseMode.MARKDOWN)
            return
        
        if step == "waiting_for_delete_group":
            text = update.message.text.strip()
            try:
                chat_id = int(text) if re.match(r'^-?\d+$', text) else text
                await update.message.reply_text(
                    f"""
{self.bi('🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗥𝗘𝗤𝗨𝗘𝗦𝗧 🗑')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + str(chat_id))}
{self.bi('⚠ 𝗕𝗼𝘁 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('💡 𝗕𝗼𝘁 𝗰𝗮𝗻 𝗱𝗲𝗹𝗲𝘁𝗲 𝗿𝗲𝗰𝗲𝗻𝘁 𝗺𝘀𝗴')}
""",
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱')}", parse_mode=ParseMode.MARKDOWN)
            if user_id in user_states:
                del user_states[user_id]
            return
        
        if step in ["waiting_for_group_manual", "waiting_for_group"]:
            text = update.message.text
            chat_id = self.parse_chat_id(text)
            
            if chat_id:
                try:
                    gname = await self.get_chat_info(context, chat_id)
                except:
                    gname = str(chat_id)
                
                saved_groups[str(chat_id)] = {"name": gname, "id": str(chat_id)}
                self.save_groups()
                
                user_states[user_id].update({"chat_id": chat_id, "group_name": gname, "step": "waiting_for_type"})
                
                keyboard = [
                    [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="type_text"),
                     InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="type_bold")],
                    [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_italic"),
                     InlineKeyboardButton("𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="type_bold_italic")],
                    [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢𝗦𝗣𝗔𝗖𝗘", callback_data="type_mono")],
                    [InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", callback_data="type_sticker"),
                     InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢", callback_data="type_photo")],
                    [InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢", callback_data="type_video"),
                     InlineKeyboardButton("📄 𝗗𝗢𝗖", callback_data="type_document")],
                    [InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢", callback_data="type_audio"),
                     InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘", callback_data="type_voice")],
                    [InlineKeyboardButton("📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘", callback_data="type_video_note")],
                    [InlineKeyboardButton("🔙 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗙𝗢𝗨𝗡𝗗 ✅')}
{self.bi('📌 ' + gname)}
{self.bi('🆔 ' + str(chat_id))}

{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘 🎯')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                keyboard = [[InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗", callback_data="saved_groups_menu"), InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_types")]]
            await update.message.reply_text(f"{self.bi('✅ 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗢𝗞')}\n{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬?')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            return
        
        if step == "waiting_for_count":
            try:
                count = int(update.message.text)
                count = max(1, min(count, 1000))
                user_states[user_id]["count"] = count
                user_states[user_id]["step"] = "waiting_for_speed"
                
                keyboard = [
                    [InlineKeyboardButton("⚡ 𝗨𝗟𝗧𝗥𝗔 (𝟬.𝟱𝘀)", callback_data="speed_ultra"),
                     InlineKeyboardButton("🚀 𝗙𝗔𝗦𝗧 (𝟭𝘀)", callback_data="speed_fast")],
                    [InlineKeyboardButton("🐢 𝗡𝗢𝗥𝗠𝗔𝗟 (𝟮𝘀)", callback_data="speed_normal"),
                     InlineKeyboardButton("🦥 𝗦𝗟𝗢𝗪 (𝟱𝘀)", callback_data="speed_slow")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_count")]
                ]
                
                await update.message.reply_text(
                    f"{self.bi('⚡ 𝗦𝗣𝗘𝗘𝗗')}\n{self.bi('🔢 ' + str(count))}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                keyboard = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_types")]]
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗')}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
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
        gname = data.get("group_name", str(chat_id))
        count = data.get("count", 1)
        delay = data.get("delay", 1.0)
        msg_type = data.get("msg_type", "text")
        content = data.get("content")
        
        try:
            await query.delete_message()
        except:
            pass
        
        status_msg = await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"""
{self.bi('🔥 𝗦𝗣𝗔𝗠 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 🔥')}
{self.bi('📌 ' + gname)}
{self.bi('🎯 ' + msg_type + ' | 🔢 ' + str(count) + ' | ⚡ ' + str(delay) + 's')}
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        error_msg = None
        sent_message_ids = []
        
        for i in range(count):
            try:
                sent_msg = None
                
                if msg_type == "text":
                    txt = content.text if content and content.text else "Premium Spam"
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=txt)
                
                elif msg_type == "bold":
                    txt = content.text if content and content.text else "Premium Spam"
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=self.make_bold(txt))
                
                elif msg_type == "italic":
                    txt = content.text if content and content.text else "Premium Spam"
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=self.make_italic(txt))
                
                elif msg_type == "bold_italic":
                    txt = content.text if content and content.text else "Premium Spam"
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=self.make_bold_italic(txt))
                
                elif msg_type == "mono":
                    txt = content.text if content and content.text else "Premium Spam"
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=self.make_monospace(txt))
                
                elif msg_type == "sticker":
                    if content and content.sticker:
                        sent_msg = await context.bot.send_sticker(chat_id=chat_id, sticker=content.sticker.file_id)
                    else:
                        failed += 1
                        break
                
                elif msg_type == "photo":
                    if content and content.photo:
                        sent_msg = await context.bot.send_photo(chat_id=chat_id, photo=content.photo[-1].file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        break
                
                elif msg_type == "video":
                    if content and content.video:
                        sent_msg = await context.bot.send_video(chat_id=chat_id, video=content.video.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        break
                
                elif msg_type == "document":
                    if content and content.document:
                        sent_msg = await context.bot.send_document(chat_id=chat_id, document=content.document.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        break
                
                elif msg_type == "audio":
                    if content and content.audio:
                        sent_msg = await context.bot.send_audio(chat_id=chat_id, audio=content.audio.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        break
                
                elif msg_type == "voice":
                    if content and content.voice:
                        sent_msg = await context.bot.send_voice(chat_id=chat_id, voice=content.voice.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        break
                
                elif msg_type == "video_note":
                    if content and content.video_note:
                        sent_msg = await context.bot.send_video_note(chat_id=chat_id, video_note=content.video_note.file_id)
                    else:
                        failed += 1
                        break
                
                else:
                    failed += 1
                    break
                
                if sent_msg:
                    sent_message_ids.append(sent_msg.message_id)
                    success += 1
                
                if success % 5 == 0:
                    try:
                        await status_msg.edit_text(
                            f"{self.bi('⚡ ' + str(success) + '/' + str(count))}",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                error_str = str(e).lower()
                if "not enough rights" in error_str:
                    error_msg = "Need ADMIN"
                    break
                elif "forbidden" in error_str:
                    error_msg = "Bot not in group"
                    break
                elif "not found" in error_str:
                    error_msg = "Group not found"
                    break
                else:
                    error_msg = str(e)[:100]
                if failed > 2:
                    break
        
        # Save sent messages for delete option
        if success > 0:
            last_spam_messages[user_id] = {
                "chat_id": chat_id,
                "message_ids": sent_message_ids,
                "group_name": gname
            }
        
        try:
            await status_msg.delete()
        except:
            pass
        
        result = f"""
{self.bi('✅ 𝗠𝗜𝗦𝗦𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('📌 ' + gname)}
{self.bi('✅ ' + str(success) + ' | ❌ ' + str(failed))}
"""
        if error_msg and success == 0:
            result += f"{self.bi('⚠ ' + error_msg)}\n"
        
        result += f"""
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('👇 𝗪𝗛𝗔𝗧 𝗡𝗘𝗫𝗧? 👇')}
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 𝗥𝗘𝗦𝗘𝗡𝗗", callback_data="resend_same"),
             InlineKeyboardButton("🆕 𝗡𝗘𝗪", callback_data="new_spam")],
            [InlineKeyboardButton("🔀 𝗦𝗧𝗬𝗟𝗘", callback_data="change_type")]
        ]
        
        if success > 0:
            keyboard.append([InlineKeyboardButton("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗡𝗧 𝗠𝗦𝗚 🗑", callback_data="delete_last_spam")])
        
        keyboard.append([InlineKeyboardButton("🔙 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", callback_data="main_menu")])
        
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=result,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("BOT_TOKEN not set")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    bot = PremiumGroupSpamBot()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("GetId", bot.getid_command))
    app.add_handler(CommandHandler("deleteall", bot.deleteall_command))
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
║   5 TEXT STYLES ACTIVE              ║
║   DELETE SENT MSG ACTIVE            ║
║   Owner: @{OWNER_USERNAME}         ║
╚══════════════════════════════════════╝
    """)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
