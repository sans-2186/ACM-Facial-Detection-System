import subprocess
import time
import sys

def start_system():
    print("🚀 Starting Security System...")

    # 1. Start the Node.js Dashboard
    print("📂 Initializing Dashboard Server...")
    # This runs 'node server.js' inside the face_recognizer folder
    node_process = subprocess.Popen(['node', 'server.js'], cwd='./face_recognizer')

    # Give the server 2 seconds to bind to the port
    time.sleep(2)

    # 2. Start the Python AI
    print("🤖 Initializing Face Recognition AI...")
    try:
        # This runs your app.py which contains the AI logic
        subprocess.run(['python3', 'app.py'], cwd='./face_recognizer', check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
    finally:
        # Kill the node process when you stop the AI
        node_process.terminate()
        print("✅ System cleaned up.")

if __name__ == "__main__":
    start_system()