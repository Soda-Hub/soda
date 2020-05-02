from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Random import get_random_bytes


def get_rsa_private_key_in_pem_bytes(key):
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )


def get_rsa_public_key_in_pem_bytes(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)


def generate_keypair():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    bpriv_key = get_rsa_private_key_in_pem_bytes(key)
    bpub_key = get_rsa_public_key_in_pem_bytes(key.public_key())

    return bpriv_key, bpub_key


def encrypt_password(password):
    salt = get_random_bytes(16)
    bcrypt_hash = bcrypt(password, 12, salt)
    return bcrypt_hash.decode()


def compare_password(password, encrypted):
    try:
        bcrypt_check(password, encrypted.encode())
    except ValueError:
        return False
    else:
        return True
