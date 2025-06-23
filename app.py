from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import random

app = Flask(__name__)
CORS(app)

output_dir = 'downloads'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 🔁 Free rotating proxies
proxy_list = [
    'http://8.210.117.141:8888',
    'http://45.92.108.112:80',
    'http://73.155.14.120:80',
    'http://51.159.28.39:80',
    'http://219.65.73.81:80',
    'http://57.129.81.201:8080',
    'http://32.223.6.94:80',
    'http://133.18.234.13:80',
    'http://123.140.160.50:5031',
    'http://123.140.160.65:5031',
    'http://85.215.64.49:80',
    'http://190.58.248.86:80',
    'http://50.122.86.118:80',
    'http://50.172.150.134:80',
    'http://123.140.160.64:5031',
    'http://103.154.87.12:80',
    'http://103.214.109.70:80',
    'http://103.214.109.67:80',
    'http://123.140.146.31:5031',
    'http://123.140.160.62:5031',
    'http://156.38.112.11:80',
    'http://200.174.198.86:8888',
    'http://198.23.143.74:80',
    'http://23.247.136.254:80',
    'http://4.245.123.244:80',
    'http://92.67.186.210:80',
    'http://154.118.231.30:80',
    'http://4.195.16.140:80'
]

@app.route("/download", methods=["POST"])
def download_audio():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    proxy_to_use = random.choice(proxy_list)
    print(f"🌐 Using proxy: {proxy_to_use}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'proxy': proxy_to_use,
        'quiet': True,
        'noplaylist': False,
        'ignoreerrors': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"status": "success", "message": "Download completed"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return "✅ YouTube Playlist MP3 Downloader API is running!"

if __name__ == "__main__":
    app.run(debug=True, port=10000)
