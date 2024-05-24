#Nayzak
import asyncio
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from Kmthon import zedub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "البحث"


ZelzalPH_cmd = (
    "**الأذكــار :**\n\n"
    "**الحمدُ لله 📿**\n\n"
    "**لا إله إلّا الله 🤍**\n\n"
    "**صلوا على النبي ♥️**\n\n"
    "**داوموا الأذكار 🥰 - سورس تيبثـون 🇵🇸🤍 .**"
)


#Nayzak
@zedub.zed_cmd(pattern="اذكار")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalPH_cmd)

