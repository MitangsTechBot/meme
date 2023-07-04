import praw
import os
import random
import re
import requests
import moviepy.editor as mp
from instagrapi import Client
import time
import sys


# Create a Reddit instance using PRAW
reddit = praw.Reddit(
    client_id="H1XhjISyjcZjh0IZwS-XPQ",
    client_secret="VfSRW9NzqJp2hCkirKSSnS-4jjhm7g",
    user_agent="Mitang/1.0 by Mituu24"
)

# # Specify the subreddit channels to choose from in the desired order
subreddit_channels = ["SaimanSays", "Indian__Memes", "PoliticalIndianMemes",
                      "IndiaKeMemes", "indianmemer", "IndianMemeTemplates", "HindiMemes", "marvelmemes", "IndianDankMemes", "dankinindia", "videomemes", "MandirGang", "IndianMeyMeys", "JEENEETards", "sunraybee", "CricketShitpost", "DesiVideoMemes", "indiameme", "FingMemes", "dankrishu", "CarryMinati"]


# Load the list of used channels from a file (if exists)
used_channels_file = 'used_channels.txt'
used_channels = []
if os.path.exists(used_channels_file):
    with open(used_channels_file, 'r') as f:
        used_channels = f.read().splitlines()

# Check if all subreddit channels have been used
if len(used_channels) == len(subreddit_channels):
    # Reset the used channels list
    used_channels = []
    print("All subreddit channels have been used. Resetting the list.")

# Exclude the used channels from the subreddit channels list
remaining_channels = [
    channel for channel in subreddit_channels if channel not in used_channels]

# Check if there are remaining channels to choose from
if not remaining_channels:
    print("All subreddit channels have been used.")
else:
    video_downloaded = False
    while not video_downloaded:
        try:
            # Select the next channel from the remaining channels
            subreddit_channel = random.choice(remaining_channels)

            # Retrieve all video posts from the subreddit channel
            subreddit = reddit.subreddit(subreddit_channel)
            posts = subreddit.new(limit=100)

            # Filter out non-video posts and keep only the URLs of videos with 9:16 aspect ratio
            urls = []
            for post in posts:
                if post.is_video:
                    video = post.media['reddit_video']
                    if video['height'] / video['width'] == 16 / 9 or video['height'] / video['width'] == 1 / 2 or video['height'] / video['width'] == 2 / 3 or video['height'] / video['width'] == 4 / 5 or video['height'] / video['width'] == 1 / 1:
                        urls.append((video['fallback_url'], post.title))

            # Choose a video URL and post title if available
            if urls:
                # Choose the first video URL and post title
                video_url, post_title = urls[0]

                # Check if the video with the same title already exists in the videos folder
                cleaned_post_title = re.sub(r'[^\w\s-]', '', post_title)
                cleaned_post_title = re.sub(r'[-\s]+', ' ', cleaned_post_title)
                video_title = f"{cleaned_post_title}.mp4"
                video_path = os.path.join('videos', video_title)
                if os.path.exists(video_path):
                    print(
                        f"Video with the same title already exists. Trying another video. ")
                    continue

                audio_url = "https://v.redd.it/" + \
                    video_url.split("/")[3] + "/DASH_audio.mp4"
                video_downloaded = True

                # Download and save the video
                video_path_temp = os.path.join(
                    'temp_videos', video_title)
                response = requests.get(video_url)
                with open(video_path_temp, "wb") as f:
                    f.write(response.content)

                # Download and save the audio
                audio_title = "audio.mp4"
                audio_path = os.path.join(
                    'temp_videos', audio_title)
                response = requests.get(audio_url)
                with open(audio_path, "wb") as f:
                    f.write(response.content)

                # Combine video and audio using moviepy
                output_path = os.path.join(
                    'videos', video_title)
                video_clip = mp.VideoFileClip(video_path_temp)
                audio_clip = mp.AudioFileClip(audio_path)
                final_clip = video_clip.set_audio(audio_clip)
                final_clip.write_videofile(
                    output_path, codec="libx264", audio_codec="aac")

                # Delete the audio and temporary video files
                os.remove(audio_path)
                os.remove(video_path_temp)

                print(
                    f'Video downloaded successfully from the subreddit channel: {subreddit_channel}!')
            else:
                print(
                    f'No videos found in subreddit channel: {subreddit_channel}. Trying another channel.')

            # Remove the current channel from the remaining channels
            remaining_channels.remove(subreddit_channel)

            # Append the current channel to the used channels list
            used_channels.append(subreddit_channel)

            # Save the updated used channels list to the file
            with open(used_channels_file, 'w') as f:
                f.write('\n'.join(used_channels))

        except IndexError:
            print("Cannot choose from an empty sequence. Rerunning the code.")

# Initialize client
client = Client()
client.login("69Memes_ai", "mitang@@321")
client.dump_settings("session.json")

# Folder path containing videos
folder_path = "C:/Users/Mitang/Desktop/ig_upload/videos"

# Get all video files in the folder
video_files = [file for file in os.listdir(
    folder_path) if file.endswith(".mp4")]

# Sort the video files by modification time (newest first)
video_files.sort(key=lambda x: os.path.getmtime(
    os.path.join(folder_path, x)), reverse=True)

if video_files:
    # Get the latest video file
    latest_video_file = video_files[0]

    # Get video file path
    video_path = os.path.join(folder_path, latest_video_file)

    # Get video title
    video_title = os.path.splitext(latest_video_file)[0]

    # Set caption as video title with #meme
    caption = f"{video_title} \n . \n . \n . \n . \n Tags:#meme #memes #memesdaily #dankmemes #funnymemes #memestagram #memepage #memes😂 #edgymemes #memer #offensivememes #dankmeme #memesespañol #dailymemes #memesbrasil"

    # Upload reel
    upload_id = client.clip_upload(video_path, caption=caption)
    time.sleep(10)  # Wait for the video to process

    # # Publish reel
    # client.media_share(upload_id, caption=caption, media_type="video")

    print(f"Latest video '{latest_video_file}' uploaded successfully.")
else:
    print("No video files found in the folder.")

# Logout
client.logout()


sys.exit()
