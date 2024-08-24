

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
import base64

# Read the private key from a file
def load_private_key(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

def decrypt_and_validate(encrypted_message, private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,  # No password if the key was generated without encryption
        backend=default_backend()
    )

    encrypted_message_bytes = base64.b64decode(encrypted_message)

    # try:
        # Decrypt using RSA-OAEP padding with SHA-256
    decrypted_message = private_key.decrypt(
        encrypted_message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # except Exception as e:
    #     print("Decryption error:", e)
    #     raise e

    decrypted_message = decrypted_message.decode()
    print(decrypted_message)
    current_time_str, gate_guard_string = decrypted_message.split("@")

    # Convert time string to datetime object

    from datetime import datetime, timedelta

    # Assuming `current_time_str` is the ISO format string you receive
    current_time_str = current_time_str.replace('Z', '')  # Convert 'Z' to UTC offset
    message_time = datetime.fromisoformat(current_time_str)

    current_time = datetime.now()

    # Check if the message time is within the last 30 seconds
    if (current_time - message_time) > timedelta(seconds=30):
        raise ValueError("Decryption failed: Time difference is greater than 30 seconds.")

    return gate_guard_string

# Example usage:
private_key_pem = load_private_key('private_key.pem')

# Use the encrypted message output from the JavaScript code
encrypted_message = "XLOFcBklP6v6SJa5NdKOHtWVXZYXZbB/T1wZ86xRp/GC1pWCO9BPMPh7XHRqVhIO1nxcsccDKMmwt3I1OWxng8ZyCSZT7umD32fKbCsXWlIdNezUSs7vjTScNQVTvBlSefA99JIwsIQHuCokqNwkyAREWxup4WoaYuZx7qGF+hVTPN+9Y5l3hxu9g3Vi+ij4RNZiQ+rN6v30mC21zkFetWRGlGHfmKgibQsn0TfQ1TNyZ8BgjtdzEtTVdfMmjgc09uMgi9JHfY2C2nFj5ZuwdE1opBqdcJheizzda20+A5/0GxvKJW/0vuNwbSFUApg0Mjlx+tf4L2cgRhXBO1tvAg=="

try:
    gate_guard_string = decrypt_and_validate(encrypted_message, private_key_pem)
    print("Decryption successful. Gate guard string:", gate_guard_string)
except ValueError as e:
    print(str(e))
