from fastapi import FastAPI,Depends,HTTPException,WebSocket
import redis
import dataset_model
from sqlalchemy.orm import sessionmaker,Session
from dataset_model import engine,User
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime,timedelta
from app.routers.chat import router as websocket_router


SessionLocal=sessionmaker(bind=engine)

key="my-name-is-karam"
algorithim="HS256"
access_time=30

def createaccesstoken(data:dict):
   expiry=datetime.utcnow()+timedelta(minutes=access_time)
   to_encode=data.copy()
   to_encode.update({"exp":expiry})
   token=jwt.encode(to_encode,key,algorithim)
   return token

def getdb():
 db=SessionLocal()
 try:
    yield db
 finally:
    db.close()


app=FastAPI()

app.include_router(websocket_router)

@app.get("/")
def read_root():
    return{"message":"hi from Docker"}

@app.post("/signup")
def signup(username:str,email:str,password:str,db:Session=Depends(getdb)):
   hash_password=bcrypt.hash(str(password))
   new_user=User(name=username,email=email,password_hash=hash_password)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return{"id":new_user.id,"email":new_user.email,"username":new_user.name,"created_at":new_user.created_at,"password":new_user.password_hash}


@app.post("/login")
def login(password:str,email:str,db:Session=Depends(getdb)):
   
   user=db.query(User).filter(User.email== email).first()
   
   if not user :
      raise HTTPException(status_code=401,detail="User not found")
   
   verify=bcrypt.verify(password,user.password_hash)
   
   if not verify:
      raise HTTPException(status_code=401,detail="invalid password")
   
   token=createaccesstoken({"sub":user.name})

   return{
      "access_token":token,
       "token_type":"bearer"
   }

@app.websocket("/websockets")
async def websocket_endpoint(websocket:WebSocket):
   await websocket.accept()
   while True:
      message=await websocket.receive_text()
      await websocket.send_text(f"you send message:{message}")












