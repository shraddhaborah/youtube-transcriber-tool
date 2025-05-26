import os
import tempfile
from pytube import YouTube
import ffmpeg
import whisper
import cv2
from keybert import KeyBERT

def process_youtube_url(url):
    if not url or not isinstance(url, str):
        raise ValueError("Please provide a valid YouTube URL")
    
    # Basic URL validation
    if not ('youtube.com' in url or 'youtu.be' in url):
        raise ValueError("The URL provided is not a valid YouTube URL")
    
    try:
        yt = YouTube(url)
        # Ensure video is available
        if not yt.check_availability():
            raise ValueError("This video is unavailable")
            
        stream = yt.streams.filter(only_audio=False, file_extension='mp4').first()
        if not stream:
            raise ValueError("No suitable video stream found")
            
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        stream.download(filename=temp_path)
        return temp_path
    except Exception as e:
        raise ValueError(f"Failed to process YouTube video: {str(e)}")

def extract_audio(video_path):
    audio_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    (
        ffmpeg
        .input(video_path)
        .output(audio_output, ac=1, ar='16000')
        .run(overwrite_output=True)
    )
    return audio_output

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['segments']

def extract_keywords(segments):
    kw_model = KeyBERT()
    key_segments = []
    for segment in segments:
        keywords = kw_model.extract_keywords(segment['text'], top_n=1)
        if keywords:
            key_segments.append({
                "timestamp": segment['start'],
                "text": segment['text'],
                "keyword": keywords[0][0]
            })
    return key_segments

def extract_frame(video_path, timestamp):
    frame_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    success, image = cap.read()
    if success:
        cv2.imwrite(frame_path, image)
    return frame_path

def generate_multimodal_transcript(video_path, segments):
    enriched_output = []
    for seg in segments:
        frame_path = extract_frame(video_path, seg["timestamp"])
        enriched_output.append({
            "timestamp": seg["timestamp"],
            "text": seg["text"],
            "keyword": seg["keyword"],
            "image": frame_path
        })
    return enriched_output

def process_uploaded_file(video_path):
    audio_path = extract_audio(video_path)
    segments = transcribe_audio(audio_path)
    key_segments = extract_keywords(segments)
    results = generate_multimodal_transcript(video_path, key_segments)
    return results
