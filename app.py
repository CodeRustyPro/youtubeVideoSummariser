import streamlit as st
import google.generativeai as genai
import yt_dlp
import os
import time
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

st.title("YouTube Video Summarizer 🎙️📜")

def download_audio(youtube_url, output_path="audio"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return output_path + ".mp3"

youtube_url = st.text_input("Enter YouTube URL")

if st.button("Summarize", disabled=not youtube_url):  # Disable if no URL
    if youtube_url:
        progress_bar = st.progress(0)  # Initialize progress bar
        status_text = st.empty()  # Placeholder for status updates

        try:
            # Step 1: Download Audio
            status_text.text("🔽 Downloading video...")
            progress_bar.progress(20)
            audio_path = download_audio(youtube_url)
            time.sleep(1)  # Simulate processing time

            # Step 2: Upload Audio
            status_text.text("☁️ Uploading...")
            progress_bar.progress(50)
            mime_type = "audio/mpeg"
            myfile = genai.upload_file(audio_path, mime_type=mime_type)
            time.sleep(1)

            # Step 3: Generate Summary
            status_text.text("🤖 Generating summary...")
            progress_bar.progress(80)
            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content([myfile, "Summarize this. Be Educational and Insightful."])
            time.sleep(1)

            # Step 4: Display Summary
            progress_bar.progress(100)
            status_text.text("✅ Done!")
            st.success("Summary:")
            st.write(result.text)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            status_text.text("❌ Process failed.")

    else:
        st.error("Please enter a valid YouTube URL.")
