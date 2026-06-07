from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
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

        # Use espeak-ng directly - no audio hardware needed
        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        tmp.close()

        subprocess.run([
            'espeak-ng',
            '-s', str(speed),
            '-w', tmp.name,
            text
        ], check=True, capture_output=True)

        return send_file(tmp.name, mimetype='audio/wav', as_attachment=False)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'YAN TTS Server running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
