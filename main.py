import discord
import datetime
import bot
import utils

TOKEN = "TOKEN"

client = bot.init()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    bot.audioPlayerUpdate.start()

@client.event
async def on_message(message:discord.Message):
    #check who sent the message
    if message.author == client.user:
        return

    msg = message.content
    #bot is invoked with . prefix
    if msg.startswith('.') and len(msg)>1:
        msg = message.content[1:].split()
        command = msg[0]
        params = msg[1:]
        print(f"{utils.get_now()}: command received: {command},  params: {params}")

        await bot.process_command(message,command,params)
    
    #bot is pinged
    elif msg.startswith("<@1183839683130691666>"):
        msg = message.content.split()
        command = msg[1]
        params = msg[2:]
        print(f"{utils.get_now()}: bot pinged command received: {command},  params: {params}")
        
        await bot.process_command(message,command,params)
    

client.run(TOKEN)
