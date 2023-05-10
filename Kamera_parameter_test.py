import os
import time
import picamera
from fractions import Fraction

# Anzahl der Fotos
num_photos = 10

# Pfad zum Ausgabeordner
output_dir = 'Test'

# Kamera-Initialisierung
camera = picamera.PiCamera(sensor_mode = 3) 
camera.resolution = (2592,1944)
camera.framerate = Fraction(1,6)

# Erstelle den Ordner "Test", wenn er nicht existiert
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Liste der Belichtungszeiten und Empfindlichkeiten zum Testen
exposure_times = [2000, 8000,32000,128000, 512000]  # in Mikrosekunden
sensitivities = [100, 200, 400, 800] 

# Testbilder aufnehmen
for exp_time ,sens in zip(exposure_times,sensitivities):
    
    # Setze die Kamera-Einstellungen für dieses Foto
    camera.shutter_speed = exp_time  # Zeit in Mikrosekunden
    camera.iso = sens  # Empfindlichkeit
    time.sleep(0.5)  # Wartezeit, damit sich die Einstellungen auswirken können

    # Dateiname für das aktuelle Foto
    filename = f"Test/img_{exp_time}us_{sens}iso.jpg"
    # Aufnahme des Fotos
    camera.capture(filename,resize=(1920, 1080))

# Kamera abschalten
camera.close()

# Kamera-Initialisierung
camera = picamera.PiCamera(sensor_mode = 3) 
camera.resolution = (2592,1944)
camera.framerate = Fraction(1,6)

modes = {'off',
    'auto',
    'night',
    'nightpreview',
    'backlight',
    'spotlight',
    'sports',
    'snow',
    'beach',
    'verylong',
    'fixedfps',
    'antishake',
    'fireworks'}

for mode in modes:

    camera.exposure_mode = mode
    time.sleep(0.5) 
    # Dateiname für das aktuelle Foto
    filename = f"Test/img_{mode}_mode_{camera.exposure_speed}_us_{100*float(camera.analog_gain)}_iso.jpg"
    # Aufnahme des Fotos
    camera.capture(filename,resize=(1920, 1080))

# Kamera abschalten
camera.close()
