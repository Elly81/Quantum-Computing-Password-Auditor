from flask import Flask, request, jsonify, render_template
import math
import string

app = Flask(__name__)

def calculate_entropy(password):
    charset = 0
    if any(c in string.ascii_lowercase for c in password):
        charset += 26
    if any(c in string.ascii_uppercase for c in password):
        charset += 26
    if any(c in string.digits for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)
    if any(c.isspace() for c in password):
        charset += 1

    entropy = math.log2(charset) * len(password) if charset else 0
    return round(entropy, 2)

def estimate_crack_time(entropy_bits, quantum=False):
    guesses = 2 ** (entropy_bits / 2 if quantum else entropy_bits)
    seconds = guesses / 1e9
    if seconds < 60:
        return f"{round(seconds)} seconds"
    elif seconds < 3600:
        return f"{round(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{round(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{round(seconds / 86400)} days"
    else:
        return f"{round(seconds / 31536000)} years"

def quantum_rating(entropy):
    if entropy < 64:
        return "❌ Weak"
    elif entropy < 90:
        return "⚠️ Moderate"
    else:
        return "✅ Strong"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    password = data.get('password', '')
    entropy = calculate_entropy(password)
    classical_time = estimate_crack_time(entropy, quantum=False)
    quantum_time = estimate_crack_time(entropy, quantum=True)
    rating = quantum_rating(entropy)
    suggestions = "Use longer passwords with a mix of upper, lower, numbers, and symbols."

    return jsonify({
        "entropy": entropy,
        "classical_time": classical_time,
        "quantum_time": quantum_time,
        "rating": rating,
        "suggestions": suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
