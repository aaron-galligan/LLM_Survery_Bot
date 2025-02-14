"""
3 possible evaluation metrics:

Solution 1. Token Efficiency and Latency Tracking
    Track the number of tokens generated per response and the time taken to generate each response.
    A similar metric is how efficient is the model at answering the users questions, a worse model may need more
    prompting a thus a higher cost, though this metric can be meassured in many ways

Solution 2. Automated LLM-Based Judging System
    Use a second LLM or even the same high-end LLM as an automated judge. After generating a response from
    your survey bot, feed the original question and the generated response into the judge LLM, asking it to 
    rate the answer for, relevance, correctness, completeness, and sentiment of the user.
    Implementation of this solution is very similar to how the score_answer() def has been implemented.

A mix between solution 1 and 2 should give a good picture of how models trade off cost, token efficiency, 
    and response quality 
    
Solution 3. Response Similarity Metrics (BLEU or ROUGE) Across Models
    BLEU (Bilingual Evaluation Understudy) and ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
    A more advanced system that scores and compares outputs from different LLMs given the same inputs.
    A set a questions (relevant to survey and the LLM requirements) would need to be created and used as a benchmark.
    Once a set of models have been evaluated and a range of metrics have been established, then a new model should be 
    able to be run through the benchmark questions and compared to other models.
    
    These were metrics that I have not researched much and would need significantly more time to understand.


A/B testing framework.
    After deployment a portion of queries can be routed to both high-end and budget models, and then take user feedback
    to assess user satisfaction. 
"""
from sqlalchemy.orm import Session
from database import Metrics
from fastapi import Depends
from main import get_db


async def add_metric(response: dict,  response_time: float, db: Session = Depends(get_db)):
    print("Response Evaluation")
    metric = Metrics(
        id = response.id,
        role = response.choices[0].message.role,
        content = response.choices[0].message.content,
        prompt_tokens = response.usage.prompt_tokens,
        completion_tokens = response.usage.completion_tokens,
        total_tokens = response.usage.total_tokens,
        cost = response._hidden_params["response_cost"],
        cost_per_token = (response._hidden_params["response_cost"])/response.usage.total_tokens,
        response_time = response_time
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)

def main():
    print("in llm_elavuation.py main")


if __name__ == "__main__":
    main()
    
















