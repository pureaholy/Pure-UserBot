import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.filters import command
from utils.misc import modules_help
from utils.scripts import with_reply


@Client.on_message(~filters.scheduled & command("del") & filters.me & ~filters.forwarded)
async def del_msg(_, message: Message):
    await message.delete()
    await message.reply_to_message.delete()


@Client.on_message(~filters.scheduled & command("purge") & filters.me & ~filters.forwarded)
@with_reply
async def purge(client: Client, message: Message):
    chunk = []
    async for msg in client.get_chat_history(
        chat_id=message.chat.id,
    ):
        if msg.id < message.reply_to_message.id:
            break
        chunk.append(msg.id)
        if len(chunk) >= 100:
            await client.delete_messages(message.chat.id, chunk)
            chunk.clear()
            await asyncio.sleep(1)

    if chunk:
        await client.delete_messages(message.chat.id, chunk)


module = modules_help.add_module("purge", __file__)
module.add_command(
    "purge", "Purge (delete all messages) chat from replied message to last", "[reply]"
)
module.add_command("del", "Delete replied message", "[reply]")
