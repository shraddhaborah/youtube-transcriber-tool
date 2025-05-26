# Copyright (c) 2025 Shraddha Borah
# All rights reserved. This file is part of a proprietary software project.
# Unauthorized use or distribution is prohibited.

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
            
        # Get highest quality stream that includes both video and audio
        stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
        if not stream:
            raise ValueError("No suitable video stream found")
            
        # Create a temporary file that will be automatically cleaned up
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
    # Return both segments and the full text
    return {
        'segments': result['segments'],
        'full_text': result['text'],
        'language': result.get('language', 'unknown')
    }

def extract_keywords(segments):
    kw_model = KeyBERT()
    key_segments = []
    for segment in segments:
        keywords = kw_model.extract_keywords(segment['text'], top_n=3)
        if keywords:
            key_segments.append({
                "start_time": segment['start'],
                "end_time": segment.get('end', segment['start'] + 5),  # Default 5s if no end time
                "text": segment['text'],
                "keywords": [kw[0] for kw in keywords],  # Get top 3 keywords
                "confidence": segment.get('confidence', 0.0)
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
        frame_path = extract_frame(video_path, seg["start_time"])
        enriched_output.append({
            "start_time": seg["start_time"],
            "end_time": seg["end_time"],
            "text": seg["text"],
            "keywords": seg["keywords"],
            "confidence": seg["confidence"],
            "image": frame_path
        })
    return enriched_output

def process_uploaded_file(video_path):
    # Extract audio and transcribe
    audio_path = extract_audio(video_path)
    transcription = transcribe_audio(audio_path)
    
    # Process segments with keywords
    key_segments = extract_keywords(transcription['segments'])
    
    # Generate final output with frames
    results = generate_multimodal_transcript(video_path, key_segments)
    
    # Add metadata
    return {
        'summary': transcription['full_text'],
        'language': transcription['language'],
        'segments': results,
        'total_duration': key_segments[-1]['end_time'] if key_segments else 0,
        'processed_at': os.path.getmtime(video_path)
    }
