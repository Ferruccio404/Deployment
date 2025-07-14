import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import random
from datetime import datetime
import os
import webserver
 
load_dotenv()
car_images = [
    "https://cdn.pixabay.com/photo/2012/05/29/00/43/car-49278_1280.jpg",
    "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604019_1280.jpg",
    "https://cdn.pixabay.com/photo/2014/09/07/21/52/car-438467_1280.jpg",
    "https://cdn.pixabay.com/photo/2015/01/19/13/51/car-604020_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/12/30/07/47/audi-1943237_1280.jpg"
]

token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content=True
intents.members=True

bot = commands.Bot(command_prefix='!', intents=intents)
secrole ="Gamer"
@bot.event 
async def on_ready():
    print(f"Hello Sir We are ready to nuke, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Wellcome to the server Sergant {member.name} ")

@bot.event
async def on_message(message):
      if message.author == bot.user:
        return
      
      content=message.content.lower()
      words=content.split() 

      if "fuck" in content:
        await message.delete()
        await message.channel.send(f"{message.author.mention} Dont use that word Homie ")
        return
      
      if "car" in words:
        image_url=random.choice(car_images)
        await message.channel.send(f"Here's a car for you 🚗{image_url}")
        
      await bot.process_commands(message)

@bot.command()
async def hello(ctx):
   await ctx.send(f" Hello {ctx.author.mention} Sergant!")

@bot.command()
async def time(ctx):
    current_time = datetime.now().strftime("%H:%M:%S")  # 24-hour format
    await ctx.send(f"Hello {ctx.author.mention}, Sergeant! ⏰ Current time is {current_time}")

@bot.command()
async def commands(ctx):
   await ctx.send("Following commands are available \n 1.Hello \n 2.Time \n 3.Assign \n 4.Remove \n 5.DM \n 6.Reply ")

@bot.command()
async def assign(ctx):
   role=discord.utils.get(ctx.guild.roles, name=secrole)
   if role:
      await ctx.author.add_roles(role)
      await ctx.send(f"{ctx.author.mention} is now assigned {secrole} !")
   else:
      await ctx.send("No role")

@bot.command()
async def remove(ctx):
   role=discord.utils.get(ctx.guild.roles, name=secrole)
   if role:
      await ctx.author.remove_roles(role)
      await ctx.send(f"{ctx.author.mention} Had the {secrole} Role, Now removed !")
   else:
      await ctx.send("No role")

@bot.command()
async def dm(ctx, * , msg):
   await ctx.author.send(f"You said {msg} ")

@bot.command()
async def reply(ctx):
   await ctx.reply("This is a reply you asked for")
   
@bot.command()
async def poll(ctx,*,msg):
   embed=discord.Embed(title="New Poll", description=msg)
   poll_message=await ctx.send(embed=embed)
   await poll_message.add_reaction("👍")
   await poll_message.add_reaction("👎")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)