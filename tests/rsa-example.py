#!/usr/bin/env python3

import rsa

# participants

(sender_pub_key, sender_priv_key) = rsa.newkeys(1024, poolsize=4)

(receiver_pub_key, receiver_priv_key) = rsa.newkeys(1024, poolsize=4)

# side of sender

message = "Hello"
print("Message: " + str(message))

binmessage = message.encode()
print("Bytes message: " + str(binmessage))

signature = rsa.sign(binmessage, sender_priv_key, "SHA-512")
print("Signature: " + str(signature))

crypto = rsa.encrypt(binmessage, receiver_pub_key)
print("Encrypted message: " + str(crypto))

# side of receiver

bindecrypted = rsa.decrypt(crypto, receiver_priv_key)
print("Decrypted bytes message: " + str(bindecrypted))

if rsa.verify(bindecrypted, signature, sender_pub_key):
    print("Message signature verified.")
else:
    print("SIGNATURE VERIFICATION ERROR!")

decrypted = bindecrypted.decode()
print("Decrypted message: " + str(decrypted))
