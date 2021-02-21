from discord.ext import commands
import os
from random import randrange
from numpy import loadtxt

class MemeCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('MemeCommands online')

        
    @commands.command()
    async def poggers(self, ctx):
        print('in poggers')
        poggers_image = self.__random_poggers()
        await ctx.send(poggers_image)

    def __random_poggers(self):
        poggers_links = loadtxt("poggers.dat", comments="#", delimiter=",", dtype=str, unpack=False)

        return poggers_links[randrange(len(poggers_links))]

def setup(client):
    client.add_cog(MemeCommands(client))