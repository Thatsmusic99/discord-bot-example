import os
import random

from discord import app_commands, ui, Interaction
from discord.ext.commands import Cog
import discord
import dotenv
from role_select_cog import PronounSelectCog
from discord._types import ClientT


dotenv.load_dotenv()

TEST_SERVER = discord.Object(id=254987557459329025)


class MyClient(discord.ext.commands.Bot):

    def __init__(self):
        intents_list = discord.Intents.default()
        intents_list.message_content = True
        super().__init__(intents=intents_list, command_prefix="$^")


    async def setup_hook(self) -> None:
        await self.add_cog(PronounSelectCog())

        self.tree.copy_global_to(guild=TEST_SERVER)
        await self.tree.sync(guild=TEST_SERVER)


client = MyClient()

SURVEY_CHANNEL = discord.Object(id=738834315462443079)


class Survey(ui.Modal, title="Cool Survey"):
    name = ui.TextInput(label="Name")
    input = ui.TextInput(label="Write something here I guess", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: Interaction) -> None:
        server = client.get_guild(TEST_SERVER.id)
        channel = server.get_channel(SURVEY_CHANNEL.id)

        embed = discord.Embed(title="New survey response!", description=f"Submitted by {interaction.user.mention}")
        embed.add_field(name="Name", value=self.name.value, inline=False)
        embed.add_field(name="Input", value=self.input.value, inline=False)

        await channel.send(embed=embed)
        await interaction.response.send_message("Thank you for filling out the survey!", ephemeral=True)


class NukeServerView(ui.View):

    @ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def confirm_nuke(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Sure thing, nuking server...")

    @ui.button(label="No", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ok! We'll put things off until a later date.")



@client.tree.command(description="Play Rock Paper Scissors against the bot.")
@app_commands.describe(
    item="The item to select."
)
async def rps(interaction: discord.Interaction, item: str):
    valid_items = ["rock", "paper", "scissors"]
    chosen_user_item = item.lower()
    if item not in valid_items:
        await interaction.response.send_message(f"You can't use **{item}**!", ephemeral=True)

    chosen_bot_item = random.choice(valid_items)

    user_item_index = valid_items.index(chosen_user_item)
    bot_item_index = valid_items.index(chosen_bot_item)

    if bot_item_index == user_item_index:
        await interaction.response.send_message(
            f"It's a draw! {interaction.user.mention} picked **{chosen_user_item}**, I picked **{chosen_bot_item}**!")

    # If the user chose the item in front (e.g. bot -> scissors, user -> rock), the user wins
    if valid_items[(bot_item_index + 1) % 3] == item:
        await interaction.response.send_message(
            f"You won! {interaction.user.mention} picked **{chosen_user_item}**, I picked **{chosen_bot_item}**!")
    else:
        await interaction.response.send_message(
            f"You lost! {interaction.user.mention} picked **{chosen_user_item}**, I picked **{chosen_bot_item}**!")


@client.tree.command()
async def embed_demo(interaction: discord.Interaction):
    embed = discord.Embed(title="About user", description=f"Insert description here", color=0xff0000)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.set_footer(text="Insert cool footer here")
    embed.add_field(name="Joined Discord", value=f"<t:{int(interaction.user.created_at.timestamp())}:D>", inline=True)
    embed.add_field(name="Joined Server", value=f"<t:{int(interaction.user.joined_at.timestamp())}:D>", inline=True)

    await interaction.response.send_message(embed=embed)


@client.tree.command()
async def take_survey(interaction: discord.Interaction):
    await interaction.response.send_modal(Survey())


@client.tree.command()
async def nuke_server(interaction: discord.Interaction):
    await interaction.response.send_message("Oh boy, are you sure you want to nuke the server?", view=NukeServerView())


client.run(os.environ["BOT_TOKEN"])
