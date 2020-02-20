#!/usr/bin/env python3

import pygame.camera
import socket

# Initialize pygame and camera
pygame.init()
pygame.camera.init()

# Start up the camera module
resolution = (640, 480)
cam = pygame.camera.Camera("/dev/video0", resolution)
cam.start()

# Initialize the server
HOST = ""
PORT = 65433
BUFFER_SIZE = 4096

# Infinite loop that listens to incoming connections and connect to them.
# When connected it listens for the key-word "img" which will capture an image and send it over the socket
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        while True:
            try:
                client_socket, address = server_socket.accept()

                with client_socket:
                    rc = client_socket.recv(512)
                    # Listen to the keyword "img"
                    if rc == b'img':
                         # Capture an image and send it
                        image = cam.get_image()
                        pygame.image.save(image, 'i.bmp')
                        img = open('i.bmp', 'rb')

                        # Sending the image
                        while True:
                            read = img.readline(BUFFER_SIZE)
                            if not read:
                                break
                            client_socket.send(read)
                        # Closing the file-stream
                        img.close()
                        print("Image sent successfully")
            # TODO: Capture errors
            except socket.error:
                print("")

# Gracefully shutdown of camera, pygame and the program
cam.stop()
pygame.quit()
quit()
