from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_ollama import OllamaLLM

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=GEMINI_API_KEY)

add_routes(
    app,
    model,
    path="/gemini"
)

llm = OllamaLLM(model="llama2")

prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me an poem about {topic} with 100 words")

add_routes(
    app,
    prompt1 | model,
    path="/essay"
)

add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)

