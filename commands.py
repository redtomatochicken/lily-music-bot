import discord
from discord import app_commands
from discord.ext import commands
import baa

def add_commands(tree: app_commands.CommandTree):
    """
    Adds all commands to the specified command tree.
    :param tree: The tree to add commands to.
    :return: Nothing
    """
    # my dear pookie fish i stole from you
    
    tree.add_command(conversion_group)

class ConversionGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name='convert', description="baaa")

    @app_commands.command(name="baa2eng", description="a")
    @app_commands.describe(string="a")
    async def baa2eng(self, interaction: discord.Interaction, string: str):
        converted = baa.convertSentence(string,True)
        #await message.reply(f">>> {converted}")
        await interaction.response.send_message(f">>> {converted}")
    
    @app_commands.command(name="eng2baa", description="a")
    @app_commands.describe(string="a")
    async def eng2baa(self, interaction: discord.Interaction, string: str):
        converted = baa.convertSentence(string,False)
        #await message.reply(f">>> {converted}")
        await interaction.response.send_message(f">>> {converted}")

conversion_group = ConversionGroup()