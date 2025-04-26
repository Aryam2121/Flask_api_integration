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

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    if provider.lower() == 'vapi':
        url = 'https://api.vapi.ai/assistants'
        payload = {
            "name": agent_name,
            "voice_id": "default",  # Or any other value
            "language": language,
            "model": "gpt-4"         # Default model
        }
    elif provider.lower() == 'retell':
        url = 'https://api.retellai.com/create-agent'  # Corrected Retell URL
        payload = {
            "response_engine": {
                "type": "retell-llm",
                "llm_id": "llm_234sdertfsdsfsdf",
                "version": 0
            },
            "agent_name": agent_name,
            "version": 0,
            "voice_id": "11labs-Adrian",
            "voice_model": "eleven_turbo_v2",
            "fallback_voice_ids": [
                "openai-Alloy",
                "deepgram-Angus"
            ],
            "voice_temperature": 1,
            "voice_speed": 1,
            "volume": 1,
            "responsiveness": 1,
            "interruption_sensitivity": 1,
            "enable_backchannel": True,
            "backchannel_frequency": 0.9,
            "backchannel_words": [
                "yeah",
                "uh-huh"
            ],
            "reminder_trigger_ms": 10000,
            "reminder_max_count": 2,
            "ambient_sound": "coffee-shop",
            "ambient_sound_volume": 1,
            "language": language,
            "webhook_url": "https://webhook-url-here",
            "boosted_keywords": [
                "retell",
                "kroger"
            ],
            "enable_transcription_formatting": True,
            "opt_out_sensitive_data_storage": True,
            "pronunciation_dictionary": [
                {
                    "word": "actually",
                    "alphabet": "ipa",
                    "phoneme": "ˈæktʃuəli"
                }
            ],
            "normalize_for_speech": True,
            "end_call_after_silence_ms": 600000,
            "max_call_duration_ms": 3600000,
            "enable_voicemail_detection": True,
            "voicemail_message": "Hi, please give us a callback.",
            "voicemail_detection_timeout_ms": 30000,
            "post_call_analysis_data": [
                {
                    "type": "string",
                    "name": "customer_name",
                    "description": "The name of the customer.",
                    "examples": [
                        "John Doe",
                        "Jane Smith"
                    ]
                }
            ],
            "post_call_analysis_model": "gpt-4o-mini",
            "begin_message_delay_ms": 1000,
            "ring_duration_ms": 30000,
            "stt_mode": "fast"
        }
    else:
        return jsonify({'error': 'Invalid provider'}), 400

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in [200, 201]:  # 201 Created is also possible
        return jsonify({'message': 'Agent created successfully', 'data': response.json()}), 200
    else:
        return jsonify({'error': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
