import socket
import threading

serverName = '192.168.0.65'   # Địa chỉ IP của server
serverPort = 65432            # Cổng kết nối server

# Nhận và hiển thị tin nhắn từ server
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print("\n[Server]:", data.decode())
            else:
                break  # Ngắt nếu server đóng kết nối
        except:
            break     # Xử lý lỗi và kết thúc

# Hàm chính để chạy client
def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverName, serverPort))              # Kết nối tới server
        print(s.recv(1024).decode())                     # Nhận lời chào / yêu cầu nhập tên
        name = input(">> ")                              # Nhập tên người dùng
        s.sendall(name.encode())                         # Gửi tên đến server

        # Tạo luồng nhận tin nhắn từ server
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        # Gửi tin nhắn tới server
        while True:
            msg = input()
            if msg.lower() == 'exit':                    # Gõ 'exit' để thoát
                break
            s.sendall(msg.encode())                      # Gửi tin nhắn

if __name__ == "__main__":
    run_client()
