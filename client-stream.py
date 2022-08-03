
"""
Zarquon
"""

from distutils.log import error
import socket,cv2, pickle,struct

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.190.129' 
port = 5050 
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
	
	#Clientten servera mesaj gönderme
	"""
	datas = "client gönderdi".encode()
	client_socket.send(datas)
	"""
	try:
		while len(data) < payload_size:
			packet = client_socket.recv(4*1024) # 4K
			if not packet: break
			data+=packet

		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("Q",packed_msg_size)[0]

		while len(data) < msg_size:
			data += client_socket.recv(4*1024)

		frame_data = data[:msg_size]
		data  = data[msg_size:]
		frame = pickle.loads(frame_data)

		b = cv2.resize(frame,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)

		cv2.imshow("Client Frame",b)

		key = cv2.waitKey(1) & 0xFF
		if key  == ord('q'):
			break
	except struct.error as e:
		print(e)


client_socket.close()
