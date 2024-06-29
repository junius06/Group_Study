from fastapi import Request, FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TelegramChatBot"}

@app.post("/chat/")
async def chat(request: Request):
    telegramrequest = await request.json()
    print(telegramrequest)
    return 0