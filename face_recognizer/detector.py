import face_recognition
import pickle
from pathlib import Path
from PIL import Image

# Set up paths relative to this script
BASE_DIR = Path(__file__).resolve().parent
ENCODINGS_PATH = BASE_DIR / "output" / "encodings.pkl"
TRAINING_DIR = BASE_DIR / "training"

# Ensure necessary directories exist
TRAINING_DIR.mkdir(exist_ok=True)
(BASE_DIR / "output").mkdir(exist_ok=True)

def register_new_face(image_array, name):
    """
    Saves a webcam frame to the training folder and updates the database.
    """
    user_folder = TRAINING_DIR / name
    user_folder.mkdir(exist_ok=True)
    
    # Save the physical image for future reference
    image_path = user_folder / f"{name}.jpg"
    img = Image.fromarray(image_array)
    img.save(image_path)

    # Re-scan all faces to update the pickle file
    return rebuild_encodings()

def rebuild_encodings():
    """
    Scans the training folder and converts images into mathematical encodings.
    """
    known_names = []
    known_encodings = []

    # Look through every folder in 'training'
    for image_path in TRAINING_DIR.glob("*/*.jpg"):
        name = image_path.parent.name
        image = face_recognition.load_image_file(image_path)
        
        # Use HOG model (faster for CPUs)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_names.append(name)
            known_encodings.append(encodings[0])
            print(f"Successfully encoded: {name}")

    # Save data to disk
    with ENCODINGS_PATH.open("wb") as f:
        pickle.dump({"names": known_names, "encodings": known_encodings}, f)
    
    return known_names, known_encodings

def load_known_encodings():
    """Loads existing encodings. Returns empty lists if file doesn't exist."""
    if not ENCODINGS_PATH.exists():
        return [], []
    try:
        with ENCODINGS_PATH.open("rb") as f:
            data = pickle.load(f)
        return data["names"], data["encodings"]
    except (EOFError, pickle.UnpicklingError):
        return [], []