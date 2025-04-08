import socket
import threading
import sys

serverName = '0.0.0.0'     # Lắng nghe tất cả địa chỉ IP
serverPort = 65432         # Cổng kết nối server

clients = {}               # Lưu tên người dùng và socket tương ứng
running = True             # Cờ kiểm soát trạng thái server

# Xử lý từng client riêng
def handle_client(conn, addr):
    try:
        conn.sendall("Nhập tên người dùng: ".encode())
        name = conn.recv(1024).decode().strip()
        clients[name] = conn
        print(f"[KẾT NỐI] {name} từ {addr}")

        while running:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{name}] gửi: {msg}")
            conn.sendall(f"Đã nhận: {msg}".encode())
    except:
        pass
    finally:
        conn.close()
        if name in clients:
            del clients[name]
        print(f"[NGẮT] {name} đã rời đi")

# Gửi tin nhắn từ server đến từng client, hoặc thoát server
def send_to_client():
    global running
    while running:
        cmd = input("\n[GỬI] Nhập tên người dùng hoặc 'quit' để thoát server: ")
        if cmd.lower() == 'quit':
            print("Đang tắt server...")
            running = False

            # Gửi thông báo và đóng kết nối với tất cả client
            for name, client in clients.items():
                try:
                    client.sendall("Server đang đóng. Tạm biệt!".encode())
                    client.close()
                except:
                    pass
            clients.clear()
            sys.exit(0)  # Thoát chương trình
        elif cmd in clients:
            msg = input(f"[NỘI DUNG] Gửi đến {cmd}: ")
            try:
                clients[cmd].sendall(f"[Server gửi bạn]: {msg}".encode())
            except:
                print(f"Không thể gửi đến {cmd}")
        else:
            print("Không tìm thấy người dùng này.")

# Hàm khởi động server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverName, serverPort))
    server.listen()
    print(f"[SERVER] Đang chạy tại {serverName}:{serverPort}")

    # Luồng riêng để nhập lệnh gửi hoặc tắt server
    threading.Thread(target=send_to_client, daemon=True).start()

    # Lắng nghe kết nối từ client
    while running:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except:
            break

    server.close()  # Đóng socket server khi thoát

if __name__ == "__main__":
    start_server()
