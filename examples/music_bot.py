
import harmony
import asyncio
import youtube_dl
import os

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(harmony.voice.FFmpegPCMAudio):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume=volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        return cls(data['url'], data=data)

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.all())
queues = {}

@bot.command()
async def join(message):
    if message.author.voice:
        channel = message.author.voice.channel
        voice_client = await channel.connect()
        await message.reply(f"Joined {channel.name}!")
    else:
        await message.reply("You need to be in a voice channel first!")

@bot.command()
async def play(message, url):
    if not message.guild.voice_client:
        await message.reply("I need to join a voice channel first!")
        return
        
    try:
        player = await YTDLSource.from_url(url)
        guild_id = message.guild.id
        
        if guild_id not in queues:
            queues[guild_id] = []
            
        queues[guild_id].append(player)
        
        if not message.guild.voice_client.is_playing():
            await play_next(message)
        else:
            await message.reply(f"Added to queue: {player.title}")
    except Exception as e:
        await message.reply(f"Error: {e}")

async def play_next(message):
    guild_id = message.guild.id
    
    if guild_id in queues and queues[guild_id]:
        player = queues[guild_id].pop(0)
        message.guild.voice_client.play(player, after=lambda e: bot.loop.create_task(play_next(message)))
        await message.channel.send(f"Now playing: {player.title}")

@bot.command()
async def skip(message):
    if message.guild.voice_client and message.guild.voice_client.is_playing():
        message.guild.voice_client.stop()
        await message.reply("Skipped the current song!")
    else:
        await message.reply("Nothing is playing right now!")

@bot.command()
async def queue(message):
    guild_id = message.guild.id
    
    if guild_id not in queues or not queues[guild_id]:
        await message.reply("The queue is empty!")
        return
        
    queue_list = "\n".join([f"{i+1}. {player.title}" for i, player in enumerate(queues[guild_id])])
    await message.reply(f"Current queue:\n{queue_list}")

@bot.command()
async def leave(message):
    if message.guild.voice_client:
        guild_id = message.guild.id
        if guild_id in queues:
            queues[guild_id] = []
            
        await message.guild.voice_client.disconnect()
        await message.reply("Left the voice channel!")
    else:
        await message.reply("I'm not in a voice channel!")

if __name__ == "__main__":
    bot.run("YOUR_TOKEN_HERE")
