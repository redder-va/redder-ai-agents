/**
 * Redder.ro LiveChat AI Widget
 * Version: 1.0
 * 
 * Includere în site:
 * <script src="https://your-cdn.com/redder-chat.js"></script>
 */

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        API_URL: 'https://127.0.0.1:5000/chat/message',  // SCHIMBĂ CU URL-UL TĂU
        WIDGET_POSITION: 'bottom-right',  // bottom-right, bottom-left, top-right, top-left
        PRIMARY_COLOR: '#667eea',
        SECONDARY_COLOR: '#764ba2',
        AVATAR_EMOJI: '🍾',
        GREETING_MESSAGE: 'Bună! 👋 Sunt asistentul virtual Redder.ro. Te ajut să găsești băuturile perfecte!',
        INITIAL_QUICK_REPLIES: [
            'Ce produse aveți?',
            'Recomandă vodcă',
            'Rețetă cocktail'
        ]
    };

    // Inject CSS
    const styles = `
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        #redder-chat-button {
            position: fixed;
            ${CONFIG.WIDGET_POSITION.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
            ${CONFIG.WIDGET_POSITION.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, ${CONFIG.PRIMARY_COLOR} 0%, ${CONFIG.SECONDARY_COLOR} 100%);
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            transition: transform 0.3s;
        }
        
        #redder-chat-button:hover { transform: scale(1.1); }
        
        #redder-chat-button svg {
            width: 32px;
            height: 32px;
            fill: white;
        }
        
        #redder-chat-window {
            position: fixed;
            ${CONFIG.WIDGET_POSITION.includes('bottom') ? 'bottom: 90px;' : 'top: 90px;'}
            ${CONFIG.WIDGET_POSITION.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            width: 380px;
            height: 600px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            display: none;
            flex-direction: column;
            z-index: 999998;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        #redder-chat-window.open { display: flex; }
        
        .chat-header {
            background: linear-gradient(135deg, ${CONFIG.PRIMARY_COLOR} 0%, ${CONFIG.SECONDARY_COLOR} 100%);
            color: white;
            padding: 20px;
            border-radius: 16px 16px 0 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .chat-header-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .chat-header-avatar {
            width: 40px;
            height: 40px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        
        .chat-header-text h3 {
            font-size: 16px;
            margin-bottom: 2px;
        }
        
        .chat-header-text p {
            font-size: 12px;
            opacity: 0.9;
        }
        
        .chat-close {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f7f8fc;
        }
        
        .message {
            margin-bottom: 16px;
            animation: messageSlideIn 0.3s ease-out;
        }
        
        @keyframes messageSlideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.bot {
            display: flex;
            gap: 8px;
        }
        
        .message.user {
            display: flex;
            justify-content: flex-end;
        }
        
        .message-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, ${CONFIG.PRIMARY_COLOR} 0%, ${CONFIG.SECONDARY_COLOR} 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }
        
        .message-content {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 4px;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, ${CONFIG.PRIMARY_COLOR} 0%, ${CONFIG.SECONDARY_COLOR} 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .quick-replies {
            display: flex;
            gap: 8px;
            margin: 12px 0;
            flex-wrap: wrap;
            padding: 0 20px;
        }
        
        .quick-reply-btn {
            padding: 8px 16px;
            border: 1px solid ${CONFIG.PRIMARY_COLOR};
            background: white;
            color: ${CONFIG.PRIMARY_COLOR};
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .quick-reply-btn:hover {
            background: ${CONFIG.PRIMARY_COLOR};
            color: white;
        }
        
        .typing-indicator {
            display: none;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            background: white;
            border-radius: 16px;
            width: fit-content;
        }
        
        .typing-indicator.active { display: flex; }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background: #999;
            border-radius: 50%;
            animation: typingBounce 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        .chat-input-area {
            padding: 16px;
            background: white;
            border-top: 1px solid #e0e0e0;
            border-radius: 0 0 16px 16px;
        }
        
        .chat-input-wrapper {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #e0e0e0;
            border-radius: 24px;
            font-size: 14px;
            outline: none;
            font-family: inherit;
        }
        
        .chat-input:focus { border-color: ${CONFIG.PRIMARY_COLOR}; }
        
        .chat-send-btn {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, ${CONFIG.PRIMARY_COLOR} 0%, ${CONFIG.SECONDARY_COLOR} 100%);
            border: none;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }
        
        .chat-send-btn:hover { transform: scale(1.1); }
        .chat-send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .product-card {
            background: #f0f0f0;
            padding: 12px;
            border-radius: 12px;
            margin: 8px 0;
            border-left: 4px solid ${CONFIG.PRIMARY_COLOR};
        }
        
        .product-card strong { color: ${CONFIG.PRIMARY_COLOR}; }
        
        @media (max-width: 480px) {
            #redder-chat-window {
                width: calc(100vw - 40px);
                height: calc(100vh - 120px);
                ${CONFIG.WIDGET_POSITION.includes('bottom') ? 'bottom: 70px;' : 'top: 70px;'}
            }
        }
    `;

    // Inject CSS into page
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Create HTML structure
    const chatHTML = `
        <div id="redder-chat-button">
            <svg viewBox="0 0 24 24">
                <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                <path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
            </svg>
        </div>

        <div id="redder-chat-window">
            <div class="chat-header">
                <div class="chat-header-info">
                    <div class="chat-header-avatar">${CONFIG.AVATAR_EMOJI}</div>
                    <div class="chat-header-text">
                        <h3>Asistent Redder.ro</h3>
                        <p>Online acum</p>
                    </div>
                </div>
                <button class="chat-close">&times;</button>
            </div>

            <div class="chat-messages" id="chat-messages">
                <div class="message bot">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">${CONFIG.GREETING_MESSAGE}</div>
                </div>
            </div>

            <div class="quick-replies" id="quick-replies"></div>

            <div class="chat-input-area">
                <div class="chat-input-wrapper">
                    <input type="text" class="chat-input" id="chat-input" placeholder="Scrie mesajul tău...">
                    <button class="chat-send-btn" id="chat-send-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;

    // Inject HTML into page
    document.body.insertAdjacentHTML('beforeend', chatHTML);

    // Chat functionality
    const chatButton = document.getElementById('redder-chat-button');
    const chatWindow = document.getElementById('redder-chat-window');
    const chatClose = document.querySelector('.chat-close');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');
    const quickRepliesContainer = document.getElementById('quick-replies');

    let conversationHistory = [];
    let sessionId = 'session_' + Date.now();

    // Initialize quick replies
    updateQuickReplies(CONFIG.INITIAL_QUICK_REPLIES);

    // Toggle chat
    chatButton.addEventListener('click', () => {
        chatWindow.classList.add('open');
        chatInput.focus();
    });

    chatClose.addEventListener('click', () => {
        chatWindow.classList.remove('open');
    });

    // Send message function
    function sendMessage(message) {
        if (!message.trim()) return;

        addMessage(message, 'user');
        conversationHistory.push({ role: 'user', content: message });
        chatInput.value = '';
        
        showTyping();

        fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                history: conversationHistory,
                session_id: sessionId
            })
        })
        .then(response => response.json())
        .then(data => {
            hideTyping();
            
            if (data.success) {
                addMessage(data.response, 'bot');
                conversationHistory.push({ role: 'assistant', content: data.response });
                
                if (data.quick_replies) {
                    updateQuickReplies(data.quick_replies);
                }
                
                if (data.suggested_products && data.suggested_products.length > 0) {
                    showProducts(data.suggested_products);
                }
            } else {
                addMessage('Îmi pare rău, a apărut o eroare. Te rog încearcă din nou.', 'bot');
            }
        })
        .catch(error => {
            hideTyping();
            console.error('Error:', error);
            addMessage('Nu pot comunica cu serverul. Verifică conexiunea.', 'bot');
        });
    }

    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        if (type === 'bot') {
            messageDiv.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-content">${text}</div>
            `;
        } else {
            messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="typing-indicator active">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) typingIndicator.remove();
    }

    function updateQuickReplies(replies) {
        quickRepliesContainer.innerHTML = '';
        replies.forEach(reply => {
            const btn = document.createElement('button');
            btn.className = 'quick-reply-btn';
            btn.textContent = reply;
            btn.onclick = () => sendMessage(reply);
            quickRepliesContainer.appendChild(btn);
        });
    }

    function showProducts(products) {
        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'message bot';
            productCard.innerHTML = `
                <div class="message-avatar">🛍️</div>
                <div class="message-content">
                    <div class="product-card">
                        <strong>${product.name}</strong><br>
                        Preț: ${product.price} RON<br>
                        ${product.stock_status === 'instock' ? '✅ În stoc' : '❌ Fără stoc'}<br>
                        <a href="${product.link}" target="_blank" style="color: ${CONFIG.PRIMARY_COLOR};">Vezi produs →</a>
                    </div>
                </div>
            `;
            chatMessages.appendChild(productCard);
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event listeners
    sendBtn.addEventListener('click', () => sendMessage(chatInput.value));
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage(chatInput.value);
    });

    console.log('Redder.ro LiveChat Widget loaded successfully! 🤖');
})();
