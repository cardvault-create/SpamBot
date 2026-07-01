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
{self.bi('👑 𝗢𝘄𝗻𝗲𝗿: @' + self.owner_username)}
"""
    
    async def get_chat_info(self, context, chat_id):
        try:
            chat = await context.bot.get_chat(chat_id)
            title = chat.title if chat.title else "Unknown"
            ctype = chat.type if chat.type else "Unknown"
            # Get member count
            try:
                count = await context.bot.get_chat_member_count(chat_id)
            except:
                count = "N/A"
            return {"title": title, "type": ctype, "members": count}
        except:
            return {"title": str(chat_id), "type": "Unknown", "members": "N/A"}
    
    async def show_main_menu(self, query):
        user_id = query.from_user.id
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await query.edit_message_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if user_id in user_states:
            del user_states[user_id]
        
        auto_status = "✅ ON" if auto_delete_enabled else "❌ OFF"
        
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
{self.bi('⭐ 𝟭𝟬 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀 | 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝘆𝘀𝘁𝗲𝗺 | 𝗚𝗿𝗼𝘂𝗽 𝗜𝗻𝗳𝗼')}
{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗢𝗣𝗧𝗜𝗢𝗡 📌')}
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
        
        auto_status = "✅ ON" if auto_delete_enabled else "❌ OFF"
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
{self.bi('⭐ 𝟭𝟬 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀 | 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝘆𝘀𝘁𝗲𝗺')}
{self.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗢𝗣𝗧𝗜𝗢𝗡 📌')}
"""
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    
    async def getid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        info = await self.get_chat_info(context, chat_id)
        chat_title = info["title"]
        chat_type = info["type"]
        members = info["members"]
        
        if chat_type in ["group", "supergroup"]:
            saved_groups[str(chat_id)] = {"name": chat_title, "type": chat_type, "id": str(chat_id), "members": str(members)}
            self.save_groups()
        
        msg = f"""
{self.bi('📋 𝗚𝗥𝗢𝗨𝗣 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 📋')}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('📌 𝗡𝗮𝗺𝗲: ' + chat_title)}
{self.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{self.bi('📂 𝗧𝘆𝗽𝗲: ' + chat_type)}
{self.bi('👥 𝗠𝗲𝗺𝗯𝗲𝗿𝘀: ' + str(members))}
{self.bi('━━━━━━━━━━━━━━━━━━')}
{self.bi('✅ 𝗚𝗿𝗼𝘂𝗽 𝗔𝘂𝘁𝗼-𝗦𝗮𝘃𝗲𝗱')}
"""
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    
    async def deleteall_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            kb = [[InlineKeyboardButton("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", url=f"https://t.me/{self.owner_username}")]]
            await update.message.reply_text(self.block_msg(), reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        user_states[user_id] = {"step": "waiting_for_delete_group"}
        kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
        await update.message.reply_text(
            f"{self.bi('🗑 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗 𝘁𝗼 𝗱𝗲𝗹𝗲𝘁𝗲 🗑')}",
            reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
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
            await query.answer(f"Auto Delete {'ON' if auto_delete_enabled else 'OFF'}", show_alert=True)
            await self.show_main_menu(query)
            return
        if data == "delete_last_spam":
            if user_id in last_spam_messages:
                sd = last_spam_messages[user_id]
                await query.edit_message_text(f"{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗶𝗻𝗴...')}", parse_mode=ParseMode.MARKDOWN)
                deleted = 0
                for mid in sd.get("message_ids", []):
                    try:
                        await context.bot.delete_message(chat_id=sd["chat_id"], message_id=mid)
                        deleted += 1
                        await asyncio.sleep(0.05)
                    except:
                        pass
                kb = [[InlineKeyboardButton("🔙 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", callback_data="main_menu")]]
                await query.edit_message_text(
                    f"{self.bi('✅ 𝗗𝗲𝗹𝗲𝘁𝗲𝗱: ' + str(deleted) + '/' + str(len(sd.get('message_ids',[]))))}",
                    reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
                )
                del last_spam_messages[user_id]
            else:
                await query.answer("No messages to delete", show_alert=True)
            return
        if data == "get_id_info":
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"{self.bi('🆔 /GetId 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽 𝘁𝗼 𝗴𝗲𝘁 𝗜𝗗')}",
                reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "saved_groups_menu":
            if not saved_groups:
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
                await query.edit_message_text(f"{self.bi('📋 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽𝘀')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
                return
            keyboard = []
            for gid, ginfo in list(saved_groups.items())[:20]:
                name = ginfo.get("name", gid)[:30]
                keyboard.append([InlineKeyboardButton(f"📌 {name}", callback_data=f"sg_{gid}")])
            keyboard.append([InlineKeyboardButton("🗑 𝗖𝗟𝗘𝗔𝗥 𝗔𝗟𝗟", callback_data="clear_groups")])
            keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")])
            await query.edit_message_text(
                f"{self.bi('📋 𝗚𝗥𝗢𝗨𝗣𝗦 (' + str(len(saved_groups)) + ')')}\n{self.bi('👇 𝗦𝗘𝗟𝗘𝗖𝗧')}",
                reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN
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
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(f"{self.bi('🗑 𝗖𝗟𝗘𝗔𝗥𝗘𝗗')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data == "add_group_manual":
            user_states[user_id] = {"step": "waiting_for_group_manual"}
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(f"{self.bi('➕ 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data == "start_spam":
            user_states[user_id] = {"step": "waiting_for_group"}
            kb = [[InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗", callback_data="saved_groups_menu"), InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(f"{self.bi('🔥 𝗦𝗲𝗻𝗱 𝗚𝗿𝗼𝘂𝗽 𝗜𝗗')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data == "my_stats":
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"{self.bi('📊 𝗦𝗧𝗔𝗧𝗦')}\n{self.bi('📋 ' + str(len(saved_groups)) + ' | 👥 ' + str(len(admin_list)))}",
                reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "help_menu":
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
            await query.edit_message_text(
                f"{self.bi('❓ /GetId | /deleteall | 10 Styles')}",
                reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "owner_panel":
            kb = [
                [InlineKeyboardButton("👥 𝗠𝗔𝗡𝗔𝗚𝗘 𝗔𝗗𝗠𝗜𝗡𝗦", callback_data="manage_admins")],
                [InlineKeyboardButton("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗔𝗟𝗟 𝗚𝗥𝗢𝗨𝗣 𝗠𝗦𝗚", callback_data="delete_all_group")],
                [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"{self.bi('🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟')}\n{self.bi('👑 @' + self.owner_username)}",
                reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "delete_all_group":
            # Show saved groups to select for delete
            if not saved_groups:
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")]]
                await query.edit_message_text(f"{self.bi('📋 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽𝘀')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
                return
            keyboard = []
            for gid, ginfo in list(saved_groups.items())[:20]:
                name = ginfo.get("name", gid)[:30]
                keyboard.append([InlineKeyboardButton(f"🗑 {name}", callback_data=f"delg_{gid}")])
            keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")])
            await query.edit_message_text(
                f"{self.bi('🗑 𝗦𝗘𝗟𝗘𝗖𝗧 𝗚𝗥𝗢𝗨𝗣 𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘 🗑')}",
                reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN
            )
            return
        if data.startswith("delg_"):
            gid = data.replace("delg_", "")
            try:
                chat_id = int(gid)
            except:
                chat_id = gid
            await query.edit_message_text(f"{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗶𝗻𝗴 𝗺𝘀𝗴 𝗳𝗿𝗼𝗺: ' + str(chat_id))}", parse_mode=ParseMode.MARKDOWN)
            # Try to delete recent messages
            deleted = 0
            try:
                # This is limited - bot can only delete messages it sent recently
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
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")]]
            await query.edit_message_text(
                f"{self.bi('✅ 𝗗𝗲𝗹𝗲𝘁𝗲𝗱: ' + str(deleted) + ' 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}",
                reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN
            )
            return
        if data == "manage_admins":
            if user_id != self.owner_id:
                await query.answer("Only Owner!", show_alert=True)
                return
            atext = f"{self.bi('👥 𝗔𝗗𝗠𝗜𝗡𝗦')}\n"
            for aid in admin_list:
                if aid != self.owner_id:
                    atext += f"{self.bi('• ' + str(aid))}\n"
            if len(admin_list) <= 1:
                atext += f"{self.bi('• 𝗡𝗼𝗻𝗲')}\n"
            atext += f"\n{self.bi('👇 𝗦𝗲𝗻𝗱 𝗜𝗗:')}"
            user_states[user_id] = {"step": "waiting_for_admin_id"}
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="owner_panel")]]
            await query.edit_message_text(atext, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data.startswith("style_"):
            msg_type = data.replace("style_", "")
            user_states[user_id]["msg_type"] = msg_type
            user_states[user_id]["step"] = "waiting_for_content"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_styles")]]
            style_names = {
                "text": "💬 𝗡𝗢𝗥𝗠𝗔𝗟", "bold": "𝗕 𝗕𝗢𝗟𝗗", "italic": "𝑰 𝗜𝗧𝗔𝗟𝗜𝗖",
                "bold_italic": "𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", "mono": "𝙼 𝗠𝗢𝗡𝗢",
                "sans": "𝖲 𝗦𝗔𝗡𝗦", "sans_bold": "𝗦𝗕 𝗦𝗔𝗡𝗦 𝗕𝗢𝗟𝗗",
                "sans_italic": "𝘚𝘐 𝘚𝘈𝘕𝘚 𝘐𝘛𝘈𝘓𝘐𝘊", "sans_bi": "𝙎𝘽𝙄 𝙎𝘼𝙉𝙎 𝘽𝙄",
                "serif_bold": "𝐒𝐁 𝐒𝐄𝐑𝐈𝐅 𝐁𝐎𝐋𝐃"
            }
            sn = style_names.get(msg_type, "SEND")
            await query.edit_message_text(f"{self.bi(sn)}\n{self.bi('📤 𝗦𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝘁𝗲𝘅𝘁:')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data.startswith("media_"):
            mtype = data.replace("media_", "")
            user_states[user_id]["msg_type"] = mtype
            user_states[user_id]["step"] = "waiting_for_content"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_styles")]]
            media_names = {
                "sticker": "🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", "photo": "🖼 𝗣𝗛𝗢𝗧𝗢", "video": "🎥 𝗩𝗜𝗗𝗘𝗢",
                "document": "📄 𝗗𝗢𝗖", "audio": "🎵 𝗔𝗨𝗗𝗜𝗢", "voice": "🎤 𝗩𝗢𝗜𝗖𝗘",
                "video_note": "📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘"
            }
            mn = media_names.get(mtype, "SEND")
            await query.edit_message_text(f"{self.bi(mn)}\n{self.bi('📤 𝗦𝗲𝗻𝗱 𝗻𝗼𝘄:')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        if data == "show_styles":
            await self.show_style_menu(query, user_id)
            return
        if data == "show_count":
            user_states[user_id]["step"] = "waiting_for_count"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_styles")]]
            await query.edit_message_text(f"{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬? (𝟭-𝟭𝟬𝟬𝟬)')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
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
            [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            f"{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘/𝗠𝗘𝗗𝗜𝗔')}\n{self.bi('📌 ' + gname)}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN
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
                    f"{self.bi('🗑 𝗗𝗲𝗹𝗲𝘁𝗶𝗻𝗴 𝗳𝗿𝗼𝗺: ' + str(chat_id))}\n{self.bi('⚠ 𝗕𝗼𝘁 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗔𝗗𝗠𝗜𝗡')}",
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
                await update.message.reply_text(f"{self.bi('✅ 𝗗𝗲𝗹𝗲𝘁𝗲𝗱: ' + str(deleted))}", parse_mode=ParseMode.MARKDOWN)
            except:
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱')}", parse_mode=ParseMode.MARKDOWN)
            if user_id in user_states:
                del user_states[user_id]
            return
        
        if step in ["waiting_for_group_manual", "waiting_for_group"]:
            text = update.message.text
            chat_id = self.parse_chat_id(text)
            if chat_id:
                info = await self.get_chat_info(context, chat_id)
                gname = info["title"]
                saved_groups[str(chat_id)] = {"name": gname, "id": str(chat_id), "members": str(info["members"])}
                self.save_groups()
                user_states[user_id].update({"chat_id": chat_id, "group_name": gname, "step": "waiting_for_type"})
                await self.show_style_menu_for_message(update, user_id)
            else:
                kb = [[InlineKeyboardButton("📋 𝗦𝗔𝗩𝗘𝗗", callback_data="saved_groups_menu"), InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]]
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
        
        if step == "waiting_for_content":
            user_states[user_id]["content"] = update.message
            user_states[user_id]["step"] = "waiting_for_count"
            kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_styles")]]
            await update.message.reply_text(f"{self.bi('✅ 𝗢𝗞')}\n{self.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬?')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
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
                    [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_count")]
                ]
                await update.message.reply_text(
                    f"{self.bi('⚡ 𝗦𝗣𝗘𝗘𝗗')}\n{self.bi('🔢 ' + str(count))}",
                    reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN
                )
            except ValueError:
                kb = [[InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="show_styles")]]
                await update.message.reply_text(f"{self.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗')}", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            return
    
    async def show_style_menu_for_message(self, update, user_id):
        gname = user_states[user_id].get("group_name", "N/A")
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
            [InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞", callback_data="main_menu")]
        ]
        await update.message.reply_text(
            f"{self.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘/𝗠𝗘𝗗𝗜𝗔')}\n{self.bi('📌 ' + gname)}",
            reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN
        )
    
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
            text=f"{self.bi('🔥 𝗦𝗣𝗔𝗠 𝗦𝗧𝗔𝗥𝗧𝗘𝗗')}\n{self.bi('📌 ' + gname + ' | 🎯 ' + msg_type + ' | 🔢 ' + str(count) + ' | ⚡ ' + str(delay) + 's')}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        error_msg = None
        sent_message_ids = []
        
        # Get style function for text types
        style_func = None
        text_types = ["text", "bold", "italic", "bold_italic", "mono", "sans", "sans_bold", "sans_italic", "sans_bi", "serif_bold"]
        if msg_type in text_types and msg_type != "text":
            style_func = self.get_style_function(msg_type)
        
        for i in range(count):
            try:
                sent_msg = None
                
                if msg_type in text_types:
                    txt = content.text if content and content.text else "Premium Spam"
                    if style_func:
                        txt = style_func(txt)
                    sent_msg = await context.bot.send_message(chat_id=chat_id, text=txt)
                
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
                
                if success % 10 == 0:
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
                if failed > 3:
                    break
        
        if success > 0:
            last_spam_messages[user_id] = {"chat_id": chat_id, "message_ids": sent_message_ids, "group_name": gname}
        
        try:
            await status_msg.delete()
        except:
            pass
        
        result = f"""
{self.bi('✅ 𝗠𝗜𝗦𝗦𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅')}
{self.bi('━━━━━━━━━━━━━━')}
{self.bi('📌 ' + gname)}
{self.bi('✅ ' + str(success) + ' | ❌ ' + str(failed) + ' | ⚡ ' + str(delay) + 's')}
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
            [InlineKeyboardButton("🎨 𝗖𝗛𝗔𝗡𝗚𝗘 𝗦𝗧𝗬𝗟𝗘", callback_data="change_style")]
        ]
        if success > 0:
            keyboard.append([InlineKeyboardButton("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗡𝗧 𝗠𝗦𝗚 🗑", callback_data="delete_last_spam")])
        keyboard.append([InlineKeyboardButton("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", callback_data="main_menu")])
        
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
╔══════════════════════════════╗
║  👑 PREMIUM SPAM BOT 👑    ║
║  10 TEXT STYLES ACTIVE      ║
║  0.1s SPEED ACTIVE          ║
║  DELETE SYSTEM ACTIVE       ║
║  Owner: @{OWNER_USERNAME}  ║
╚══════════════════════════════╝
    """)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
