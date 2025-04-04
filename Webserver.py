from socket import *
import sys  # Để dừng chương trình khi cần

# Tạo socket server
serverSocket = socket(AF_INET, SOCK_STREAM)

# Thiết lập thông tin máy chủ
serverPort = 6789  # Cổng server
serverSocket.bind(("", serverPort))  # Bind socket tới cổng
serverSocket.listen(1)  # Lắng nghe kết nối (1 kết nối mỗi lần)

print("Server is ready to serve...")

while True:
    # Chấp nhận kết nối từ client
    connectionSocket, addr = serverSocket.accept()
    
    try:
        # Nhận yêu cầu từ client
        message = connectionSocket.recv(1024).decode()
        
        # Phân tích yêu cầu để lấy tên file
        filename = message.split()[1]
        
        # Mở file được yêu cầu
        f = open(filename[1:], "r")
        outputdata = f.read()
        f.close()
        
        # Gửi dòng header HTTP 200 OK
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        
        # Gửi nội dung file đến client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Gửi phản hồi 404 Not Found nếu file không tồn tại
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Dừng chương trình
