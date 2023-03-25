from gpiozero import OutputDevice
from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import CPUTemperature

from collections import deque
import pytz
from datetime import datetime
from threading import Thread
import time
import sys
import cv2
import numpy as np
import io, gc

class Camera:
    def __init__(self,):
        IRPin = OutputDevice(36)
        IRPin.off() # Set the pin to low
        time.sleep(2)

    def fill_queue(self, deque):
        with PiCamera(resolution=(2592, 1944), framerate=3, sensor_mode=4) as camera:
            camera.vflip = False
            camera.hflip = False
            camera.exposure_mode = 'sports'
            time.sleep(2)
            stream = io.BytesIO()
            for i, frame in enumerate(camera.capture_continuous(stream, format="jpeg", use_video_port=True)):
                stream.seek(0)
                data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
                image = cv2.imdecode(data, 1)
                deque.append(
                    (datetime.now(pytz.timezone('Europe/Zurich')).strftime("%Y_%m_%d_%H-%M-%S.%f"), image))
                print("Quelength: " + str(len(deque)) + "\tStreamsize: " + str(sys.getsizeof(stream)))
                if i == 60:
                    print("Loop ended, starting over.")
                    stream.seek(0)
                    stream.truncate()
                    time.sleep(2)
                    continue
                stream.seek(0)
                stream.truncate()


