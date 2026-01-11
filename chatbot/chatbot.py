import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

# JSON 출력을 위한 데이터 구조 정의
class ChatResponse(BaseModel):
    message: str = Field(description="사용자 질문에 대한 답변")
    source: str = Field(description="답변의 출처 문서명과 페이지 번호")
    reason: str = Field(description="답변에 대한 추론 근거")

# PDF 파일 로드
class Chatbot:
    def __init__(self):
        
        # 원문 수집
        loader = PyPDFLoader(os.path.abspath(os.path.dirname(__file__) + "/../") + "/data/agreements_naha_kr.pdf")
        documents = loader.load()

        # 텍스트 분할 
        splitter = CharacterTextSplitter(separator=".", chunk_size=500, chunk_overlap=100)
        docs = splitter.split_documents(documents)

        # 임베딩 모델 
        embeddings = OpenAIEmbeddings()

        # 벡터 스토어 생성 및 문서 저장(인메모리 기반 FAISS 인덱스 생성)
        vectorstore = FAISS.from_documents(docs, embeddings) 

        # Retriever 설정
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3}) # 상위 3개 유사 청크 조회

        # LLM 및 메모리 설정
        llm = ChatOpenAI(model_name="gpt-5-mini")
        history = ChatMessageHistory()
        history_message = history.messages if history.messages else "이전 대화 내역이 없습니다."


        # JsonOutputParser 생성
        parser = JsonOutputParser(pydantic_object=ChatResponse)

        # 프롬프트 구성
        system_prompt = """
        당신은 호텔 상담원입니다. [Context]와 이전 대화 내용인 [Chat History]를 참고해서 답변해주세요. 
        - 호텔 이용 관련은 [Context]만을 참고하여 답변하며 관련 내용이 없다면 "죄송합니다. 잘 모르겠습니다."라고 답변해주세요.    
        - 호텔 이용과 관련없는 내용은 상냥하게 답변합니다.
        - 추가 질문은 고객의 이름을 [Chat History]를 참고해서 붙여서 답변합니다.

        {format_instructions}

        [Context]
        {context}

        [Chat History]
        {chat_history}
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user","{question}")
        ]).partial(format_instructions=parser.get_format_instructions())


        # 체인 구성
        self.chain = (
            {"context": retriever, 
             "chat_history": lambda x: history_message,
             "question": RunnablePassthrough()}
            | prompt 
            | llm 
            | parser
        )

    def answer(self, question):
        # 체인 실행
        return  self.chain.invoke(question)
