import discord
from discord.ext import commands, tasks
from modules.mysql_wrapper import MySqlPoolWrapper
from pypika import Query, Table, Field, Order
from pypika.dialects import SnowflakeQuery
import os

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.pool = MySqlPoolWrapper(size=5)
        self.users_table = Table('Users')
        self.points_table = Table('Points')
        self.periodic_donation.start()

    def cog_unload(self):
        self.periodic_donation.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy online dfadsfadsf')

    @commands.command()
    async def economy_test(self, ctx):
        print('In economy test')

    @tasks.loop()
    async def check_existing_users(self):
        pass

    @commands.command(aliases=['points'])
    async def show_points(self, ctx):
        user_id = ctx.message.author.id
        cnx = self.pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = SnowflakeQuery.from_(self.users_table).select(self.users_table.id, self.users_table.nick, self.users_table.name).where(self.users_table.discord_id == str(user_id))
        print(query.get_sql())
        cursor.execute(query.get_sql())

        row1 = cursor.fetchone()
        print(row1)

        if row1 is not None:
            user_id = row1['id']
            query = SnowflakeQuery.from_(self.points_table).select(self.points_table.star).where(self.points_table.id == str(user_id))
            print(query.get_sql())
            cursor.execute(query.get_sql())
            row2 = cursor.fetchone()
            print(row2)
            points = row2['points']
            # user_name = row1['nick'] if not row1['nick'] == 'None' else row1['name']
            await ctx.send('Points for {}: {}'.format(ctx.message.author.mention, str(points)))
            
        else:
            await ctx.send('Ur not in database yet bitch, sorry havent implemented it ;-; type .play to get points')
            
        cnx.commit()
        cnx.close()

    @commands.command(aliases=['leaderboard'])
    async def display_leaderboard(self, ctx, arg1):
        cnx = self.pool.get_connection()
        try:
            leaderboard_cnt = abs(int(arg1))

            embed = discord.Embed(title=f"__**{ctx.guild.name} Results:**__", color=0x03f8fc,timestamp= ctx.message.created_at)
            
            cursor = cnx.cursor(dictionary=True)
            query = SnowflakeQuery.from_(self.users_table).join(self.points_table).on(self.points_table.id == self.users_table.id).select(self.users_table.nick, self.users_table.name, self.points_table.points).orderby(self.points_table.points, order=Order.desc).limit(leaderboard_cnt)
            print(query.get_sql())
            cursor.execute(query.get_sql())

            rows = cursor.fetchall()

            for i, row in enumerate(rows):  
                name = row['nick'] if not row['nick'] == 'None' else row['name']
                points = row['points']
                embed.add_field(name=f'**{i + 1}. {name}**', value=f'Points: {points}',inline=False)
            
            await ctx.send(embed=embed)

        except ValueError:
            await ctx.send('not an integer dipshit')
        
        cnx.close()
    
    @commands.command()
    async def donate(self, ctx, user: discord.Member, arg1):

        if (ctx.message.author.id == user.id):
            await ctx.send('why are you even trying lmao')
            return

        cnx = self.pool.get_connection()

        try:
            donation_amount = abs(int(arg1))

            user_to_donate_id = user.id
            user_donating_id = ctx.message.author.id 

            cursor = cnx.cursor(dictionary=True)
            query = SnowflakeQuery.from_(self.users_table).select(self.users_table.id).where(self.users_table.discord_id == str(user_to_donate_id))
            cursor.execute(query.get_sql())
            donatee = cursor.fetchone()

            print(query.get_sql())
            print(donatee)

            query = SnowflakeQuery.from_(self.users_table).select(self.users_table.id).where(self.users_table.discord_id == str(user_donating_id))
            cursor.execute(query.get_sql())
            donator = cursor.fetchone()

            print(query.get_sql())
            print(donator)
            

            if (donatee != None):
                donatee_id = donatee['id']
                donator_id = donator['id']

                # query = SnowflakeQuery.from_(self.points_table).select(self.points_table.star).where(self.points_table.id == str(id))
                # donatee_row = cursor.execute(query.get_sql())

                # donatee_points = donatee_row['points']

                query = SnowflakeQuery.from_(self.points_table).select(self.points_table.star).where(self.points_table.id == str(donator_id))
                print(query.get_sql())

                cursor.execute(query.get_sql())
                donator_row = cursor.fetchone()
                print(donator_row)

                donator_points = donator_row['points']
                

                if (donation_amount > donator_points):
                    await ctx.send('lmfao u cant even donate broke bitch')
                else:
                    query = SnowflakeQuery.update(self.points_table).set(self.points_table.points, self.points_table.points + donation_amount).where(self.points_table.id == donatee_id)
                    print(query.get_sql())
                    cursor.execute(query.get_sql())

                    query = SnowflakeQuery.update(self.points_table).set(self.points_table.points, self.points_table.points - donation_amount).where(self.points_table.id == donator_id)
                    print(query.get_sql())
                    cursor.execute(query.get_sql())

                    await ctx.send(f'{ctx.message.author.mention} donated {donation_amount} to {user.mention} can we get a .poggers in the chat')
        except ValueError: 
            await ctx.send('not an integer dipshit')
        
        cnx.commit()
        cnx.close()
    
    ## Update all users points to points + 8
    @tasks.loop(minutes=1.0)
    async def periodic_donation(self):
        print('periodically adding points')
        cnx = self.pool.get_connection()

        cursor = cnx.cursor()
        query = SnowflakeQuery.update(self.points_table).set(self.points_table.points, self.points_table.points + 8)
        cursor.execute(query.get_sql())
        cnx.commit()
        cnx.close()

    ## Wait until client starts up before running periodic donation loop
    @periodic_donation.before_loop
    async def before_periodic_donation(self):
        print('waiting...')
        await self.client.wait_until_ready()

    @commands.command()
    async def test_mention_user(self, ctx, user: discord.Member, arg1):
        print(f'{user.id} {arg1}')
        await ctx.send(user.mention)


def setup(client):
    client.add_cog(Economy(client))