import sys
import os
from flask import Flask, render_template, request, jsonify
import re
import json
from datetime import datetime

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

@app.route('/save_conversation', methods=['POST'])
def save_conversation():
    try:
        # Create conversations directory if it doesn't exist
        os.makedirs('conversations', exist_ok=True)
        
        # Create the conversation data
        conversation_data = {
            'id': chat_client.conversation_id,
            'timestamp': datetime.now().isoformat(),
            'messages': chat_client.conversation_history
        }
        
        # Save to individual conversation file
        file_path = os.path.join('conversations', f'conversation_{chat_client.conversation_id}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_conversations')
def get_conversations():
    conversations = []
    try:
        if os.path.exists('conversations'):
            for filename in os.listdir('conversations'):
                if filename.endswith('.json'):
                    with open(os.path.join('conversations', filename), 'r', encoding='utf-8') as f:
                        conv = json.load(f)
                        # Get the first non-system message as preview
                        preview = next((msg['content'] for msg in conv['messages'] 
                                     if msg['role'] != 'system'), '')[:100] + '...'
                        conversations.append({
                            'id': conv['id'],
                            'timestamp': conv['timestamp'],
                            'preview': preview
                        })
        return jsonify(conversations)
    except Exception as e:
        return jsonify([])

@app.route('/load_conversation/<conversation_id>')
def load_conversation(conversation_id):
    if chat_client.load_conversation(conversation_id):
        return jsonify({'success': True, 'messages': chat_client.conversation_history})
    return jsonify({'success': False})

@app.route('/end_conversation', methods=['POST'])
def end_conversation():
    chat_client.end_conversation()
    chat_client.start_new_conversation()
    return jsonify({'success': True, 'new_conversation_id': chat_client.conversation_id})

if __name__ == '__main__':
    app.run(debug=True)