import sys
import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

from base64 import b64decode, b64encode

# x = [True]*(sys.int)


srcData = 'To be, or not to be - that is the question.'
srcData = srcData.encode()

"""
srcData = str.encode(srcData)
print("This is the data\n" + srcData.decode())
"""
class CryptoService:

    def generateKeys(self):
        # generates the RSA keypair by the number of Bytes
        key = RSA.generate(2048)
        return key


    def savePublicKey(self, key):
        #### PUBLIC KEY ####
        # Public Key to be sent to the Client. -> exported to a PEM File for now
        publicKey = key.publickey()
        publicKey = publicKey.exportKey()
        return publicKey.decode()
        # print('This is the public key\n', publicKey)

        # writing to a pem file
        # public_key = open("publickey.pem", "w")
        # public_key.write(publicKey.decode())  # decode converts the bytes to a string #
        # public_key.close()


    def savePrivateKey(self, key):
        ####  PRIVATE KEY ####
        privateKey = key.exportKey()
        # return privateKey.decode()
        # print('This is the public key\n', privateKey)
        # writing to a pem file
        private_key = open("privatekey.pem", "w")
        private_key.write(privateKey.decode())  # decode converts the bytes to a string #
        private_key.close()


    # # generates the RSA keypair by the number of Bytes
    # key = RSA.generate(2048)

    def encryptServerData(publicKey, srcData):
        # ENCRYPTS THE PLAINTEXT WITH PUBLIC KEY
        cipher_rsa = PKCS1_OAEP.new(publicKey)
        encryptedData = cipher_rsa.encrypt(srcData)

        # WE CAN SEND THE PEM FILE OVER TO THE CLIENT
        # print("This is the Encrypted Data", encryptedData)

        return encryptedData
    def readServerPrivateKey(self):
        privkey = RSA.importKey(open('privatekey.pem').read())
        return privkey

    def readServerPublicKey(self):
        # NEEDS TO READ THIS FROM FILE IN ORDER TO ENCRYPT
        publicKey = RSA.importKey(open("publickey.pem").read())
        # print("this is the function server pubkey: ", publicKey)
        # pubkey = PKCS1_OAEP.new(key)  # key is the original pair key generated
        return publicKey
        # print("This is the pubkey from file", pubkey)


    def readClientPublicKey(self):
        client_publicKey = RSA.importKey(open("clientpublickey.pem").read())
        # print("this is the function client pubkey: ", client_publicKey)
        return client_publicKey

    def decryptMessage(self, encryptedData):
        # this reads the private key and decrypts the incoming message
        privkey = RSA.importKey(open('privatekey.pem').read())
        print("This is the privKey after reading it:", type(privkey))
        # privkey = self.savePrivateKey(key)
        privateCipher = PKCS1_OAEP.new(privkey)
        print(type(privateCipher))
        message = privateCipher.decrypt(encryptedData)

        print('this is the decrypted message', message.decode())

        return message.decode()

    def readClientData(self, text):
        # reads the message from the client in the text file
        # encryptedText = open("C:\Users\USER\Desktop\encrpytionTests\encryption\message.txt").read()
        # checks to see if it is a bytes array
        print("This is the read client text:", type(text))

        # since message in forge was encoded in b64 we have to encode the string message
        # and then decode it from b64
        b64_decrypted_message = b64decode(text.encode())
        return b64_decrypted_message

    # def encodeString(str):
    #     return str.encode('utf-8')
    #
    # def saveToText(text):
    #     message = open("server_message.txt", "w")
    #     message.write(text)
    #     message.close()

    # def main():
    #
    #     # SERVER -> CLIENT -> SERVER  ENCRYPTION/DECRYPTION
    #
    #     # key pair generation
    #     key = geneerateKeys()
    #
    #     # saves the public and private keys to a pem for transfer and later use
    #     savePublicKey(key)
    #     savePrivateKey(key)
    #
    #     # reads the encrypted text from the client
    #     encrypted = readClientData()
    #
    #     # reads the private key from the pem file then decrypts the message accordingly
    #     decryptMessage(encrypted)
    #
    #     # Testing in server encryption -> it works
    #     pubkey = readServerPublicKey()
    #     print("this is the read public key: ", pubkey)
    #     encrypted = encryptServerData(pubkey, encodeString("to be or not to be"))


        # ## CLIENT -> SERVER -> CLIENT ENCRYPTION DECRYPTION
        # ## reads the public key from the client
        # client_pubkey = readClientPublicKey()

        # ## uses the client public key to encrypt a message of our choice
        # encrypted = encryptServerData(client_pubkey, encodeString("to be or not to be"))

        # ## base 64 encryption is needed as to save to a text file to save the message as a string -> makes it easier to decrypt
        # b64_encrypted = b64encode(encrypted)

        # ## saves the decoded (string) base64 encoded message to a txt file
        # saveToText(b64_encrypted.decode())









