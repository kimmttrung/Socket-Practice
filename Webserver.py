from socket import *
import sys
import os  # Để kiểm tra sự tồn tại của file

# Khởi tạo socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Thiết lập địa chỉ và cổng
serverPort = 1200
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

print(f"Web server đang chạy tại http://localhost:{serverPort}")

while True:
    # Chờ kết nối từ client
    connectionSocket, addr = serverSocket.accept()

    try:
        # Nhận request từ trình duyệt
        message = connectionSocket.recv(1024).decode()
        print("Yêu cầu nhận được:")
        print(message)

        # Kiểm tra nếu không có yêu cầu hợp lệ
        if not message:
            connectionSocket.close()
            continue

        # Phân tích tên file từ HTTP request
        request_line = message.splitlines()[0]
        requested_file = request_line.split()[1]

        # Mặc định là index.html nếu không chỉ định file
        if requested_file == "/":
            requested_file = "/index.html"

        # Tạo đường dẫn file
        filepath = requested_file[1:]  # Bỏ dấu "/"

        # Kiểm tra file tồn tại
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                outputdata = f.read()

            # Gửi header HTTP 200 OK
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

            # Gửi nội dung file
            connectionSocket.send(outputdata.encode())
        else:
            # Trả về lỗi 404 nếu không tìm thấy file
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
            error_message = "<html><body><h1>404 Not Found</h1><p>File không tồn tại.</p></body></html>"
            connectionSocket.send(error_message.encode())

        if message.strip().lower() == "quit":
            print("Đang tắt server...")
            connectionSocket.close()
            break

        # Đóng kết nối
        connectionSocket.close()

    except Exception as e:
        print("Lỗi:", e)
        connectionSocket.close()

# Không bao giờ tới đây nhưng để đảm bảo an toàn
serverSocket.close()
sys.exit()
