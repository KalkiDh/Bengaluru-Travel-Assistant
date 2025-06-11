import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError

# Load environment variables from .env file
load_dotenv()

class ChatClient:
    def __init__(self):
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4.1"
        self.conversation_history = []
        
        # Get token from .env file
        try:
            self.token = os.getenv("GITHUB_TOKEN")
            if not self.token:
                raise ValueError("GITHUB_TOKEN not found in .env file")
        except Exception as e:
            raise ValueError(f"Error loading GITHUB_TOKEN: {str(e)}")
            
        # Initialize the client
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token)
        )

    def get_chat_response(self, user_message: str) -> str:
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Create messages list with system message and conversation history
            messages = [
                SystemMessage("""You are a friendly Bengaluru/Bangalore city travel assistant.
                For greetings like 'hi', 'hello', 'how are you', respond naturally and warmly.
                For other questions, provide clear and direct answers about Bengaluru.
                If the question is not about Bengaluru/Bangalore, politely ask for Bengaluru-related questions.""")
            ]
            
            # Add conversation history to messages
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    messages.append(UserMessage(msg["content"]))
                else:
                    messages.append(SystemMessage(msg["content"]))

            response = self.client.complete(
                messages=messages,
                temperature=0.7,
                top_p=0.95,
                model=self.model
            )
            
            ai_response = response.choices[0].message.content
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
            
        except AzureError as e:
            print(f"Error calling AI service: {str(e)}")
            return None

def main():
    chat = ChatClient()
    print("Bangalore Travel Assistant: Hi! I'm your Bangalore travel guide. How can I help you today?")
    print("(Type 'quit', 'bye', or 'exit' to end the conversation)")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'bye', 'exit']:
            print("Bangalore Travel Assistant: Goodbye! Have a great day!")
            break
            
        response = chat.get_chat_response(user_input)
        if response:
            print(f"\nBangalore Travel Assistant: {response}")

if __name__ == "__main__":
    main()