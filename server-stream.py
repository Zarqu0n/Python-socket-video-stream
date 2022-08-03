"""
Zarquon
"""

import socket, cv2, pickle, struct, imutils


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = ''#server ip
port = 5050
print('Server {0}:{1} adresinde kuruldu'.format(host_ip,port))
socket_address = (host_ip, port)

server_socket.bind(socket_address)

server_socket.listen(5)

print(socket_address,' adresinde dinleniyor.')

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print("----->Bağlantı sağlandı:",addr)

    if client_socket:
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):

            #Client'ten alınan verinin okunması
            """
            dataFromServer = client_socket.recv(1024).decode()
            print(dataFromServer)
            """

            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow('Server frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()