from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException

from src.api.dependencies.token_dependency import get_current_user
from src.api.schemas import UserRead

websocket_router = APIRouter(tags=["Websockets"])

@websocket_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: UUID, current_user: Annotated[UserRead, Depends(get_current_user)]):
    if user_id != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")