from enum import Enum
from typing import List, Dict, Any, Optional, Union, Callable


class ButtonStyle(Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class ComponentType(Enum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8


class Button:
    def __init__(self, 
                 custom_id: Optional[str] = None, 
                 label: str = "", 
                 style: int = ButtonStyle.PRIMARY.value,
                 url: Optional[str] = None,
                 emoji: Optional[Dict[str, Any]] = None,
                 disabled: bool = False):
        self.type = ComponentType.BUTTON.value
        self.custom_id = custom_id
        self.label = label
        self.style = style
        self.url = url
        self.emoji = emoji
        self.disabled = disabled

    @classmethod
    def primary(cls, custom_id: str, label: str, disabled: bool = False) -> 'Button':
        return cls(custom_id=custom_id, label=label, style=ButtonStyle.PRIMARY.value, disabled=disabled)

    @classmethod
    def secondary(cls, custom_id: str, label: str, disabled: bool = False) -> 'Button':
        return cls(custom_id=custom_id, label=label, style=ButtonStyle.SECONDARY.value, disabled=disabled)

    @classmethod
    def success(cls, custom_id: str, label: str, disabled: bool = False) -> 'Button':
        return cls(custom_id=custom_id, label=label, style=ButtonStyle.SUCCESS.value, disabled=disabled)

    @classmethod
    def danger(cls, custom_id: str, label: str, disabled: bool = False) -> 'Button':
        return cls(custom_id=custom_id, label=label, style=ButtonStyle.DANGER.value, disabled=disabled)

    @classmethod
    def link(cls, url: str, label: str, disabled: bool = False) -> 'Button':
        return cls(url=url, label=label, style=ButtonStyle.LINK.value, disabled=disabled)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.type,
            "style": self.style,
            "label": self.label,
            "disabled": self.disabled
        }

        if self.custom_id:
            result["custom_id"] = self.custom_id

        if self.url:
            result["url"] = self.url

        if self.emoji:
            result["emoji"] = self.emoji

        return result


class SelectOption:
    def __init__(self, 
                 label: str, 
                 value: str,
                 description: Optional[str] = None,
                 emoji: Optional[Dict[str, Any]] = None,
                 default: bool = False):
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "label": self.label,
            "value": self.value,
            "default": self.default
        }

        if self.description:
            result["description"] = self.description

        if self.emoji:
            result["emoji"] = self.emoji

        return result


class SelectMenu:
    def __init__(self, 
                 custom_id: str,
                 placeholder: Optional[str] = None,
                 min_values: int = 1,
                 max_values: int = 1,
                 disabled: bool = False):
        self.type = ComponentType.SELECT_MENU.value
        self.custom_id = custom_id
        self.options = []
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def add_option(self, 
                  value: str,
                  label: str,
                  description: Optional[str] = None,
                  emoji: Optional[Dict[str, Any]] = None,
                  default: bool = False) -> 'SelectMenu':
        option = SelectOption(label, value, description, emoji, default)
        self.options.append(option)
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "custom_id": self.custom_id,
            "options": [option.to_dict() for option in self.options],
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }


class UserSelectMenu:
    def __init__(self, 
                 custom_id: str,
                 placeholder: Optional[str] = None,
                 min_values: int = 1,
                 max_values: int = 1,
                 disabled: bool = False):
        self.type = ComponentType.USER_SELECT.value
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }


class RoleSelectMenu:
    def __init__(self, 
                 custom_id: str,
                 placeholder: Optional[str] = None,
                 min_values: int = 1,
                 max_values: int = 1,
                 disabled: bool = False):
        self.type = ComponentType.ROLE_SELECT.value
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }


class ChannelSelectMenu:
    def __init__(self, 
                 custom_id: str,
                 placeholder: Optional[str] = None,
                 min_values: int = 1,
                 max_values: int = 1,
                 channel_types: Optional[List[int]] = None,
                 disabled: bool = False):
        self.type = ComponentType.CHANNEL_SELECT.value
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.channel_types = channel_types
        self.disabled = disabled

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.type,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

        if self.channel_types:
            result["channel_types"] = self.channel_types

        return result


class ActionRow:
    def __init__(self, components: List[Any] = None):
        self.type = ComponentType.ACTION_ROW.value
        self.components = components or []

    def add_component(self, component: Any) -> 'ActionRow':
        if not hasattr(self, 'components'):
            self.components = []
        if len(self.components) >= 5:
            raise ValueError("An action row can only contain up to 5 components")
        self.components.append(component)
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "components": [component.to_dict() for component in self.components]
        }


class TextInput:
    SHORT = 1
    PARAGRAPH = 2

    def __init__(self, 
                 custom_id: str,
                 label: str,
                 style: int = SHORT,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 required: bool = True,
                 value: Optional[str] = None,
                 placeholder: Optional[str] = None):
        self.type = ComponentType.TEXT_INPUT.value
        self.custom_id = custom_id
        self.label = label
        self.style = style
        self.min_length = min_length
        self.max_length = max_length
        self.required = required
        self.value = value
        self.placeholder = placeholder

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.type,
            "custom_id": self.custom_id,
            "label": self.label,
            "style": self.style,
            "required": self.required
        }

        if self.min_length is not None:
            result["min_length"] = self.min_length

        if self.max_length is not None:
            result["max_length"] = self.max_length

        if self.value is not None:
            result["value"] = self.value

        if self.placeholder is not None:
            result["placeholder"] = self.placeholder

        return result


class Modal:
    def __init__(self, custom_id: str, title: str, components: List[TextInput] = None):
        self.custom_id = custom_id
        self.title = title
        self.components = []

        if components:
            for component in components:
                row = ActionRow()
                row.add_component(component)
                self.components.append(row)

    def add_component(self, component: TextInput) -> 'Modal':
        row = ActionRow()
        row.add_component(component)
        self.components.append(row)
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "custom_id": self.custom_id,
            "title": self.title,
            "components": [component.to_dict() for component in self.components]
        }