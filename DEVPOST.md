# ACM Facial Detection System - DevPost Submission

## Inspiration

Many schools, companies, and organizations still use Excel sheets and manual records for attendance and access control. This is time-consuming and error-prone. We wanted to automate this process using facial recognition AI to help frontline workers (security guards, receptionists) do their jobs more efficiently—assisting them rather than replacing them.

## Languages/Frameworks Used

- Python, NumPy, Tkinter, dlib, OpenCV, face_recognition, SQLite3
- Node.js, Express.js, JavaScript, HTML/CSS
- CORS, Body-parser for API communication

## What It Does

A complete facial recognition system for automated attendance tracking:
- Real-time face detection from webcam
- Automatic check-in/check-out logging with timestamps
- Face registration interface for new users
- Desktop app (Tkinter) and web dashboard (Node.js)
- SQLite database storing user faces and attendance records
- REST API for integration with other systems

## How You Built It

1. **Facial Recognition Engine** - Used pre-trained dlib models for face detection and encoding faces into 128-dimensional vectors
2. **Desktop Application** - Built Tkinter GUI with OpenCV webcam stream for real-time detection and face registration
3. **Database Design** - SQLite with two tables: one for storing face encodings, one for attendance records
4. **Web Backend** - Express.js REST API for querying and managing attendance data
5. **System Integration** - Created main.py orchestrator to launch both the Python app and Node.js server
6. **Image Processing** - Converts frames, detects faces, generates encodings, and compares against known faces using distance metrics

## Challenges You Ran Into

- Different lighting conditions affecting recognition accuracy
- Real-time processing speed on standard hardware
- False positives (recognizing different people as the same)
- Cross-platform GUI compatibility issues
- Serializing NumPy arrays to SQLite database
- Managing multiple processes (Node.js + Python) together
- Privacy and consent concerns with facial data storage

## Accomplishments You're Proud Of

- Built a complete end-to-end system (not just a prototype) with desktop and web interfaces
- Achieved real-time face recognition on standard hardware without GPU
- Designed with ethics in mind—augmenting workers instead of replacing them
- Works across macOS, Linux, and Windows
- Clean, modular architecture that's easy to extend
- Comprehensive documentation for deployment

## What You Learned

- How to deploy pre-trained deep learning models in real-world applications
- Full-stack development (AI backend + web frontend)
- Database design for complex data types (face embeddings)
- Building systems with multiple coordinated processes
- Computer vision fundamentals (image preprocessing, feature extraction, recognition)
- Importance of ethical considerations in AI deployment
- Cross-platform application development

## What's Next for the Project

**Near-term:**
- Multi-face detection (recognize multiple people at once)
- Configurable detection sensitivity
- Bulk user import from CSV
- Enhanced reporting (daily/weekly/monthly summaries)
- Mobile app for attendance queries

**Medium-term:**
- GPU acceleration for faster processing
- Liveness detection (prevent photo spoofing)
- Email/SMS notifications for anomalies
- Integration with HRIS systems (Workday, SuccessFactors)
- Multi-camera support for larger spaces

**Long-term:**
- Edge deployment with optimized models
- Support for additional biometrics (iris, fingerprint)
- Enterprise multi-site deployment
- Compliance framework for GDPR/CCPA
- Advanced analytics and threat detection

---

**Current Status**: MVP complete and functional

**Deployment Ready**: Yes, with local-only architecture and privacy documentation
