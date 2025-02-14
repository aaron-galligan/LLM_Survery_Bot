from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

# Database config
DATABASE_URL = "sqlite:///./SurveryQuestionsDatabase.db"  # SQLite locally stored DB

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    quality_guideline = Column(String, default="")
    score = Column(Integer, default=0)
    
    # Relationship with answers
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String)
    score = Column(Integer, default=0)
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    # Relationship with question
    question = relationship("Question", back_populates="answers") 

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)  # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.now) 

class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(String, primary_key=True, index=True)
    role = Column(String)
    content = Column(String)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_tokens = Column(Integer)
    cost = Column(Integer) #response._hidden_params["response_cost"]
    cost_per_token = Column(Integer)
    response_time = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.now) 



class previous_conversations(Base):
    __tablename__ = "previous conversations"

    id = Column(Integer, primary_key=True, index=True)
    conversation = Column(String)

    user_sentiment_description = Column(String)
    user_sentiment_score = Column(Integer) #score 1 to 5

    timestamp = Column(DateTime, default=datetime.now)