from sqlalchemy import String,Integer , Column , create_engine,ForeignKey,DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker,declarative_base
import os

Base =declarative_base()

DATABASE_URL=os.getenv("DATABASE_URL")
print(DATABASE_URL)
engine=create_engine(DATABASE_URL)
print(engine)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(String,unique=True)
    password_hash=Column(String)
    created_at=Column(DateTime,default=datetime.utcnow)

class Project(Base):
    __tablename__="projects"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    name=Column(String)
    description=Column(String)
    created_at=Column(DateTime,default=datetime.utcnow)

class Conversation(Base):
    __tablename__="conversations"
    id=Column(Integer,primary_key=True)
    project_id=Column(Integer,ForeignKey("projects.id"))
    title=Column(String)
    created_at=Column(DateTime,default=datetime.utcnow)

class Message(Base):
    __tablename__="messages"
    id=Column(Integer,primary_key=True)
    conversation_id=Column(Integer,ForeignKey("conversations.id"))
    content=Column(String)
    timestamp=Column(DateTime,default=datetime.utcnow)

Base.metadata.create_all(engine)