import os
import time
import openai
import threading
import queue as q
from dotenv import load_dotenv
from fastapi import Request, FastAPI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = API_KEY

def txtResFormat(bot_res):
    res = {"version": "2.0", "template": { 
        "outputs": [
            {
                "simpleText": {
                    "text": bot_res
                }
            }
        ], 
        "quickReplies": []
    }}
    return res

def imgResFormat(bot_res, prompt):
    output_txt = prompt + "내용에 관한 이미지입니다."
    res = {"version": "2.0", "template": {
        "outputs": [
            {
                "simpleImg": {
                    "imgURL": bot_res, "altTxt": output_txt
                }
            }
        ], 
        "quickReplies": []
    }}
    return res

def timeover():
    res = {"version": "2.0", "template": {
        "outputs": [
            {
                "simpleTxt": {
                    "txt": "Creating Image.....\n잠시 후 아래 말풍선 클릭"
                }
            }
        ],
        "quickReplies": [
            {
                "action": "message",
                "label": "done",
                "msgTxt": "You done?"
            }
        ]
    }}
    return res

def getTxtFromGPT(prompt):
    msg_prompt = [{"role": "system", "content": "You are a 어쩌고"}]
    msg_prompt += [{"role": "system", "content": prompt}]
    res = openai.chat.completions.create(model="gpt-4o", msg=msg_prompt)
    
def getImgURLFromDallE(messages):
    res = openai.images.generate(
        model="dall-e-3",
        prompt=messages,
        size="1024x1024",
        quality="standard",
        n=1
    )
    img_url = res.data[0].url
    return img_url

def dbReset(filename):
    with open(filename, 'w') as f:
        f.write("")
        

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "kakaoTest"}

@app.post("/chat/")
async def chat(request: Request):
    kakaoreq = await request.json()
    return mainChat(kakaoreq)


def mainChat(kakaoreq):
    run_flag = False
    start_time = time.time()
    
    cwd = os.getcwd()
    filename = cwd + "/botlog.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")
    else:
        print("File Exists")
        
    res_queue = q.Queue()
    res_res = threading.Thread(target=resOpenAI,
                               args=(kakaoreq, res_queue, filename))
    res_res.start()
    
    while (time.time() - start_time < 3.5):
        if not res_queue.empty():
            res = res_queue.get()
            run_flag =True
            break
        time.sleep(0.01)
        
    if run_flag == False:
        res = timeover()
        
    return res

def resOpenAI(request, res_qeueu, filename):
    if '생각 끝?' in request["userRequest"]["utterance"]:
        with open(filename) as f:
            last_update = f.read()
        if len(last_update.split()) > 1:
            kind = last_update.split()[0]
            if kind == "img":
                bot_res, prompt = last_update.split()[1], last_update.split()[2]
                res_qeueu.put(imgResFormat(bot_res, prompt))
            else:
                bot_res = last_update[4:]
                res_qeueu.put(txtResFormat(bot_res))
            dbReset(filename)
    elif '/img' in request["userRequest"]["utterance"]:
        dbReset(filename)
        prompt = request["userRequest"]["utterance"].replace("/img", "")
        bot_res = getImgURLFromDallE(prompt)
        res_qeueu.put(imgResFormat(bot_res, prompt))
        save_log = "img" + " " + str(bot_res) + " " + str(prompt)
        with open(filename, 'w') as f:
            f.write(save_log)
            
    elif '/ask' in request["userRequset"]["utterance"]:
        dbReset(filename)
        prompt = request["userRequest"]["utterance"].replace("/ask", "")
        bot_res = getTxtFromGPT(prompt)
        res_qeueu.put(txtResFormat(bot_res))
        
        save_log = "ask" + " " + str(bot_res)
        with open(filename, 'w') as f:
            f.write(save_log)
            
    else:
        base_res = {"version": "2.0", "template": {
            "output": [],
            "quickReplies": []
        }}
        res_qeueu.put(base_res)