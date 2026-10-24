from cryptography.fernet import Fernet
import hashlib

def generate_and_save_key():
    """Generate a Fernet key and save it to key.key file."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the Fernet key from the key.key file."""
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

def read_data():
    """Read data from data.txt."""
    try:
        with open("data.txt", "r") as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print("data.txt not found. Please ensure the file exists.")
        return None

def encrypt_data(data, cipher_suite):
    """Encrypt data using Fernet symmetric encryption."""
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def hash_data(data):
    """Generate MD5 hash of the data."""
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    return md5_hash

def write_to_storage(encrypted_data, md5_hash):
    """Write encrypted data and MD5 hash to storage.txt."""
    with open("storage.txt", "wb") as sf:
        sf.write(encrypted_data)

    with open("hash.txt", "w") as hf:
        hf.write(md5_hash)
        
def display_storage():
    """Display the contents of storage.txt."""
    try:
        with open("storage.txt", "r") as file:
            content = file.read()
        print(content)
    except FileNotFoundError:
        print("storage.txt not found. Please ensure the file was written.")

def ingest_data():
    """Main ingestion function to handle reading, encrypting, hashing, and saving data."""
    key = generate_and_save_key()  # Generate and save the key
    cipher_suite = Fernet(key)
    
    data = read_data()
    if data is not None:
        encrypted_data = encrypt_data(data, cipher_suite)
        md5_hash = hash_data(data)
        write_to_storage(encrypted_data, md5_hash)
        return"Data successfully ingested and encrypted!"
        
    else:
        print("Ingestion failed: No data found.")
if __name__ == "__main__":
    ingest_data()
