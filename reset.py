import shutil
import os

# Define directory paths
image_dir_path = "/home/raspi/Desktop/Zeitraffer/Images"
video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video"
log_dir_path = "/home/raspi/Desktop/Zeitraffer/Log"


# Delete directories if they exist
if os.path.exists(image_dir_path):
    shutil.rmtree(image_dir_path)
    
if os.path.exists(video_dir_path):
    shutil.rmtree(video_dir_path)
    
if os.path.exists(log_dir_path):
    shutil.rmtree(log_dir_path)

print("Folders deleted.")
