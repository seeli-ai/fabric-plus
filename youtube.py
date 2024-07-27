import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
from datetime import datetime
import os


def get_video_id(url):
    # Extract video ID from URL
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_comments(youtube, video_id):
    comments = []

    try:
        # Fetch top-level comments
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100  # Adjust based on needs
        )

        while request:
            response = request.execute()
            for item in response['items']:
                # Top-level comment
                topLevelComment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(topLevelComment)

                # Check if there are replies in the thread
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        replyText = reply['snippet']['textDisplay']
                        # Add incremental spacing and a dash for replies
                        comments.append("    - " + replyText)

            # Prepare the next page of comments, if available
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list_next(
                    previous_request=request, previous_response=response)
            else:
                request = None

    except HttpError as e:
        print(f"Failed to fetch comments: {e}")

    return comments


def get_transcript(url, lang="en") -> str:
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found")
        return None

    # Extract video ID from URL
    video_id = get_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")
        return None

    try:
        # Initialize the YouTube API client
        youtube = build("youtube", "v3", developerKey=api_key)

        # Get video details
        video_response = youtube.videos().list(
            id=video_id, part="contentDetails,snippet").execute()

        title = video_response['items'][0]['snippet']['title']
        channel = video_response['items'][0]['snippet']['channelTitle']

        title = title + " - " + channel

        # Get video transcript
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, languages=[lang])
            transcript_text = " ".join([item["text"]
                                       for item in transcript_list])
            # transcript_text = transcript_text.replace("\n", " ")
        except Exception as e:
            transcript_text = f"Transcript not available in the selected language ({lang}). ({e})"

        transcript_text = f"### {title} \n\n {transcript_text}"

        return transcript_text.encode('utf-8').decode('unicode-escape')

    except HttpError as e:
        print(
            f"Error: Failed to access YouTube API. Please check your YOUTUBE_API_KEY and ensure it is valid: {e}")


if __name__ == "__main__":
    res = get_transcript("https://youtu.be/RMV130vU8gA?si=l5narmlO2SL6vtH8")
    print(res)
