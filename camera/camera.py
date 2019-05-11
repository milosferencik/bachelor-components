import time
import io
import threading
import picamera
import os


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    name = "camera/" + os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
    nickname = name
    settings_topic = "settings/" + name
    save_video = False

    def set_nickname(self, name):
        Camera.nickname = "camera/" + name

    def get_nickname(self):
        return Camera.nickname

    def get_name(self):
        return Camera.name
    
    def get_settings_topic(self):
        return Camera.settings_topic

    def is_initialize(self):
        if Camera.thread is None:
            return False
        return True

    def initialize(self):
        # start background frame thread
        Camera.thread = threading.Thread(target=self._thread)
        Camera.thread.start()

        # wait until frames start to be available
        while self.frame is None:
            time.sleep(0)
            

    def record_video(self):
        t = time.time() + 15
        if not self.is_initialize():
            self.initialize()
            t = t + 5
        while t > time.time():
            Camera.last_access = time.time()
        Camera.save_video = True    
        

    def get_frame(self):
        Camera.last_access = time.time()
        if not self.is_initialize():
            self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (640, 480)
            camera.framerate = 24
            #camera.hflip = True
            #camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)
            
            stream_video = picamera.PiCameraCircularIO(camera, seconds=20)
            stream_foto = io.BytesIO()
            camera.start_recording(stream_video, format='h264')
            try:
                while True:
                    #create and store frame
                    camera.capture(stream_foto, 'jpeg', use_video_port=True)
                    stream_foto.seek(0)
                    cls.frame = stream_foto.read()

                    # reset stream for next frame
                    stream_foto.seek(0)
                    stream_foto.truncate()

                    if cls.save_video:
                        name = Camera.nickname.replace('/', '-') + "-" + time.strftime("%d%b%Y-%H:%M:%S") + ".h264"
                        print(name)
                        stream_video.copy_to(name)
                        cls.save_video = False

                    # if there hasn't been any clients asking for frames in
                    # the last 10 seconds stop the thread
                    if time.time() - cls.last_access > 10:
                        break
            finally:
                camera.stop_recording()
        cls.thread = None