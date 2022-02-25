from discord.ext import commands
import discord

import aiosqlite as sqlite3

from random import uniform as generate_float
from random import choice as generate_choice
from random import randint as generate_int

import functions as func

from secrets import token_urlsafe as generate_id
import json

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_message(self, msg):

        if msg.author == self.bot.user: return
        if msg.author.bot: return

        # if msg.content.startswith("!"):
        #     return
        async with sqlite3.connect("database.db") as db:
            # get ALL channels
            async with db.execute("SELECT channel FROM serverdata") as c:
                channels = await c.fetchall()
                channels = [item[0] for item in channels]
                if not channels:
                    channels = [()]
            # get ALL banned users
            async with db.execute("SELECT user FROM bans") as c:
                bans = await c.fetchall()
                bans = [item[0] for item in bans]
                if not bans:
                    bans = [()]
            if msg.channel.id not in channels:
                return

            if msg.author.id in bans:
                await msg.add_reaction("❌")
                return

            # connect to the db to get user data

            async with db.execute("SELECT user FROM userdata WHERE user = ?", (msg.author.id,)) as c:
                fetch_user = await c.fetchone()
                if not fetch_user:
                    random_color = generate_int(1, 7)
                    random_id = generate_id(5)
                    await db.execute("INSERT INTO userdata(id, user, color, xp, messages) VALUES(?,?,?,?,?)", (random_id, msg.author.id, random_color, 0, 0))
                    await db.commit()
                else:
                    fetch_user = fetch_user[0]
            async with db.execute("SELECT color FROM userdata WHERE user = ?", (msg.author.id,)) as c:
                fetch_color = await c.fetchone()
                fetch_color = fetch_color[0]

            async with db.execute("SELECT xp FROM userdata WHERE user = ?", (msg.author.id,)) as c:
                fetch_xp = await c.fetchone()
                fetch_xp = fetch_xp[0]
            async with db.execute("SELECT messages FROM userdata WHERE user = ?", (msg.author.id,)) as c:
                fetch_messages = await c.fetchone()
                fetch_messages = fetch_messages[0]
            async with db.execute("SELECT id FROM userdata WHERE user = ?", (msg.author.id,)) as c:
                fetch_id = await c.fetchone()
                fetch_id = fetch_id[0]

            async with sqlite3.connect("database.db") as db:
                new_xp = fetch_xp + generate_int(1, 3)
                new_messages = fetch_messages + 1
                await db.execute("UPDATE userdata SET xp = ?, messages = ? WHERE user = ?", (new_xp, new_messages, msg.author.id))
                await db.commit()
            # calculate the level of the user
            fetch_level = func.calc_level(fetch_xp)

            # get the server name
            fetch_server = msg.guild.name

            # get color url and hex code using the function
            color = func.embed_colors(fetch_color)[0]
            color_url = func.embed_colors(fetch_color)[1]


        # get moderators (config file)
        with open("config.json") as f:
            try:
                config: dict = json.load(f)
                mods: list = config["moderators"]
            except KeyError:
                mods: list = []

        # append moderator badge
        if msg.author.id in mods:
            badge = "   <:badge_moderator:946093575710597160>"
        else:
            badge = ''
        
        if msg.attachments:
            attachment = f"\n**Anhang:** {msg.attachments[0]}"
        else:
            attachment = ''
        
        # a little bit buggy
        if msg.reference:
            reply_channel = self.bot.get_channel(msg.reference.channel_id)
            print(reply_channel)
            reply_msg = await reply_channel.fetch_message(msg.reference.message_id)
            print()
            if reply_msg.author is not self.bot.user:
                return
            reply = f"[**Antwort**]({msg.reference.jump_url})\n"
        else:
            reply = ''

        content = (f"――――――――\n{msg.content}")
        await msg.add_reaction("🔄")
        global_embed = discord.Embed()
        global_embed.title = (f"Nachricht{badge}")
        global_embed.description = f"{reply}{content}\n{attachment}"
        global_embed.set_author(icon_url=msg.author.avatar.url, name=msg.author.name)
        global_embed.set_footer(text=f"XP: {fetch_xp}   |  Level: {round(fetch_level['lvl'])} • {fetch_level['text']} \nServer: {fetch_server}\nBenutzer ID: {fetch_id}\nNachrichten: {fetch_messages}")
        global_embed.color = discord.Color(color)
        global_embed.set_image(url=color_url)
        # get the guild_icon and set the icon to the default one if no icon is set.
        try:
            guild_icon = msg.guild.icon.url
        except AttributeError:
            guild_icon = "https://logodownload.org/wp-content/uploads/2017/11/discord-logo-1-1.png"

        global_embed.set_thumbnail(url=guild_icon)
        for channel in channels:
            try:
                load_channel = self.bot.get_channel(channel)
                await load_channel.send(embed=global_embed)
            except:
                # except if a channel does not exist:
                pass
        await msg.delete()
                


def setup(bot):
    bot.add_cog(Listener(bot))