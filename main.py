from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from chatbot.chatbot import Chatbot


app = FastAPI()

templates = Jinja2Templates(directory="templates")

chatbot = Chatbot()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question")
    return { "message": chatbot.answer(question)}
