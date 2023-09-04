import os
import subprocess
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image

def merge_Video(video_dir_path, merged_video_dir_path):
    # Verzeichnis erstellen, wenn es noch nicht existiert
    if not os.path.exists(merged_video_dir_path):
        os.makedirs(merged_video_dir_path)

    # Dateinamen-Präfix, Suffix und Videoformat definieren
    video_filename_prefix = "timelapse_video"
    video_suffix = "_merged"
    video_format = "mp4"

    # Pfad zur Ausgabedatei des zusammengeführten Videos festlegen
    merged_video_filename = "timelapse_video{}.".format(video_suffix) + video_format
    merged_video_file_path = os.path.join(merged_video_dir_path, merged_video_filename)
    
    # Überprüfen, ob die zusammengeführte Videodatei bereits existiert
    if os.path.exists(merged_video_file_path):
        os.remove(merged_video_file_path)
    
    # Liste der Eingabevideodateipfade erstellen
    video_file_paths = sorted([os.path.join(video_dir_path, filename) for filename in os.listdir(video_dir_path) if filename.startswith(video_filename_prefix) and filename.endswith(video_format)])

    # video_file_paths in mylist.txt schreiben
    with open("mylist.txt", "w") as f:
        for path in video_file_paths:
            f.write("file '{}'\n".format(path))
            print("file '{}'\n".format(path))

    # Videos mit ffmpeg zusammenführen
    subprocess.call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "mylist.txt", "-vf", "setpts=0.125*PTS,select='not(mod(n,2))'", "-c:v", "libx264", "-preset", "ultrafast", merged_video_file_path])
    os.remove("mylist.txt")
    return merged_video_file_path 

def check_brightness(frame):
    # Frame in den HSV-Farbraum konvertieren
    hsv_frame = frame.convert("HSV")
    
    # V-Kanal (Helligkeitskanal) extrahieren
    v_channel = np.array(hsv_frame)[:, :, 2]
    
    # Helligkeitsschwelle definieren
    brightness_threshold = 20  # Beispielwert für die Helligkeitsschwelle
    
    # Helligkeit des Frames überprüfen
    is_bright = np.mean(v_channel) > brightness_threshold
    
    return is_bright

def create_select_frames_array(input_video):
    # Video mit MoviePy öffnen
    video = VideoFileClip(input_video)

    # Array zum Speichern der Informationen über ausgewählte Frames erstellen
    select_frames = []

    # Schleife über jeden Frame im Video
    for idx, frame in enumerate(video.iter_frames(), start=1):
        # Helligkeit des Frames überprüfen
        is_bright = check_brightness(Image.fromarray(frame))
        
        # Auswählen des Frames und Status zum Array hinzufügen
        select_frames.append(is_bright)
        
        print(f"Frame Nr. : {idx}")

    # Video-Objekt freigeben
    video.close()

    return select_frames

def create_selected_frames_video(merged_video_file_path, select_frames):
    merged_video_dir_path = os.path.dirname(merged_video_file_path)
    merged_video_filename = os.path.basename(merged_video_file_path)
    filtered_video_file_path = os.path.join(merged_video_dir_path, "filtered_" + merged_video_filename)
    my_select_string = select_string(select_frames)
    
    # Überprüfen, ob die gefilterte Videodatei bereits existiert
    if os.path.exists(filtered_video_file_path):
        os.remove(filtered_video_file_path)

    # ffmpeg-Befehl zum Erstellen eines Videos mit den hellen Frames
    ffmpeg_command = [
        "ffmpeg",
        "-threads",
        "4",
        "-i",
        merged_video_file_path,
        "-vf",
        my_select_string,
        "-preset",
        "ultrafast",
        "-c:v",
        "libx264",
        "-c:a",
        "copy",
        filtered_video_file_path
    ]

    print(ffmpeg_command)

    # ffmpeg-Befehl ausführen
    subprocess.call(ffmpeg_command)

def select_string(bool_array):
    # Liste der Indexe erstellen, bei denen der Wert True ist
    selected_frames = [str(i) for i, is_frame_bright in enumerate(bool_array) if is_frame_bright]
    
    # Den String im gewünschten Format erstellen
    ffmpeg_select_string = "+".join([f"eq(n,{frame_index})" for frame_index in selected_frames])
    
    return f"select='{ffmpeg_select_string}',setpts=N/FRAME_RATE/TB"


if __name__ == "__main__":
    # Verzeichnispfade definieren
    video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video"
    merged_video_dir_path = "/home/raspi/Desktop/Zeitraffer/Video_komplett"
    
    merged_video_file_path = merge_Video(video_dir_path, merged_video_dir_path)
    #select_frames = create_select_frames_array(merged_video_file_path)
    #create_selected_frames_video(merged_video_file_path, select_frames)
