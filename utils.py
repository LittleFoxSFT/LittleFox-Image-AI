import json
import aiosqlite
import discord
from discord import app_commands
import sqlite3
from datetime import datetime
logname = datetime.now()
logname_pretty = logname.strftime("%d-%m-%Y")
logname_file = str(logname_pretty)
curremt_time = datetime.now()
current_time_fancy = curremt_time.strftime("%d-%m-%Y-%H:%M:%S")


def load_json(filepath):
    """Load json file and return"""
    with open(filepath) as f:
        return json.load(f)

async def connectdb(path):
    """Database connection"""
    return await aiosqlite.connect(path)


def write_log(message):
    with open(f"./logs/{logname_file}.log", "a+") as f:
        f.write(message + "\n")
        f.close()
    print("[INFO]    Saved log")


def is_bot_admin():
    async def predicate(interaction: discord.Interaction):
        if is_bot_developer(interaction.user.id):
            return True
    return app_commands.check(predicate)


def is_bot_developer(member_id):
    database = sqlite3.connect("./database.db")
    try:
        listdevs = database.execute(
            f"SELECT * FROM botdevs WHERE userid = {member_id}")
        returndevs = listdevs.fetchall()
        if not returndevs:
            database.close()
            return False
        else:
            database.close()
            return True
    except ValueError:
        pass