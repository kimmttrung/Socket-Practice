from socket import *

serverIP = '192.168.0.65' # Địa chỉ của server (có thể là IP hoặc tên miền)
serverPort = 12000 #  Cổng server đang lắng nghe

clientSocket = socket(AF_INET, SOCK_DGRAM)  # Tạo socket UDP 

while True:
    message = input('Client: ')
    clientSocket.sendto(message.encode(),(serverIP, serverPort)) # Gửi dữ liệu đến server
    if message.lower() == 'quit':
        print('Client đã thoát.')
        break

    reply, serverAddress = clientSocket.recvfrom(2048) #Nhận phản hồi từ server
    print('Từ Server: ', reply.decode()) # Hiển thị phản hồi

    if reply.decode().lower() == 'quit':
        print("Server đã thoát.")
        break

clientSocket.close() # Đóng kết nối