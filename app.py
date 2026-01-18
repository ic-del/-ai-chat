from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

# Initialize DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Initialize Perplexity client
perplexity_client = OpenAI(
        api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai"
    )

# In-memory conversation history (use a database for production)
conversations = {}

@app.route('/simon', methods=['POST'])
def simon():
    """
    SIMON endpoint that returns {reply, actions, memory_updates}
    """
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
        model = data.get('model', 'deepseek')  # 'deepseek' or 'perplexity'
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Choose client and model based on selection
                if model == 'perplexity':
                                selected_client = perplexity_client
                                selected_model = "sonar-pro"
                                system_message = "You are an AI assistant with web search capabilities."
                            else:
                                            selected_client = client
                                            selected_model = "deepseek-chat"
                                            system_message = "You are SIMON, an autonomous AI assistant with tool-calling capabilities. You help with tasks, can access file systems, browse the web, and interact with compliance databases."response = client.chat.completions.create(
        # Call selected API
        # For now, return basic structure
        return jsonify({
            "reply": assistant_message,
            "actions": [],  # TODO: Parse actions from response
            "memory_updates": {
                "last_interaction": user_message,
                "conversation_length": len(conversations[session_id])
            }
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "reply": "I encountered an error processing your request.",
            "actions": [],
            "memory_updates": {}
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "SIMON AI"})



if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
