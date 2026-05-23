from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/download")
async def download_instagram(url: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',  # કૂકીઝ ફાઈલ અહીં કનેક્ટ કરી દીધી છે
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # વિડીયોનું ટાઈટલ મેળવો
            title = info.get('title', 'Instagram_Video')
            # વિડીયોની ડાયરેક્ટ લિંક
            video_url = info.get('url')

            if not video_url:
                raise HTTPException(status_code=400, detail="વિડીયો લિંક મળી નહિ.")

            # આ રિટર્ન ડેટા જ છે
            return {
                "status": "success",
                "download_url": video_url,
                "title": title
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
