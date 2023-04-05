import discord
from discord.ext import commands
from discord.app_commands import Choice
from discord import app_commands
import utils
import replicate
import assets

class imgen(commands.Cog):
    """Image generation ai commands for all users"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="generate", description="Generate a image with our AI.")
    @app_commands.describe(aimodel = "What AI model you want to use, different models make different images", imagimation = "Your prompt or the text you want to imagine" )
    @app_commands.choices(aimodel = [
        Choice(name="Stable diffusion", value="stablediff")
    ])
    async def generate(self, interaction : discord.Interaction, aimodel:str, imagimation:str):
        reader = utils.load_json(assets.jsonfile)
        api = reader["reptoken"]
        if aimodel == "stablediff":
            AiGen  = replicate.Client(api_token=api)
            model = AiGen.models.get(name="stability-ai/stable-diffusion")
            version = model.versions.get(id="db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
            await interaction.response.send_message("I will send the result in your dms!", ephemeral=True)
            utils.write_log(message=f"{interaction.user.id} -- {interaction.user.name}#{interaction.user.discriminator} has requested a image on {aimodel} with the prompt {imagimation}")
            output = version.predict(prompt = f"{imagimation}")
            await interaction.user.send(output[0])
        else:
            return await interaction.response.send_message("Sorry no other models are available at the moment.")





async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(imgen(bot))