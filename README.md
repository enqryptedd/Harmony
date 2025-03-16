
# HarmonyPy Discord Library

HarmonyPy is a powerful custom Discord API wrapper for Python to make Discord bot development simpler.

## Features

- Full Discord API coverage
- Object-oriented design
- Event-based architecture
- Support for slash commands and UI components
- Permissions and role management
- Thread creation and management
- Voice support with music playback
- Webhooks integration
- And much more!

## Installation

```bash
git clone https://github.com/enqryptedd/harmony.git

pip install -r requirements.txt
```

## Quick Start

Here's a simple example to get you started with HarmonyPy:

```python
import harmony

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.default())

@bot.event
async def ready():
    print(f"Logged in as {bot.user.username}")

@bot.command()
async def ping(message):
    await message.reply("Pong!")

bot.run("YOUR_TOKEN_HERE")
```

## Creating UI Components

HarmonyPy supports rich Discord UI components:

```python
from harmony.ui import Button, ActionRow

action_row = ActionRow()
action_row.add_component(Button.primary("btn_id", "Click Me"))
action_row.add_component(Button.success("btn_success", "Success"))

await message.channel.send("Interactive message", components=[action_row])
```

## Adding Slash Commands

```python
from harmony.interactions import SlashCommand, InteractionHandler

handler = InteractionHandler(bot)

async def greet_command(ctx, user: str = None):
    await ctx.reply(f"Hello, {user or ctx.user.username}!")

greet = SlashCommand("greet", "Greet a user", greet_command)
greet.add_option(CommandOption("user", "User to greet", CommandOptionType.STRING))

handler.register_command(greet)
await handler.sync_commands()
```

## Voice Support

```python
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
```

## Advanced Features

### Working with Embeds

```python
from harmony.embeds import EmbedBuilder

embed = EmbedBuilder() \
    .set_title("My Embed") \
    .set_description("This is a fancy embed") \
    .set_color(0x3498db) \
    .add_field("Field 1", "Value 1", True) \
    .add_field("Field 2", "Value 2", True) \
    .build()

await message.channel.send(embed=embed)
```

### Creating Threads

```python
from harmony.threads import Thread

thread = await Thread.create(
    channel_id,
    name="Discussion Thread",
    auto_archive_duration=60,
    type=harmony.enums.ChannelType.GUILD_PUBLIC_THREAD
)

await thread.send("This is a new thread!")
```

### Using Webhooks

```python
from harmony.webhooks import Webhook

webhook = await Webhook.create(channel_id, "My Webhook", "https://example.com/avatar.png")

await webhook.send("Message from webhook", username="Custom Name")
```

### Managing Permissions

```python
from harmony.permissions import Permissions

perms = Permissions()
perms.add_permission("SEND_MESSAGES")
perms.add_permission("READ_MESSAGES")

await channel.set_permissions(user_id, perms)
```

## Full Documentation

See the `examples` directory for more detailed examples and use cases.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
