from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from chatbot.chatbot import Chatbot


app = FastAPI()

# 템플릿 엔진 설정
templates = Jinja2Templates(directory="templates")

# 정적 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")


chatbot = Chatbot()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat")
async def chat(request: Request):
    question = request.query_params.get("question")
    return chatbot.answer(question)
