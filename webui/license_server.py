from flask import Flask, request, jsonify

app = Flask(__name__)

# Load valid keys from a local file
def load_keys():
    try:
        with open('valid_keys.txt', 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    key = data.get('key', '').strip()
    valid_keys = load_keys()

    if key in valid_keys:
        return jsonify({'status': 'success', 'message': 'Key valid!'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid key'}), 403

if __name__ == '__main__':
    app.run(port=8787)
