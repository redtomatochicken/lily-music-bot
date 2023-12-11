import pytube
import discord

class AudioPlayer:
    def __init__(self,name="lily"):
        self.name = name
        self.queue = []
        self.queue_titles = []
        self.queue_position = -1
        self.playing_queue = False
        self.last_message:discord.Message = None
    def increment_queue(self):
        #print(audioPlayer.queue_position)
        self.queue_position+=1
        
        
async def get_url(video_link):
    Id = video_link.split("v=")[1]
    #stream = pytube.YouTube.from_id(video_id=Id).streams
    itag_list = [141,140,139,251,171,250,249]#These are the lists of itags that can be played by ffmpeg.
    for itag in itag_list:
        try:
            #pytube.YouTube(video_link).title
            audio = pytube.YouTube(video_link).streams.get_by_itag(itag).url#get stream url
            print("itag: " + str(itag))
            return audio
        except AttributeError:#cannot find stream by current itag, as itag not avaliable
            continue
    return "failed"

async def play_song(message, video_link):
    bot_voice = message.guild.voice_client
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    audio = await get_url(video_link)
    print(audio) #prints stream url for debugging

    if audio == "failed":
        await message.reply(f">>> i cant find the song at {video_link}... sorry...")
        return
    source = discord.FFmpegPCMAudio(audio, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
    bot_voice.play(source)
    
    
async def stop_song(message):
    bot_voice:discord.VoiceClient = message.guild.voice_client
    bot_voice.stop()