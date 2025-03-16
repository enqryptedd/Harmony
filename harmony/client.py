
import asyncio
import aiohttp
import json
import logging
import traceback
from typing import Optional, Dict, Any, List, Callable, Union

from .events import EventDispatcher
from .models import User, Guild, Message, Channel

logger = logging.getLogger('harmony')

class MessageSender:
    """Helper class to send messages with components"""

    @staticmethod
    async def send_message(client, channel_id, content=None, embed=None, components=None):
        """Send a message to a channel with components"""
        payload = {}

        if content:
            payload['content'] = content

        if embed:
            payload['embeds'] = [embed]

        if components:
            # Make sure components are dictionaries
            comp_list = []
            for comp in components:
                if hasattr(comp, 'to_dict'):
                    comp_list.append(comp.to_dict())
                elif isinstance(comp, dict):
                    comp_list.append(comp)

            if comp_list:
                payload['components'] = comp_list

        # Send to Discord API
        if hasattr(client, 'rest') and hasattr(client.rest, 'create_message'):
            return await client.rest.create_message(channel_id, payload)
        return None

class Client:
    """Base client for interacting with the Discord API"""

    def __init__(self, intents: int = 0):
        self.token: Optional[str] = None
        self.user: Optional[User] = None
        self.guilds: Dict[str, Guild] = {}
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.heartbeat_interval: Optional[float] = None
        self.sequence: Optional[int] = None
        self.intents = intents

        self.events = EventDispatcher()
        self._ready = asyncio.Event()

    async def login(self, token: str) -> None:
        """Login to Discord with the provided token"""
        self.token = token
        self.session = aiohttp.ClientSession()

        logger.info("Logging in to Discord...")

        # Validate token by making a request to /users/@me
        async with self.session.get(
            'https://discord.com/api/v10/users/@me',
            headers={'Authorization': f'Bot {self.token}'}
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Invalid token (Status: {resp.status})")

            data = await resp.json()
            self.user = User(self, data)

        logger.info(f"Logged in as {self.user.username}#{self.user.discriminator}")

    async def connect(self) -> None:
        """Connect to Discord gateway and start processing events"""
        if not self.token:
            raise Exception("Not logged in")

        gateway_url = "wss://gateway.discord.gg/?v=10&encoding=json"

        async with self.session.ws_connect(gateway_url) as ws:
            self.ws = ws
            await self._gateway_handler()

    async def _gateway_handler(self) -> None:
        """Handle the gateway connection and dispatch events"""
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                op = data['op']

                if op == 10:  # Hello
                    self.heartbeat_interval = data['d']['heartbeat_interval'] / 1000
                    await self._identify()
                    asyncio.create_task(self._heartbeat())

                elif op == 0:  # Dispatch
                    self.sequence = data['s']
                    event_name = data['t']
                    event_data = data['d']

                    await self._handle_dispatch(event_name, event_data)

    async def _identify(self) -> None:
        """Send identify payload to Discord"""
        payload = {
            'op': 2,
            'd': {
                'token': self.token,
                'intents': self.intents,
                'properties': {
                    '$os': 'linux',
                    '$browser': 'harmony',
                    '$device': 'harmony'
                }
            }
        }

        await self.ws.send_json(payload)

    async def _heartbeat(self) -> None:
        """Send regular heartbeats to Discord"""
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            await self.ws.send_json({
                'op': 1,
                'd': self.sequence
            })

    async def _handle_dispatch(self, event_name: str, data: Dict[str, Any]) -> None:
        """Process dispatched events from Discord"""
        if event_name == 'READY':
            self.user = User(self, data['user'])
            for guild_data in data['guilds']:
                guild = Guild(self, guild_data)
                self.guilds[guild.id] = guild

            self._ready.set()
            await self.events.dispatch('ready')

        elif event_name == 'MESSAGE_CREATE':
            message = Message(self, data)
            await self.events.dispatch('message', message)

        elif event_name == 'GUILD_CREATE':
            guild = Guild(self, data)
            self.guilds[guild.id] = guild
            await self.events.dispatch('guild_join', guild)

    async def wait_until_ready(self) -> None:
        """Wait until the client is fully connected and ready"""
        await self._ready.wait()

    def run(self, token: str) -> None:
        """Start the client with the provided token"""
        async def runner():
            try:
                await self.login(token)
                await self.connect()
            finally:
                if self.session:
                    await self.session.close()

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(runner())
        except KeyboardInterrupt:
            logger.info("Client shutting down...")
            loop.run_until_complete(self.close())
        finally:
            loop.close()

    async def close(self) -> None:
        """Close the connection to Discord"""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()

    def event(self, coro: Callable) -> Callable:
        """Decorator to register an event handler"""
        event_name = coro.__name__
        self.events.add_listener(event_name, coro)
        return coro

    async def send_message(self, channel_id: str, content: str) -> Message:
        """Send a message to a channel"""
        async with self.session.post(
            f'https://discord.com/api/v10/channels/{channel_id}/messages',
            headers={'Authorization': f'Bot {self.token}'},
            json={'content': content}
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to send message (Status: {resp.status})")

            data = await resp.json()
            return Message(self, data)


class Bot(Client):
    """Extended client with command handling capabilities"""

    # Static reference to store the current instance
    _current_instance = None

    def __init__(self, command_prefix: str, intents: int = 0):
        super().__init__(intents=intents)
        self.command_prefix = command_prefix
        self.commands = {}

        # Set the current instance
        Bot._current_instance = self

        # Register message handler for commands
        self.events.add_listener('message', self._process_commands)

    def command(self, name: Optional[str] = None):
        """Decorator to register a command"""
        def decorator(func):
            command_name = name or func.__name__
            self.commands[command_name] = func
            return func
        return decorator

    async def _process_commands(self, message: Message):
        """Process messages for command invocation"""
        if not message.content.startswith(self.command_prefix):
            return

        content = message.content[len(self.command_prefix):]
        command_name, *args = content.split()

        if command_name in self.commands:
            command = self.commands[command_name]
            try:
                await command(message, *args)
            except Exception as e:
                logger.error(f"Error executing command {command_name}: {e}")

    async def process_event(self, event_data):
        """Process a Discord gateway event"""
        try:
            if event_data.get('t') == 'READY':
                data = event_data.get('d', {})
                self.user = User(self, data.get('user', {}))
                self.session_id = data.get('session_id')

                self.application_id = data.get('application', {}).get('id')

                # Process guilds
                for guild_data in data.get('guilds', []):
                    self.guilds[guild_data['id']] = Guild(self, guild_data)

                await self.events.emit('ready')

            elif event_data.get('t') == 'MESSAGE_CREATE':
                message_data = event_data.get('d', {})
                message = Message(self, message_data)

                # Check if this is a command
                if message.content.startswith(self.command_prefix):
                    # Extract command name and arguments
                    parts = message.content[len(self.command_prefix):].split()
                    command_name = parts[0].lower()
                    args = parts[1:]

                    # Execute the command if it exists
                    if command_name in self.commands:
                        try:
                            await self.commands[command_name](message, *args)
                        except Exception as e:
                            print(f"Error executing command {command_name}: {e}")
                            traceback.print_exc()

                await self.events.emit('message', message)

            # Handle interaction events
            elif event_data.get('t') == 'INTERACTION_CREATE':
                interaction_data = event_data.get('d', {})
                interaction_type = interaction_data.get('type')

                # Handle component interactions (buttons, select menus)
                if interaction_type == 3:  # MESSAGE_COMPONENT
                    data = interaction_data.get('data', {})
                    custom_id = data.get('custom_id')
                    component_type = data.get('component_type')

                    # Create context for the interaction
                    from harmony.interactions import InteractionContext
                    ctx = InteractionContext(self, interaction_data)
                    
                    # Initialize rest client if not already set
                    if not hasattr(self, 'rest'):
                        from harmony.rest import RESTClient
                        self.rest = RESTClient(self)

                    # Emit component interaction event
                    try:
                        print(f"Processing interaction: {custom_id}, type: {component_type}")
                        await self.events.emit('component_interaction', ctx, custom_id, component_type)
                    except Exception as e:
                        print(f"Error handling component interaction: {e}")
                        import traceback
                        traceback.print_exc()

                # Handle other interaction types
                elif interaction_type == 2:  # APPLICATION_COMMAND
                    # Slash commands
                    await self.events.emit('application_command', interaction_data)
                elif interaction_type == 5:  # MODAL_SUBMIT
                    # Modal submissions
                    await self.events.emit('modal_submit', interaction_data)

            # Handle other event types...
            elif event_data.get('t') == 'GUILD_CREATE':
                guild_data = event_data.get('d', {})
                self.guilds[guild_data['id']] = Guild(self, guild_data)

            # ... more event handling
        except Exception as e:
            logger.error(f"Error processing event: {e}")
