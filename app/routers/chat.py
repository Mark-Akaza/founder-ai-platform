from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Depends
from app.services.gemini_services import gen_response
from pydantic import BaseModel
from app.services.embedding_service import gen_embeddings
from app.database.database import getdb
from sqlalchemy.orm import Session
from dataset_model import Message
router = APIRouter()


full_resposne=""
@router.websocket("/ws/chat")
async def websocket_connection(websocket:WebSocket,db:Session=Depends(getdb)):
    await websocket.accept()
    try:
       user_message=await websocket.receive_text()
       user_embeddings=gen_embeddings(user_message)
       message=Message(sender="user",content=user_message,embedding=user_embeddings)
       db.add(message)
       db.commit()

       full_response=""
       async for chunks in gen_response(user_message):
           full_response+=chunks
           await websocket.send_text(chunks)
       await websocket.send_text("[DONE]")
       assistant_embeddings=gen_embeddings(full_response)
       message=Message(sender="assistant",content=full_response,embedding=assistant_embeddings)
       db.add(message)
       db.commit()
    except WebSocketDisconnect:
        print("CLient Disconnected")

       

