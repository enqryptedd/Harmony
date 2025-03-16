import harmony

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.default())

@bot.event
async def ready():
    print(f"Logged in as {bot.user.username}")

@bot.command()
async def ping(message):
    await message.reply("Pong!")

if __name__ == "__main__":
    bot.run("YOUR_TOKEN_HERE")
