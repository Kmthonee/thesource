# Zed-Thon - ZelZal
# Copyright (C) 2022 Zedthon . All Rights Reserved
#
# This file is a part of < https://github.com/Zed-Thon/ZelZal/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Zed-Thon/ZelZal/blob/main/LICENSE/>.
""" الوصـف : تحـديث اوامـر النشـر التلقـائـي للقنـوات ™
الاوامـر صـارت تدعـم المعـرفـات والروابـط الى جانب ايديـات القنـوات
حقـوق : @ZedThon
@zzzzl1l - كتـابـة الملـف :  زلــزال الهيبــه"""
import asyncio
import requests
import logging

from telethon import *
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

from Kmthon import zedub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from Kmthon.core.logger import logging
from ..sql_helper.globals import gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from . import *

plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)

SPRS = gvarstatus("Z_SPRS") or "(نشر_تلقائي|نشر|تلقائي)"
OFSPRS = gvarstatus("Z_OFSPRS") or "(ايقاف_النشر|ايقاف النشر|ستوب)"

ZelzalNSH_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝗞𝗺𝘁𝗵𝗼𝗻  - اوامـر السبـام والتكـرار](t.me/Kmthon) 𓆪\n\n"
    "`.كرر` + عـدد + كلمـه\n"
    "**⪼ لـ تكـرار كلمـه معينـه لعـدد معيـن من المـرات**\n\n"
    "`.مؤقت + عدد الثواني + عدد التكرار + الكليشة`\n"
    "**⪼ لـ تكـرار نص لوقت معين وعدد معين من المـرات**\n"
    "**⪼ الامر يفيد جماعة الاعلانات وكروبات الشراء**\n\n"
    "`.تكرار ملصق`\n"
    "**⪼ لـ تكـرار ملصقـات من حزمـه معينـه**\n\n"
    "`.سبام` + كلمـه\n"
    "**⪼ لـ تكـرار كلمـة او جملـة نصيـه**\n\n"
    "`.وسبام` + كلمـه\n"
    "**⪼ لـ تكـرار حـروف كلمـة على حرف حرف**\n\n"
    "`.تعبير تلقائي`\n"
    "**⪼ لـ تكـرار تفاعـلات رياكشـن** 👍👎❤🔥🥰👏😁🤔🤯😱🤬😢🎉🤩🤮💩\n\n"
    "`.ايقاف مؤقت`\n"
    "**⪼ لـ إيقـاف أي تكـرار جـاري تنفيـذه**\n\n"
)


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="(نشر تلقائي|تلقائي)(?:\s|$)([\s\S]*)")
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "**⎉╎عـذراً .. النشر التلقائي خـاص بالقنـوات فقـط\n⎉╎قم باستخـدام الامـر داخـل القنـاة الهـدف**")
    if input_str := event.pattern_match.group(2):
        try:
            zch = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**", 5)
        try:
            if is_post(zch.id , event.chat_id):
                return await edit_or_reply(event, "**⎉╎النشـر التلقـائي مفعـل مسبقـاً ✓**")
            if zch.first_name:
                await asyncio.sleep(1.5)
                add_post(zch.id, event.chat_id)
                await edit_or_reply(event, "**⎉╎تم تفعيـل النشـر التلقـائي من القنـاة .. بنجـاح ✓**")
        except Exception:
            try:
                if is_post(zch.id , event.chat_id):
                    return await edit_or_reply(event, "**⎉╎النشـر التلقـائي مفعـل مسبقـاً ✓**")
                if zch.title:
                    await asyncio.sleep(1.5)
                    add_post(zch.id, event.chat_id)
                    return await edit_or_reply(event, "**⎉╎تم تفعيـل النشـر التلقـائي من القنـاة .. بنجـاح ✓**")
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")



# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="(ايقاف النشر|ستوب)(?:\s|$)([\s\S]*)")
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "**⎉╎عـذراً .. النشر التلقائي خـاص بالقنـوات فقـط\n⎉╎قم باستخـدام الامـر داخـل القنـاة الهـدف**")
    if input_str := event.pattern_match.group(2):
        try:
            zch = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**", 5)
        try:
            if not is_post(zch.id, event.chat_id):
                return await edit_or_reply(event, "**⎉╎عـذراً .. النشـر التلقـائي غير مفعـل من اساسـاً ؟!**")
            if zch.first_name:
                await asyncio.sleep(1.5)
                remove_post(zch.id, event.chat_id)
                await edit_or_reply(event, "**⎉╎تم تعطيـل النشر التلقـائي هنـا .. بنجـاح ✓**")
        except Exception:
            try:
                if not is_post(zch.id, event.chat_id):
                    return await edit_or_reply(event, "**⎉╎عـذراً .. النشـر التلقـائي غير مفعـل من اساسـاً ؟!**")
                if zch.title:
                    await asyncio.sleep(1.5)
                    remove_post(zch.id, event.chat_id)
                    return await edit_or_reply(event, "**⎉╎تم تعطيـل النشر التلقـائي هنـا .. بنجـاح ✓**")
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")



@zedub.zed_cmd(incoming=True, forword=None)
async def _(event):
    if event.is_private:
        return
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set  = get_all_post(chat_id)
    if channels_set == []:
        return
    for chat in channels_set:
        if event.media:
            await event.client.send_file(int(chat), event.media, caption=event.text)
        elif not event.media:
            await zedub.send_message(int(chat), event.message)



# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="النشر")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalNSH_cmd)

