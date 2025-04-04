from socket import *

serverIP = '0.0.0.0'  # Lắng nghe trên tất cả các địa chỉ IP
serverPort = 12000  # Chạy trên cổng 12000

serverSocket = socket(AF_INET, SOCK_STREAM)  # Tạo socket TCP
serverSocket.bind((serverIP, serverPort))  # Gán socket với cổng
serverSocket.listen(1) # Lắng nghe kết nối (tối đa 1 hàng đợi)

print('Server sẵn sàng nhận kết nối')

while True:
    connectionSocket, addr = serverSocket.accept() # Chấp nhận kết nối từ client
    print('Đã kết nối với:', addr)

    isContinue = True
    while isContinue: # Lặp lại việc nhận và trả lời tin nhắn, khi không muốn kết nối với client này nữa thì đóng 
        sentence = connectionSocket.recv(1024).decode()
        print('Client:', addr, 'vừa gửi:', sentence)
        if sentence == 'quit': # Kiểm tra 'quit' không phân biệt hoa/thường
            isContinue = False
            break
        replyMessage = input("Server: ")
        connectionSocket.send(replyMessage.encode()) 

    connectionSocket.close() 
    print('Đã đóng kết nối với:', addr)


