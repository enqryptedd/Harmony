
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
    
    @staticmethod
    def default():
        return (
            Intents.GUILDS |
            Intents.GUILD_BANS |
            Intents.GUILD_EMOJIS |
            Intents.GUILD_INTEGRATIONS |
            Intents.GUILD_WEBHOOKS |
            Intents.GUILD_INVITES |
            Intents.GUILD_VOICE_STATES |
            Intents.GUILD_MESSAGES |
            Intents.GUILD_MESSAGE_REACTIONS |
            Intents.GUILD_MESSAGE_TYPING |
            Intents.DIRECT_MESSAGES |
            Intents.DIRECT_MESSAGE_REACTIONS |
            Intents.DIRECT_MESSAGE_TYPING
        )
    
    @staticmethod
    def all():
        return (
            Intents.default() |
            Intents.GUILD_MEMBERS |
            Intents.GUILD_PRESENCES |
            Intents.MESSAGE_CONTENT |
            Intents.GUILD_SCHEDULED_EVENTS
        )
