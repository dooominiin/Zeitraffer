import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    print(camera.exposure_speed,camera.iso)
    time.sleep(5)
    
    camera.stop_preview()