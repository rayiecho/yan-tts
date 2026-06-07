from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pyttsx3
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text', '')
        speed = data.get('speed', 150)
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        engine = pyttsx3.init()
        engine.setProperty('rate', int(speed))
        engine.setProperty('volume', 1.0)
        tmp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tmp.close()
        engine.save_to_file(text, tmp.name)
        engine.runAndWait()
        return send_file(tmp.name, mimetype='audio/mp3', as_attachment=False)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'YAN TTS Server running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
