# ACM Facial Detection System

A comprehensive face recognition and attendance tracking system that combines Python's advanced AI capabilities with a web-based dashboard for real-time monitoring and management.

## 🎯 Features

- **Real-time Face Detection & Recognition**: Powered by state-of-the-art `face_recognition` library
- **Automated Attendance Tracking**: Capture check-in/check-out times using facial recognition
- **Interactive GUI**: User-friendly Tkinter interface with live webcam feed
- **Web Dashboard**: Modern Node.js/Express backend for remote access and monitoring
- **Local Database**: SQLite database for storing known faces and attendance records
- **Cross-platform Support**: Works on macOS, Linux, and Windows

## 🛠️ Technology Stack

**Backend (Python)**
- `face_recognition` - Deep learning-based face recognition
- `dlib` - Machine learning library for face detection
- `OpenCV (cv2)` - Computer vision for webcam streaming
- `Tkinter` - GUI framework
- `SQLite3` - Local database
- `NumPy` & `Pillow` - Image processing

**Frontend (Node.js)**
- `Express` - Web framework
- `CORS` - Cross-origin resource sharing
- `Body-parser` - HTTP request parsing

## 📋 Prerequisites

- Python 3.7 or higher
- Node.js 14.0 or higher
- A working webcam
- macOS, Linux, or Windows

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ACM-Facial-Detection-System.git
cd ACM-Facial-Detection-System
```

### 2. Create and Activate Virtual Environment (Python)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies
```bash
cd face_recognizer
npm install
cd ..
```

## 💻 Usage

### Starting the System
Run the main entry point, which automatically starts both the Node.js dashboard and Python AI:

```bash
python main.py
```

This will:
1. Start the Node.js Express server on `http://localhost:5000`
2. Launch the Python Tkinter application with live face detection
3. Coordinate between both systems for seamless attendance tracking

### Manual Startup (Alternative)

**Start Node.js Dashboard:**
```bash
cd face_recognizer
npm start
```

**Start Python Application (in a separate terminal):**
```bash
cd face_recognizer
python app.py
```

## 📁 Project Structure

```
ACM-Facial-Detection-System/
├── main.py                          # Main entry point (starts both systems)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── face_recognizer/
    ├── app.py                       # Python AI application with Tkinter GUI
    ├── server.js                    # Node.js Express server
    ├── package.json                 # Node.js dependencies
    ├── public/
    │   └── index.html              # Web dashboard interface
    ├── output/                      # Generated outputs and logs
    ├── training/                    # Training data for the ML model
    └── validation/                  # Validation dataset
```

## 🎓 How It Works

1. **Face Registration**: Users can register their faces through the Tkinter GUI
2. **Face Encoding**: The system creates numerical encodings of registered faces
3. **Real-time Detection**: Webcam feed is continuously analyzed for face detection
4. **Recognition**: Detected faces are compared against known encodings
5. **Attendance Logging**: Recognized individuals are automatically logged in/out
6. **Dashboard Sync**: Attendance data is synced with the web server

## 🔧 Configuration

The system uses SQLite for local storage with two main tables:
- **known_faces**: Stores registered user names and their face encodings
- **attendance**: Logs check-in/check-out events with timestamps

## 📊 API Endpoints

The Node.js server provides the following endpoints:

- `POST /api/attendance` - Log attendance event
- `GET /api/attendance` - Retrieve attendance records
- `POST /api/faces` - Register a new face
- `GET /api/faces` - Get all registered faces

## 🐛 Troubleshooting

### Webcam not detected
- Check that your webcam is properly connected
- Verify camera permissions in your OS settings
- Try accessing the webcam through another application

### Face recognition not working
- Ensure there is adequate lighting
- Make sure faces are clearly visible and facing the camera
- Re-register faces for better accuracy

### Port already in use
- Change the port in `server.js` if port 5000 is already in use
- Or kill the process using: `lsof -i :5000` (macOS/Linux)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License - see the LICENSE file for details.

## 👥 Authors

Created for the ACM (Association for Computing Machinery) community.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Note**: This system is designed for attendance and identification purposes. Ensure compliance with local privacy and data protection laws when deploying in production environments.
