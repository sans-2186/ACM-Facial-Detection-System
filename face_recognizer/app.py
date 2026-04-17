import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import face_recognition
import detector  # Importing our logic from detector.py

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Recognition System")
        self.root.geometry("800x750")

        # Load existing user data
        self.known_names, self.known_encodings = detector.load_known_encodings()

        # Initialize Webcam
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not access webcam.")
            self.root.destroy()
            return

        # UI Elements
        self.video_label = tk.Label(self.root)
        self.video_label.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.register_button = tk.Button(
            self.button_frame, text="Register User", width=15, height=2,
            command=self.register_action, bg="#4CAF50"
        )
        self.register_button.grid(row=0, column=0, padx=10)

        self.recognize_button = tk.Button(
            self.button_frame, text="Recognize", width=15, height=2,
            command=self.recognize_action, bg="#2196F3"
        )
        self.recognize_button.grid(row=0, column=1, padx=10)

        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            # Convert BGR to RGB for display
            display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            display_frame = cv2.resize(display_frame, (760, 570))

            image = Image.fromarray(display_frame)
            imgtk = ImageTk.PhotoImage(image=image)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.root.after(15, self.update_frame)

    def register_action(self):
        if self.current_frame is None: return
        
        name = simpledialog.askstring("Register", "Enter Name for User:")
        if name:
            # Convert current frame to RGB for encoding
            rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            self.known_names, self.known_encodings = detector.register_new_face(rgb_frame, name)
            messagebox.showinfo("Success", f"{name} has been registered!")

    def recognize_action(self):
        if self.current_frame is None: return
        if not self.known_encodings:
            messagebox.showwarning("Warning", "No registered users found. Please register someone first.")
            return

        # Convert to RGB and find faces
        rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        found_people = []
        for encoding in face_encodings:
            # Compare current face against known faces
            matches = face_recognition.compare_faces(self.known_encodings, encoding, tolerance=0.6)
            name = "User Not Found"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_names[first_match_index]
            
            found_people.append(name)

        # Show result
        if not found_people:
            messagebox.showinfo("Result", "No face detected in the frame.")
        else:
            result_msg = "\n".join(found_people)
            messagebox.showinfo("Recognition Result", f"Detected:\n{result_msg}")

    def on_close(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()