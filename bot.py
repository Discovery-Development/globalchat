import discord
from datetime import datetime
import json
import os
import sqlite3


#########################################################################

db = sqlite3.connect("database.db")
cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS userdata(id INT PRIMARY KEY NOT NULL, user INT, color INT, xp INT, messages INT)
""")
db.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS serverdata(guild INT PRIMARY KEY NOT NULL, channel INT NOT NULL)
""")
db.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS bans(user INT PRIMARY KEY NOT NULL, reason TEXT, mod INT, time TEXT)

""")
db.commit()


cur.close()
db.close()

#########################################################################


print("Starting up…")


# Define the bot variable. 
bot = discord.Bot(intents=discord.Intents.all())

def load_token() -> str:
    """
    Returns the token in the config file.
    """

    with open("config.json") as f:
        try:
            config: dict = json.load(f)
            token: str = config["token"]
        except KeyError:
            token: str = None
    return token


# loading all extensions (cogs)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Prints informational text when bot is logged in
@bot.event
async def on_ready():
    print(f"{datetime.now()}: The bot is now logged in as {bot.user}.\n=============================\n")


# Run the bot
try:
    bot.run(load_token())
except Exception as e:
    print(f"We got an error:\n{e}\n\n")