from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import uuid
import os

app = Flask(__name__)
CORS(app)

@app.route("/download", methods=["POST"])
def download_audio():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    temp_filename = f"{uuid.uuid4()}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': temp_filename,
        'quiet': True,
        'noplaylist': True,  # Only one video at a time for streaming
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = send_file(temp_filename, as_attachment=True)

        @response.call_on_close
        def cleanup():
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        return response

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ YouTube MP3 Stream API running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
