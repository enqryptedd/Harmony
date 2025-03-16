from typing import Dict, List, Callable, Awaitable, Any

class Event:
    def __init__(self, name: str):
        self.name = name
        self.listeners: List[Callable[..., Awaitable[Any]]] = []

    def add_listener(self, callback: Callable[..., Awaitable[Any]]):
        self.listeners.append(callback)

    async def dispatch(self, *args, **kwargs):
        for listener in self.listeners:
            await listener(*args, **kwargs)


class EventDispatcher:
    def __init__(self):
        self.events: Dict[str, Event] = {}

    def add_listener(self, event_name: str, callback: Callable[..., Awaitable[Any]]):
        if event_name not in self.events:
            self.events[event_name] = Event(event_name)

        self.events[event_name].add_listener(callback)

    async def dispatch(self, event_name: str, *args, **kwargs):
        if event_name in self.events:
            await self.events[event_name].dispatch(*args, **kwargs)

    async def emit(self, event_name: str, *args, **kwargs):
        await self.dispatch(event_name, *args, **kwargs)