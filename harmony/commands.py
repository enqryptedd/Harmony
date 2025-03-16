from typing import Dict, Any, Optional, List, Callable, Awaitable, Union

class CommandContext:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.channel = message.channel if hasattr(message, 'channel') else None
        self.guild = message.guild if hasattr(message, 'guild') else None
        self.author = message.author if hasattr(message, 'author') else None

    async def reply(self, content: str = None, **kwargs):
        if hasattr(self.message, 'reply'):
            return await self.message.reply(content, **kwargs)
        elif hasattr(self.message, 'channel') and hasattr(self.message.channel, 'send'):
            return await self.message.channel.send(content, **kwargs)

class Command:
    def __init__(self, name: str, callback: Callable, description: str = None):
        self.name = name
        self.callback = callback
        self.description = description

    async def invoke(self, ctx: CommandContext, *args, **kwargs):
        return await self.callback(ctx, *args, **kwargs)

class CommandHandler:
    def __init__(self, prefix: str = "!"):
        self.commands: Dict[str, Command] = {}
        self.prefix = prefix

    def register(self, command: Union[Command, str], callback: Optional[Callable] = None, description: str = None):
        if isinstance(command, Command):
            self.commands[command.name] = command
        elif isinstance(command, str) and callback is not None:
            self.commands[command] = Command(command, callback, description)

    async def process_message(self, message):
        if not hasattr(message, 'content') or not message.content.startswith(self.prefix):
            return False

        content = message.content[len(self.prefix):]
        parts = content.split()

        if not parts:
            return False

        command_name = parts[0]
        args = parts[1:]

        if command_name in self.commands:
            ctx = CommandContext(None, message)
            try:
                await self.commands[command_name].invoke(ctx, *args)
                return True
            except Exception as e:
                print(f"Error executing command {command_name}: {e}")
                return False

        return False