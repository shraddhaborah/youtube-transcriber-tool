# 🎥 YouTube & Video Multimodal Transcriber

A Streamlit-based application that takes either a **YouTube URL** or **uploaded video file** and returns a rich, multimodal transcript:
- Speech-to-text transcription
- Keyword detection
- Timestamp-aligned keyframe extraction

## ✨ Features
- Upload any `.mp4`, `.webm`, `.mov` file OR paste a YouTube video URL
- Automatic transcription with OpenAI Whisper
- Keyword extraction using KeyBERT
- Visual frames from key timestamps
- Viewer-friendly Streamlit interface

---

## 🚀 How to Run It

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/youtube-transcriber-tool.git
cd youtube-transcriber-tool
```

### 2. Install Requirements
Make sure you have Python 3.8+
```bash
pip install -r requirements.txt
```

### 3. Launch the App
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
youtube_transcriber_tool/
├── app.py               # Streamlit app frontend
├── main.py              # Core logic (transcription, frame extraction)
├── requirements.txt     # Dependencies
├── README.md
```

---

## 📌 Notes
- YouTube download works with `pytube`, but only for publicly available or authorized videos
- Uploaded files are stored temporarily
- Transcription and frame extraction is done locally

---

## 🛡️ Disclaimer
This tool is for educational/demo purposes. Please **do not use it to download copyrighted content from YouTube** without proper rights.

---

## 👨‍💻 Author
Made with 💡 by Shraddha Borah
