from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/create_agent', methods=['POST'])
def create_agent():
    data = request.json
    provider = data.get('provider')
    agent_name = data.get('agent_name')
    language = data.get('language')
    api_key = data.get('api_key')

    if not provider or not agent_name or not language or not api_key:
        return jsonify({'error': 'Missing required fields'}), 400

    if provider == 'VAPI':
        url = 'https://api.vapi.ai/assistants/create'
        payload = {
            'api_key': api_key,
            'agent_name': agent_name,
            'language': language
        }
    elif provider == 'Retell':
        url = 'https://api.retellai.com/v1/agents'
        payload = {
            'api_key': api_key,
            'agent_name': agent_name,
            'language': language
        }
    else:
        return jsonify({'error': 'Invalid provider'}), 400

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return jsonify({'message': 'Agent created successfully', 'data': response.json()})
    else:
        return jsonify({'error': response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
