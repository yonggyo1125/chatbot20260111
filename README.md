# LangChain으로 만드는 웹 기반 챗봇 실습 과제

### 프로젝트 주제 및 개요 
- 호텔 이용 약관 Q&amp;A 챗봇
> 호텔 이용약관 pdf 파일을 청크화 및 벡터화하여 유사도 기반 외부지식 주입 방식의 호텔 도메인 특화 챗봇 개발

### 주요 기능 설명
- LangChain 프레임워크 기반으로 prompt -> llm -> parser로 이어지는 체인 구성 흐름
- ChatMessageHistory를 이용한 기존 대화 기억 기능 구현
- 인메모리 기반 FAISS 벡터 스토어 사용하여 코사인 유사도 기반 관련 문서 조회(3개)하여 컨텍스트 제공
- PyPDFLoader 사용하여 호텔 이용 약관 chunk화(최대 500개, 100개씩은 오버래핑 하여 문맥을 최대한 고려하도록 분리)

### 실행 예시 및 결과 캡처

### 실행 방법
- 의존성 설치
```bash
pip install -r requirements.txt
```

- FastAPI 서버 실행
```bash
uvicorn main:app --reload
```

- 웹브라우저 주소창에 다음 주소 입력

```
http://localhost:8000
```