import moviepy

print(moviepy.__version__)
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
    is_bright = np.mean(v_channel) > brightness_threshold
    
    return is_bright

def create_delete_frames_array(input_video):
    # Video mit MoviePy öffnen
    video = VideoFileClip(input_video)

    # Array zum Speichern der Löschinformationen erstellen
    delete_frames = []

    # Schleife über jeden Frame im Video
    for idx, frame in enumerate(video.iter_frames(), start=1):
        # Überprüfen Sie die Helligkeit des Frames
        is_bright = check_brightness(frame)
        
        # Hinzufügen des Löschstatus zum Array
        delete_frames.append(not is_bright)
        
        print(f"Frame Nr. : {idx}")

    # Video-Objekt freigeben
    video.close()

    return delete_frames

def delete_frames_in_video(input_video, output_video, delete_frames):
    # ffmpeg-Befehl zum Löschen der Frames
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_video,
        "-vf",
        f"select='not(eq(n\,{'+'.join(str(i) for i, delete in enumerate(delete_frames) if delete))})',setpts=N/FRAME_RATE/TB",
        "-af",
        f"aselect='not(eq(n\,{'+'.join(str(i) for i, delete in enumerate(delete_frames) if delete))})',asetpts=N/SR/TB",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_video
    ]

    # ffmpeg-Befehl ausführen
    subprocess.call(ffmpeg_command)
