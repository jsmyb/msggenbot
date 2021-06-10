#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import mkdir, remove
from random import choice, randint
from re import findall, sub

from aiofile import AIOFile
from markovify import NewlineText
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.bot import ChatActionRule

from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def invited(message: Message) -> None:
    """welcome msg."""
    if message.group_id == -message.action.member_id:
        await message.answer(
            """men faq me in de ass"""
        )


@bot.on.chat_message(text=["/сбросs", "/resett"])
async def reset(message: Message) -> None:
    """ok men."""
    peer_id = message.peer_id
    try:
        members = await message.ctx_api.messages.get_conversation_members(
            peer_id=peer_id
        )
    except Exception:
        await message.answer(
            "no admin men, "
            + "giv me admin men."
        )
    else:
        admins = [
            member.member_id for member in members.items if member.is_admin
        ]
        from_id = message.from_id
        if from_id in admins:

            # deleting datebase
            try:
                remove(f"db/{peer_id}.txt")
            except FileNotFoundError:
                pass

            await message.answer(
                f"@id{from_id}, done men."
            )
        else:
            await message.answer(
                "only admins men."
            )


@bot.on.chat_message()
async def talk(message: Message) -> None:

    # ignoring messages from communities 
    if message.from_id > 0:

        text = message.text.lower()

        # deleting empty lines from incoming msg
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")

        # converting [id1|@durov] to @id1
        user_ids = list(set(findall(r"\[id(\d*?)\|.*?]", text)))
        for user_id in user_ids:
            text = sub(rf"\[id{user_id}\|.*?]", f"@id{user_id}", text)

        # mkdir db, if not created
        try:
            mkdir("db")
        except FileExistsError:
            pass

        # recording for DB
        peer_id = message.peer_id
        if text:
            async with AIOFile(f"db/{peer_id}.txt", "a") as f:
                await f.write(f"\n{text}")

        # 5% percentage of sending
        if randint(0, 9) == 0 or @bot.on.chat_message(text=["seqso"]):
            # reading db
            async with AIOFile(f"db/{peer_id}.txt") as f:
                db = await f.read()
            db = db.strip().lower()

            # generating a message 
            text_model = NewlineText(
                input_text=db, well_formed=False, state_size=1
            )
            sentence = text_model.make_sentence(tries=10000) or choice(
                db.splitlines()
            )

            await message.answer(sentence)


if __name__ == "__main__":
    bot.run_forever()
