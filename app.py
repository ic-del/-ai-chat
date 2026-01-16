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
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are SIMON, an autonomous AI assistant with tool-calling capabilities. You help with tasks, can access file systems, browse the web, and interact with compliance databases. When responding, structure your output to include any actions you'd like to take."},
                *conversations[session_id]
            ],
            temperature=0.7,
            max_tokens=2000
        })
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversations[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Parse response for actions (you can enhance this)
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
