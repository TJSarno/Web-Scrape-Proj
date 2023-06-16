from discord.ext import commands, tasks
import discord
import datetime
import time
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

#Load in .env variables
cwd = str(Path(__file__).resolve().parent)
env = cwd + "\\.env"
load_dotenv(env)

#Assign .env Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
#CHANNEL_ID = os.environ.get("CHANNEL_ID")

##Testing Channel
CHANNEL_ID = os.environ.get("TEST_CHANNEL")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Time variables
#Left fluff years in case time delta is ever used in the future to make additions.
start_of_day = datetime.datetime(100,1,1, hour= 11, minute= 0, second=0)
end_of_day = datetime.datetime(100,1,1, hour = 20, minute= 0, second=0)

##BOT COMMANDS##
#Disconnect from server
@bot.command()
async def dc(ctx):
    await quit()


##BOT EVENTS##
#Start reminders (happens at set start of day interval)
@tasks.loop(time=start_of_day.time()) #Create the task
async def GoodMorning():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Good morning! May your outlook be empty and your teams chat dead. Take your meds.")
    print("Morning Working")
    if not HourlyReminder.is_running():
        HourlyReminder.start() #If the task is not already running, start it.
        print("Hourly reminder has started")

#Hourly reminder
@tasks.loop(hours = 1)
async def HourlyReminder():   
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Posture, hydration and standup/stretch your wrists check homies <:PatrickPray:879074456528650250>")
    print("reminder sent")

#End reminders (happens at set end of day internal)
@tasks.loop(time=end_of_day.time()) #Create the task
async def GoodNight():
    channel = bot.get_channel(CHANNEL_ID)
    HourlyReminder.stop()
    time.sleep(15)
    await channel.send("Good night! Make sure to go to sleep early, and get enough sleep!")
    print("Night Working")


#EVENT SEMAPHORES#
@bot.event
async def on_ready():
    if not GoodMorning.is_running():
        GoodMorning.start() #If the task is not already running, start it.
        print("Good morning task started")
    if not GoodNight.is_running():
        GoodNight.start() #If the task is not already running, start it.
        print("Good night task started")
    #Set channel ID
    

bot.run(BOT_TOKEN)