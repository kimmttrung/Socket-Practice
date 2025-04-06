from socket import *

serverIP = '0.0.0.0'
serverPort = 12000

serverSocket = socket(AF_INET,SOCK_DGRAM) # Tạo socket UDP
serverSocket.bind((serverIP, serverPort)) # Gán socket với cổng 12000
print('Server sẵn sàng nhận kết nối')

while True:
    recevMessage, clientAddress = serverSocket.recvfrom(2048) # Nhận dữ liệu từ client
    print('Client:', clientAddress, 'Vừa gửi:', recevMessage.decode())
    
    if recevMessage.lower() == 'quit':
        print('Server thoát')
        break
    reply = input("Server: ").encode()
    serverSocket.sendto(reply, clientAddress) # Gửi kết quả về cho client 
    if reply.decode().lower() == 'quit':
        print("Server thoát.")
        break

serverSocket.close()