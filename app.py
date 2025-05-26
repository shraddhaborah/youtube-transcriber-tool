import streamlit as st
import os
import torch
from main import process_uploaded_file, process_youtube_url

# Disable torch's default multi-threading to avoid event loop conflicts
torch.set_num_threads(1)
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

st.set_page_config(page_title="🎬 Multimodal Transcriber", layout="wide")
st.title("🎥 YouTube & Video Multimodal Transcriber")

st.markdown("""
Upload your own video **OR** paste a YouTube URL to generate a visual + text transcript. 

⚠️ Only download videos you own or have permission to use. This tool supports both modes.
""")

mode = st.radio("Choose input method:", ["Upload Video File", "YouTube URL"])
video_path = None

if mode == "Upload Video File":
    uploaded_file = st.file_uploader("Upload a video file (.mp4, .webm, .mov)", type=["mp4", "webm", "mov"])
    if uploaded_file is not None:
        with open("temp_uploaded_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
        video_path = "temp_uploaded_video.mp4"

elif mode == "YouTube URL":
    youtube_url = st.text_input("Paste YouTube URL and press Enter:", help="Enter a valid YouTube video URL (e.g., https://www.youtube.com/watch?v=...)")
    if youtube_url:
        with st.spinner("⏳ Processing YouTube video..."):
            try:
                video_path = process_youtube_url(youtube_url)
            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")

if video_path:
    with st.spinner("🔍 Transcribing and analyzing the video..."):
        results = process_uploaded_file(video_path)
        st.success("✅ Transcript with visuals ready!")

        # Display summary and metadata
        st.header("📝 Summary")
        st.write(results['summary'])
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Language", results['language'].upper())
        with col2:
            st.metric("Duration", f"{results['total_duration']:.2f}s")
        with col3:
            st.metric("Segments", len(results['segments']))

        # Display detailed segments
        st.header("🎬 Detailed Transcript")
        for segment in results['segments']:
            with st.expander(f"Segment {segment['start_time']:.2f}s - {segment['end_time']:.2f}s"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(segment["image"])
                with col2:
                    st.markdown(f"**Text:** {segment['text']}")
                    st.markdown(f"**Keywords:** {', '.join(segment['keywords'])}")
                    st.progress(segment['confidence'])
