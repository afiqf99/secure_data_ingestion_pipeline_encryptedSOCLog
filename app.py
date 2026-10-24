from flask import Flask, render_template, redirect, url_for,request,jsonify
import subprocess
import threading
import os
import logging

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Adjust the path as needed
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

  # Create the folder if it doesn't exist

@app.route("/")
def index():
    message = request.args.get('message', '')  # Retrieve message from query parameters
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    # Save the file to the UPLOAD_FOLDER
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200



# Function to handle the ingestion in the background
def ingest_data_in_background():
    try:
        result = subprocess.run(["python", "ingest.py"], check=True, capture_output=True, text=True)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during ingestion: {e.stderr}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    # You can log or process the message here if needed (e.g., storing in a log or sending it somewhere)

@app.route('/ingestfile', methods=['GET', 'POST'])
def ingestfile():
    if request.method == 'POST':
        # Handle the uploaded file
        file = request.files['file']
        if file:
            # Process the file (save, upload, etc.)
            file.save(f"uploads/{file.filename}")  # Save to a folder (make sure the folder exists)
            
            file = request.files['file']
        if file:
            file.save(f"uploads/{file.filename}")  # Save the file
            message = f"File {file.filename} uploaded successfully!"
            return render_template('ingestfile.html', message=message)  # Show the message on the same page
    return render_template('ingestfile.html')  # Render page for GET requests
    

@app.route("/ingest")
def ingest_data():
        # Start the ingestion in a background thread
    threading.Thread(target=ingest_data_in_background).start()

    # Immediately return a response to the user
    return render_template('index.html', message="Ingestion started, data will be processed.")

@app.route("/display")
def display_storage():
    """Display the contents of storage.txt."""
    try:
        with open("storage.txt", "rb") as file:
            content = file.read().decode('utf-8')  # Decode bytes to string
        return render_template('display.html', content=content)
    except FileNotFoundError:
        return "Error: storage.txt not found."

@app.route("/decrypt")
def decrypt_data():
    """Run the functionality of decrypt.py and display the result."""
    try:
        result = subprocess.run(["python", "decrypt.py"], capture_output=True, text=True, check=True)
        decrypted_data = result.stdout  # Get the output from decrypt.py
        return render_template('decrypt.html', decrypted_data=decrypted_data)
    except subprocess.CalledProcessError:
        return "Decryption failed."
if __name__ == "__main__":
    app.run(debug=True)
