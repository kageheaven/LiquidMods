#          █▄  █ █▀█ ▀█▀ █▀▄ █▀▀ █▄▀ █▀▄▀█ ▄▀█
#          █ ▀ █ █▄█  █  █▄▀ ██▄ █ █ █ ▀ █ █▀█
#                © Copyright 2026
#            ✈ https://t.me/LiquidModules
# meta developer: @LiquidModules
# scope: heroku_only

__version__ = (1, 1, 0)

import contextlib
import logging

from herokutl.tl.types import Message

from heroku import loader, utils

logger = logging.getLogger(__name__)


class EphemeralMod(loader.Module):
    strings = {
        "name": "Ephemeral",
        "unsupported": "<aside>⚠️ This build has no ephemeral support (<code>ephemeral.sendMessage</code>)</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Usage:</aside>\n"
            "<code>.eph &lt;text&gt;</code> — reply to a message: only its author sees it\n"
            "<code>.eph &lt;chat&gt; &lt;user&gt; &lt;text&gt;</code> — chat + recipient"
        ),
        "no_chat": "<aside>❌ Can't resolve chat <code>{}</code></aside>",
        "_cmd_doc_eph": "<text> — ephemeral message, visible only to the author of the message you reply to",
        "no_user": "<aside>❌ Can't resolve user <code>{}</code></aside>",
    }

    strings_ru = {
        "unsupported": "<aside>⚠️ В этой сборке нет поддержки ephemeral (<code>ephemeral.sendMessage</code>)</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Использование:</aside>\n"
            "<code>.eph &lt;текст&gt;</code> — реплаем: видно только автору сообщения\n"
            "<code>.eph &lt;чат&gt; &lt;юзер&gt; &lt;текст&gt;</code> — чат + получатель"
        ),
        "no_chat": "<aside>❌ Не могу найти чат <code>{}</code></aside>",
        "_cmd_doc_eph": "<текст> — ephemeral-сообщение, видно только автору сообщения, на которое ответил",
        "no_user": "<aside>❌ Не могу найти юзера <code>{}</code></aside>",
    }

    strings_ua = {
        "unsupported": "<aside>⚠️ У цій збірці немає підтримки ephemeral (<code>ephemeral.sendMessage</code>)</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Використання:</aside>\n"
            "<code>.eph &lt;текст&gt;</code> — реплаєм: бачить лише автор повідомлення\n"
            "<code>.eph &lt;чат&gt; &lt;юзер&gt; &lt;текст&gt;</code> — чат + отримувач"
        ),
        "no_chat": "<aside>❌ Не можу знайти чат <code>{}</code></aside>",
        "_cmd_doc_eph": "<текст> — ephemeral-повідомлення, бачить лише автор повідомлення, на яке відповів",
        "no_user": "<aside>❌ Не можу знайти юзера <code>{}</code></aside>",
    }

    strings_de = {
        "unsupported": "<aside>⚠️ Dieser Build hat keine Ephemeral-Unterstützung (<code>ephemeral.sendMessage</code>)</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Verwendung:</aside>\n"
            "<code>.eph &lt;Text&gt;</code> — als Antwort: nur der Autor sieht es\n"
            "<code>.eph &lt;Chat&gt; &lt;User&gt; &lt;Text&gt;</code> — Chat + Empfänger"
        ),
        "no_chat": "<aside>❌ Chat <code>{}</code> nicht gefunden</aside>",
        "_cmd_doc_eph": "<Text> — Ephemeral-Nachricht, nur für den Autor der beantworteten Nachricht sichtbar",
        "no_user": "<aside>❌ User <code>{}</code> nicht gefunden</aside>",
    }

    strings_jp = {
        "unsupported": "<aside>⚠️ このビルドは ephemeral (<code>ephemeral.sendMessage</code>) に対応していません</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 使い方:</aside>\n"
            "<code>.eph &lt;テキスト&gt;</code> — 返信: 相手にだけ表示\n"
            "<code>.eph &lt;チャット&gt; &lt;ユーザー&gt; &lt;テキスト&gt;</code> — チャット + 受信者"
        ),
        "no_chat": "<aside>❌ チャット <code>{}</code> が見つかりません</aside>",
        "_cmd_doc_eph": "<テキスト> — ephemeral メッセージ、返信先の相手にだけ表示",
        "no_user": "<aside>❌ ユーザー <code>{}</code> が見つかりません</aside>",
    }

    strings_neofit = {
        "unsupported": "<aside>⚠️ EphemeralSupportError: <code>ephemeral.sendMessage</code> отсутствует в данной сборке</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Usage:</aside>\n"
            "<code>.eph &lt;text&gt;</code> — reply: receiver = message.author\n"
            "<code>.eph &lt;chat&gt; &lt;user&gt; &lt;text&gt;</code> — chat + receiver"
        ),
        "no_chat": "<aside>❌ EntityLookupError: chat <code>{}</code></aside>",
        "_cmd_doc_eph": "<text> — ephemeral message; receiver = author of the replied message",
        "no_user": "<aside>❌ EntityLookupError: user <code>{}</code></aside>",
    }

    strings_tiktok = {
        "unsupported": "<aside>⚠️ В этой сборке ephemeral нет, сорян</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Юзай так:</aside>\n"
            "<code>.eph &lt;текст&gt;</code> — реплай: видит только тот, кому ответил\n"
            "<code>.eph &lt;чат&gt; &lt;юзер&gt; &lt;текст&gt;</code> — чат + чел"
        ),
        "no_chat": "<aside>❌ Чат <code>{}</code> не нашёл</aside>",
        "_cmd_doc_eph": "<текст> — ephemeral, видит только тот, кому ответил",
        "no_user": "<aside>❌ Юзера <code>{}</code> не нашёл</aside>",
    }

    strings_uwu = {
        "unsupported": "<aside>⚠️ This build has no ephemeraw suppowt (<code>ephemeral.sendMessage</code>)</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 Usage:</aside>\n"
            "<code>.eph &lt;text&gt;</code> — wepwy: onwy the authow sees it\n"
            "<code>.eph &lt;chat&gt; &lt;usew&gt; &lt;text&gt;</code> — chat + wecipient"
        ),
        "no_chat": "<aside>❌ Can't find chat <code>{}</code></aside>",
        "_cmd_doc_eph": "<text> — ephemeraw message, visibwe onwy to the authow of the wepwied message",
        "no_user": "<aside>❌ Can't find usew <code>{}</code></aside>",
    }

    strings_leet = {
        "unsupported": "<aside>⚠️ 7h15 bu1ld h45 n0 3ph3m3r4l 5upp0r7 (<code>ephemeral.sendMessage</code>)</aside>",
        "error": "<aside>❌ {}</aside>",
        "eph_usage": (
            "<aside>📖 U54g3:</aside>\n"
            "<code>.eph &lt;73x7&gt;</code> — r3ply: 0nly 7h3 4u7h0r 5335 17\n"
            "<code>.eph &lt;ch47&gt; &lt;u53r&gt; &lt;73x7&gt;</code> — ch47 + r3c31v3r"
        ),
        "no_chat": "<aside>❌ C4n'7 f1nd ch47 <code>{}</code></aside>",
        "_cmd_doc_eph": "<73x7> — 3ph3m3r4l m3554g3, v151bl3 0nly 70 7h3 4u7h0r 0f 7h3 r3pl13d m3554g3",
        "no_user": "<aside>❌ C4n'7 f1nd u53r <code>{}</code></aside>",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def _bot_client(self):
        bot = getattr(getattr(self, "inline", None), "bot", None)
        return getattr(bot, "client", None)

    async def _resolve_peer(self, bot, value):
        for client in (bot, self.client):
            try:
                return await client.get_input_entity(value)
            except Exception:
                continue
        raise ValueError(f"cannot resolve peer: {value}")

    async def _send(self, chat, receiver, html: str) -> bool:
        client = self._bot_client()
        if client is None:
            return False

        try:
            from herokutl.tl.functions.ephemeral import SendMessageRequest
            from herokutl.tl.types import InputRichMessageHTML
        except Exception:
            return False

        peer = await self._resolve_peer(client, chat)
        user = await self._resolve_peer(client, receiver)

        await client(
            SendMessageRequest(
                peer=peer,
                receiver_id=user,
                message="",
                rich_message=InputRichMessageHTML(html=html),
            )
        )
        return True

    @staticmethod
    def _is_peer(ref: str) -> bool:
        ref = (ref or "").strip()
        if not ref:
            return False
        return (
            ref.startswith("@")
            or ref.startswith("https://t.me/")
            or ref.startswith("t.me/")
            or ref.lstrip("-").isdigit()
            or ref.lower() == "me"
        )

    @loader.command()
    async def eph(self, message: Message):
        """<text> — ephemeral message, visible only to the author of the replied message"""
        raw = (utils.get_args_raw(message) or "").strip()
        parts = raw.split(maxsplit=2)
        reply = await message.get_reply_message()

        text = raw
        explicit = len(parts) >= 3 and self._is_peer(parts[0]) and self._is_peer(parts[1])
        two_peers = len(parts) >= 2 and self._is_peer(parts[0]) and self._is_peer(parts[1])

        if two_peers and not explicit:
            await utils.answer(message, self.strings["eph_usage"])
            return

        if explicit:
            chat_ref, user_ref, text = parts[0], parts[1], parts[2]

            try:
                await self.client.get_entity(chat_ref)
            except Exception:
                await utils.answer(
                    message,
                    self.strings["no_chat"].format(utils.escape_html(chat_ref)),
                )
                return

            try:
                await self.client.get_entity(user_ref)
            except Exception:
                await utils.answer(
                    message,
                    self.strings["no_user"].format(utils.escape_html(user_ref)),
                )
                return
        else:
            chat_ref = message.chat_id
            if reply is not None and reply.sender_id:
                user_ref = reply.sender_id
            else:
                user_ref = message.sender_id

        if not text:
            if reply is not None:
                text = reply.raw_text or ""
            if not text:
                await utils.answer(message, self.strings["eph_usage"])
                return

        try:
            ok = await self._send(
                chat_ref,
                user_ref,
                utils.escape_html(text),
            )
        except Exception as e:
            logger.exception("eph failed")
            await utils.answer(
                message, self.strings["error"].format(utils.escape_html(str(e)[:200]))
            )
            return

        if not ok:
            await utils.answer(message, self.strings["unsupported"])
            return

        with contextlib.suppress(Exception):
            await message.delete()
