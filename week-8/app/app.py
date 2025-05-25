from flask import Flask, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
import requests
import logging
from auth import token_required

logging.basicConfig(level=logging.DEBUG)

class MyTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        resp = requests.post(
            'http://localhost:8080/realms/custom-realm/protocol/openid-connect/token/introspect',
            data={
                'token': token_string,
                'client_id': 'my-flask-client',
                'client_secret': 'p7VppIvzzQgA1tVywGHTRqejaXOCOPS4',
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        token_data = resp.json()
        logging.debug(f"Introspection response: {token_data}")
        if token_data.get("active"):
            return token_data
        raise ValueError("Token is not active")


app = Flask(__name__)
require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyTokenValidator())

@app.route('/')
def public():
    return jsonify(message='This is a public route.')

@app.route('/protected')
@require_oauth()
def protected():
    return jsonify(message='Access granted to protected route.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
