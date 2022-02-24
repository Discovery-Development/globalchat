from discord.commands import slash_command
from discord.ext import commands
from discord.commands import Option

import aiosqlite as sqlite3
from asyncio import sleep
import discord
from datetime import datetime
import json

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # add help embed later
    @slash_command(description="Wie man diesen Bot nutzen tut.", name="help")
    async def help(self, ctx):
        await ctx.respond("Ja.")

    @slash_command(description="Erstelle den GlobalChat-Channel auf diesem Server", name="install")
    async def install(self, ctx, recreate: Option(str, "Falls vorhanden, wird der alte Kanal aus der Datenbank gelöscht und ein neuer erstellt.", choices=["An"], required=False)):
        if not ctx.author.guild_permissions.manage_channels:
            embed = discord.Embed(title="Fehler", color=discord.Color(0xFF431F), description="Du benötigst die Berechtigung, Kanäle zu verwalten.")
            await ctx.respond(embed=embed, ephemeral=True)
            return
        async with sqlite3.connect("database.db") as db:

            async with db.execute("SELECT * FROM serverdata WHERE guild = ?", (ctx.guild.id,)) as c:
                fetch_guild = await c.fetchone()
            if recreate == "An":
                pass
            else:
                if fetch_guild is not None:
                    embed = discord.Embed(title="Hinweis", color=discord.Color(0xFF9531), description="Es befindet sich bereits ein Channel in der Datenbank. Bitte nutze die Option `recreate`, um den Channel neu zu erstellen und den alten aus meiner Datenbank zu entfernen.")
                    await ctx.respond(embed=embed)
                    return
            
            category = ctx.channel.category
            created_channel = await ctx.guild.create_text_channel(name="🌍-globalchat", category=category)
            
            # add the channel to the database
            
            await db.execute("INSERT OR REPLACE INTO serverdata(guild,channel) VALUES(?,?)", (ctx.guild.id, created_channel.id))
            await db.commit()
            await ctx.respond(created_channel.mention, ephemeral=True)
            async with created_channel.typing():
                await sleep(2)
            embed = discord.Embed(color=0xB1FF1F, title="Willkommen", description=f"Ich freue mich sehr, dass **`{ctx.guild.name}`** nun dem Globalen Chat beigetreten ist.")
            embed.set_footer(text="Sag 'Hallo' zu den anderen!")
            await created_channel.send(embed=embed)
            await created_channel.edit(position=1, sync_permissions=True, slowmode_delay=3, topic="🌍 In diesem Channel kann mit anderen Mitgliedern über Servern hinweg geschrieben werden.\n**REGELN:**\n"+"""
            
            • Kein Spam
            • Keine Beleidigungen
            • Kein NSFW
            • Keine Werbung

-> Hinweis an Moderatoren: Bitte lasst den Slowmode bei mindestens 3 Sekunden, um eine Überlastung des Bots zu vermeiden.
            
            """)
    @slash_command(description="Bannt einen User von dem Globalen Chat", name="ban")
    async def ban(self, ctx, user: Option(discord.Member, "Welcher Nutzer gebannt werden soll."), reason: Option(str, "Der Grund für den Ban", default="Kein Grund angegeben", required=False)):
        # create a function later for fetching moderators
        with open("config.json") as f:
            try:
                config: dict = json.load(f)
                mods: list = config["moderators"]
            except KeyError:
                mods: list = []
        if not ctx.author.id in mods:
            embed = discord.Embed(title="Fehler", color=discord.Color(0xFF431F), description="Du bist kein Bot-Moderator. Es ist nötig, Bot-Moderator zu sein, um Benutzer im GlobalChat zu bannen.")
            await ctx.respond(embed=embed, ephemeral=True)
            return
        
        async with sqlite3.connect("database.db") as db:

            async with db.execute("SELECT user FROM bans WHERE user = ?", (user.id,)) as c:
                fetch_user = await c.fetchone()
                if not fetch_user:
                    fetch_user = (0,)
            if user.id in fetch_user:
                embed = discord.Embed(title="Fehler", color=discord.Color(0xFF431F), description="Dieser Nutzer ist bereits gebannt.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            embed = discord.Embed(color=discord.Color(0xB1FF1F), title="User gebannt", description=f"**`Benutzer`** {user.mention}\n**`Moderator:`** {ctx.author.mention}\
                \n**`Grund:`** {reason}")
            await db.execute("INSERT INTO bans(user,reason,mod,time) VALUES(?,?,?,?)", (user.id, reason, ctx.author.id, datetime.utcnow()))
            await db.commit()
            await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(MainCog(bot))