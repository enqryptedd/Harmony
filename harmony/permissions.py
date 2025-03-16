from enum import IntFlag, auto
from typing import Dict, Any, List

from enum import IntFlag

class Permissions:
    def __init__(self):
        self.value = 0

    def add_permission(self, permission_name):
        if hasattr(PermissionFlags, permission_name):
            self.value |= getattr(PermissionFlags, permission_name)

    def remove_permission(self, permission_name):
        if hasattr(PermissionFlags, permission_name):
            self.value &= ~getattr(PermissionFlags, permission_name)

    def has_permission(self, permission_name):
        if hasattr(PermissionFlags, permission_name):
            return (self.value & getattr(PermissionFlags, permission_name)) != 0
        return False

class PermissionFlags(IntFlag):
    CREATE_INSTANT_INVITE = 1 << 0
    KICK_MEMBERS = 1 << 1
    BAN_MEMBERS = 1 << 2
    ADMINISTRATOR = 1 << 3
    MANAGE_CHANNELS = 1 << 4
    MANAGE_GUILD = 1 << 5
    ADD_REACTIONS = 1 << 6
    VIEW_AUDIT_LOG = 1 << 7
    PRIORITY_SPEAKER = 1 << 8
    STREAM = 1 << 9
    VIEW_CHANNEL = 1 << 10
    SEND_MESSAGES = 1 << 11
    SEND_TTS_MESSAGES = 1 << 12
    MANAGE_MESSAGES = 1 << 13
    EMBED_LINKS = 1 << 14
    ATTACH_FILES = 1 << 15
    READ_MESSAGE_HISTORY = 1 << 16
    MENTION_EVERYONE = 1 << 17
    USE_EXTERNAL_EMOJIS = 1 << 18
    VIEW_GUILD_INSIGHTS = 1 << 19
    CONNECT = 1 << 20
    SPEAK = 1 << 21
    MUTE_MEMBERS = 1 << 22
    DEAFEN_MEMBERS = 1 << 23
    MOVE_MEMBERS = 1 << 24
    USE_VAD = 1 << 25
    CHANGE_NICKNAME = 1 << 26
    MANAGE_NICKNAMES = 1 << 27
    MANAGE_ROLES = 1 << 28
    MANAGE_WEBHOOKS = 1 << 29
    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    USE_APPLICATION_COMMANDS = 1 << 31
    REQUEST_TO_SPEAK = 1 << 32
    MANAGE_EVENTS = 1 << 33
    MANAGE_THREADS = 1 << 34
    CREATE_PUBLIC_THREADS = 1 << 35
    CREATE_PRIVATE_THREADS = 1 << 36
    USE_EXTERNAL_STICKERS = 1 << 37
    SEND_MESSAGES_IN_THREADS = 1 << 38
    USE_EMBEDDED_ACTIVITIES = 1 << 39
    MODERATE_MEMBERS = 1 << 40

    @classmethod
    def all(cls):
        return cls(2199023255551)

    @classmethod
    def none(cls):
        return cls(0)


class PermissionOverwrite:
    def __init__(self, allow: int = 0, deny: int = 0):
        self.allow = allow
        self.deny = deny

    @classmethod
    def from_pair(cls, allow: Permissions, deny: Permissions) -> 'PermissionOverwrite':
        return cls(allow=int(allow), deny=int(deny))

    def update(self, **permissions) -> None:
        for permission, value in permissions.items():
            perm_value = getattr(Permissions, permission.upper(), None)

            if perm_value is None:
                raise ValueError(f"Unknown permission: {permission}")

            if value is True:
                self.allow |= perm_value
                self.deny &= ~perm_value
            elif value is False:
                self.allow &= ~perm_value
                self.deny |= perm_value
            else:
                self.allow &= ~perm_value
                self.deny &= ~perm_value

    def to_dict(self) -> Dict[str, int]:
        return {
            "allow": str(self.allow),
            "deny": str(self.deny)
        }