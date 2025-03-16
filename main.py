
#!/usr/bin/env python3
"""
HarmonyPy example script
"""
import os
import harmony

def main():
    print("HarmonyPy Example")
    print("To use this library in your own bot:")
    
    example_code = """
    import harmony

    bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.default())

    @bot.event
    async def ready():
        print(f"Logged in as {bot.user.username}")

    @bot.command()
    async def ping(message):
        await message.reply("Pong!")

    bot.run("YOUR_TOKEN_HERE")
    """
    
    print(example_code)
    print("\nTo see more examples, check the examples/ directory")

if __name__ == "__main__":
    main()
