from enum import Enum
from typing import Optional, Dict, Any, List, Callable, Union


class CommandOptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class CommandOption:
    def __init__(self, name: str, description: str, option_type: CommandOptionType, required: bool = False):
        self.name = name
        self.description = description
        self.type = option_type
        self.required = required
        self.choices = []
        self.options = []

    def add_choice(self, name: str, value: Union[str, int, float]) -> 'CommandOption':
        self.choices.append({
            'name': name,
            'value': value
        })
        return self

    def add_option(self, option: 'CommandOption') -> 'CommandOption':
        self.options.append(option)
        return self

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'description': self.description,
            'type': self.type.value,
            'required': self.required
        }

        if self.choices:
            result['choices'] = self.choices

        if self.options:
            result['options'] = [option.to_dict() for option in self.options]

        return result


class SlashCommand:
    def __init__(self, name: str, description: str, callback: Callable):
        self.name = name
        self.description = description
        self.callback = callback
        self.options = []

    def add_option(self, option: CommandOption) -> 'SlashCommand':
        self.options.append(option)
        return self

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'name': self.name,
            'description': self.description,
            'type': 1
        }

        if self.options:
            result['options'] = [option.to_dict() for option in self.options]

        return result


class InteractionContext:
    def __init__(self, bot, interaction_data):
        self.bot = bot
        self.interaction_id = interaction_data.get('id')
        self.application_id = interaction_data.get('application_id')
        self.type = interaction_data.get('type')
        self.data = interaction_data.get('data', {})
        self.guild_id = interaction_data.get('guild_id')
        self.channel_id = interaction_data.get('channel_id')
        self.member = interaction_data.get('member', {})
        self.user = interaction_data.get('user', self.member.get('user', {}))
        self.token = interaction_data.get('token')
        self.version = interaction_data.get('version')
        self.message = interaction_data.get('message')
        self.locale = interaction_data.get('locale')
        self.guild_locale = interaction_data.get('guild_locale')

    async def reply(self, content=None, embeds=None, components=None, ephemeral=False) -> None:
        payload = {}

        if content:
            payload['content'] = content

        if embeds:
            payload['embeds'] = embeds if isinstance(embeds, list) else [embeds]

        if components:
            comp_list = []
            for comp in components:
                if hasattr(comp, 'to_dict'):
                    comp_list.append(comp.to_dict())
                elif isinstance(comp, dict):
                    comp_list.append(comp)

            if comp_list:
                payload['components'] = comp_list

        if ephemeral:
            payload['flags'] = 64

        if not hasattr(self.bot, 'rest'):
            from harmony.rest import RESTClient
            self.bot.rest = RESTClient(self.bot)

        try:
            await self.bot.rest.create_interaction_response(
                self.interaction_id,
                self.token,
                {
                    'type': 4,
                    'data': payload
                }
            )
        except Exception as e:
            print(f"Error in interaction reply: {e}")
            import traceback
            traceback.print_exc()

    async def defer(self, ephemeral: bool = False) -> None:
        payload = {
            "type": 5,
            "data": {
                "flags": 64 if ephemeral else 0
            }
        }

        await self.bot.rest.create_interaction_response(
            self.interaction_id,
            self.token,
            payload
        )

    async def show_modal(self, modal) -> None:
        await self.bot.rest.create_interaction_response(
            self.interaction_id,
            self.token,
            {
                'type': 9,
                'data': modal.to_dict()
            }
        )


class InteractionHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}

        @bot.event
        async def interaction_create(interaction_data):
            await self.handle_interaction(interaction_data)

    def register_command(self, command: SlashCommand) -> None:
        self.commands[command.name] = command

    async def sync_commands(self, guild_id: Optional[str] = None) -> None:
        commands_data = [command.to_dict() for command in self.commands.values()]

        if guild_id:
            await self.bot.rest.bulk_overwrite_guild_application_commands(
                self.bot.application_id,
                guild_id,
                commands_data
            )
        else:
            await self.bot.rest.bulk_overwrite_global_application_commands(
                self.bot.application_id,
                commands_data
            )

    async def handle_interaction(self, interaction_data: Dict[str, Any]) -> None:
        interaction_type = interaction_data.get('type')

        if interaction_type == 2:
            await self.handle_application_command(interaction_data)
        elif interaction_type == 3:
            await self.handle_component_interaction(interaction_data)
        elif interaction_type == 5:
            await self.handle_modal_submit(interaction_data)

    async def handle_application_command(self, interaction_data: Dict[str, Any]) -> None:
        command_name = interaction_data.get('data', {}).get('name')
        options = interaction_data.get('data', {}).get('options', [])

        if command_name in self.commands:
            command = self.commands[command_name]
            ctx = InteractionContext(self.bot, interaction_data)

            kwargs = {}
            for option in options:
                kwargs[option['name']] = option['value']

            await command.callback(ctx, **kwargs)

    async def handle_component_interaction(self, interaction_data: Dict[str, Any]) -> None:
        custom_id = interaction_data.get('data', {}).get('custom_id')
        component_type = interaction_data.get('data', {}).get('component_type')

        ctx = InteractionContext(self.bot, interaction_data)

        await self.bot.events.emit('component_interaction', ctx, custom_id, component_type)

    async def handle_modal_submit(self, interaction_data: Dict[str, Any]) -> None:
        custom_id = interaction_data.get('data', {}).get('custom_id')
        components = interaction_data.get('data', {}).get('components', [])

        values = {}
        for action_row in components:
            for component in action_row.get('components', []):
                values[component.get('custom_id')] = component.get('value')

        ctx = InteractionContext(self.bot, interaction_data)

        await self.bot.events.emit('modal_submit', ctx, custom_id, values)