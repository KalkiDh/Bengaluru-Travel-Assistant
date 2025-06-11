# 🧳 Bengaluru Travel Assistant – A Gen AI-Powered Smart Guide

**Bengaluru Travel Assistant** is a **Generative AI (Gen AI)**-driven web application built using **Flask**, designed to enhance the travel experience in **Bengaluru (Bangalore), India**. By integrating with cutting-edge language models (via Azure AI or OpenAI), it offers intelligent, conversational assistance tailored to exploring the city.

---

## 🧠 What Makes This a Gen AI Project?

This project leverages **Generative AI models** to:

- Generate **context-aware travel recommendations**
- Understand **natural language queries** from users
- Provide **interactive, intelligent conversations**
- Adapt and scale to any **LLM (Large Language Model)** provider like **Azure OpenAI** or **OpenAI API** with minimal changes

---

## 🌐 Core Technologies

- **Flask** – Lightweight web framework for building the user interface
- **Azure AI / OpenAI GPT** – Powers the conversational and recommendation engine using LLMs
- **python-dotenv** – Manages configuration via `.env` files for security
- **HTML / Jinja2 Templates** – For dynamic and responsive web views

---

## ⚙️ Key Features

- 🔍 **Conversational Travel Assistant** – Ask about places, routes, or itineraries
- 📍 **Location-aware suggestions** – Explore nearby attractions
- 🤖 **Gen AI Recommendations** – Get contextual and dynamic advice
- 🛠️ **Easily Switch to OpenAI** – Just update your `.env` and a model import

---

## 📁 Project Structure

bengaluru-travel-assistant/
│
├── app/
│ ├── templates/ # HTML templates
│ ├── static/ # CSS, JS, image files
│ ├── routes.py # Flask routes and logic
│
├── .env # API keys and secrets
├── requirements.txt # Python dependencies
├── run.py # Main entry point
└── README.md # Project documentation


---

## 🔑 How to Use

### 1. Clone the Project

```bash
git clone https://github.com/your-username/bengaluru-travel-assistant.git
cd bengaluru-travel-assistant
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Add Your OpenAI API Key
Create a .env file in the root directory with your OpenAI credentials:

dotenv
Copy
Edit
OPENAI_API_KEY=your_api_key_here




## 🖼️ Sample Frontend Screenshots

### Main Chat Area

!(/images/Bengaluru assistant.png)

---

### Context Understanding

!(/images/Context understanding.png)

---

### Saving the conversation

!(/images/Saving the conversation.png)

### Conversation History

!(/images/Convo history .png)








📌 Future Enhancements
Integration with real-time location APIs

Personalized itinerary generation

Voice-based assistant mode

Multilingual support


🧾 License
MIT License. See LICENSE file for details.

