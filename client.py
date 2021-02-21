import discord
from discord.ext import commands, tasks
import aiomysql
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix= '.')
# loop = asyncio.get_event_loop()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print('User name: %s, Discord Id: %s' % (message.author.nick, message.author.id))
    print(message.content)
    # print('Discord Guild Id: %s, Discord Id: %s' % (message.author.nick, message.author.id))
    if message.author == client.user:
        return
        
    await client.process_commands(message)

@client.event
async def on_command_error(context, exception):
    if exception.__class__ == discord.ext.commands.errors.MissingRequiredArgument:
        await context.send("Dumbass ur missing an argument to the command.")

for filename in os.listdir('./cogs'):
    if (filename.endswith('.py')) and  not (filename.startswith('__init__')):
        client.load_extension(f'cogs.{filename[:-3]}')

# client.load_extension('cogs.meme_commands')
# client.load_extension('cogs.economy')
# client.load_extension('cogs.gamble')

def main():
    client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == '__main__':
    main()
