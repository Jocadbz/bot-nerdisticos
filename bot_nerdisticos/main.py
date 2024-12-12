import discord
import os
import sys
from pathlib import Path
from discord.ext import commands
from discord import app_commands


# Check the bot's filesystem
if Path("profile").exists() is False:
    os.makedirs("profile")


# Function to create user's profile (If they exist at all)
def check_user(user_id):
    if Path(f"profile/{user_id}").exists() is False:
        os.makedirs(f"profile/{user_id}")
    if Path(f"profile/{user_id}/score").exists() is False:
        with open(f"profile/{user_id}/score", 'w') as f:
            f.write(0)


def increase_score(user_sent):
    check_user(user_sent)
    current_score = int(open(f"profile/{user_sent}/score", "r+").read()) + 1
    with open(f'profile/{user_sent}/score', 'w') as f:
        f.write(current_score)


def decrease_score(user_sent):
    check_user(user_sent)
    current_score = int(open(f"profile/{user_sent}/score", "r+").read()) - 1
    with open(f'profile/{user_sent}/score', 'w') as f:
        f.write(current_score)


# Starting discord Main functions
TOKEN = sys.argv[1]


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents.all()
client = MyClient(intents=intents)
bot = commands.Bot(command_prefix="nd!", intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    print(f"Logado como {bot.user}")


@bot.event
async def on_message(message):
    check_user(message.author.id)
    await bot.process_commands(message)


@client.tree.context_menu(name='Upvote')
async def upvote(interaction: discord.Interaction, message: discord.Message):
    if message.author == interaction.author:
        await interaction.response.send_message(f'Você não pode upvotar as suas próprias mensagens', ephemeral=True)
        return
    increase_score(message.author.id)
    await interaction.response.send_message(f'Você upvotou a mensagem de {message.author.mention}', ephemeral=True)


@client.tree.context_menu(name='Downvote')
async def downvote(interaction: discord.Interaction, message: discord.Message):
    if message.author == interaction.author:
        await interaction.response.send_message(f'Você não pode downvotar as suas próprias mensagens', ephemeral=True)
        return
    decrease_score(message.author.id)
    await interaction.response.send_message(f'Você downvotou a mensagem de {message.author.mention}', ephemeral=True)


@bot.hybrid_command(name="checkscore", description="Olhe o seu score e o de outros.")
@app_commands.describe(rsuser="O usuário que você quer olhar o score")
async def echo(ctx: commands.Context, rsuser: discord.User | None = None):
    rsuser = rsuser or None
    if rsuser is not None:
        user_sent = rsuser.id
        if bot.get_user(int(rsuser)) is None:
            await ctx.reply(f"Tem certeza de que esse user existe?")
            return
    else:
        user_sent = ctx.author.id
    if user_sent == ctx.author.id:
        await ctx.reply(f"Olá {ctx.author.display_name}, seu score atual é de {open(f'profile/{rsuser}/score', 'r+').read()}.")
    else:
        await ctx.reply(f"O score atual de {bot.get_user(int(rsuser)).display_name} é de {open(f'profile/{rsuser}/score', 'r+').read()}.")


bot.run(TOKEN)
