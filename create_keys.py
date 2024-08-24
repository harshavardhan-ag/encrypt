from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_rsa_key_pair():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Serialize private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Generate public key
    public_key = private_key.public_key()
    
    # Serialize public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_key_pem, public_key_pem

# Generate keys
private_key_pem, public_key_pem = generate_rsa_key_pair()

# Save the keys to files (optional)
with open('private_key.pem', 'wb') as f:
    f.write(private_key_pem)

with open('public_key.pem', 'wb') as f:
    f.write(public_key_pem)

print("Private Key:")
print(private_key_pem.decode())

print("\nPublic Key:")
print(public_key_pem.decode())
