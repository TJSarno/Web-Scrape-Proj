from discord.ext import commands, tasks
import discord
import datetime
import time
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import sys
import subprocess

#Load in .env variables
cwd = str(Path(__file__).resolve().parent)
env = cwd + "\\.env"
load_dotenv(env)

#Assign .env Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
#CHANNEL_ID = os.environ.get("CHANNEL_ID")
#test

##Testing Channel
CHANNEL_ID = os.environ.get("TEST_CHANNEL")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Time variables, set at 9am and 8pm by default
start_hour = 9
end_hour = 20
#Left fluff years in case time delta is ever used in the future to make additions.
start_of_day = datetime.datetime(100,1,1, hour= start_hour, minute= 0, second=0)
end_of_day = datetime.datetime(100,1,1, hour = end_hour, minute= 0, second=0)

start_of_day_task = None

##BOT COMMANDS##
#Disconnect from server
@bot.command()
async def dc(ctx):
    await quit()

@bot.command()
async def restart(ctx):
    await ctx.send("Restarting bot...")
    await restart_bot()

async def restart_bot():
    print("checkpoint 1")
    await asyncio.sleep(1)
    python = sys.executable
    subprocess.Popen([python] + sys.argv)
    await bot.close()
    sys.exit(0)  # Optional, use if necessary
    print("checkpoint 2")

  

@bot.command()
async def update_start_hour(ctx,arg):
    print(arg)
    global start_of_day
    print(start_of_day)
    start_of_day = datetime.datetime(2023,6,19, hour= int(arg), minute= 40, second=0)
    print(start_of_day)

    GoodMorning.restart()
    print("good morning restarted")

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


##EVENT SEMAPHORES##
@bot.event
async def on_ready():
    if not GoodMorning.is_running():
        GoodMorning.start() #If the task is not already running, start it.
        print("Good morning task started")
    if not GoodNight.is_running():
        GoodNight.start() #If the task is not already running, start it.
        print("Good night task started")



##MISC FUNCTIONS##
#Getters and setters for start of day
def get_start_of_day():
    return start_of_day

def set_start_of_day(new_hour):
    start_of_day = datetime.datetime(100,1,1, hour= new_hour, minute= 0, second=0)

#Getters and setters for end of day
def get_end_of_day():
    return end_of_day

def set_end_of_day(new_hour):
    end_of_day = datetime.datetime(100,1,1, hour= new_hour, minute= 0, second=0)


bot.run(BOT_TOKEN)