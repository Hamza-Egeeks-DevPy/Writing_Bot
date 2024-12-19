import secrets

# Generate a 24-byte (192-bit) random secret key
secret_key = secrets.token_hex(24)
print(secret_key)
