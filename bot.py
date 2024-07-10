import discord
import utils
from audio_player import AudioPlayer
import audio_player
from discord.utils import get
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
import pytube
from discord.ext import tasks
import asyncio
import baa
# note: must install master version from youtube dl manually
# pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz

def init(read_messages: bool=True,join_vc: bool=True):
    intents = discord.Intents.default()
    intents.message_content = read_messages
    intents.voice_states = join_vc
    global client
    client = discord.Client(intents=intents)
    global audioPlayer
    audioPlayer = init_audio_player()
    return client

def init_audio_player():
    return AudioPlayer()

async def process_command(message:discord.Message,command:str,params:list[str]):
    match command:
        case "hello":
            await message.reply("hello!")
        case "baa2eng":
            sent = " ".join(params)
            converted = baa.convertSentence(sent,True)
            await message.reply(f">>> {converted}")
        case "eng2baa":
            sent = "  ".join(params)
            converted = baa.convertSentence(sent,False)
            await message.reply(f">>> {converted}")
        case "join":
            await join_vc(message)
        #case "leave":
        #    await leave_vc(message)
        case "play" | "p":
            await play_audio_vc(message,params)
        case "skip" | "s":
            await skip_audio_vc(message)
        case "stop":
            await stop_audio_vc(message)
        case "q" | "queue":
            await show_queue(message)
        
async def join_vc(message:discord.Message):
    if message.author.voice:
        await message.author.voice.channel.connect()
        return 0
    else:
        await message.reply(">>> please be in vc first so i can join you... ")
        return 1

async def leave_vc(message:discord.Message):
    bot_voice:discord.VoiceClient = message.guild.voice_client
    
    if bot_voice and bot_voice.is_connected():
        await bot_voice.disconnect()
    else:
        await message.reply(">>> im not in vc right now sorry... ")
        
async def play_audio_vc(message:discord.Message,params:list):
    bot_voice:discord.VoiceClient = message.guild.voice_client
    if not bot_voice or not bot_voice.is_connected():
        if await join_vc(message) == 1:
            return

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    
    if len(params) == 0:
        video_link = "https://www.youtube.com/watch?v=qpNHzrM0CKQ"
        params.append(video_link)
        
    for i in params:
        audioPlayer.queue.append(i)
        audioPlayer.queue_titles.append(pytube.YouTube(i).title)
    audioPlayer.last_message = message
    audioPlayer.playing_queue = True
    await message.reply(f">>> adding {len(params)} songs to queue... ")
        
async def skip_audio_vc(message:discord.Message):
    await audio_player.stop_song(audioPlayer.last_message)
    await message.reply(">>> skipping current song... ")

async def stop_audio_vc(message:discord.Message):
    await audio_player.stop_song(audioPlayer.last_message)
    audioPlayer.queue_position = len(audioPlayer.queue)-1
    audioPlayer.playing_queue = False
    await message.reply(">>> stopping playback... ")
    print(audioPlayer.queue_position)

async def show_queue(message:discord.Message):
    if len(audioPlayer.queue) == 0:
        await message.reply(">>> the queue is empty...")
        return
    lower = audioPlayer.queue_position-3
    upper = audioPlayer.queue_position+7
    if lower<0:
        lower = 0
    if upper>(len(audioPlayer.queue)):
        upper = len(audioPlayer.queue)
    response = f">>> queue ({len(audioPlayer.queue)} songs)\n\n"
    for i in range(lower,upper):
        if i==audioPlayer.queue_position:
            response+=f"> #{i}: **[{audioPlayer.queue_titles[i]}]({audioPlayer.queue[i]})**\n"
            continue
        response+=f"#{i}: **[{audioPlayer.queue_titles[i]}]({audioPlayer.queue[i]})**\n"
    await message.reply(response,suppress_embeds=True)
    

@tasks.loop(seconds = 1)
async def audioPlayerUpdate():
    try:
        bot_voice:discord.VoiceClient = audioPlayer.last_message.guild.voice_client
    except:
        return
    if bot_voice is None:
        return
    if not bot_voice.is_connected():
        return
    if not audioPlayer.playing_queue:
        await asyncio.sleep(5)
        while bot_voice.is_playing():
            break
        else:
            while audioPlayer.playing_queue:
                break
            else:
                await bot_voice.disconnect()   
        return
    
    if not bot_voice.is_playing():
        #song has ended, increment queue
        #play next song in queue if available
        
        audioPlayer.increment_queue()
        if audioPlayer.queue_position>(len(audioPlayer.queue)-1):
            audioPlayer.playing_queue = False
            await audioPlayer.last_message.channel.send(f">>> queue has finished playing {len(audioPlayer.queue)} songs...")
            audioPlayer.queue_position-=1
            return
        
        await audio_player.play_song(audioPlayer.last_message,audioPlayer.queue[audioPlayer.queue_position])
        await audioPlayer.last_message.channel.send(f">>> now playing #{audioPlayer.queue_position}: **[{audioPlayer.queue_titles[audioPlayer.queue_position]}]({audioPlayer.queue[audioPlayer.queue_position]})**",suppress_embeds=True)