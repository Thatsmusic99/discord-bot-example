from typing import Any

import discord
from discord._types import ClientT
from discord.ext import commands
from discord import app_commands, Interaction

SHE_ROLE = discord.Object(id=1314632976063004744)
THEY_ROLE = discord.Object(id=1314632944702460066)
HE_ROLE = discord.Object(id=1314632916214485013)


class PronounSelect(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(label="He/Him"),
            discord.SelectOption(label="She/Her"),
            discord.SelectOption(label="They/Them")
        ]
        super().__init__(placeholder="Select your pronouns", min_values=0, max_values=3, options=options)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        guild = interaction.guild
        removing_roles = {
            "He/Him": guild.get_role(HE_ROLE.id),
            "She/Her": guild.get_role(SHE_ROLE.id),
            "They/Them": guild.get_role(THEY_ROLE.id)
        }
        for value in self.values:
            if value in removing_roles:
                role = removing_roles.pop(value)
                await interaction.user.add_roles(role)

        for role in removing_roles.values():
            await interaction.user.remove_roles(role)

        await interaction.response.send_message("Updated your pronouns!", ephemeral=True)


class PronounSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PronounSelect())


class PronounSelectCog(commands.Cog):

    @app_commands.command()
    async def send_pronouns(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pick your pronouns: ", view=PronounSelectView())
