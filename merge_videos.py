import os
import subprocess

# Define directory paths
video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video"
merged_video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video_komplett"

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


# Filter the frames based on brightness using ffmpeg
brightness_threshold = 100
filtered_video_file_path = os.path.join(merged_video_dir_path, "filtered_" + merged_video_filename)
subprocess.call(["ffmpeg", "-i", merged_video_file_path, "-vf", "blackdetect=d={}:pix_th={}".format(1/60, brightness_threshold), "-c:v", "copy", "-an", "-f", "null", "-",
                 "-vf", "select=not(between(t\, {}, {}))".format(0, 1/60), "-c:v", "libx264", "-preset", "ultrafast", filtered_video_file_path])
