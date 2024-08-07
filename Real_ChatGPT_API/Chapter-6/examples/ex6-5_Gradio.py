import os
import openai
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
# from langchain.chains import retrieval_qa
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from collections import Counter
from dotenv import load_dotenv

# API_KEY from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env', 'dev.env'))
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

# Data directory path
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

loader = DirectoryLoader(data_dir, glob="*.txt", loader_cls=TextLoader)
documents = loader.load()
print('문서의 개수 : ', len(documents))

print('1번 문서 : ', documents[1])
print('-' * 20)
print('1번 문서 : ', documents[21])
print('-' * 20)

# 6-2. 텍스트 분할하기
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

print('분할된 텍스트의 개수 : ', len(texts))
print(texts[0])

source_lst = []
for i in range(0, len(texts)):
    source_lst.append(texts[i].metadata['source'])
    
element_counts = Counter(source_lst)
filtered_counts = {key: value for key, value in element_counts.items() if value >= 2}
print('2개 이상으로 분할된 문서 :', filtered_counts)
print('분할된 텍스트의 개수 : ', len(documents) + len(filtered_counts))

# 6-3. ChromaDB를 이용한 검색기 사용하기
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embedding)
retriever = vectordb.as_retriever()
docs = retriever.get_relevant_documents("신혼부부를 위한 정책이 있어?")
print('유사도가 높은 텍스트 개수 : ', len(docs))
print('--' * 20)
print('유사도가 높은 텍스트 중 첫 번째 텍스트 출력 : ', docs[0])
print('--' * 20)
print('유사도가 높은 텍스트들의 문서 출처 : ')
for doc in docs:
    print(doc.metadata["source"])
    
retriever = vectordb.as_retriever(search_kwargs={"k": 2})
docs = retriever.get_relevant_documents("신혼부부를 위한 정책이 있어?")

for doc in docs:
    print(doc.metadata["source"])
    
# 6-4. 질문으로부터 답변 얻기
qa_chain = RetrievalQA.from_chain_type( # retrieval_qa.from_chain_type()
    llm = ChatOpenAI(model_name = "gpt-4o", temperature=0),
    chain_type="stuff",
    retriever = retriever,
    return_source_documents = True
)

input_text = "대출과 관련된 정책이 궁금합니다."
chatbot_response = qa_chain(input_text)
print(chatbot_response)
print(chatbot_response)

def get_chatbot_response(chatbot_response):
    print(chatbot_response['result'].strip())
    print('\n문서 출처 : ')
    for source in chatbot_response["source_documents"]:
        print(source.metadata['source'])
        
print(chatbot_response)

# 6-5. Gradio로 챗봇의 UI 만들기
import gradio as gr

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="청년정책챗봇")
    msg = gr.Textbox(label="질문해주세요!")
    clear = gr.Button("대화 초기화")
    
    # 챗봇 답변 처리 함수
    def  respond(message, chat_history):
        result = qa_chain(message)
        bot_message = result['result']
        bot_message += ' # sources : '
        
        # 답변의 출처 표기
        for i, doc in enumerate(result['source_documents']):
            bot_message += '[' + str(i+1) + '] ' + doc.metadata['source'] + ' '
            
        # 채팅 기록에 사용자의 메세지와 봇의 응답 추가
        chat_history.append((message, bot_message))
        return "", chat_history
    
    # 사용자의 입력을 제출(submit)하면 respond 함수 호출
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    
    # '초기화' 버튼을 클릭하면 채팅 기록 초기화
    clear.click(lambda: None, None, chatbot, queue=False)
    
# 인터페이스 실행
demo.launch(debug=True)