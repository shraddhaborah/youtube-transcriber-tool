import streamlit as st
from main import process_uploaded_file, process_youtube_url

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
    youtube_url = st.text_input("Paste YouTube URL:")
    if st.button("Download Video") and youtube_url:
        try:
            video_path = process_youtube_url(youtube_url)
            st.success("YouTube video downloaded successfully!")
        except Exception as e:
            st.error(f"❌ Failed to download YouTube video. Reason: {e}")

if video_path:
    with st.spinner("🔍 Transcribing and analyzing the video..."):
        results = process_uploaded_file(video_path)
        st.success("✅ Transcript with visuals ready!")

        for r in results:
            st.image(r["image"], caption=f"{r['keyword']} @ {r['timestamp']:.2f}s")
            st.markdown(f"**Transcript:** {r['text']}")
