# LLM-Survey-Bot

## Overview

The LLM Survey Bot is a web application built with FastAPI that leverages a language model (LLM) to facilitate surveys and gather user feedback. The application allows users to interact with the LLM, submit responses, and evaluate the quality of those responses.

## Requirements

To run this application, you need to have Python 3.7 or higher installed. Once the requirements.txt is downloaded you can install the required packages using the following command:

```bash
pip install -r requirements.txt
```

Alternatively use:
```bash
pip install fastapi==0.68.1 uvicorn==0.15.0 sqlalchemy==1.4.23 pydantic==1.8.2 httpx==0.19.0 python-dotenv==0.19.0 jinja2==3.0.1 
```

## Usage


1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/llm_survey_bot.git
   cd llm_survey_bot
   ```
   or use the Github website tools to clone the repository.


2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your environment variables (e.g.,The LiteLLM API key, and api base URL).

3. **Run the Application**:
   Use Uvicorn to run the FastAPI application:
   ```bash
   uvicorn LLM_Survey_Bot_App.main:app --reload
   ```
   or just run using you prefered IED.

4. **Access the Application**:
   Open your web browser and navigate to `http://localhost:8000` to access the application.



## Other useage features

**Access the Application Documentation**
Open your web browser and navigate to `http://localhost:8000/docs` to access the application documentation to add questions and edit the database.


**Changing the model used**
Open the llm.py file, and change the "LITE_LLM_MODEL" variable to the model you want to use. Possible models are:
- openai/gpt-4o
- anthropic/claude-3-sonnet-20240229
- xai/grok-2-latest
- vertex_ai/gemini-1.5-pro
- huggingface/WizardLM/WizardCoder-Python-34B-V1.0
- ollama/llama2
- openrouter/google/palm-2-chat-bison

With more models are offerd by each provider, read more here: https://docs.litellm.ai/docs/providers
