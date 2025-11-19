from __future__ import annotations
from moviepy import VideoFileClip 

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