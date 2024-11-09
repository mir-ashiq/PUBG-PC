import os
import requests
from dotenv import load_dotenv

load_dotenv()
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('PAGE_ID')
VIDEO_DIRECTORY = os.getenv('VIDEO_DIRECTORY')


def upload_reel_to_facebook(video_path, description):

    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/video_reels"
    
    data = {
        'access_token': PAGE_ACCESS_TOKEN,
        'upload_phase': "start",
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        video_id = response.json().get('video_id')
        print("Video uploaded successfully!")
        print("Video ID: ", video_id)
    else:
        print("Failed to upload video")
        print("Response:", response.json())
    
    upload_url = f"https://rupload.facebook.com/video-upload/v21.0/{video_id}"

    headers = {
        'Authorization': f'OAuth {PAGE_ACCESS_TOKEN}',
        'offset': 0,
        'file_size': os.path.getsize(video_path),
    }
    with open(video_path, 'rb') as video_file:
        upload_response = requests.post(upload_url, headers=headers, data=video_file)
    
    if upload_response.status_code == 200:
        print("Video uploaded successfully!")
        print(upload_response.json())
    else:
        print("Failed to upload video")
        print("Response:", upload_response.json())
    
    publish_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/video_reels"

    data = {
        'access_token': PAGE_ACCESS_TOKEN,
        'upload_phase': "finish",
        'video_id': video_id,
        'description': description,
        'video_state': "PUBLISHED"
    }

    publish_response = requests.post(publish_url, data=data)
    if publish_response.status_code == 200:
        print("Video published successfully!")
        print(publish_response.json())
    else:
        print("Failed to publish video")
        print("Response:", publish_response.json())

if __name__ == "__main__":
    
    VIDEO_PATH = 'path_to_your_video.mp4'
    DESCRIPTION = 'Your video description'

    upload_reel_to_facebook(VIDEO_PATH, DESCRIPTION)