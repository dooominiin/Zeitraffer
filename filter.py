from PIL import Image
import numpy as np

# Pfad zum Bild angeben
image_path = "Images/timelapse_0131.jpg"

# Bild mit Pillow öffnen
image = Image.open(image_path)

# Bild in den HSV-Farbraum konvertieren
hsv_image = image.convert("HSV")

# HSV-Bild als Numpy-Array konvertieren
hsv_array = np.array(hsv_image)

# V-Kanal extrahieren
v_channel = hsv_array[:, :, 2]

# Mittelwert des V-Kanals berechnen
mean_v = np.mean(v_channel)

# Mittelwert ausgeben
print("Mittelwert des V-Kanals:", mean_v)