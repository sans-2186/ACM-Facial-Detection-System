import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import sqlite3
import io
from tkmacosx import Button # For better button styling on Mac

# --- DATABASE UTILITIES ---
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS known_faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- MAIN APP CLASS ---
class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACM Facial Detection System")
        self.root.geometry("1100x900")
        self.root.configure(bg="#1e272e")

        # --- Initialize System ---
        init_db()
        self.load_known_faces()
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None

        # --- Critical Logic Variables ---
        self.process_this_frame = True
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []

        # --- UI LAYOUT ---
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # 1. Header Frame
        self.header = tk.Frame(self.root, bg="#1e272e", pady=20)
        self.header.grid(row=0, column=0, sticky="ew")

        btn_container = tk.Frame(self.header, bg="#1e272e")
        btn_container.pack()

        # --- MAC BUTTON SAFETY CHECK ---
        try:
            self.register_button = Button(
                btn_container, text=" ＋ REGISTER USER ＋ ", 
                command=self.register_action,
                bg="#2ecc71", fg="black", font=("Arial", 14, "bold"),
                borderless=1, padx=20, pady=10
            )
            self.delete_button = Button(
                btn_container, text=" ✖ DELETE USER ✖ ", 
                command=self.delete_user,
                bg="#e74c3c", fg="white", font=("Arial", 14, "bold"),
                borderless=1, padx=20, pady=10
            )
        except ImportError:
            # Fallback to standard buttons if tkmacosx isn't found
            print("System: tkmacosx not found, using standard buttons.")
            self.register_button = tk.Button(
                btn_container, text="REGISTER", command=self.register_action,
                bg="green", fg="white"
            )
            self.delete_button = tk.Button(
                btn_container, text="DELETE", command=self.delete_user,
                bg="red", fg="white"
            )

        self.register_button.pack(side=tk.LEFT, padx=15)
        self.delete_button.pack(side=tk.LEFT, padx=15)

        # 2. Video Label - THE MOST IMPORTANT PART
        self.video_label = tk.Label(self.root, bg="#2f3542", borderwidth=2, relief="groove")
        self.video_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Cleanly handle closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_frame()

    def load_known_faces(self):
        self.known_names = []
        self.known_encodings = []
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, encoding FROM known_faces")
        
        for row in cursor.fetchall():
            self.known_names.append(row[0])
            # This line MUST match the .tobytes() used in registration
            encoding = np.frombuffer(row[1], dtype=np.float64)
            self.known_encodings.append(encoding)
            
        conn.close()
        print(f"System: Memory updated. {len(self.known_names)} users active.")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
            
        self.current_frame = frame

        if self.process_this_frame:
            # 1. Faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # 2. Find ALL faces
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            # 3. Match Logic
            self.face_names = []
            for face_encoding in face_encodings:
                # 1. ALWAYS start with Unknown
                name = "Unknown" 

                # 2. Check if we have anyone in the database at all
                if len(self.known_encodings) > 0:
                    matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.5)
                    face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                    
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        # Only change "Unknown" to a name if the math is a solid match
                        if matches[best_match_index]:
                            name = self.known_names[best_match_index]

                # 3. Add whatever name we found (or "Unknown") to the list
                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # 4. DRAWING (This must be outside the 'if' to stop the flicker)
        if not self.face_locations:
            self.face_names = []
        
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top, right, bottom, left = top*4, right*4, bottom*4, left*4

            # Green for known, Red for Unknown
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            
            # Draw the box and the name
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # 5. Push to GUI
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # 6. Smoothness check: 20ms is better for MacBook Air
        self.video_label.after(20, self.update_frame)

    
    def register_action(self):
        # 1. PAUSE background processing to stop lag
        self.process_this_frame = False
        
        if self.current_frame is None:
            messagebox.showwarning("Warning", "No camera feed found.")
            self.process_this_frame = True
            return

        # 2. Get the name
        name = simpledialog.askstring("Register", "Enter User Name:")
        if not name:
            self.process_this_frame = True
            return

        # 3. Process the snapshot
        snap = self.current_frame.copy()
        small_frame = cv2.resize(snap, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)

        if len(face_locations) == 1:
            # Generate encoding and convert to raw bytes (Fixes Pickle Error)
            encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
            encoding_blob = encoding.tobytes() 

            try:
                # 4. Database Save
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO known_faces (name, encoding) VALUES (?, ?)", 
                             (name, encoding_blob))
                conn.commit()
                conn.close()
                
                # 5. REFRESH MEMORY
                self.load_known_faces() 
                messagebox.showinfo("Success", f"User '{name}' registered!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not save: {e}")
        else:
            messagebox.showwarning("Error", "Need exactly one face in view.")

        # 6. RESUME background processing
        self.process_this_frame = True

    def check_users(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM known_faces")
        users = cursor.fetchall()
        print("--- Registered Users ---")
        for u in users:
            print(f"- {u[0]}")
        conn.close()

    def delete_user(self):
        name_to_delete = simpledialog.askstring("Delete", "Enter the exact name to delete:")
        if not name_to_delete:
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Check if user exists first
        cursor.execute("SELECT name FROM known_faces WHERE name = ?", (name_to_delete,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM known_faces WHERE name = ?", (name_to_delete,))
            conn.commit()
            conn.close()
            
            self.load_known_faces() # Refresh memory so they aren't recognized anymore
            self.check_users()      # Print updated list
            messagebox.showinfo("Deleted", f"User '{name_to_delete}' has been removed.")
        else:
            conn.close()
            messagebox.showwarning("Error", f"No user found with the name '{name_to_delete}'.")
        
    def on_close(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()