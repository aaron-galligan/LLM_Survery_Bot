from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import database as models 
from database import SessionLocal
from database import Conversation
import llm
from typing import List
from pydantic import BaseModel



# Init database
models.Base.metadata.create_all(bind=models.engine)

app = FastAPI(title="LLM Survey Bot")

# Initialize templates
templates = Jinja2Templates(directory="LLM_Survey_Bot_App/templates")

'''Pydantic models that are used for creating and questions and answers
using the localhost:8000/docs'''
class QuestionCreate(BaseModel):
    question_text: str
    quality_guideline: str = ""

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    quality_guideline: str
    score: int

    class Config:
        orm_mode = True

class AnswerCreate(BaseModel):
    answer_text: str

class AnswerResponse(BaseModel):
    question_id: int
    answer_text: str
    score: int
    feedback: str = ""

# Add new model for chat
class ChatMessage(BaseModel):
    message: str

# Dependency to get the database session, opens and then closes the session after use.
def get_db():
    db = SessionLocal()
    print("Database session opened") 
    try:
        yield db
    finally:
        db.close()
        print("Database session closed")

def add_answer_to_db(question_id: int, answer_text: str, score: int, db: Session):
    """Add an answer to the database"""
    db_answer = models.Answer(
        question_id=question_id,
        answer_text=answer_text,
        score=score
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@app.post("/questions/", response_model=QuestionResponse)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """Create a new survey question"""
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.get("/questions/", response_model=List[QuestionResponse])
async def get_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all survey questions"""
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    return questions

@app.post("/questions/{question_id}/answer", response_model=AnswerResponse)
async def submit_answer(
    question_id: int,
    answer: AnswerCreate,
    db: Session = Depends(get_db)
):
    """Submit and score an answer for a specific question"""
    # Check if the question exists
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Score the answer with llm
    score = await llm.score_answer(answer.answer_text, question_id, db)

    # Use the separate function to add the answer
    
    db_answer = add_answer_to_db(question_id, answer.answer_text, score, db)

    system_message = Conversation(role="system", content= f"The users answer was: '{answer.answer_text}' to the question: '{db_question.question_text}' and the score was: '{score}')")
    db.add(system_message)
    db.commit()
    db.refresh(system_message)

    # Return the response
    return AnswerResponse(
        question_id=question_id,
        answer_text=db_answer.answer_text,
        score=db_answer.score,
        feedback="Answer processed successfully"
    )

@app.post("/chat")
async def chat_with_llm(message: ChatMessage, db: Session = Depends(get_db)):
    """Endpoint for chatting with the LLM
    Add user msg to history,
    Get whole history,
    get response from llm,
    add response to history,
    return response
    """

    user_message = Conversation(role="user", content=message.message)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    conversation_history = db.query(Conversation).all()
    messages = [{"role": entry.role, "content": entry.content} for entry in conversation_history]    
    
    response = await llm.chat_message(messages, db)
    response = response.choices[0].message.content

    assistant_message = Conversation(role="assistant", content=response)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": response}

@app.post("/lowScoreChat")
async def low_score_chat(db: Session = Depends(get_db)):
    print("low score chat")
    system_promt = """
        The users response to a survery question gave a low score, could you gently suggest that the response they gave
        may not address the question best, and give some pointers to how they could give an answer more relevant to the question.
        The previous system prompt was the users response to the survey question."""

    system_message = Conversation(role="system", content= f"{system_promt}")
    db.add(system_message)
    db.commit()
    db.refresh(system_message)

    conversation_history = db.query(Conversation).all()
    messages = [{"role": entry.role, "content": entry.content} for entry in conversation_history]    
    
    response = await llm.chat_message(messages, db)
    response = response.choices[0].message.content

    assistant_message = Conversation(role="assistant", content=response)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": response}

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """For rendering the home page using the index.html template"""
    questions = db.query(models.Question).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "questions": questions}
    )

# Call this function at startup
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    llm.delete_all_answers(db)
    llm.init_conversation(db)
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
