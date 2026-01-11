document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');

    // 메시지 추가 함수 (type: 'user-message' 또는 'bot-message')
    function appendMessage(type, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.innerText = text;
        chatWindow.appendChild(messageDiv);
        
        // 새로운 메시지 추가 후 자동 스크롤
        scrollToBottom();
        return messageDiv;
    }

    // 로딩 아이콘 추가 함수
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot-message', 'loading-container');
        loadingDiv.id = 'loading-indicator';
        loadingDiv.innerHTML = `
            <div class="loading">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatWindow.appendChild(loadingDiv);
        scrollToBottom();
    }

    // 로딩 아이콘 제거 함수
    function hideLoading() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    // 스크롤을 항상 아래로 유지하는 함수
    function scrollToBottom() {
        chatWindow.scrollTo({
            top: chatWindow.scrollHeight,
            behavior: 'smooth' // 부드럽게 스크롤
        });
    }

    // 폼 제출 이벤트 리스너
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const question = userInput.value.trim();
        if (!question) return;

        // 1. 사용자 메시지 화면에 표시
        appendMessage('user-message', question);
        userInput.value = '';

        // 2. 로딩 애니메이션 표시
        showLoading();

        try {
            // 3. FastAPI 서버로 GET 요청 (쿼리 파라미터 전달)
            const response = await fetch(`/chat?question=${encodeURIComponent(question)}`);
            
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();

            // 4. 로딩 제거 후 봇 응답 표시
            hideLoading();
            appendMessage('bot-message', data.message);
        } catch (error) {
            console.error('Error:', error);
            hideLoading();
            appendMessage('bot-message', '죄송합니다. 오류가 발생했습니다. 다시 시도해 주세요.');
        }
    });
});