
from typing import Dict, Any, Optional, List, Union
import json

class RESTClient:
    def __init__(self, client):
        self.client = client
        self.base_url = "https://discord.com/api/v10"

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        return await self._request("GET", f"/users/{user_id}")

    async def get_channel(self, channel_id: str) -> Dict[str, Any]:
        return await self._request("GET", f"/channels/{channel_id}")

    async def get_guild(self, guild_id: str) -> Dict[str, Any]:
        return await self._request("GET", f"/guilds/{guild_id}")

    async def get_guild_channels(self, guild_id: str) -> List[Dict[str, Any]]:
        return await self._request("GET", f"/guilds/{guild_id}/channels")

    async def get_guild_members(self, guild_id: str, limit: int = 1000) -> List[Dict[str, Any]]:
        return await self._request("GET", f"/guilds/{guild_id}/members", params={"limit": limit})

    async def create_message(self, channel_id: str, content: str = None, 
                           embed: Dict[str, Any] = None, embeds: List[Dict[str, Any]] = None,
                           tts: bool = False) -> Dict[str, Any]:
        payload = {}
        if content:
            payload["content"] = content
        if tts:
            payload["tts"] = tts
        if embed:
            payload["embed"] = embed
        if embeds:
            payload["embeds"] = embeds

        return await self._request("POST", f"/channels/{channel_id}/messages", json=payload)

    async def edit_message(self, channel_id: str, message_id: str, content: str = None, 
                         embed: Dict[str, Any] = None, embeds: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {}
        if content:
            payload["content"] = content
        if embed:
            payload["embed"] = embed
        if embeds:
            payload["embeds"] = embeds

        return await self._request("PATCH", f"/channels/{channel_id}/messages/{message_id}", json=payload)

    async def delete_message(self, channel_id: str, message_id: str) -> None:
        await self._request("DELETE", f"/channels/{channel_id}/messages/{message_id}")

    async def bulk_delete_messages(self, channel_id: str, message_ids: List[str]) -> None:
        await self._request("POST", f"/channels/{channel_id}/messages/bulk-delete", json={"messages": message_ids})

    async def create_reaction(self, channel_id: str, message_id: str, emoji: str) -> None:
        import urllib.parse
        emoji = urllib.parse.quote(emoji)
        await self._request("PUT", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me")

    async def delete_reaction(self, channel_id: str, message_id: str, emoji: str, user_id: str = "@me") -> None:
        import urllib.parse
        emoji = urllib.parse.quote(emoji)
        await self._request("DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}")

    async def get_reactions(self, channel_id: str, message_id: str, emoji: str) -> List[Dict[str, Any]]:
        import urllib.parse
        emoji = urllib.parse.quote(emoji)
        return await self._request("GET", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}")

    async def clear_reactions(self, channel_id: str, message_id: str) -> None:
        await self._request("DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions")
    
    async def join_voice_channel(self, guild_id: str, channel_id: str, self_mute: bool = False, self_deaf: bool = False):
        return await self._request("PATCH", f"/guilds/{guild_id}/voice-states/@me", json={
            "channel_id": channel_id,
            "self_mute": self_mute,
            "self_deaf": self_deaf
        })
    
    async def leave_voice_channel(self, guild_id: str):
        return await self._request("PATCH", f"/guilds/{guild_id}/voice-states/@me", json={
            "channel_id": None
        })
    
    async def move_user_to_voice_channel(self, guild_id: str, user_id: str, channel_id: str):
        return await self._request("PATCH", f"/guilds/{guild_id}/voice-states/{user_id}", json={
            "channel_id": channel_id
        })

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        headers = {
            "Authorization": f"Bot {self.client.token}",
            "Content-Type": "application/json"
        }

        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        url = f"{self.base_url}{endpoint}"

        async with self.client.session.request(method, url, headers=headers, **kwargs) as resp:
            if resp.status == 204:
                return None

            if resp.status not in (200, 201, 204):
                error = await resp.text()
                raise Exception(f"API error {resp.status}: {error}")

            return await resp.json()

    async def create_interaction_response(self, interaction_id, interaction_token, data):
        try:
            print(f"Sending interaction response: {interaction_id} {interaction_token}")
            print(f"Response data: {json.dumps(data)}")
            
            async with self.client.session.post(
                f'{self.base_url}/interactions/{interaction_id}/{interaction_token}/callback',
                headers={"Authorization": f"Bot {self.client.token}", "Content-Type": "application/json"},
                json=data
            ) as resp:
                if resp.status not in range(200, 300):
                    error_text = await resp.text()
                    print(f"Error in interaction response: {resp.status} - {error_text}")
                    raise Exception(f"Failed to respond to interaction: {resp.status}")

                try:
                    return await resp.json()
                except:
                    return None
        except Exception as e:
            print(f"Exception in interaction response: {e}")
            raise
