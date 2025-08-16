from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String, Time, create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy.orm import relationship
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True)
    fullname = Column(String(50), nullable=False)
    location = Column(String,default="Tashkent")
    pr_time = Column(Time, default="07:00:00")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")

    @staticmethod
    def get_all():
        return session.query(User).all()
    
    def save(self, session):
        existing_user = session.query(User).filter_by(chat_id=self.chat_id).first()
        if existing_user:
            return
        session.add(self)
        session.commit()

    @classmethod
    def update(cls, session, chat_id, **kwargs):
        user = session.query(cls).filter(chat_id == cls.chat_id).first()  # None
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            session.commit()
            return True
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.fullname!r})"
    

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.chat_id"))
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="todos")

    @staticmethod
    def add(session, user_id, text):
        todo = Todo(user_id=user_id, text=text)
        session.add(todo)
        session.commit()

    @classmethod
    def delete_all(cls, session):
        session.query(cls).delete()
        session.commit()

    def __repr__(self):
        return self.text
    
def init_db():
    Base.metadata.create_all(bind=engine)
