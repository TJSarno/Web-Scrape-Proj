from discord.ext import commands, tasks
import discord
import datetime
import time
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import sys
import subprocess
import pandas as pd

#Load in .env variables
cwd = str(Path(__file__).resolve().parent)
env = cwd + "\\.env"
load_dotenv(env)

#Assign .env Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
#CHANNEL_ID = os.environ.get("CHANNEL_ID")
##Testing Channel
CHANNEL_ID = int(os.environ.get("TEST_CHANNEL"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Read in Codsworth variable csv
csv_path = cwd + "\\csvs\\variables.csv"
df = pd.read_csv(csv_path, header=None)

#Assign start and end times based of the .csv
print(df)
start_hour, start_minute, end_hour, end_minute = df[0]

start_of_day = datetime.time(hour= start_hour, minute= start_minute, second=0)
end_of_day = datetime.time(hour = end_hour, minute= end_minute, second=0)


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

@bot.command()
async def update_schedule(ctx,arg1,arg2,arg3,arg4):
    csv_path = cwd + "\\csvs\\variables.csv"
    #Takes 4 arguments as the two new starting times 9 30 20 00 would update the schedule to 9:30am-8pm
    new_schedule = [int(arg1),int(arg2),int(arg3),int(arg4)]

    df = pd.DataFrame(new_schedule)
    df.to_csv(csv_path, index= False,header= False)

    #Restart thhe bot to reflect new schedule
    await restart_bot()


##BOT EVENTS##
#Schedule message for either morning or evening
async def schedule_message(hour, minute, period):
    #Compare current time with scheudled time and calculate time difference to send message at correct time
    #Currently this always sends a message if started post scheduled time
    now = datetime.datetime.now()
    then = now.replace(hour=hour, minute=minute)
    wait_time = (then-now).total_seconds()
    await asyncio.sleep(wait_time)
    channel = bot.get_channel(CHANNEL_ID)

    #Switch case to select morning or night message/routine
    match period:
        case "morning":
            await channel.send("Good Morning")
            print("Morning Working")
            if not hourly_reminder.is_running():
                hourly_reminder.start() #If the task is not already running, start it.
                print("Hourly reminder has started")
        case "night":
            print("Night Working")
            if hourly_reminder.is_running():
                hourly_reminder.stop() #If the task is not already running, start it.
                print("Hourly reminder has stopped")
                #Small time delay ensure good night message is posted after hourly reminder
                time.sleep(5)
                await channel.send("Good Night")
    
#Hourly reminder
@tasks.loop(hours = 1)
async def hourly_reminder():   
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Posture, hydration and standup/stretch your wrists check homies <:PatrickPray:879074456528650250>")
    print("reminder sent")


##EVENT SEMAPHORES##
@bot.event
async def on_ready():
    await schedule_message(start_hour, start_minute, "morning")
    await schedule_message(end_hour, end_minute, "night")

bot.run(BOT_TOKEN)