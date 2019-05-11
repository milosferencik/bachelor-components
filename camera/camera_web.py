import io
import logging
import socketserver
from threading import Condition
from http import server
from camera import Camera
from servo import Servo_motor

PAGE="""\
<html>
<head>
<title>{}</title>
</head>
<body>
<img src="stream.mjpg" width="640" height="480" />
<form action="/" method="POST">
    <button type='submit' name='submit' value='right'>Right</button>
    <button type='submit' name='submit' value='left'>Left</button>
</form>
</body>
</html>
"""

class Streaming_handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        camera = Camera()
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.format(camera.get_nickname()).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    frame = camera.get_frame()
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        """ do_POST() can be tested using curl command 
            'curl -d "submit=On" http://server-ip-address:port' 
        """
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        post_data = post_data.split("=")[1]    # Only keep the value
        with Servo_motor() as servo_motor:
            if post_data == "right":
                servo_motor.right()
            if post_data == "left":
                servo_motor.left()

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

        

class Streaming_server(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
