import discord
from discord.ext import commands
from discord import app_commands
import utils
import assets
import utils
from typing import Optional
from discord.ext.commands import Greedy, Context
from datetime import datetime
start_date = datetime.now()
start_date_pretty = start_date.strftime("%d/%m/%Y %H:%M:%S")
intents = discord.Intents.all()
DEV_GUILD =  discord.Object(id=1038431009676460082) 

# json
jsonreader = utils.load_json(assets.jsonfile)
token = jsonreader["btoken"]
url = jsonreader["burl"]
appid = jsonreader["bappid"]
class lfoxbot(commands.Bot):
    def __init__(self, intents=intents):
        super().__init__(intents=intents, command_prefix=commands.when_mentioned, application_id = appid, description="707's official discord bot.")
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=DEV_GUILD)
    
    async def on_ready(self):
        print("[INFO]    Bot is starting...")
        for extension in assets.modules:
            await bot.load_extension(extension)
            utils.write_log(f"Loaded {extension}")
            print(f"[INFO]    Loaded {extension}")
        print("[INFO]    Bot Loaded all extensions")
        await bot.change_presence(activity=discord.Game(name="May the image generation spirits be with you! || https://little-fox.info"))
        print("[INFO]    Bot custom status updated")
        print("[INFO]    Bot finished starting up!\n")
        print(f"[INFO]    Connected as: {bot.user}\n[INFO]    Invite URL: {url}\n[INFO]    Token: {token}")
        utils.write_log(message=f"Bot started on {start_date_pretty}")

bot = lfoxbot(intents = intents)
"""
*sync -> global sync
*sync guild -> sync current guild
*sync copy -> copies all global app commands to current guild and syncs
*sync delete -> clears all commands from the current guild target and syncs (removes guild commands)
*sync id_1 id_2 -> sync  guilds with 1 and 2
"""


@bot.command(name="synccmd")
@utils.is_bot_admin()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[str] = None) -> None:
    if not guilds:
        if spec == "guild":
            synced = await ctx.bot.tree.sync()
            utils.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator}) Synced commands to the current guild.")
        elif spec == "copy":
            ctx.bot.tree.copy_global_to(guild=DEV_GUILD)
            synced = await ctx.bot.tree.sync()
            utils.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator} Copied commands to the guild.)")
        elif spec == "delete":
            ctx.bot.tree.clear_commands()
            await ctx.bot.tree.sync()
            utils.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator}) Deleted commands from the current guild.")
            synced = []
        else:
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        print(
            f"[INFO]    Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    utils.write_log(f"{ctx.author.id} ({ctx.author.name}#{ctx.author.discriminator} Synced commands globally.)")


bot.run(token)