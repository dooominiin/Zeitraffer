import moviepy

import os
import subprocess
import re
from moviepy.editor import VideoFileClip, concatenate
from moviepy.editor import ImageSequenceClip
import numpy as np
from PIL import Image

# Define directory paths
video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video"
merged_video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video_komplett"


def merge_Video(video_dir_path, merged_video_dir_path):
    # Create directory if it doesn't exist
    if not os.path.exists(merged_video_dir_path):
        os.makedirs(merged_video_dir_path)

    # Define file name prefix, suffix, and video format
    video_filename_prefix = "timelapse_video"
    video_suffix = "_merged"
    video_format = "mp4"

    # Define output video file path
    merged_video_filename = "timelapse_video{}.".format(video_suffix) + video_format
    merged_video_file_path = os.path.join(merged_video_dir_path, merged_video_filename)
    
    # Check if merged video file already exists
    if os.path.exists(merged_video_file_path):
        index = 1
        while True:
            # Append an index to the filename to avoid overwriting existing files
            merged_video_filename = "timelapse_video{}_{}.".format(video_suffix, index) + video_format
            merged_video_file_path = os.path.join(merged_video_dir_path, merged_video_filename)
            if not os.path.exists(merged_video_file_path):
                break
            index += 1
    
    # Create list of input video file paths
    video_file_paths = sorted([os.path.join(video_dir_path, filename) for filename in os.listdir(video_dir_path) if filename.startswith(video_filename_prefix) and filename.endswith(video_format)])

    # Write video_file_paths to mylist.txt
    with open("mylist.txt", "w") as f:
        for path in video_file_paths:
            f.write("file '{}'\n".format(path))
            print("file '{}'\n".format(path))

    # Concatenate the videos using ffmpeg
    subprocess.call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "mylist.txt", "-vf", "setpts=0.125*PTS,select='not(mod(n,2))'", "-c:v", "libx264", "-preset", "ultrafast", merged_video_file_path])
    return [merged_video_file_path] 

def check_brightness(frame):
    # Konvertieren Sie den Frame in den HSV-Farbraum
    hsv_frame = frame.convert("HSV")
    
    # Extrahieren Sie den V-Kanal (Helligkeitskanal)
    v_channel = np.array(hsv_frame)[:, :, 2]
    
    # Definieren Sie Ihre Bedingungen für die Helligkeit
    brightness_threshold = 20  # Beispielwert für die Helligkeitsschwelle
    
    # Überprüfen Sie die Helligkeit des Frames
    is_not_bright = np.mean(v_channel) < brightness_threshold
    
    return is_not_bright

def create_delete_frames_array(input_video):
    # Video mit MoviePy öffnen
    video = VideoFileClip(input_video)

    # Array zum Speichern der Löschinformationen erstellen
    delete_frames = []

    # Schleife über jeden Frame im Video
    for idx, frame in enumerate(video.iter_frames(), start=1):
        # Überprüfen Sie die Helligkeit des Frames
        is_bright = check_brightness(Image.fromarray(frame))
        
        # Hinzufügen des Löschstatus zum Array
        delete_frames.append(not is_bright)
        
        print(f"Frame Nr. : {idx}")

    # Video-Objekt freigeben
    video.close()

    return delete_frames

def delete_frames_in_video(merged_video_file_path, delete_frames):
    merged_video_dir_path = os.path.dirname(merged_video_file_path)
    merged_video_filename = os.path.basename(merged_video_file_path)
    filtered_video_file_path = os.path.join(merged_video_dir_path, "filtered_" + merged_video_filename)
    
    
    # ffmpeg-Befehl zum Löschen der Frames
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        merged_video_file_path,
        "-vf",
        f"select='not(eq(n\,{''.join(str(i) for i, delete in enumerate(delete_frames) if delete)})',setpts=N/FRAME_RATE/TB",
        "-af",
        f"aselect='not(eq(n\,{''.join(str(i) for i, delete in enumerate(delete_frames) if delete)})',asetpts=N/SR/TB",
        "-c:v",
        "libx264",
        "-c:a",
        "copy",
        filtered_video_file_path
    ]


    # ffmpeg-Befehl ausführen
    subprocess.call(ffmpeg_command)



if __name__ == "__main__":
    #merged_video_file_path = merge_Video(video_dir_path, merged_video_dir_path)
    print("hallo")
    merged_video_file_path = "/home/raspi/Desktop/Zeitraffer/Video_komplett/timelapse_video_merged.mp4"
    delete_frames = create_delete_frames_array(merged_video_file_path)
    
    delete_frames_in_video(merged_video_file_path, delete_frames)
