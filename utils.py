from __future__ import annotations
import os
import cv2
from moviepy import VideoFileClip


def process_video_segments(input_path, start_time, end_time, window_size, output_dir="output_segments"):
    """
    Iterates through a time range and processes video segments.
    
    Args:
        input_path (str): Path to the source video.
        start_time (int): Start time in seconds.
        end_time (int): End time in seconds.
        window_size (int): The duration of each segment (sliding window size).
        output_dir (str): Directory to save outputs. Defaults to "output_segments".
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for current_start in range(start_time, end_time, window_size):
        # Determine the end of the current segment (handling the last chunk)
        current_end = min(current_start + window_size, end_time)

        print(f"Processing from {current_start} to {current_end}")

        # Construct file paths safely
        vid_filename = f"video_{current_start}_{current_end}.mp4"
        aud_filename = f"audio_{current_start}_{current_end}.mp3"
        
        process_video(
            input_path=input_path,
            start_sec=current_start,
            end_sec=current_end,
            output_video_path=os.path.join(output_dir, vid_filename),
            output_audio_path=os.path.join(output_dir, aud_filename)
        )

def get_duration(filename):
    video = cv2.VideoCapture(filename)
    
    if not video.isOpened():
        print("Could not open video")
        return None

    # Get frame count and fps (frames per second)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    
    duration = frame_count / fps
    
    video.release()
    print(f"Duration: {duration} seconds") 



def process_video(input_path, output_video_path, output_audio_path, start_sec, end_sec):
    try:
        # 1. Load the video file
        print(f"Loading video: {input_path}")
        video = VideoFileClip(input_path)

        # 2. Cut the video (subclip)
        sliced_video = video.subclipped(start_sec, end_sec)

        # 3. Write the sliced video to a file
        print(f"Saving sliced video to: {output_video_path}")
        # Note: In v2.0, we usually don't need to specify codec='libx264' manually 
        # unless there is an issue, but we will keep it for safety.
        sliced_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

        # 4. Extract and save the audio from the sliced portion
        print(f"Extracting audio to: {output_audio_path}")
        
        # Check if video actually has audio
        if sliced_video.audio:
            sliced_video.audio.write_audiofile(output_audio_path)
        else:
            print("Warning: The video slice has no audio track.")

        # 5. Clean up resources
        video.close()
        sliced_video.close()
        print("Done!")

    except Exception as e:
        print(f"An error occurred: {e}")