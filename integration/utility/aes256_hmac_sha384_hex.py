import base64
import os
import hmac
import hashlib
from Crypto.Cipher import AES

class AES256HMACSHA384HEX:
    IV_SIZE = 12  
    TAG_SIZE = 16  
    HMAC_LENGTH = 48  

    def __init__(self, auth_key, auth_iv):
        
        auth_key = auth_key.strip()
        auth_iv = auth_iv.strip()

        self.auth_key = base64.b64decode(auth_key)
        self.auth_iv = base64.b64decode(auth_iv)

    @staticmethod
    def bytes_to_hex(b):
        return b.hex().upper()

    @staticmethod
    def hex_to_bytes(h):
        return bytes.fromhex(h)

    def encrypt(self, plaintext):
        iv = os.urandom(self.IV_SIZE)
        cipher = AES.new(self.auth_key, AES.MODE_GCM, nonce=iv, mac_len=self.TAG_SIZE)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))

        encrypted_message = iv + ciphertext + tag
        hmac_calculated = hmac.new(self.auth_iv, encrypted_message, hashlib.sha384).digest()
        final_message = hmac_calculated + encrypted_message

        return self.bytes_to_hex(final_message)

    def decrypt(self, hex_ciphertext):
        full_message = self.hex_to_bytes(hex_ciphertext)

        if len(full_message) < self.HMAC_LENGTH + self.IV_SIZE + self.TAG_SIZE:
            raise ValueError("Invalid ciphertext length")

        hmac_received = full_message[:self.HMAC_LENGTH]
        encrypted_data = full_message[self.HMAC_LENGTH:]

        hmac_calculated = hmac.new(self.auth_iv, encrypted_data, hashlib.sha384).digest()
        if not hmac.compare_digest(hmac_received, hmac_calculated):
            raise ValueError("HMAC validation failed. Data may be tampered!")

        iv = encrypted_data[:self.IV_SIZE]
        ciphertext_with_tag = encrypted_data[self.IV_SIZE:]

        ciphertext = ciphertext_with_tag[:-self.TAG_SIZE]
        tag = ciphertext_with_tag[-self.TAG_SIZE:]

        cipher = AES.new(self.auth_key, AES.MODE_GCM, nonce=iv, mac_len=self.TAG_SIZE)
        plaintext_bytes = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext_bytes.decode('utf-8')
