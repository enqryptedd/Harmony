
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

class Model:
    def __init__(self, client, data: Dict[str, Any]):
        self._client = client
        self._update(data)
    
    def _update(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)


class User(Model):
    id: str
    username: str
    discriminator: str
    avatar: Optional[str]
    bot: bool = False
    
    async def send(self, content: str):
        async with self._client.session.post(
            'https://discord.com/api/v10/users/@me/channels',
            headers={'Authorization': f'Bot {self._client.token}'},
            json={'recipient_id': self.id}
        ) as resp:
            channel_data = await resp.json()
            channel_id = channel_data['id']
            
        return await self._client.send_message(channel_id, content)


class Guild(Model):
    id: str
    name: str
    icon: Optional[str]
    owner_id: str
    channels: Dict[str, 'Channel'] = {}
    members: Dict[str, 'Member'] = {}
    
    async def reply(self, content: str = None, embed: Dict[str, Any] = None, components: List[Dict[str, Any]] = None):
        payload = {}
        
        if content:
            payload["content"] = content
            
        if embed:
            payload["embeds"] = [embed]
            
        if components:
            payload["components"] = [comp.to_dict() for comp in components]
        
        channel_id = self.channel_id
        
        async with self._client.session.post(
            f'https://discord.com/api/v10/channels/{channel_id}/messages',
            headers={'Authorization': f'Bot {self._client.token}'},
            json=payload
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to send message (Status: {resp.status})")
            
            data = await resp.json()
            return Message(self._client, data)
    
    async def create_channel(self, name: str, channel_type: int = 0):
        async with self._client.session.post(
            f'https://discord.com/api/v10/guilds/{self.id}/channels',
            headers={'Authorization': f'Bot {self._client.token}'},
            json={'name': name, 'type': channel_type}
        ) as resp:
            data = await resp.json()
            channel = Channel(self._client, data)
            self.channels[channel.id] = channel
            return channel


class Channel(Model):
    id: str
    name: str
    type: int
    guild_id: Optional[str] = None
    
    async def send(self, content: str):
        return await self._client.send_message(self.id, content)
    
    async def connect(self):
        if self.type != 2:  # Voice channel
            raise TypeError("Cannot connect to a non-voice channel")
        
        from harmony.voice import connect_to_voice_channel
        return await connect_to_voice_channel(self)


class Message(Model):
    id: str
    content: str
    author: User
    channel_id: str
    guild_id: Optional[str] = None
    
    def _update(self, data: Dict[str, Any]):
        super()._update(data)
        if 'author' in data:
            self.author = User(self._client, data['author'])
    
    async def reply(self, content: str = None, embed: Dict[str, Any] = None, components: List[Dict[str, Any]] = None):
        payload = {'message_reference': {'message_id': self.id}}
        
        if content:
            payload["content"] = content
            
        if embed:
            payload["embeds"] = [embed]
            
        if components:
            comp_list = []
            for comp in components:
                if hasattr(comp, 'to_dict'):
                    comp_list.append(comp.to_dict())
                elif isinstance(comp, dict):
                    comp_list.append(comp)
            
            if comp_list:
                payload["components"] = comp_list
        
        async with self._client.session.post(
            f'https://discord.com/api/v10/channels/{self.channel_id}/messages',
            headers={'Authorization': f'Bot {self._client.token}'},
            json=payload
        ) as resp:
            if resp.status not in range(200, 300):
                error_text = await resp.text()
                raise Exception(f"Failed to send message (Status: {resp.status}, Error: {error_text})")
            
            data = await resp.json()
            return Message(self._client, data)
    
    async def delete(self):
        async with self._client.session.delete(
            f'https://discord.com/api/v10/channels/{self.channel_id}/messages/{self.id}',
            headers={'Authorization': f'Bot {self._client.token}'}
        ) as resp:
            return resp.status == 204


class Member(Model):
    user: User
    nick: Optional[str] = None
    roles: List[str] = []
    joined_at: str
    voice: Optional[Dict[str, Any]] = None
    
    def _update(self, data: Dict[str, Any]):
        super()._update(data)
        if 'user' in data:
            self.user = User(self._client, data['user'])
    
    @property
    def name(self) -> str:
        return self.nick or self.user.username
