import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

import googleapiclient.discovery


# Dev
load_dotenv()  # take environment variables from .env.


app = FastAPI(title="Talk2Me_Nice ProxyAPI")

API_SERVICE = os.getenv('GOOGLE_API_SERVICE', "youtube")
API_VERSION = os.getenv('GOOGLE_API_VERSION', "v3")
DEVELOPER_KEY = os.getenv('GOOGLE_DEVELOPER_KEY')

@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/api/yt/test/")
def test():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        API_SERVICE, API_VERSION, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part=["snippet", "replies"],
        # parentId="UgzDE2tasfmrYLyNkGt4AaABAg"
        videoId="wtLJPvx7-ys",
        textFormat="plainText"
    )
    response = request.execute()

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        
    # print(f"Comment by {author}: {text}")
    return {'comment': comment, 'author': author, 'text': text}


# We'll extract the video ID from the frontend (I guess)
@app.get("/api/yt/v1/search/")
async def video_comments(vid_id: str):
    """ `/api/yt/v1/search/?v=YZakS8vFcu4` """
    pass  # Forward API call to YT


class Comments(BaseModel):
    vid_id: str
    user_id: str
    token: Union[str, None] = None  # Or session, depending on how we do things

@app.post("/api/yt/v1/comments/")
def video_comments():
    pass