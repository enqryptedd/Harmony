from typing import Dict, Any, Optional, List
import datetime

class EmbedBuilder:
    def __init__(self):
        self.data = {
            "fields": []
        }

    def set_title(self, title: str) -> 'EmbedBuilder':
        self.data["title"] = title
        return self

    def set_description(self, description: str) -> 'EmbedBuilder':
        self.data["description"] = description
        return self

    def set_url(self, url: str) -> 'EmbedBuilder':
        self.data["url"] = url
        return self

    def set_color(self, color: int) -> 'EmbedBuilder':
        self.data["color"] = color
        return self

    def set_timestamp(self, timestamp: Optional[datetime.datetime] = None) -> 'EmbedBuilder':
        if timestamp is None:
            timestamp = datetime.datetime.now()
        self.data["timestamp"] = timestamp.isoformat()
        return self

    def set_author(self, name: str, url: Optional[str] = None, icon_url: Optional[str] = None) -> 'EmbedBuilder':
        author = {"name": name}
        if url:
            author["url"] = url
        if icon_url:
            author["icon_url"] = icon_url
        self.data["author"] = author
        return self

    def set_footer(self, text: str, icon_url: Optional[str] = None) -> 'EmbedBuilder':
        footer = {"text": text}
        if icon_url:
            footer["icon_url"] = icon_url
        self.data["footer"] = footer
        return self

    def set_image(self, url: str) -> 'EmbedBuilder':
        self.data["image"] = {"url": url}
        return self

    def set_thumbnail(self, url: str) -> 'EmbedBuilder':
        self.data["thumbnail"] = {"url": url}
        return self

    def add_field(self, name: str, value: str, inline: bool = False) -> 'EmbedBuilder':
        self.data["fields"].append({
            "name": name,
            "value": value,
            "inline": inline
        })
        return self

    def build(self) -> Dict[str, Any]:
        return self.data