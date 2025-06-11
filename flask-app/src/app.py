import sys
import os
from flask import Flask, render_template, request, jsonify
import re

# Add parent directory to system path to import main.py
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)
from main import ChatClient

app = Flask(__name__)
chat_client = ChatClient()

def format_response(text):
    # Format numbered lists
    text = re.sub(r'(\d+\.\s+\*\*.*?\*\*)', r'<div class="list-item">\1</div>', text)
    
    # Convert markdown bold to HTML
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert markdown italic to HTML
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Add paragraph tags for better spacing
    paragraphs = text.split('\n\n')
    text = ''.join([f'<p>{p}</p>' for p in paragraphs if p.strip()])
    
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    response = chat_client.get_chat_response(user_message)
    formatted_response = format_response(response)
    return jsonify({'response': formatted_response})

if __name__ == '__main__':
    app.run(debug=True)