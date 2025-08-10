from typing import Dict, Optional, List
from uuid import UUID

from fastapi import WebSocket

class ConnectionManager:
    """
    Класс для управления активными WebSocket-соединениями.
    """
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, user_uuid: UUID, websocket: WebSocket):
        """
        Принимает новое WebSocket-соединение и добавляет его в список активных.
        """
        await websocket.accept()
        self.active_connections[user_uuid] = websocket

    def disconnect(self, user_uuid: UUID):
        """
        Удаляет соединение из списка активных.
        """
        self.active_connections.pop(user_uuid, None)

    async def send_personal_message(self, message: str, user_uuid: UUID):
        """
        Отправляет сообщение конкретному пользователю.
        """
        if user_uuid in self.active_connections:
            websocket = self.active_connections[user_uuid]
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Отправляет сообщение всем активным соединениям.
        """
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()