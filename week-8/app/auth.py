import jwt
import requests
from flask import request, jsonify
from functools import wraps
 
# Replace with your Keycloak realm URL
KEYCLOAK_REALM_URL = "http://localhost:8080/realms/custom-realm"
CLIENT_ID = "my-flask-client"
 
# Get Keycloak public key dynamically
def get_public_key():
    res = requests.get(f"{KEYCLOAK_REALM_URL}/protocol/openid-connect/certs")
    jwks = res.json()
    cert = jwks["keys"][0]["x5c"][0]
    return (
        "-----BEGIN CERTIFICATE-----\n" +
        cert +
        "\n-----END CERTIFICATE-----"
    )
 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({'error': 'Missing Authorization header'}), 401
 
        try:
            token = auth_header.split(" ")[1]
            public_key = get_public_key()
            payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=CLIENT_ID)
            request.user = payload  # Optional: attach user info
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': 'Invalid token', 'message': str(e)}), 401
 
        return f(*args, **kwargs)
    return decorated
 