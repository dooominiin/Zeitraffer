import time
import picamera
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import glob
import subprocess
from datetime import datetime
from fractions import Fraction

# Set camera resolution and frame rate
#camera = picamera.PiCamera(sensor_mode = 3) 
camera = picamera.PiCamera()
# Turn the camera's LED off
camera.led = False
camera.resolution = (2592,1458)
camera.rotation = 180
camera.framerate = 2
camera.iso = 100 
camera.shutter_speed = 33333  # Zeit in Mikrosekunden
time.sleep(2)  # Wartezeit, damit sich die Einstellungen auswirken können
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = (Fraction(110, 100), Fraction(180, 100))
time.sleep(0.2)  # Wartezeit, damit sich die Einstellungen auswirken können

# Define file name prefix and image format
filename_prefix = "timelapse"
image_format = "jpg"

# Set up array to store images
images = []
max_Images = 360
# Define directory paths
image_dir_path = "/home/raspi/Desktop/Zeitraffer/Images"
video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video"
log_dir_path = "/home/raspi/Desktop/Zeitraffer/Log"

# Create directories if they don't exist
if not os.path.exists(image_dir_path):
    os.makedirs(image_dir_path)

if not os.path.exists(video_dir_path):
    os.makedirs(video_dir_path)
    
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

# Capture image
filename = "{}_{:04d}.{}".format(filename_prefix, len(glob.glob(os.path.join(image_dir_path, "*.{}".format(image_format)))), image_format)
file_path = os.path.join(image_dir_path, filename)
camera.capture(file_path,resize = (1920,1080))

# Get current timestamp
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# Write to log file
log_filename = "timelapse_log.txt"
log_file_path = os.path.join(log_dir_path, log_filename)
log_string = "{} {} exposure_speed: {} awb_gains: {} analog_gain: {} digital_gain: {}\n".format(timestamp, filename,camera.exposure_speed,camera.awb_gains,camera.analog_gain,camera.digital_gain)
with open(log_file_path, "a") as f:
    f.write(log_string)

# Load image as PIL Image object
image = Image.open(file_path)

# Add timestamp as text to image
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
draw = ImageDraw.Draw(image)
draw.text((10, 10), timestamp, font=font, fill=(255, 255, 255))

# Save image with timestamp
image.save(file_path)

# Kamera abschalten
camera.close()


# Load image as numpy array and append to list
image = np.array(Image.open(file_path))
images.append(image)

# Check if there are more than a number of images in the directory
if len(glob.glob(os.path.join(image_dir_path, "*.{}".format(image_format)))) >= max_Images:
    # Create video with images
    video_filename_prefix = "timelapse_video"
    video_filename = "{}_{:04d}.{}".format(video_filename_prefix, len(glob.glob(os.path.join(video_dir_path, "*.mp4"))) + 1, "mp4")
    video_file_path = os.path.join(video_dir_path, video_filename)
    subprocess.call(["ffmpeg", "-framerate", "30", "-pattern_type", "glob", "-i", "{}/*.{}".format(image_dir_path, image_format), "-c:v", "libx264", "-preset", "ultrafast", video_file_path])
    # Delete images
    for file_path in glob.glob(os.path.join(image_dir_path, "*.{}".format(image_format))):
        os.remove(file_path)