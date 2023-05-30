import os
import subprocess
import re

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
brightness_threshold = 0.9
filtered_video_file_path = os.path.join(merged_video_dir_path, "filtered_" + merged_video_filename)

# Extract blackdetect information from ffmpeg output
ffmpeg_cmd = ["ffmpeg", "-i", merged_video_file_path, "-vf", "blackdetect=d=0.016666666666666666:pix_th={}".format(brightness_threshold), "-f", "null", "-"]
output = subprocess.check_output(ffmpeg_cmd, stderr=subprocess.STDOUT)
output_str = output.decode("utf-8")

blackdetect_info = []
pattern = r"black_start:([\d.]+) black_end:([\d.]+)"
matches = re.findall(pattern, output_str)
for match in matches:
    start_time = float(match[0])
    end_time = float(match[1])
    blackdetect_info.append({"lavfi.black_start": start_time, "lavfi.black_end": end_time})

# Process blackdetect information
trim_filter = ""
for i, info in enumerate(blackdetect_info):
    start_time = float(info["lavfi.black_start"])
    end_time = float(info["lavfi.black_end"])
    trim_filter += "[0:v]trim=start={}:end={},setpts=PTS-STARTPTS[v{}];[0:a]atrim=start={}:end={},asetpts=PTS-STARTPTS[a{}];".format(
        start_time, end_time, i, start_time, end_time, i
    )

filter_complex = "{}concat=n={}:v=1:a=1[v][a]".format(trim_filter, len(blackdetect_info))
subprocess.call(
    [
        "ffmpeg",
        "-i",
        merged_video_file_path,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        filtered_video_file_path,
    ]
)