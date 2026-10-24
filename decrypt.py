import os
from cryptography.fernet import Fernet
import traceback

def decrypt_data():
    try:
        # Define file paths
        key_file = os.path.join(os.getcwd(), "key.key")
        storage_file = os.path.join(os.getcwd(), "storage.txt")

        print(f"Looking for key file: {key_file}")
        print(f"Looking for storage file: {storage_file}")

        # Check if required files exist
        if not os.path.exists(key_file):
            raise FileNotFoundError(f"Key file not found: {key_file}")
        if not os.path.exists(storage_file):
            raise FileNotFoundError(f"Storage file not found: {storage_file}")

        # Load the encryption key
        with open(key_file, "rb") as kf:
            key = kf.read()
        

        # Initialize Fernet
        fernet = Fernet(key)

        # Load the encrypted data
        with open(storage_file, "rb") as sf:
            encrypted_data = sf.read()
        print(f"Loaded encrypted data: {encrypted_data}")

        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        print("Decrypted data:", decrypted_data.decode())

    except FileNotFoundError as fnfe:
        print(f"File not found: {fnfe}")
    except ValueError as ve:
        print(f"Decryption failed: {ve}")
    except Exception as e:
        print(f"Unexpected error during decryption: {e}")
        traceback.print_exc()  # Print the full traceback for debugging

if __name__ == "__main__":
    decrypt_data()
