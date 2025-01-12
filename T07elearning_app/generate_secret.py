#!/usr/bin/env python3
"""
generate_secret.py

Tạo và in ra một SECRET_KEY ngẫu nhiên để dùng cho Flask.
"""

import secrets

def main():
    # Tạo key 32 byte (64 hex) - đủ mạnh cho SECRET_KEY
    secret_key = secrets.token_hex(32)  
    print("SECRET_KEY =", secret_key)

if __name__ == "__main__":
    main()

# SECRET_KEY = babeba465ea4b280c53af81e0173f8b61914c8ff9bc1093fbe6b00778cb69127