import flask
from flask import Flask, render_template, request
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import json
from test import CryptoService
from flask_cors import CORS

from base64 import b64decode, b64encode


app = Flask(__name__)
CORS(app)

encrypt = CryptoService()
global key
key = encrypt.generateKeys()

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/api/publickey')
def pubKey():

    # this save the public key to a string and then sends it to the frontend
    pubkey = encrypt.savePublicKey(key)
    print(pubkey)
    encrypt.savePrivateKey(key)
    # privkey = encrypt.readServerPrivateKey()
    return flask.jsonify(pubkey)
    # return render_template('index.html', privkey=privkey, pubkey=pubkey)

@app.route('/api/message', methods=['POST'])
def userMessage():
    userdata = request.get_json(force=True) # get json data
    message = userdata['message']
    # read the client data first and decrypt the base64 and ting
    b64_data = encrypt.readClientData(message);
    # privkey = encrypt.savePrivateKey(key);
    message = encrypt.decryptMessage(b64_data)
    return render_template('index.html', pubkey=message)
    # program says incorrect decryption due to different keys on front and backend



if __name__ == '__main__':
    app.run()