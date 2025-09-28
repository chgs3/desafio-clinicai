const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat-btn');

const API_URL = 'http://127.0.0.1:8000/chat';

// guardando o ID do chat atual
let chatId = null;

// converter formatações markdown simples para HTML
function markdownToHtml(text) {
    let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\* /g, '<br>&bull; ');
    return html;
}

// Função para adicionar mensagens ao chat
function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'agent-message');

    const htmlMessage = markdownToHtml(message);
    messageElement.innerHTML = htmlMessage;

    chatBox.appendChild(messageElement);

    // Rolando para a última mensagem
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Função para enviar mensagem ao backend
async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (!userMessage) return;

    // Adicionando a mensagem do usuário ao chat
    addMessage(userMessage, 'user');
    userInput.value = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({               
                chat_id: chatId,
                message: userMessage,
             }),
        });

        if (!response.ok) {
            throw new Error('Erro na resposta do servidor');
        }

        const data = await response.json();
        addMessage(data.response, 'agent');

    } catch (error) {
        console.error('Erro:', error);
        addMessage('Desculpe, não consegui me conectar ao servidor. Tente novamente mais tarde.', 'agent');
    }
}

// função para iniciar um novo chat
function startNewChat() {
    chatId = `chat_${Date.now()}`;
    chatBox.innerHTML = '';
    addMessage('Olá! Sou o assistente virtual da ClinicAI e vou te ajudar a fazer uma triagem inicial. Lembre-se, esta é uma coleta de informações e não substitui uma consulta médica. Qual é a sua queixa principal?', 'agent');
}

// eventos
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
})
newChatBtn.addEventListener('click', startNewChat);

// iniciar o primeiro chat quando a página carregar
startNewChat();