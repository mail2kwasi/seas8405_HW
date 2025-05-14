from flask import Flask, request, jsonify
import os
import ast
import ipaddress
import subprocess
import shlex
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secure password from environment
PASSWORD = os.getenv("APP_PASSWORD")
if not PASSWORD:
    raise RuntimeError("APP_PASSWORD is not set")

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum() or len(name) > 30:
        return jsonify({"error": "Invalid name. Must be alphanumeric and ≤ 30 chars."}), 400
    return f"Hello, {name}!"

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400

    try:
        result = subprocess.check_output(shlex.split(f"ping -c 1 {ip}"), stderr=subprocess.STDOUT, timeout=5)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Ping failed", "details": e.output.decode()}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping timed out"}), 504

@app.route('/calculate')
def calculate():
    expr = request.args.get('expr')
    if not expr or len(expr) > 50:
        return jsonify({"error": "Invalid expression length"}), 400
    try:
        result = ast.literal_eval(expr)
        if not isinstance(result, (int, float, list, tuple, dict)):
            raise ValueError("Unsupported type")
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": "Expression error", "details": str(e)}), 400

@app.route('/auth')
def auth():
    pw = request.args.get('pw', '')
    if pw != PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify({"message": "Access granted"})

# ✅ Restrict to localhost only
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
