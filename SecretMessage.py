#          █▄  █ █▀█ ▀█▀ █▀▄ █▀▀ █▄▀ █▀▄▀█ ▄▀█
#          █ ▀ █ █▄█  █  █▄▀ ██▄ █ █ █ ▀ █ █▀█
#                © Copyright 2026
#            ✈ https://t.me/LiquidModules
# meta developer: @LiquidModules

import logging
from ..inline.types import InlineCall, InlineQuery
from .. import loader, utils

__version__ = (1, 0, 0)

@loader.tds
class SecretMessageMod(loader.Module):
    """Whisper stdin via inline"""
    
    strings = {
        "name": "SecretMessage",
        "for_user_message": "🔐 This is whisper for {name}",
        "open": "👀 Checking whisper",
        "no_user_or_message": " Where is username with text ?",
        "secret_message": "Secret message",
        "send_message": "🔐 Send whisper to {name}",
        "help_message": "⌨️ Usage: @{bot} whisper @username text",
        "not_for_you": "🚫 This not for you !",
        "eaten": "😿 Kitten eaten this whisper ..."
    }
    
    strings_ru = {
        "name": "SecretMessage",
        "for_user_message": "🔐 Это шёпот для {name}",
        "open": "👀 Просмотреть шёпот",
        "no_user_or_message": " Где юзернейм с текстом?",
        "secret_message": "Секретное сообщение",
        "send_message": " Отправить шёпот для {name}",
        "help_message": "⌨️ Использование: @{bot} whisper @username текст",
        "not_for_you": "🚫 Это не для тебя!",
        "eaten": "😿 Котёнок съел этот шёпот..."
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._opened = self.pointer("opened_msgs", [])

    @loader.inline_handler()
    async def whisper(self, query: InlineQuery):
        """[uid] [stdin] - Secret message"""
        args = query.args.split()
        
        if len(args) > 1:
            try:
                target = args[0]
                
                if target.lower() in ["self", "me", "owner"]:
                    target_id = self._tg_id
                    name = "Owner"
                else:
                    try:
                        if target.isdigit():
                            for_user = await self.client.get_entity(int(target))
                        else:
                            for_user = await self.client.get_entity(target)
                        
                        target_id = for_user.id
                        name = getattr(for_user, 'first_name', str(target))
                    except Exception:
                        target_id = int(target) if target.isdigit() else target
                        name = str(target)
                
                name = utils.escape_html(name)
                text = " ".join(args[1:])
                
                return {
                    "title": f"{self.strings('secret_message')}",
                    "description": self.strings("send_message").format(name=name),
                    "message": self.strings("for_user_message").format(name=name),
                    "parse_mode": "HTML",
                    "thumb": "https://img.icons8.com/?size=100&id=kDMAGBvpqAyW&format=png&color=000000",
                    "reply_markup": {
                        "text": self.strings("open"),
                        "callback": self._handler,
                        "args": (text, target_id),
                        "disable_security": True
                    },
                }
                
            except Exception as e:
                logging.error(f"Whisper Error: {e}")
                return
        
        bot_me = await self.inline.bot.get_me()
        return {
            "title": f"{self.strings('secret_message')}",
            "description": self.strings("no_user_or_message"),
            "message": self.strings("help_message").format(bot=bot_me.username),
            "parse_mode": "HTML",
            "thumb": "https://img.icons8.com/?size=100&id=T9nkeADgD3z6&format=png&color=000000",
        }

    async def _handler(self, call: InlineCall, text: str, for_user_id: int):
        if call.from_user.id == self._tg_id:
            return await call.answer(text, show_alert=True)

        if str(call.from_user.id) == str(for_user_id):
            if call.inline_message_id in self._opened:
                return await call.answer(self.strings("eaten"), show_alert=True)
            
            await call.answer(text, show_alert=True)
            self._opened.append(call.inline_message_id)
            return

        await call.answer(self.strings("not_for_you"), show_alert=True)
