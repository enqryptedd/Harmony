
import harmony

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.all())

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
    
    audio_source = harmony.voice.FFmpegPCMAudio(url)
    message.guild.voice_client.play(audio_source)
    await message.reply(f"Now playing: {url}")

@bot.command()
async def leave(message):
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()
        await message.reply("Left the voice channel!")
    else:
        await message.reply("I'm not in a voice channel!")

if __name__ == "__main__":
    bot.run("YOUR_TOKEN_HERE")
