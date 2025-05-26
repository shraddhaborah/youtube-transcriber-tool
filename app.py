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
    youtube_url = st.text_input("Paste YouTube URL:", help="Enter a valid YouTube video URL (e.g., https://www.youtube.com/watch?v=...)")
    if st.button("Download Video"):
        if not youtube_url:
            st.warning("⚠️ Please enter a YouTube URL first")
        else:
            with st.spinner("⏳ Downloading video..."):
                try:
                    video_path = process_youtube_url(youtube_url)
                    st.success("✅ YouTube video downloaded successfully!")
                except ValueError as e:
                    st.error(f"❌ {str(e)}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")

if video_path:
    with st.spinner("🔍 Transcribing and analyzing the video..."):
        results = process_uploaded_file(video_path)
        st.success("✅ Transcript with visuals ready!")

        for r in results:
            st.image(r["image"], caption=f"{r['keyword']} @ {r['timestamp']:.2f}s")
            st.markdown(f"**Transcript:** {r['text']}")
