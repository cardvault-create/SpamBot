import os
import asyncio
import logging
import json
import re
import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import FloodWaitError

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 API CREDENTIALS
API_ID = int(os.getenv("API_ID", "37864401"))
API_HASH = os.getenv("API_HASH", "e7747bfa480eb76256f96976b9dccabc")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8887965375:AAEwf6UR5F0oFSTqS5KTCmNxIVDyysyx4s8")
OWNER_ID = int(os.getenv("OWNER_ID", "7614459746"))
OWNER_USERNAME = "BeStChEaT_OwNeR"

# Initialize Client
client = TelegramClient('premium_bot', API_ID, API_HASH)

user_states = {}
saved_groups = {}
admin_list = set()
auto_delete_enabled = True
last_spam_messages = {}

GROUPS_FILE = "saved_groups.json"
ADMIN_FILE = "admin_list.json"
CONFIG_FILE = "config.json"

class PremiumSpamBot:
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
    
    async def get_chat_info(self, chat_id):
        """Get REAL group info with EXACT online count"""
        try:
            chat = await client.get_entity(chat_id)
            title = chat.title if hasattr(chat, 'title') else "Unknown"
            
            # Get FULL chat info with REAL online count
            online_count = 0
            total_members = 0
            admin_count = 0
            
            try:
                if hasattr(chat, 'megagroup') and chat.megagroup:
                    full_chat = await client(GetFullChannelRequest(channel=chat))
                else:
                    full_chat = await client(GetFullChatRequest(chat_id=chat_id))
                
                # REAL ONLINE COUNT
                online_count = full_chat.full_chat.online_count if hasattr(full_chat.full_chat, 'online_count') else 0
                
                # TOTAL MEMBERS
                if hasattr(full_chat.full_chat, 'participants_count'):
                    total_members = full_chat.full_chat.participants_count
                elif hasattr(chat, 'participants_count'):
                    total_members = chat.participants_count
                
                # ADMIN COUNT
                try:
                    admins = await client.get_participants(chat_id, filter=ChannelParticipantsAdmins)
                    admin_count = len(admins)
                except:
                    admin_count = 0
            except:
                online_count = 0
                total_members = 0
            
            # Description
            desc = ""
            if hasattr(full_chat.full_chat, 'about') and full_chat.full_chat.about:
                desc = full_chat.full_chat.about[:100]
            
            return {
                "title": title,
                "members": total_members,
                "online": online_count,
                "admins": admin_count,
                "desc": desc if desc else "No description"
            }
        except Exception as e:
            logger.error(f"Error getting chat info: {e}")
            return {"title": str(chat_id), "members": 0, "online": 0, "admins": 0, "desc": "N/A"}

bot = PremiumSpamBot()

# 🟢 START COMMAND
@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.sender_id
    
    if not bot.is_authorized(user_id):
        keyboard = [[Button.url("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", f"https://t.me/{OWNER_USERNAME}")]]
        await event.reply(bot.block_msg(), buttons=keyboard, parse_mode='markdown')
        return
    
    if user_id in user_states:
        del user_states[user_id]
    
    auto_status = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
    
    keyboard = [
        [Button.inline("🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥", b"start_spam")],
        [Button.inline("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", b"saved_groups"),
         Button.inline("➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 ➕", b"add_group")],
        [Button.inline("🆔 𝗚𝗘𝗧 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 🆔", b"get_id_info"),
         Button.inline("❓ 𝗛𝗘𝗟𝗣 ❓", b"help_menu")],
        [Button.inline("📊 𝗦𝗧𝗔𝗧𝗦 📊", b"my_stats"),
         Button.inline("🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐", b"owner_panel")],
        [Button.inline(f"🔄 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟: {auto_status}", b"toggle_auto_delete")],
        [Button.url("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", f"https://t.me/{OWNER_USERNAME}")]
    ]
    
    msg = f"""
{bot.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}

{bot.bi('💎 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞 𝗠𝗔𝗦𝗧𝗘𝗥 💎')}

{bot.bi('⭐ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦 ⭐')}
{bot.bi('• 𝟭𝟬 𝗨𝗻𝗶𝗾𝘂𝗲 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀')}
{bot.bi('• 🟢 𝗥𝗘𝗔𝗟 𝗢𝗻𝗹𝗶𝗻𝗲 𝗠𝗲𝗺𝗯𝗲𝗿𝘀 𝗖𝗼𝘂𝗻𝘁')}
{bot.bi('• 𝗗𝗲𝗹𝗲𝘁𝗲 𝗦𝗲𝗻𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀')}
{bot.bi('• 𝗦𝗮𝘃𝗲𝗱 𝗚𝗿𝗼𝘂𝗽𝘀 𝗦𝘆𝘀𝘁𝗲𝗺')}
{bot.bi('• 𝗔𝗱𝗺𝗶𝗻 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁')}
{bot.bi('• 𝗨𝗹𝘁𝗿𝗮 𝗙𝗮𝘀𝘁 𝟬.𝟭𝘀 𝗦𝗽𝗲𝗲𝗱')}

{bot.bi('🔒 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗠𝗼𝗱𝗲')}
{bot.bi('👑 𝗔𝗖𝗖𝗘𝗦𝗦: 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗢𝗻𝗹𝘆')}
{bot.bi('💎 𝗣𝗟𝗔𝗡: 𝗘𝘅𝗰𝗹𝘂𝘀𝗶𝘃𝗲 𝗣𝗿𝗲𝗺𝗶𝘂𝗺')}

{bot.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 📌')}
"""
    await event.reply(msg, buttons=keyboard, parse_mode='markdown')

# 🟢 /GetId COMMAND - WITH REAL ONLINE COUNT
@client.on(events.NewMessage(pattern='/GetId'))
async def getid_handler(event):
    chat_id = event.chat_id
    
    if event.is_private:
        await event.reply(
            f"{bot.bi('💬 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗖𝗵𝗮𝘁')}\n{bot.bi('🆔 𝗜𝗗: ' + str(chat_id))}",
            parse_mode='markdown'
        )
        return
    
    # Get REAL info
    info = await bot.get_chat_info(chat_id)
    
    # Save group
    saved_groups[str(chat_id)] = {
        "name": info["title"],
        "id": str(chat_id),
        "members": str(info["members"]),
        "online": str(info["online"]),
        "admins": str(info["admins"])
    }
    bot.save_groups()
    
    msg = f"""
{bot.bi('📋 𝗚𝗥𝗢𝗨𝗣 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 📋')}
{bot.bi('━━━━━━━━━━━━━━━━━━')}
{bot.bi('📌 𝗡𝗮𝗺𝗲: ' + str(info['title']))}
{bot.bi('🆔 𝗜𝗗: ' + str(chat_id))}
{bot.bi('👥 𝗧𝗼𝘁𝗮𝗹 𝗠𝗲𝗺𝗯𝗲𝗿𝘀: ' + str(info['members']))}
{bot.bi('🟢 𝗢𝗻𝗹𝗶𝗻𝗲 𝗡𝗼𝘄: ' + str(info['online']) + ' (𝗥𝗘𝗔𝗟)')}
{bot.bi('👑 𝗔𝗱𝗺𝗶𝗻𝘀: ' + str(info['admins']))}
{bot.bi('📝 𝗗𝗲𝘀𝗰: ' + str(info['desc']))}
{bot.bi('━━━━━━━━━━━━━━━━━━')}
{bot.bi('✅ 𝗚𝗿𝗼𝘂𝗽 𝗔𝘂𝘁𝗼-𝗦𝗮𝘃𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆')}
"""
    await event.reply(msg, parse_mode='markdown')

# 🟢 BUTTON HANDLER
@client.on(events.CallbackQuery())
async def callback_handler(event):
    user_id = event.sender_id
    
    if not bot.is_authorized(user_id):
        await event.answer("🔐 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱!", alert=True)
        return
    
    data = event.data.decode()
    
    if data == "start_spam":
        user_states[user_id] = {"step": "waiting_for_group"}
        keyboard = [
            [Button.inline("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦", b"saved_groups")],
            [Button.inline("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", b"main_menu")]
        ]
        await event.edit(
            f"{bot.bi('🔥 𝗦𝗘𝗡𝗗 𝗚𝗥𝗢𝗨𝗣 𝗜𝗗 𝗢𝗥 @𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘')}\n{bot.bi('📌 𝗙𝗼𝗿𝗺𝗮𝘁: -𝟭𝟬𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data == "main_menu":
        if user_id in user_states:
            del user_states[user_id]
        auto_status = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
        keyboard = [
            [Button.inline("🔥 𝗦𝗧𝗔𝗥𝗧 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚 🔥", b"start_spam")],
            [Button.inline("📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 📋", b"saved_groups"),
             Button.inline("➕ 𝗔𝗗𝗗 𝗚𝗥𝗢𝗨𝗣 ➕", b"add_group")],
            [Button.inline("📊 𝗦𝗧𝗔𝗧𝗦 📊", b"my_stats"),
             Button.inline("🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🔐", b"owner_panel")],
            [Button.inline(f"🔄 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟: {auto_status}", b"toggle_auto_delete")],
            [Button.url("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", f"https://t.me/{OWNER_USERNAME}")]
        ]
        await event.edit(
            f"{bot.bi('👑 𝗘𝗫𝗖𝗟𝗨𝗦𝗜𝗩𝗘 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑')}\n\n{bot.bi('📌 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 📌')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data == "saved_groups":
        if not saved_groups:
            keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"main_menu")]]
            await event.edit(
                f"{bot.bi('📋 𝗡𝗢 𝗚𝗥𝗢𝗨𝗣𝗦 𝗦𝗔𝗩𝗘𝗗')}\n{bot.bi('𝗦𝗲𝗻𝗱 /𝗚𝗲𝘁𝗜𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}",
                buttons=keyboard, parse_mode='markdown'
            )
            return
        
        keyboard = []
        for gid, ginfo in list(saved_groups.items())[:20]:
            name = ginfo.get("name", gid)[:30]
            keyboard.append([Button.inline(f"📌 {name}", f"sg_{gid}".encode())])
        keyboard.append([Button.inline("🔙 𝗕𝗔𝗖𝗞", b"main_menu")])
        
        await event.edit(
            f"{bot.bi('📋 𝗦𝗔𝗩𝗘𝗗 𝗚𝗥𝗢𝗨𝗣𝗦 (' + str(len(saved_groups)) + ')')}\n{bot.bi('👇 𝗦𝗘𝗟𝗘𝗖𝗧 𝗧𝗢 𝗦𝗣𝗔𝗠')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data.startswith("sg_"):
        gid = data.replace("sg_", "")
        ginfo = saved_groups.get(gid, {})
        gname = ginfo.get("name", gid)
        try:
            chat_id = int(gid)
        except:
            chat_id = gid
        
        user_states[user_id] = {"step": "waiting_for_type", "chat_id": chat_id, "group_name": gname}
        await show_style_menu(event, user_id)
    
    elif data.startswith("style_"):
        msg_type = data.replace("style_", "")
        user_states[user_id]["msg_type"] = msg_type
        user_states[user_id]["step"] = "waiting_for_content"
        
        keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"show_styles")]]
        style_names = {
            "text": "💬 𝗡𝗢𝗥𝗠𝗔𝗟", "bold": "𝗕 𝗕𝗢𝗟𝗗", "italic": "𝑰 𝗜𝗧𝗔𝗟𝗜𝗖",
            "bold_italic": "𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", "mono": "𝙼 𝗠𝗢𝗡𝗢",
            "sans": "𝖲 𝗦𝗔𝗡𝗦", "sans_bold": "𝗦𝗕 𝗦𝗔𝗡𝗦 𝗕𝗢𝗟𝗗",
            "sans_italic": "𝘚𝘐 𝘚𝘈𝘕𝘚 𝘐𝘛𝘈𝘓𝘐𝘊", "sans_bi": "𝙎𝘽𝙄 𝙎𝘼𝙉𝙎 𝘽𝙄",
            "serif_bold": "𝐒𝐁 𝐒𝐄𝐑𝐈𝐅 𝐁𝐎𝐋𝐃"
        }
        sn = style_names.get(msg_type, "𝗦𝗘𝗡𝗗")
        await event.edit(
            f"{bot.bi(sn)}\n{bot.bi('📤 𝗦𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝘁𝗲𝘅𝘁:')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data.startswith("media_"):
        mtype = data.replace("media_", "")
        user_states[user_id]["msg_type"] = mtype
        user_states[user_id]["step"] = "waiting_for_content"
        keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"show_styles")]]
        await event.edit(
            f"{bot.bi('📤 𝗦𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 𝗺𝗲𝗱𝗶𝗮:')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data == "show_styles":
        await show_style_menu(event, user_id)
    
    elif data == "show_count":
        user_states[user_id]["step"] = "waiting_for_count"
        keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"show_styles")]]
        await event.edit(
            f"{bot.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬? (𝟭-𝟭𝟬𝟬𝟬)')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data.startswith("speed_"):
        speed_map = {"speed_ultra": 0.1, "speed_fast": 0.3, "speed_normal": 0.5, "speed_slow": 1}
        user_states[user_id]["delay"] = speed_map.get(data, 0.1)
        await execute_spam(event, user_id)
    
    elif data == "resend_same":
        if user_id in user_states and "chat_id" in user_states[user_id]:
            await execute_spam(event, user_id)
    
    elif data == "delete_last":
        if user_id in last_spam_messages:
            sd = last_spam_messages[user_id]
            deleted = 0
            for mid in sd.get("message_ids", []):
                try:
                    await client.delete_messages(sd["chat_id"], mid)
                    deleted += 1
                    await asyncio.sleep(0.05)
                except:
                    pass
            keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"main_menu")]]
            await event.edit(
                f"{bot.bi('✅ 𝗗𝗘𝗟𝗘𝗧𝗘𝗗: ' + str(deleted) + '/' + str(len(sd.get('message_ids',[]))))}",
                buttons=keyboard, parse_mode='markdown'
            )
            del last_spam_messages[user_id]
    
    elif data == "toggle_auto_delete":
        global auto_delete_enabled
        auto_delete_enabled = not auto_delete_enabled
        bot.save_config()
        s = "✅ 𝗢𝗡" if auto_delete_enabled else "❌ 𝗢𝗙𝗙"
        await event.answer(f"𝗔𝘂𝘁𝗼 𝗗𝗲𝗹𝗲𝘁𝗲 {s}", alert=True)
    
    elif data == "owner_panel":
        keyboard = [
            [Button.inline("👥 𝗠𝗔𝗡𝗔𝗚𝗘 𝗔𝗗𝗠𝗜𝗡𝗦", b"manage_admins")],
            [Button.inline("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗔𝗟𝗟 𝗠𝗦𝗚", b"delete_all_group")],
            [Button.inline("🔙 𝗕𝗔𝗖𝗞", b"main_menu")]
        ]
        await event.edit(
            f"{bot.bi('🔐 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟')}\n{bot.bi('👑 @' + OWNER_USERNAME)}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif data == "manage_admins":
        if user_id != OWNER_ID:
            await event.answer("🔐 𝗢𝗻𝗹𝘆 𝗢𝘄𝗻𝗲𝗿!", alert=True)
            return
        user_states[user_id] = {"step": "waiting_for_admin_id"}
        keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"owner_panel")]]
        await event.edit(
            f"{bot.bi('👥 𝗦𝗲𝗻𝗱 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗮𝗱𝗱/𝗿𝗲𝗺𝗼𝘃𝗲:')}",
            buttons=keyboard, parse_mode='markdown'
        )

async def show_style_menu(event, user_id):
    gname = user_states[user_id].get("group_name", "N/A")
    user_states[user_id]["step"] = "waiting_for_type"
    
    keyboard = [
        [Button.inline("💬 𝗡𝗢𝗥𝗠𝗔𝗟", b"style_text"),
         Button.inline("𝗕 𝗕𝗢𝗟𝗗", b"style_bold")],
        [Button.inline("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", b"style_italic"),
         Button.inline("𝑩𝑰 𝗕𝗢𝗟𝗗+𝗜𝗧𝗔𝗟𝗜𝗖", b"style_bold_italic")],
        [Button.inline("𝙼 𝗠𝗢𝗡𝗢", b"style_mono"),
         Button.inline("𝖲 𝗦𝗔𝗡𝗦", b"style_sans")],
        [Button.inline("𝗦𝗕 𝗦𝗔𝗡𝗦 𝗕𝗢𝗟𝗗", b"style_sans_bold"),
         Button.inline("𝘚𝘐 𝘚𝘈𝘕𝘚 𝘐𝘛𝘈𝘓𝘐𝘊", b"style_sans_italic")],
        [Button.inline("𝙎𝘽𝙄 𝙎𝘼𝙉𝙎 𝘽𝙄", b"style_sans_bi"),
         Button.inline("𝐒𝐁 𝐒𝐄𝐑𝐈𝐅 𝐁𝐎𝐋𝐃", b"style_serif_bold")],
        [Button.inline("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", b"media_sticker"),
         Button.inline("🖼 𝗣𝗛𝗢𝗧𝗢", b"media_photo")],
        [Button.inline("🎥 𝗩𝗜𝗗𝗘𝗢", b"media_video"),
         Button.inline("📄 𝗗𝗢𝗖", b"media_document")],
        [Button.inline("🎵 𝗔𝗨𝗗𝗜𝗢", b"media_audio"),
         Button.inline("🎤 𝗩𝗢𝗜𝗖𝗘", b"media_voice")],
        [Button.inline("📹 𝗩𝗜𝗗 𝗡𝗢𝗧𝗘", b"media_video_note")],
        [Button.inline("🔙 𝗕𝗔𝗖𝗞 𝗧𝗢 𝗠𝗘𝗡𝗨", b"main_menu")]
    ]
    
    await event.edit(
        f"""
{bot.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘 𝗢𝗥 𝗠𝗘𝗗𝗜𝗔 🎯')}
{bot.bi('📌 𝗚𝗿𝗼𝘂𝗽: ' + gname)}

{bot.bi('👇 𝟭𝟬 𝗧𝗲𝘅𝘁 𝗦𝘁𝘆𝗹𝗲𝘀 + 𝟳 𝗠𝗲𝗱𝗶𝗮 𝗧𝘆𝗽𝗲𝘀 👇')}
""",
        buttons=keyboard, parse_mode='markdown'
    )

# 🟢 MESSAGE HANDLER
@client.on(events.NewMessage())
async def message_handler(event):
    user_id = event.sender_id
    
    if not bot.is_authorized(user_id):
        if not event.is_private:
            return
        keyboard = [[Button.url("🥡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 - 𝗙𝗮𝗧𝗵𝗘𝗿 🩵", f"https://t.me/{OWNER_USERNAME}")]]
        await event.reply(bot.block_msg(), buttons=keyboard, parse_mode='markdown')
        return
    
    if user_id not in user_states:
        return
    
    state = user_states[user_id]
    step = state.get("step")
    
    if step == "waiting_for_admin_id":
        if user_id != OWNER_ID:
            return
        try:
            tid = int(event.message.text.strip())
            if tid in admin_list:
                admin_list.remove(tid)
                bot.save_admins()
                await event.reply(f"{bot.bi('✅ 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: ' + str(tid))}", parse_mode='markdown')
            else:
                admin_list.add(tid)
                bot.save_admins()
                await event.reply(f"{bot.bi('✅ 𝗔𝗱𝗱𝗲𝗱: ' + str(tid))}", parse_mode='markdown')
        except:
            await event.reply(f"{bot.bi('❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗜𝗗')}", parse_mode='markdown')
        return
    
    if step == "waiting_for_group":
        text = event.message.text
        chat_id = parse_chat_id(text)
        
        if chat_id:
            info = await bot.get_chat_info(chat_id)
            gname = info["title"]
            saved_groups[str(chat_id)] = {
                "name": gname, "id": str(chat_id),
                "members": str(info["members"]),
                "online": str(info["online"])
            }
            bot.save_groups()
            user_states[user_id].update({"chat_id": chat_id, "group_name": gname, "step": "waiting_for_type"})
            
            keyboard = [
                [Button.inline("💬 𝗡𝗢𝗥𝗠𝗔𝗟", b"style_text"),
                 Button.inline("𝗕 𝗕𝗢𝗟𝗗", b"style_bold")],
                [Button.inline("𝑰 𝗜𝗧𝗔𝗟𝗜𝗖", b"style_italic"),
                 Button.inline("𝑩𝑰 𝗕&𝗜", b"style_bold_italic")],
                [Button.inline("𝙼 𝗠𝗢𝗡𝗢", b"style_mono"),
                 Button.inline("𝖲 𝗦𝗔𝗡𝗦", b"style_sans")],
                [Button.inline("🎯 𝗦𝗧𝗜𝗖𝗞𝗘𝗥", b"media_sticker"),
                 Button.inline("🖼 𝗣𝗛𝗢𝗧𝗢", b"media_photo")],
                [Button.inline("🔙 𝗕𝗔𝗖𝗞", b"main_menu")]
            ]
            
            await event.reply(
                f"""
{bot.bi('✅ 𝗚𝗥𝗢𝗨𝗣 𝗙𝗢𝗨𝗡𝗗 ✅')}
{bot.bi('📌 ' + gname)}
{bot.bi('🆔 ' + str(chat_id))}
{bot.bi('👥 ' + str(info['members']) + ' | 🟢 ' + str(info['online']) + ' (𝗥𝗘𝗔𝗟)')}

{bot.bi('🎯 𝗦𝗘𝗟𝗘𝗖𝗧 𝗦𝗧𝗬𝗟𝗘 🎯')}
""",
                buttons=keyboard, parse_mode='markdown'
            )
        else:
            keyboard = [[Button.inline("📋 𝗦𝗔𝗩𝗘𝗗", b"saved_groups"), Button.inline("🔙 𝗕𝗔𝗖𝗞", b"main_menu")]]
            await event.reply(
                f"{bot.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗')}\n{bot.bi('𝗨𝘀𝗲 /𝗚𝗲𝘁𝗜𝗱 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽')}",
                buttons=keyboard, parse_mode='markdown'
            )
    
    elif step == "waiting_for_content":
        user_states[user_id]["content"] = event.message
        user_states[user_id]["step"] = "waiting_for_count"
        keyboard = [[Button.inline("🔙 𝗕𝗔𝗖𝗞", b"show_styles")]]
        await event.reply(
            f"{bot.bi('✅ 𝗖𝗢𝗡𝗧𝗘𝗡𝗧 𝗢𝗞')}\n{bot.bi('🔢 𝗛𝗢𝗪 𝗠𝗔𝗡𝗬?')}",
            buttons=keyboard, parse_mode='markdown'
        )
    
    elif step == "waiting_for_count":
        try:
            count = int(event.message.text)
            count = max(1, min(count, 1000))
            user_states[user_id]["count"] = count
            user_states[user_id]["step"] = "waiting_for_speed"
            
            keyboard = [
                [Button.inline("⚡ 𝗨𝗟𝗧𝗥𝗔 (𝟬.𝟭𝘀)", b"speed_ultra"),
                 Button.inline("🚀 𝗙𝗔𝗦𝗧 (𝟬.𝟯𝘀)", b"speed_fast")],
                [Button.inline("🐢 𝗡𝗢𝗥𝗠𝗔𝗟 (𝟬.𝟱𝘀)", b"speed_normal"),
                 Button.inline("🦥 𝗦𝗟𝗢𝗪 (𝟭𝘀)", b"speed_slow")],
                [Button.inline("🔙 𝗕𝗔𝗖𝗞", b"show_count")]
            ]
            await event.reply(
                f"{bot.bi('⚡ 𝗦𝗣𝗘𝗘𝗗')}\n{bot.bi('🔢 ' + str(count))}",
                buttons=keyboard, parse_mode='markdown'
            )
        except:
            await event.reply(f"{bot.bi('❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗')}", parse_mode='markdown')

def parse_chat_id(text):
    if not text:
        return None
    text = text.strip()
    if re.match(r'^-?\d{10,}$', text):
        return int(text)
    match = re.search(r'@([a-zA-Z0-9_]+)', text)
    if match:
        return match.group(1)
    match = re.search(r'(?:https?://)?t\.me/([a-zA-Z0-9_]+)', text)
    if match:
        return match.group(1)
    if re.match(r'^[a-zA-Z0-9_]{4,}$', text):
        return text
    return None

async def execute_spam(event, user_id):
    data = user_states.get(user_id, {})
    chat_id = data.get("chat_id", "")
    gname = data.get("group_name", str(chat_id))
    count = data.get("count", 1)
    delay = data.get("delay", 0.1)
    msg_type = data.get("msg_type", "text")
    content = data.get("content")
    
    await event.edit(f"{bot.bi('🔥 𝗦𝗣𝗔𝗠 𝗦𝗧𝗔𝗥𝗧𝗘𝗗...')}", parse_mode='markdown')
    
    success = 0
    failed = 0
    sent_message_ids = []
    
    text_types = ["text", "bold", "italic", "bold_italic", "mono", "sans", "sans_bold", "sans_italic", "sans_bi", "serif_bold"]
    style_func = None
    if msg_type in text_types and msg_type != "text":
        style_func = bot.get_style_function(msg_type)
    
    for i in range(count):
        try:
            sent_msg = None
            
            if msg_type in text_types:
                txt = content.text if content and content.text else "🔥 Premium Spam 🔥"
                if style_func:
                    txt = style_func(txt)
                sent_msg = await client.send_message(chat_id, txt)
            
            elif msg_type == "sticker":
                if content and content.sticker:
                    sent_msg = await client.send_file(chat_id, content.sticker)
                else:
                    failed += 1
                    break
            elif msg_type == "photo":
                if content and content.photo:
                    sent_msg = await client.send_file(chat_id, content.photo)
                else:
                    failed += 1
                    break
            elif msg_type == "video":
                if content and content.video:
                    sent_msg = await client.send_file(chat_id, content.video)
                else:
                    failed += 1
                    break
            elif msg_type in ["document", "audio", "voice", "video_note"]:
                if content and content.media:
                    sent_msg = await client.send_file(chat_id, content.media)
                else:
                    failed += 1
                    break
            else:
                failed += 1
                break
            
            if sent_msg:
                sent_message_ids.append(sent_msg.id)
                success += 1
            
            await asyncio.sleep(delay)
            
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception as e:
            failed += 1
            if failed > 3:
                break
    
    if success > 0:
        last_spam_messages[user_id] = {
            "chat_id": chat_id,
            "message_ids": sent_message_ids,
            "group_name": gname
        }
    
    result = f"""
{bot.bi('✅ 𝗠𝗜𝗦𝗦𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅')}
{bot.bi('━━━━━━━━━━━━━━')}
{bot.bi('📌 ' + gname)}
{bot.bi('✅ ' + str(success) + ' | ❌ ' + str(failed))}
{bot.bi('🎯 ' + msg_type + ' | ⚡ ' + str(delay) + 's')}
{bot.bi('━━━━━━━━━━━━━━')}
{bot.bi('👇 𝗪𝗛𝗔𝗧 𝗡𝗘𝗫𝗧? 👇')}
"""
    
    keyboard = [
        [Button.inline("🔄 𝗥𝗘𝗦𝗘𝗡𝗗", b"resend_same"),
         Button.inline("🎨 𝗦𝗧𝗬𝗟𝗘", b"show_styles")]
    ]
    if success > 0:
        keyboard.append([Button.inline("🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗡𝗧 𝗠𝗦𝗚 🗑", b"delete_last")])
    keyboard.append([Button.inline("🔙 𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨", b"main_menu")])
    
    await client.send_message(event.chat_id, result, buttons=keyboard, parse_mode='markdown')

# 🚀 START BOT
async def main():
    await client.start(bot_token=BOT_TOKEN)
    print(f"""
╔══════════════════════════════════════╗
║                                      ║
║   👑 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗣𝗔𝗠 𝗕𝗢𝗧 👑        ║
║   🔒 𝗣𝗥𝗜𝗩𝗔𝗧𝗘 𝗠𝗢𝗗𝗘 𝗔𝗖𝗧𝗜𝗩𝗘 🔒         ║
║   𝟭𝟬 𝗧𝗘𝗫𝗧 𝗦𝗧𝗬𝗟𝗘𝗦 𝗔𝗖𝗧𝗜𝗩𝗘            ║
║   🟢 𝗥𝗘𝗔𝗟 𝗢𝗡𝗟𝗜𝗡𝗘 𝗖𝗢𝗨𝗡𝗧            ║
║   𝟬.𝟭𝘀 𝗨𝗟𝗧𝗥𝗔 𝗦𝗣𝗘𝗘𝗗 𝗔𝗖𝗧𝗜𝗩𝗘          ║
║   🗑 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗬𝗦𝗧𝗘𝗠 𝗔𝗖𝗧𝗜𝗩𝗘        ║
║                                      ║
║   👤 𝗢𝘄𝗻𝗲𝗿: @{OWNER_USERNAME}     ║
║                                      ║
╚══════════════════════════════════════╝
    """)
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
