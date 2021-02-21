from discord.ext import commands
from modules.mysql_wrapper import MySqlPoolWrapper
from pypika import Query, Table, Field
from pypika.dialects import SnowflakeQuery
import mysql.connector
import uuid
import os
from random import randrange

class Gamble(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.pool = MySqlPoolWrapper(size=5)
        self.users_table = Table('Users')
        self.points_table = Table('Points')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Gamble online')
        
    @commands.command()
    async def gamble_test(self, ctx):
        print('In gamble test')

    @commands.command(aliases=['play'])
    async def gamble_play(self, ctx):

        cnx = self.pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = SnowflakeQuery.from_(self.users_table).select(self.users_table.star).where(self.users_table.discord_id == str(ctx.message.author.id))
        print(query.get_sql())
        cursor.execute(query.get_sql())
        row = cursor.fetchone()
        print(row)

        if (row is None):
            query = SnowflakeQuery.into(self.users_table).insert(str(uuid.uuid1()), str(ctx.message.author.name), str(ctx.message.author.nick), str(ctx.message.author.id))
            print(query.get_sql())
            cursor.execute(query.get_sql())
            row = cursor.fetchone()
            print(row)

            query = SnowflakeQuery.from_(self.users_table).select(self.users_table.star).where(self.users_table.discord_id == str(ctx.message.author.id))
            print(query.get_sql())
            cursor.execute(query.get_sql())
            row = cursor.fetchone()

            print(row)
            query = SnowflakeQuery.into(self.points_table).insert(row['id'], 1000)
            print(query.get_sql())
            cursor.execute(query.get_sql())

            cnx.commit()
            await ctx.send('Ur points have been set up xd')

        else:
            await ctx.send('U already have points dipshit')

        cnx.close()

    @commands.command(aliases=['gamble'])
    async def gamble_amount(self, ctx, arg1):
        query = SnowflakeQuery.from_(self.users_table).select(self.users_table.id).where(self.users_table.discord_id == str(ctx.message.author.id))
        # print(query.get_sql())
        cnx = self.pool.get_connection()
        print(cnx)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query.get_sql())
        row = cursor.fetchone()
        # print(row)
        user_id = row['id']
        # print(user_id)

        if (str(arg1).upper() == 'ALL'):
            query = SnowflakeQuery.from_(self.points_table).select(self.points_table.star).where(self.points_table.id == str(user_id))
            # print(query.get_sql())
            cursor.execute(query.get_sql())
            row = cursor.fetchone()
            # print(row)
            user_points = int(row['points'])

            # print(user_points)

            randnum = randrange(2)
            if (randnum == 1):
                user_points += user_points
            else:
                user_points -= user_points
                user_points = 0 if user_points < 0 else user_points

            query = SnowflakeQuery.update(self.points_table).set(self.points_table.points, user_points).where(self.points_table.id == str(user_id))
            cursor.execute(query.get_sql())
            await ctx.send('New points {}'.format(user_points))
        else:    
            try:
                gamble_amnt = abs(int(arg1))

                query = SnowflakeQuery.from_(self.points_table).select(self.points_table.star).where(self.points_table.id == str(user_id))
                cursor.execute(query.get_sql())
                row = cursor.fetchone()
                # print(row)
                user_points = int(row['points'])

                print(user_points)
                if gamble_amnt > user_points:
                    await ctx.send('u broke af lmao')
                else:
                    randnum = randrange(2)
                    if (randnum == 1):
                        user_points += gamble_amnt
                    else:
                        user_points -= gamble_amnt
                        user_points = 0 if user_points < 0 else user_points
                    
                    
                    query = SnowflakeQuery.update(self.points_table).set(self.points_table.points, user_points).where(self.points_table.id == str(user_id))
                    # print(query.get_sql())
                    cursor.execute(query.get_sql())
                    await ctx.send('New points {}'.format(user_points))
                        
            except ValueError:
                await ctx.send('not an integer dipshit')

        cnx.commit()
        cnx.close()
        
        
def setup(client):
    client.add_cog(Gamble(client))