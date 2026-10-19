import os
import sys
import argparse
import yt_dlp

def download_media(url, mode="video", quality="1080", proxy=None):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
    }

    if proxy:
        ydl_opts['proxy'] = proxy

    if mode == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        if quality == "best":
            format_str = 'bestvideo+bestaudio/best'
        else:
            format_str = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best'
        
        ydl_opts.update({
            'format': format_str,
            'merge_output_format': 'mp4',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos or audio.")
    parser.add_argument("--url", required=True, help="YouTube URL")
    parser.add_argument("--mode", choices=["video", "audio"], default="video", help="Download mode")
    parser.add_argument("--quality", default="1080", help="Video height limit (e.g. 720, 1080, best)")
    
    args = parser.parse_args()
    proxy_env = os.getenv("PROXY_URL")
    download_media(args.url, args.mode, args.quality, proxy_env)
  
