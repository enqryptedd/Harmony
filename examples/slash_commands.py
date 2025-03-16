
import harmony
from harmony.interactions import CommandOption, CommandOptionType

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.default())

@bot.event
async def ready():
    handler = harmony.interactions.InteractionHandler(bot)
    
    async def greet_command(ctx, user=None):
        await ctx.reply(f"Hello, {user or 'there'}!")
    
    greet = harmony.interactions.SlashCommand("greet", "Greet a user", greet_command)
    greet.add_option(
        harmony.interactions.CommandOption("user", "User to greet", 
                                          harmony.interactions.CommandOptionType.STRING)
    )
    
    handler.register_command(greet)
    await handler.sync_commands()
    print("Commands registered!")

if __name__ == "__main__":
    bot.run("YOUR_TOKEN_HERE")
