from flask import Flask, request, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ YouTube Playlist MP3 Downloader API is running!"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    playlist_url = data.get("url")
    if not playlist_url:
        return jsonify({"error": "No playlist URL provided"}), 400

    download_id = str(uuid.uuid4())
    output_dir = os.path.join("downloads", download_id)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ffmpeg_location': 'ffmpeg',
        'quiet': True,
        'noplaylist': False,
        'ignoreerrors': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        return jsonify({"status": "success", "message": f"Downloaded to folder: {download_id}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
