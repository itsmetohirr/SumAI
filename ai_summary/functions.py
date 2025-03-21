import os
import re

import dotenv
from openai import OpenAI
from supadata import Supadata
import googleapiclient.discovery as google

dotenv.load_dotenv()


def url_to_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/|.*[?&]v=)|youtu\.be\/)([\w-]{11})'
    video_id = re.search(pattern, url).group(1)

    return video_id


def get_transcript(url):
    api_key = os.getenv('SUPADATA_API_KEY')
    supadata = Supadata(api_key=api_key)

    video_id = url_to_id(url)

    text_transcript = supadata.youtube.transcript(
        video_id=video_id,
        text=True
    )

    return text_transcript.content


def summarize_transcript(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a blog post writer."},
            {
                "role": "user",
                "content": (
                    "Based on the following transcript from a YouTube video, summarize the video. Use emojis to make it engaging. in Uzbek language"
                    f"Transcript:\n\n{text}\n\n"
                ),
            },
        ],
        max_tokens=700,
    )
    
    content = response.choices[0].message.content
    print(content)
    return content


def get_video_title(url):
    DEV_KEY = os.getenv('GOOGLE_API_KEY')
    youtube = google.build('youtube', 'v3', developerKey=DEV_KEY)


    response = youtube.videos().list(part='snippet', id=url_to_id(url)).execute()

    if 'items' in response and len(response['items']) > 0:
        video_title = response['items'][0]['snippet']['title']
        return video_title
    else:
        return 'Video not found'

print(get_video_title('https://youtu.be/-qjE8JkIVoQ?si=1gZ-zeQo1zZlduPt'))
