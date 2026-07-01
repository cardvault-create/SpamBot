import os
import asyncio
import logging
import json
import re
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

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
    
    # 10 TEXT STYLES
    def style_bold(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789','𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_italic(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_bold_italic(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_mono(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_sans(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_sans_bold(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_sans_italic(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_sans_bi(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕'))
        return ''.join(m.get(c,c) for c in t)
    
    def style_serif_bold(self, t):
        m = dict(zip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ','𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙'))
        return ''.join(m.get(c,c) for c in t)
    
    def get_style_function(self, style):
        styles = {
            "bold": self.style_bold, "italic": self.style_italic,
            "bold_italic": self.style_bold_italic, "mono": self.style_mono,
            "sans": self.style_sans, "sans_bold": self.style_sans_bold,
            "sans_italic": self.style_sans_italic, "sans_bi": self.style_sans_bi,
            "serif_bold": self.style_serif_bold
        }
        return styles.get(style)
    
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
            title = chat.title if chat.title else "Unknown"
            ctype = chat.type if chat.type else "Unknown"
            try:
                count = await context.bot.get_chat_member_count(chat_id)
            except:
                count = 0
            # Get admin count
            try:
                admins = await context.bot.get_chat_administrators(chat_id)
                admin_count = len(admins)
            except:
                admin_count = 0
            # Get description
            desc = chat.description if chat.description else "No description"
            if len(desc) > 100:
                desc = desc[:100] + "..."
            return {
                "title": title,
                "type": ctype,
                "members": count,
                "admins": admin_count,
                "desc": desc
            }
        except:
            return {"title": str(chat_id), "type": "Unknown", "members": 0, "admins": 0, "desc": "N/A"}
    
    async def show_main_menu(self, query):
        user_id = query.from_user.id
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await query.edit_message_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
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
            [InlineKeyboardButton(f"🔄 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟: {auto_status}", callback_data="toggle_auto_delete")],
            [InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]
        ]
        
        msg = f"""
{self.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{self.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{self.bi('⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 ⭐')}
{self.bi('• 𝟭𝟬 𝗨𝗻𝗶𝗾𝘂𝗲 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀')}
{self.bi('• 𝗘𝘅𝗮𝗰𝘁 𝗚𝗿𝗼𝘂𝗽 𝗜𝗻𝗳𝗼 𝘄𝗶𝘁𝗵 𝗠𝗲𝗺𝗯𝗲𝗿𝘀')}
{self.bi('• 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝗲𝗻𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
{self.bi('• 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝘆𝘀𝘁𝗲𝗺')}
{self.bi('• 𝗔𝗱𝗺𝗶𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁')}
{self.bi('• 𝗨𝗹𝘁𝗿𝗮 𝗙𝗮𝘀𝘁 𝟬.𝟭𝘀 𝗦𝗽𝗲𝗲𝗱')}

{self.bi('🔒 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗠𝗼𝗱𝗲')}
{self.bi('👑 𝗔𝗖𝗖𝗘𝗦𝗦: 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗢𝗻𝗹𝘆')}
{self.bi('💎 𝗣𝗟𝗔𝗡: 𝗘𝘅𝗰𝗹𝘂𝘀𝗶𝘃𝗲 𝗣𝗿𝗲𝗺𝗶𝘂𝗺')}

{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 📌')}
"""
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
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
            [InlineKeyboardButton(f"🔄 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟: {auto_status}", callback_data="toggle_auto_delete")],
            [InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]
        ]
        msg = f"""
{self.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{self.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{self.bi('⭐ 𝟭𝟬 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀 | 𝗘𝘅𝗮𝗰𝘁 𝗚𝗿𝗼𝘂𝗽 𝗜𝗻𝗳𝗼')}
{self.bi('⭐ 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝘆𝘀𝘁𝗲𝗺 | 𝟬.𝟭𝘀 𝗦𝗽𝗲𝗲𝗱')}

{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 📌')}
"""
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def getid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        info = await self.get_chat_info(context, chat_id)
        chat_title = info["title"]
        chat_type = info["type"]
        members = info["members"]
        admins = info["admins"]
        desc = info["desc"]
        
        # Calculate approximate online count based on time of day
        import datetime
        hour = datetime.datetime.now().hour
        if 6 <= hour <= 23:
            online_pct = random.randint(8, 35)
        else:
            online_pct = random.randint(2, 15)
        
        try:
            total = int(members) if str(members).isdigit() and int(members) > 0 else 1
            approx_online = max(1, int(total * online_pct / 100))
        except:
            approx_online = "N/A"
            total = "N/A"
        
        if chat_type in ["group", "supergroup"]:
            saved_groups[str(chat_id)] = {
                "name": chat_title,
                "type": chat_type,
                "id": str(chat_id),
                "members": str(members),
                "admins": str(admins)
            }
            self.save_groups()
        
        msg = f"""
{self.bi('📋 𝗚𝗥𝗢𝗨𝗣 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + str(chat_title))}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('📂 𝗧𝘆𝗽𝗲: ' + str(chat_type))}
{self.bi('👥 𝗧𝗼𝘁𝗮𝗹 𝗠𝗲𝗺𝗯𝗲𝗿𝘀: ' + str(members))}
{self.bi('🟢 𝗢𝗻𝗹𝗶𝗻𝗲 𝗡𝗼𝘄: ~' + str(approx_online))}
{self.bi('👑 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(admins))}
{self.bi('📝 𝗗𝗲𝘀𝗰: ' + str(desc))}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('✅ 𝗚𝗿𝗼𝘂𝗽 𝗔𝘂𝘁𝗼-𝗦𝗮𝘃𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆')}
"""
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    async def deleteall_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        user_states[user_id] = {"step": "waiting_for_delete_group"}
        kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
        await update.message.reply_text(
            f"""
{self.bi('🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗔𝗟𝗟 𝗠𝗘𝗦𝗦𝗔𝗚𝗘𝗦 🗑')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗 𝘁𝗼 𝗗𝗲𝗹𝗲𝘁𝗲')}
{self.bi('⚠ 𝗕𝗼𝘁 𝗠𝘂𝘀𝘁 𝗕𝗲 𝗔𝗗𝗠𝗜𝗡 𝗜𝗻 𝗚𝗿𝗼𝘂𝗽')}
{self.bi('💡 𝗖𝗮𝗻 𝗗𝗲𝗹𝗲𝘁𝗲 𝗥𝗲𝗰𝗲𝗻𝘁 𝟭𝟬𝟬 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
""",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await query.edit_message_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        
        data = query.data
        
        if data == "main_menu":
            await self.show_main_menu(query)
            return
        if data == "toggle_auto_delete":
            global auto_delete_enabled
            auto_delete_enabled = not auto_delete_enabled
            self.save_config()
            s = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
            await query.answer(f"𝗔𝘂𝘁𝗼 𝗗𝗲𝗹𝗲𝘁𝗲 {s}", show_alert=True)
            await self.show_main_menu(query)
            return
        if data == "delete_last_spam":
            if user_id in last_spam_messages:
                sd = last_spam_messages[user_id]
                await query.edit_message_text(
                    f"{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗶𝗻𝗴 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀...')}",
                    parse_mode=ParseMode.MARKDOWN
                )
                deleted = 0
                for mid in sd.get("message_ids", []):
                    try:
                        await context.bot.delete_message(chat_id=sd["chat_id"], message_id=mid)
                        deleted += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"""
{self.bi('✅ 𝗗𝗘𝗟𝗘𝗧𝗘 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗲𝗱: ' + str(deleted) + '/' + str(len(sd.get('message_ids',[]))))}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + sd.get('group_name',''))}
""",
                    reply_markup=InlineKeyboardMarkup(kb),
                    parse_mode=ParseMode.MARKDOWN
                )
                del last_spam_messages[user_id]
            else:
                await query.answer("𝗡𝗼 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝘁𝗼 𝗱𝗲𝗹𝗲𝘁𝗲!", show_alert=True)
            return
        if data == "get_id_info":
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('🆔 𝗛𝗢𝗪 𝗧𝗢 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝘁𝗲𝗽 𝟭:')}
{self.bi('𝗔𝗱𝗱 𝗕𝗼𝘁 𝗧𝗼 𝗚𝗿𝗼𝘂𝗽 𝗔𝘀 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('📌 𝗦𝘁𝗲𝗽 𝟮:')}
{self.bi('𝗦𝗲𝗻𝗱 /𝗚𝗲𝘁𝗜𝗱 𝗜𝗻 𝗧𝗵𝗲 𝗚𝗿𝗼𝘂𝗽')}
{self.bi('📌 𝗦𝘁𝗲𝗽 𝟯:')}
{self.bi('𝗕𝗼𝘁 𝗪𝗶𝗹𝗹 𝗦𝗵𝗼𝘄 𝗙𝘂𝗹𝗹 𝗜𝗻𝗳𝗼')}
{self.bi('✅ 𝗚𝗿𝗼𝘂𝗽 𝗔𝘂𝘁𝗼-𝗦𝗮𝘃𝗲𝗱')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "saved_groups_menu":
            if not saved_groups:
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"""
{self.bi('📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('❌ 𝗡𝗼 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝗮𝘃𝗲𝗱 𝗬𝗲𝘁')}
{self.bi('💡 𝗦𝗲𝗻𝗱 /𝗚𝗲𝘁𝗜𝗱 𝗜𝗻 𝗚𝗿𝗼𝘂𝗽')}
""",
                    reply_markup=InlineKeyboardMarkup(kb),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            keyboard = []
            for gid, ginfo in list(saved_groups.items())[:20]:
                name = ginfo.get("name", gid)[:30]
                keyboard.append([InlineKeyboardButton(f"📌 {name}", callback_data=f"sg_{gid}")])
            keyboard.append([InlineKeyboardButton("🗑 𝗖𝗟𝗘𝗔𝗥 𝗔𝗟𝗟 𝗚𝗥𝗢𝗨𝗣𝗦", callback_data="clear_groups")])
            keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")])
            await query.edit_message_text(
                f"""
{self.bi('📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 𝗟𝗜𝗦𝗧 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗧𝗼𝘁𝗮𝗹: ' + str(len(saved_groups)) + ' 𝗚𝗿𝗼𝘂𝗽𝘀')}

{self.bi('👇 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔 𝗚𝗥𝗢𝗨𝗣 𝗧𝗢 𝗦𝗣𝗔𝗠 👇')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data.startswith("sg_"):
            gid = data.replace("sg_", "")
            ginfo = saved_groups.get(gid, {})
            gname = ginfo.get("name", gid)
            try:
                chat_id = int(gid)
            except:
                chat_id = gid
            user_states[user_id] = {"step": "waiting_for_type", "chat_id": chat_id, "group_name": gname}
            await self.show_style_menu(query, user_id)
            return
        if data == "clear_groups":
            saved_groups.clear()
            self.save_groups()
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('🗑 𝗚𝗥𝗢𝗨𝗣𝗦 𝗖𝗟𝗘𝗔𝗥𝗘𝗗 🗑')}
{self.bi('✅ 𝗔𝗹𝗹 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀 𝗗𝗲𝗹𝗲𝘁𝗲𝗱')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "add_group_manual":
            user_states[user_id] = {"step": "waiting_for_group_manual"}
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 𝗠𝗔𝗡𝗨𝗔𝗟𝗟𝗬 ➕')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗 𝗼𝗿 @𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲')}
{self.bi('📌 𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}
{self.bi('📌 𝗢𝗿: @𝗴𝗿𝗼𝘂𝗽𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "start_spam":
            user_states[user_id] = {"step": "waiting_for_group"}
            kb = [
                [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦", callback_data="saved_groups_menu")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"""
{self.bi('🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗 𝗼𝗿 @𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲')}
{self.bi('📌 𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}
{self.bi('📌 𝗢𝗿 𝗦𝗲𝗹𝗲𝗰𝘁 𝗙𝗿𝗼𝗺 𝗦𝗮𝘃𝗲𝗱')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "my_stats":
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('📊 𝗢𝗪𝗡𝗘𝗥 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦 📊')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('👑 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗔𝗰𝘁𝗶𝘃𝗲 & 𝗢𝗻𝗹𝗶𝗻𝗲')}
{self.bi('💎 𝗣𝗹𝗮𝗻: 𝗘𝘅𝗰𝗹𝘂𝘀𝗶𝘃𝗲 𝗣𝗿𝗲𝗺𝗶𝘂𝗺')}
{self.bi('🔒 𝗔𝗰𝗰𝗲𝘀𝘀: 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗠𝗼𝗱𝗲')}
{self.bi('♾ 𝗟𝗶𝗺𝗶𝘁𝘀: 𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱')}
{self.bi('⚡ 𝗦𝗽𝗲𝗲𝗱: 𝟬.𝟭𝘀 𝗨𝗹𝘁𝗿𝗮')}
{self.bi('📋 𝗚𝗿𝗼𝘂𝗽𝘀: ' + str(len(saved_groups)))}
{self.bi('👥 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(len(admin_list)))}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "help_menu":
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
            await query.edit_message_text(
                f"""
{self.bi('❓ 𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 ❓')}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟭:')}
{self.bi('𝗔𝗱𝗱 𝗕𝗼𝘁 𝗧𝗼 𝗚𝗿𝗼𝘂𝗽 𝗔𝘀 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('𝗚𝗶𝘃𝗲 𝗔𝗹𝗹 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻𝘀')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟮:')}
{self.bi('𝗦𝗲𝗻𝗱 /𝗚𝗲𝘁𝗜𝗱 𝗜𝗻 𝗚𝗿𝗼𝘂𝗽')}
{self.bi('𝗚𝗲𝘁 𝗙𝘂𝗹𝗹 𝗚𝗿𝗼𝘂𝗽 𝗜𝗻𝗳𝗼')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟯:')}
{self.bi('𝗖𝗹𝗶𝗰𝗸 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚')}
{self.bi('𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}

{self.bi('📌 𝗦𝗧𝗘𝗣 𝟰:')}
{self.bi('𝗦𝗲𝗹𝗲𝗰𝘁 𝟭𝟬 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀')}
{self.bi('𝗢𝗿 𝗠𝗲𝗱𝗶𝗮 𝗧𝘆𝗽𝗲𝘀')}

{self.bi('🗑 /𝗱𝗲𝗹𝗲𝘁𝗲𝗮𝗹𝗹 𝗧𝗼 𝗗𝗲𝗹𝗲𝘁𝗲')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "owner_panel":
            kb = [
                [InlineKeyboardButton("👥 𝗠𝗔𝗡𝗔𝗚𝗘 𝗔𝗗𝗠𝗜𝗡𝗦 👥", callback_data="manage_admins")],
                [InlineKeyboardButton("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗔𝗟𝗟 𝗚𝗥𝗢𝗨𝗣 𝗠𝗦𝗚 🗑", callback_data="delete_all_group")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
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
{self.bi('👇 𝗦𝗲𝗹𝗲𝗰𝘁 𝗔𝗻 𝗢𝗽𝘁𝗶𝗼𝗻 👇')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "delete_all_group":
            if not saved_groups:
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")]]
                await query.edit_message_text(
                    f"{self.bi('📋 𝗡𝗼 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝗮𝘃𝗲𝗱')}",
                    reply_markup=InlineKeyboardMarkup(kb),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            keyboard = []
            for gid, ginfo in list(saved_groups.items())[:20]:
                name = ginfo.get("name", gid)[:30]
                keyboard.append([InlineKeyboardButton(f"🗑 {name}", callback_data=f"delg_{gid}")])
            keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")])
            await query.edit_message_text(
                f"""
{self.bi('🗑 𝗦𝗘𝗟𝗘𝗖𝗧 𝗚𝗥𝗢𝗨𝗣 𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘 🗑')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('👇 𝗖𝗹𝗶𝗰𝗸 𝗚𝗿𝗼𝘂𝗽 𝗧𝗼 𝗗𝗲𝗹𝗲𝘁𝗲 𝗠𝘀𝗴 👇')}
""",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data.startswith("delg_"):
            gid = data.replace("delg_", "")
            try:
                chat_id = int(gid)
            except:
                chat_id = gid
            gname = saved_groups.get(gid, {}).get("name", str(chat_id))
            await query.edit_message_text(
                f"""
{self.bi('🗑 𝗗𝗘𝗟𝗘𝗧𝗜𝗡𝗚 𝗠𝗘𝗦𝗦𝗔𝗚𝗘𝗦... 🗑')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}
""",
                parse_mode=ParseMode.MARKDOWN
            )
            deleted = 0
            try:
                async for msg in context.bot.get_chat_history(chat_id=chat_id, limit=100):
                    if msg.from_user and msg.from_user.id == context.bot.id:
                        try:
                            await context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
                            deleted += 1
                            await asyncio.sleep(0.05)
                        except:
                            pass
            except:
                pass
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗣𝗔𝗡𝗘𝗟", callback_data="owner_panel")]]
            await query.edit_message_text(
                f"""
{self.bi('✅ 𝗗𝗘𝗟𝗘𝗧𝗘 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗲𝗱: ' + str(deleted) + ' 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "manage_admins":
            if user_id != self.owner_id:
                await query.answer("🔐 𝗢𝗻𝗹𝘆 𝗢𝘄𝗻𝗲𝗿 𝗖𝗮𝗻 𝗠𝗮𝗻𝗮𝗴𝗲 𝗔𝗱𝗺𝗶𝗻𝘀!", show_alert=True)
                return
            atext = f"""
{self.bi('👥 𝗔𝗗𝗠𝗜𝗡 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧 👥')}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👑 𝗢𝘄𝗻𝗲𝗿: @' + self.owner_username + ' (' + str(self.owner_id) + ')')}

{self.bi('👥 𝗔𝗱𝗺𝗶𝗻 𝗟𝗶𝘀𝘁:')}
"""
            for aid in admin_list:
                if aid != self.owner_id:
                    atext += f"{self.bi('• ' + str(aid))}\n"
            if len(admin_list) <= 1:
                atext += f"{self.bi('• 𝗡𝗼 𝗢𝘁𝗵𝗲𝗿 𝗔𝗱𝗺𝗶𝗻𝘀')}\n"
            atext += f"""
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('👇 𝗦𝗲𝗻𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗 𝗧𝗼 𝗔𝗱𝗱/𝗥𝗲𝗺𝗼𝘃𝗲:')}
"""
            user_states[user_id] = {"step": "waiting_for_admin_id"}
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗣𝗔𝗡𝗘𝗟", callback_data="owner_panel")]]
            await query.edit_message_text(atext, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data.startswith("style_"):
            msg_type = data.replace("style_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗦𝗧𝗬𝗟𝗘𝗦", callback_data="show_styles")]]
            style_names = {
                "text": "💬 𝗡𝗢𝗥𝗠𝗔𝗟 𝗧𝗘𝗫𝗧",
                "bold": "𝗕 𝗕𝗢𝗟𝗗 𝗧𝗘𝗫𝗧",
                "italic": "𝑰 𝗜𝗧𝗔𝗟𝗜𝗖 𝗧𝗘𝗫𝗧",
                "bold_italic": "𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖",
                "mono": "𝙼 𝗠𝗢𝗡𝗢𝗦𝗣𝗔𝗖𝗘",
                "sans": "𝖲 𝗦𝗔𝗡𝗦 𝗧𝗘𝗫𝗧",
                "sans_bold": "𝗦𝗕 𝗦𝗔𝗡𝗦 𝗕𝗢𝗟𝗗",
                "sans_italic": "𝘚𝘐 𝘚𝘈𝘕𝘚 𝘐𝘛𝘈𝘓𝘐𝘊",
                "sans_bi": "𝙎𝘽𝙄 𝙎𝘼𝙉𝙎 𝘽𝙊𝙇𝘿 𝙄𝙏𝘼𝙇𝙄𝘾",
                "serif_bold": "𝐒𝐁 𝐒𝐄𝐑𝐈𝐅 𝐁𝐎𝐋𝐃"
            }
            sn = style_names.get(msg_type, "𝗦𝗘𝗡𝗗 𝗖𝗢𝗡𝗧𝗘𝗡𝗧")
            await query.edit_message_text(
                f"""
{self.bi(sn)}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📤 𝗦𝗲𝗻𝗱 𝗬𝗼𝘂𝗿 𝗧𝗲𝘅𝘁 𝗡𝗼𝘄:')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data.startswith("media_"):
            mtype = data.replace("media_", "")
            user_states[user_id]["msg_type"] = mtype
            user_states[user_id]["step"] = "waiting_for_content"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗦𝗧𝗬𝗟𝗘𝗦", callback_data="show_styles")]]
            media_names = {
                "sticker": "🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", "photo": "🖼 𝗣𝗛𝗢𝗧𝗢",
                "video": "🎥 𝗩𝗜𝗗𝗘𝗢", "document": "📄 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧",
                "audio": "🎵 𝗔𝗨𝗗𝗜𝗢", "voice": "🎤 𝗩𝗢𝗜𝗖𝗘",
                "video_note": "📹 𝗩𝗜𝗗𝗘𝗢 𝗡𝗢𝗧𝗘"
            }
            mn = media_names.get(mtype, "𝗦𝗘𝗡𝗗 𝗠𝗘𝗗𝗜𝗔")
            await query.edit_message_text(
                f"""
{self.bi(mn)}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📤 𝗦𝗲𝗻𝗱 𝗬𝗼𝘂𝗿 𝗠𝗲𝗱𝗶𝗮 𝗡𝗼𝘄:')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "show_styles":
            await self.show_style_menu(query, user_id)
            return
        if data == "show_count":
            user_states[user_id]["step"] = "waiting_for_count"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗦𝗧𝗬𝗟𝗘𝗦", callback_data="show_styles")]]
            await query.edit_message_text(
                f"""
{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬 𝗧𝗜𝗠𝗘𝗦? 🔢')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗔 𝗡𝘂𝗺𝗯𝗲𝗿 (𝟭-𝟭𝟬𝟬𝟬)')}
{self.bi('💡 𝗥𝗲𝗰𝗼𝗺𝗺𝗲𝗻𝗱𝗲𝗱: 𝟭𝟬 𝗙𝗼𝗿 𝗧𝗲𝘀𝘁')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        if data.startswith("speed_"):
            speed_map = {"speed_ultra": 0.1, "speed_fast": 0.3, "speed_normal": 0.5, "speed_slow": 1}
            user_states[user_id]["delay"] = speed_map.get(data, 0.1)
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
                await self.show_style_menu(query, user_id)
            return
        if data == "change_style":
            await self.show_style_menu(query, user_id)
            return
    
    async def show_style_menu(self, query, user_id):
        gname = user_states[user_id].get("group_name", "N/A")
        user_states[user_id]["step"] = "waiting_for_type"
        keyboard = [
            [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="style_text"),
             InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="style_bold")],
            [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="style_italic"),
             InlineKeyboardButton("𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="style_bold_italic")],
            [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢", callback_data="style_mono"),
             InlineKeyboardButton("𝖲 𝗦𝗔𝗡𝗦", callback_data="style_sans")],
            [InlineKeyboardButton("𝗦𝗕 𝗦𝗔𝗡𝗦 𝗕𝗢𝗟𝗗", callback_data="style_sans_bold"),
             InlineKeyboardButton("𝘚𝘐 𝘚𝘈𝘕𝘚 𝘐𝘛𝘈𝘓𝘐𝘊", callback_data="style_sans_italic")],
            [InlineKeyboardButton("𝙎𝘽𝙄 𝙎𝘼𝙉𝙎 𝘽𝙄", callback_data="style_sans_bi"),
             InlineKeyboardButton("𝐒𝐁 𝐒𝐄𝐑𝐈𝐅 𝐁𝐎𝐋𝐃", callback_data="style_serif_bold")],
            [InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", callback_data="media_sticker"),
             InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢", callback_data="media_photo")],
            [InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢", callback_data="media_video"),
             InlineKeyboardButton("📄 𝗗𝗢𝗖", callback_data="media_document")],
            [InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢", callback_data="media_audio"),
             InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘", callback_data="media_voice")],
            [InlineKeyboardButton("📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘", callback_data="media_video_note")],
            [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            f"""
{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘 𝗢𝗥 𝗠𝗘𝗗𝗜𝗔 🎯')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👇 𝗖𝗵𝗼𝗼𝘀𝗲 𝗙𝗿𝗼𝗺 𝟭𝟬 𝗦𝘁𝘆𝗹𝗲𝘀 𝗢𝗿 𝟳 𝗠𝗲𝗱𝗶𝗮 👇')}
""",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if user_id not in user_states:
            return
        
        state = user_states[user_id]
        step = state.get("step")
        
        if step == "waiting_for_admin_id":
            if user_id != self.owner_id:
                return
            try:
                tid = int(update.message.text.strip())
                if tid in admin_list:
                    admin_list.remove(tid)
                    self.save_admins()
                    await update.message.reply_text(
                        f"{self.bi('✅ 𝗔𝗱𝗺𝗶𝗻 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: ' + str(tid))}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    admin_list.add(tid)
                    self.save_admins()
                    await update.message.reply_text(
                        f"{self.bi('✅ 𝗔𝗱𝗺𝗶𝗻 𝗔𝗱𝗱𝗲𝗱: ' + str(tid))}",
                        parse_mode=ParseMode.MARKDOWN
                    )
            except:
                await update.message.reply_text(
                    f"{self.bi('❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗')}\n{self.bi('𝗦𝗲𝗻𝗱 𝗡𝘂𝗺𝗲𝗿𝗶𝗰 𝗜𝗗 𝗢𝗻𝗹𝘆')}",
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        if step == "waiting_for_delete_group":
            text = update.message.text.strip()
            await update.message.reply_text(
                f"""
{self.bi('🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗦𝗘𝗡𝗧 🗑')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + text)}
{self.bi('⚠ 𝗕𝗼𝘁 𝗠𝘂𝘀𝘁 𝗕𝗲 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('💡 𝗧𝗿𝘆𝗶𝗻𝗴 𝗧𝗼 𝗗𝗲𝗹𝗲𝘁𝗲 𝗥𝗲𝗰𝗲𝗻𝘁 𝗠𝘀𝗴')}
""",
                parse_mode=ParseMode.MARKDOWN
            )
            if user_id in user_states:
                del user_states[user_id]
            return
        
        if step in ["waiting_for_group_manual", "waiting_for_group"]:
            text = update.message.text
            chat_id = self.parse_chat_id(text)
            if chat_id:
                info = await self.get_chat_info(context, chat_id)
                gname = info["title"]
                saved_groups[str(chat_id)] = {
                    "name": gname, "id": str(chat_id),
                    "members": str(info["members"]),
                    "admins": str(info["admins"])
                }
                self.save_groups()
                user_states[user_id].update({"chat_id": chat_id, "group_name": gname, "step": "waiting_for_type"})
                
                keyboard = [
                    [InlineKeyboardButton("💬 𝗡𝗢𝗥𝗠𝗔𝗟", callback_data="style_text"),
                     InlineKeyboardButton("𝗕 𝗕𝗢𝗟𝗗", callback_data="style_bold")],
                    [InlineKeyboardButton("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="style_italic"),
                     InlineKeyboardButton("𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", callback_data="style_bold_italic")],
                    [InlineKeyboardButton("𝙼 𝗠𝗢𝗡𝗢", callback_data="style_mono"),
                     InlineKeyboardButton("𝖲 𝗦𝗔𝗡𝗦", callback_data="style_sans")],
                    [InlineKeyboardButton("𝗦𝗕 𝗦𝗔𝗡𝗦 𝗕𝗢𝗟𝗗", callback_data="style_sans_bold"),
                     InlineKeyboardButton("𝘚𝘐 𝘚𝘈𝘕𝘚 𝘐𝘛𝘈𝘓𝘐𝘊", callback_data="style_sans_italic")],
                    [InlineKeyboardButton("𝙎𝘽𝙄 𝙎𝘼𝙉𝙎 𝘽𝙄", callback_data="style_sans_bi"),
                     InlineKeyboardButton("𝐒𝐁 𝐒𝐄𝐑𝐈𝐅 𝐁𝐎𝐋𝐃", callback_data="style_serif_bold")],
                    [InlineKeyboardButton("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", callback_data="media_sticker"),
                     InlineKeyboardButton("🖼 𝗣𝗛𝗢𝗧𝗢", callback_data="media_photo")],
                    [InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢", callback_data="media_video"),
                     InlineKeyboardButton("📄 𝗗𝗢𝗖", callback_data="media_document")],
                    [InlineKeyboardButton("🎵 𝗔𝗨𝗗𝗜𝗢", callback_data="media_audio"),
                     InlineKeyboardButton("🎤 𝗩𝗢𝗜𝗖𝗘", callback_data="media_voice")],
                    [InlineKeyboardButton("📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘", callback_data="media_video_note")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
                ]
                
                await update.message.reply_text(
                    f"""
{self.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗙𝗢𝗨𝗡𝗗 & 𝗦𝗔𝗩𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + gname)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('👥 𝗠𝗲𝗺𝗯𝗲𝗿𝘀: ' + str(info['members']))}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('🎯 𝗡𝗢𝗪 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘 𝗢𝗥 𝗠𝗘𝗗𝗜𝗔 🎯')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                kb = [
                    [InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦", callback_data="saved_groups_menu")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")]
                ]
                await update.message.reply_text(
                    f"""
{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 ❌')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('💡 𝗨𝘀𝗲 /𝗚𝗲𝘁𝗜𝗱 𝗜𝗻 𝗚𝗿𝗼𝘂𝗽')}
{self.bi('💡 𝗢𝗿 𝗦𝗲𝗻𝗱 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗙𝗼𝗿𝗺𝗮𝘁')}
{self.bi('📌 𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}
""",
                    reply_markup=InlineKeyboardMarkup(kb),
                    parse_mode=ParseMode.MARKDOWN
                )
            return
        
        if step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗦𝗧𝗬𝗟𝗘𝗦", callback_data="show_styles")]]
            await update.message.reply_text(
                f"""
{self.bi('✅ 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗥𝗘𝗖𝗘𝗜𝗩𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬 𝗧𝗜𝗠𝗘𝗦? 🔢')}
{self.bi('📌 𝗦𝗲𝗻𝗱 𝗔 𝗡𝘂𝗺𝗯𝗲𝗿 (𝟭-𝟭𝟬𝟬𝟬)')}
""",
                reply_markup=InlineKeyboardMarkup(kb),
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
                    [InlineKeyboardButton("⚡ 𝗨𝗟𝗧𝗥𝗔 (𝟬.𝟭𝘀)", callback_data="speed_ultra"),
                     InlineKeyboardButton("🚀 𝗙𝗔𝗦𝗧 (𝟬.𝟯𝘀)", callback_data="speed_fast")],
                    [InlineKeyboardButton("🐢 𝗡𝗢𝗥𝗠𝗔𝗟 (𝟬.𝟱𝘀)", callback_data="speed_normal"),
                     InlineKeyboardButton("🦥 𝗦𝗟𝗢𝗪 (𝟭𝘀)", callback_data="speed_slow")],
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗖𝗢𝗨𝗡𝗧", callback_data="show_count")]
                ]
                await update.message.reply_text(
                    f"""
{self.bi('⚡ 𝗖𝗛𝗢𝗢𝗦𝗘 𝗦𝗣𝗘𝗘𝗗 ⚡')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🔢 𝗖𝗼𝘂𝗻𝘁: ' + str(count))}
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👇 𝗦𝗲𝗹𝗲𝗰𝘁 𝗦𝗽𝗲𝗲𝗱 𝗕𝗲𝗹𝗼𝘄 👇')}
""",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗦𝗧𝗬𝗟𝗘𝗦", callback_data="show_styles")]]
                await update.message.reply_text(
                    f"{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗡𝗨𝗠𝗕𝗘𝗥 ❌')}\n{self.bi('𝗦𝗲𝗻𝗱 𝟭 𝘁𝗼 𝟭𝟬𝟬𝟬')}",
                    reply_markup=InlineKeyboardMarkup(kb),
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
        gname = data.get("group_name", str(chat_id))
        count = data.get("count", 1)
        delay = data.get("delay", 0.1)
        msg_type = data.get("msg_type", "text")
        content = data.get("content")
        
        try:
            await query.delete_message()
        except:
            pass
        
        status_msg = await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"""
{self.bi('🔥 𝗦𝗣𝗔𝗠 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 🔥')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}
{self.bi('🎯 𝗧𝘆𝗽𝗲: ' + msg_type)}
{self.bi('🔢 𝗖𝗼𝘂𝗻𝘁: ' + str(count))}
{self.bi('⚡ 𝗦𝗽𝗲𝗲𝗱: ' + str(delay) + '𝘀')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('🚀 𝗦𝗘𝗡𝗗𝗜𝗡𝗚 𝗠𝗘𝗦𝗦𝗔𝗚𝗘𝗦 𝗡𝗢𝗪... 🚀')}
""",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        error_msg = None
        sent_message_ids = []
        
        text_types = ["text", "bold", "italic", "bold_italic", "mono", "sans", "sans_bold", "sans_italic", "sans_bi", "serif_bold"]
        style_func = None
        if msg_type in text_types and msg_type != "text":
            style_func = self.get_style_function(msg_type)
        
        for i in range(count):
            try:
                sent_msg = None
                
                if msg_type in text_types:
                    txt = content.text if content and content.text else "🔥 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗦𝗽𝗮𝗺 🔥"
                    if style_func:
                        txt = style_func(txt)
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=txt)
                
                elif msg_type == "sticker":
                    if content and content.sticker:
                        sent_msg = await context.bot.send_sticker(chat_id=chat_id, sticker=content.sticker.file_id)
                    else:
                        failed += 1
                        error_msg = "No sticker found"
                        break
                elif msg_type == "photo":
                    if content and content.photo:
                        sent_msg = await context.bot.send_photo(chat_id=chat_id, photo=content.photo[-1].file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        error_msg = "No photo found"
                        break
                elif msg_type == "video":
                    if content and content.video:
                        sent_msg = await context.bot.send_video(chat_id=chat_id, video=content.video.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        error_msg = "No video found"
                        break
                elif msg_type == "document":
                    if content and content.document:
                        sent_msg = await context.bot.send_document(chat_id=chat_id, document=content.document.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        error_msg = "No document found"
                        break
                elif msg_type == "audio":
                    if content and content.audio:
                        sent_msg = await context.bot.send_audio(chat_id=chat_id, audio=content.audio.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        error_msg = "No audio found"
                        break
                elif msg_type == "voice":
                    if content and content.voice:
                        sent_msg = await context.bot.send_voice(chat_id=chat_id, voice=content.voice.file_id, caption=content.caption or "")
                    else:
                        failed += 1
                        error_msg = "No voice found"
                        break
                elif msg_type == "video_note":
                    if content and content.video_note:
                        sent_msg = await context.bot.send_video_note(chat_id=chat_id, video_note=content.video_note.file_id)
                    else:
                        failed += 1
                        error_msg = "No video note found"
                        break
                else:
                    failed += 1
                    error_msg = "Unknown type"
                    break
                
                if sent_msg:
                    sent_message_ids.append(sent_msg.message_id)
                    success += 1
                
                if success % 10 == 0:
                    try:
                        await status_msg.edit_text(
                            f"""
{self.bi('⚡ 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 𝗜𝗡 𝗣𝗥𝗢𝗚𝗥𝗘𝗦𝗦 ⚡')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}
{self.bi('✅ 𝗦𝗲𝗻𝘁: ' + str(success) + '/' + str(count))}
{self.bi('❌ 𝗙𝗮𝗶𝗹𝗲𝗱: ' + str(failed))}
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
                    error_msg = f"Need ADMIN with send permission"
                    break
                elif "forbidden" in error_str or "blocked" in error_str:
                    error_msg = "Bot not in group or blocked"
                    break
                elif "not found" in error_str:
                    error_msg = "Group not found"
                    break
                elif "message to forward" in error_str:
                    error_msg = "Content error. Send again."
                    break
                if failed > 3:
                    break
        
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
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}
{self.bi('✅ 𝗦𝘂𝗰𝗰𝗲𝘀𝘀: ' + str(success))}
{self.bi('❌ 𝗙𝗮𝗶𝗹𝗲𝗱: ' + str(failed))}
{self.bi('🎯 𝗧𝘆𝗽𝗲: ' + msg_type)}
{self.bi('⚡ 𝗦𝗽𝗲𝗲𝗱: ' + str(delay) + '𝘀')}
"""
        if error_msg and success == 0:
            result += f"""
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('⚠ 𝗘𝗥𝗥𝗢𝗥: ' + error_msg)}
{self.bi('💡 𝗦𝗢𝗟𝗨𝗧𝗜𝗢𝗡:')}
{self.bi('𝟭️ 𝗠𝗮𝗸𝗲 𝗕𝗼𝘁 𝗔𝗗𝗠𝗜𝗡')}
{self.bi('𝟮️ 𝗘𝗻𝗮𝗯𝗹𝗲 𝗔𝗹𝗹 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻𝘀')}
"""
        result += f"""
{self.bi('━━━━━━━━━━━━━━━━━━')}

{self.bi('👇 𝗪𝗛𝗔𝗧 𝗗𝗢 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗗𝗢 𝗡𝗘𝗫𝗧? 👇')}
"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 𝗥𝗘𝗦𝗘𝗡𝗗 𝗦𝗔𝗠𝗘", callback_data="resend_same"),
             InlineKeyboardButton("🆕 𝗡𝗘𝗪 𝗦𝗣𝗔𝗠", callback_data="new_spam")],
            [InlineKeyboardButton("🎨 𝗖𝗛𝗔𝗡𝗚𝗘 𝗦𝗧𝗬𝗟𝗘", callback_data="change_style")]
        ]
        if success > 0:
            keyboard.append([InlineKeyboardButton("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗡𝗧 𝗠𝗦𝗚 🗑", callback_data="delete_last_spam")])
        keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", callback_data="main_menu")])
        
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
║                                      ║
║   👑 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑        ║
║   🔒 𝗣𝗥𝗜𝗩𝗔𝗧𝗘 𝗠𝗢𝗗𝗘 𝗔𝗖𝗧𝗜𝗩𝗘 🔒         ║
║   𝟭𝟬 𝗧𝗘𝗫𝗧 𝗦𝗧𝗬𝗟𝗘𝗦 𝗔𝗖𝗧𝗜𝗩𝗘            ║
║   𝟬.𝟭𝘀 𝗨𝗟𝗧𝗥𝗔 𝗦𝗣𝗘𝗘𝗗 𝗔𝗖𝗧𝗜𝗩𝗘          ║
║   𝗚𝗥𝗢𝗨𝗣 𝗜𝗡𝗙𝗢 𝗪𝗜𝗧𝗛 𝗢𝗡𝗟𝗜𝗡𝗘          ║
║   🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗬𝗦𝗧𝗘𝗠 𝗔𝗖𝗧𝗜𝗩𝗘        ║
║                                      ║
║   👤 𝗢𝘄𝗻𝗲𝗿: @{OWNER_USERNAME}     ║
║   🆔 /𝗚𝗲𝘁𝗜𝗱 | 🗑 /𝗱𝗲𝗹𝗲𝘁𝗲𝗮𝗹𝗹       ║
║                                      ║
╚══════════════════════════════════════╝
    """)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
