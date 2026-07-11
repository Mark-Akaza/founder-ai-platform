from sqlalchemy.orm import sessionmaker,Session
from dataset_model import engine

sessionLocal=sessionmaker(bind=engine)
def getdb():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
