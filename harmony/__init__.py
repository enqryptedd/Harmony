import sys
print("HarmonyPy - A powerful Discord API wrapper for Python", file=sys.stderr)

from .client import Client, Bot
from .models import User, Guild, Message, Channel
from .events import Event, EventDispatcher

class _Enums:
    class ChannelType:
        GUILD_TEXT = 0
        DM = 1
        GUILD_VOICE = 2
        GROUP_DM = 3
        GUILD_CATEGORY = 4
        GUILD_NEWS = 5
        GUILD_STORE = 6
        GUILD_NEWS_THREAD = 10
        GUILD_PUBLIC_THREAD = 11
        GUILD_PRIVATE_THREAD = 12
        GUILD_STAGE_VOICE = 13

    class MessageType:
        DEFAULT = 0
        RECIPIENT_ADD = 1
        RECIPIENT_REMOVE = 2
        CALL = 3
        CHANNEL_NAME_CHANGE = 4
        CHANNEL_ICON_CHANGE = 5
        CHANNEL_PINNED_MESSAGE = 6

    class UserStatus:
        ONLINE = "online"
        IDLE = "idle"
        DND = "dnd"
        INVISIBLE = "invisible"
        OFFLINE = "offline"

    class Intents:
        @staticmethod
        def default():
            return 32767

        @staticmethod
        def all():
            return 131071

        GUILDS = 1 << 0
        GUILD_MEMBERS = 1 << 1
        GUILD_BANS = 1 << 2
        GUILD_EMOJIS = 1 << 3
        GUILD_INTEGRATIONS = 1 << 4
        GUILD_WEBHOOKS = 1 << 5
        GUILD_INVITES = 1 << 6
        GUILD_VOICE_STATES = 1 << 7
        GUILD_PRESENCES = 1 << 8
        GUILD_MESSAGES = 1 << 9
        GUILD_MESSAGE_REACTIONS = 1 << 10
        GUILD_MESSAGE_TYPING = 1 << 11
        DIRECT_MESSAGES = 1 << 12
        DIRECT_MESSAGE_REACTIONS = 1 << 13
        DIRECT_MESSAGE_TYPING = 1 << 14
        MESSAGE_CONTENT = 1 << 15
        GUILD_SCHEDULED_EVENTS = 1 << 16

ChannelType = _Enums.ChannelType
MessageType = _Enums.MessageType
UserStatus = _Enums.UserStatus
Intents = _Enums.Intents

from .ui import (
    Button, ActionRow, SelectMenu, TextInput, Modal,
    UserSelectMenu, RoleSelectMenu, ChannelSelectMenu
)

from .interactions import (
    SlashCommand, CommandOption, CommandOptionType,
    InteractionContext, InteractionHandler
)

from .webhooks import Webhook
from .permissions import Permissions, PermissionOverwrite
from .threads import Thread, ThreadMetadata
from .commands import Command, CommandHandler, CommandContext
from .embeds import EmbedBuilder
from .voice import VoiceClient, AudioSource, FFmpegPCMAudio

__version__ = '0.5.0'