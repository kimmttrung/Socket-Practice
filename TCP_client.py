import socket

serverName = '127.0.0.1' # Địa chỉ IP của server
serverPort = 12000 # Cổng server

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Tạo socket TCP
clientSocket.connect((serverName,serverPort)) # Kết nối đến server

isContinue = True

while isContinue:
    sentence = input('Nhập tin nhắn: ') # Nhập dữ liệu từ bàn phím

    clientSocket.send(sentence.encode()) # Gửi dữ liệu (chuyển thành bytes

    if sentence == 'quit':
        isContinue = False
        break

    recevMessage = clientSocket.recv(1024) # Nhận phản hồi từ server
    print ('Từ Server:', recevMessage.decode())  # In kết quả nhận được
clientSocket.close()