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
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (message === '') return;

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