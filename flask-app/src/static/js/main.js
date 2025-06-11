// src/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("Welcome to the Flask app!");

    // Example of adding interactivity
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', function() {
            alert('Button clicked!');
        });
    }

    // Load conversations when page loads
    loadConversations();
});

function loadConversations() {
    fetch('/get_conversations')
        .then(response => response.json())
        .then(conversations => {
            const list = document.getElementById('conversation-list');
            list.innerHTML = '';
            
            // Sort conversations by timestamp in descending order
            conversations.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            
            conversations.forEach(conv => {
                const item = document.createElement('div');
                item.className = 'conversation-item';
                item.innerHTML = `
                    <div class="conversation-time">${new Date(conv.timestamp).toLocaleString()}</div>
                    <div class="conversation-preview">${conv.preview}</div>
                `;
                item.onclick = () => loadConversation(conv.id);
                list.appendChild(item);
            });
        });
}

function loadConversation(conversationId) {
    fetch(`/load_conversation/${conversationId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const chatMessages = document.getElementById('chat-messages');
                chatMessages.innerHTML = '';
                data.messages.forEach(msg => {
                    addMessage(msg.content, msg.role);
                });
            }
        });
}

function startNewConversation() {
    fetch('/end_conversation', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('chat-messages').innerHTML = '';
            addMessage("Hi! I'm your Bangalore travel guide. How can I help you today?", 'assistant');
            loadConversations();
        }
    });
}

function saveConversation() {
    fetch('/save_conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadConversations(); // Reload the conversation list
        }
    });
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (message === '') return;
    
    if (['quit', 'bye', 'exit'].includes(message.toLowerCase())) {
        saveConversation(); // Save before ending
        fetch('/end_conversation', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addMessage('Goodbye! Have a great day!', 'assistant');
                loadConversations();
                setTimeout(() => {
                    document.getElementById('chat-messages').innerHTML = '';
                    addMessage("Hi! I'm your Bangalore travel guide. How can I help you today?", 'assistant');
                }, 2000);
            }
        });
    } else {
        // Add user message to chat
        addMessage(message, 'user');
        input.value = '';

        // Send message to server
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'assistant');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, something went wrong.', 'assistant');
        });
    }
}

function addMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    
    // Use innerHTML for assistant messages to render HTML formatting
    if (sender === 'assistant') {
        messageDiv.innerHTML = message;
    } else {
        messageDiv.textContent = message;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Allow sending message with Enter key
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});