import socket
import threading
import sys
import time

serverName = '0.0.0.0'  # localhost
serverPort = 65432        # Port không bị chiếm

clients = {}  # lưu tên -> socket
running = True  # trạng thái server

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

def send_to_client():
    global running
    while running:
        cmd = input("\n[GỬI] Nhập tên người dùng hoặc 'quit' để thoát server: ")
        if cmd.lower() == 'quit':
            print("Đang tắt server...")
            running = False

            # Đóng tất cả client
            for name, client in clients.items():
                try:
                    client.sendall("Server đang đóng. Tạm biệt!".encode())
                    client.close()
                except:
                    pass
            clients.clear()
            # Tự thoát luôn khỏi chương trình
            sys.exit(0)
        elif cmd in clients:
            msg = input(f"[NỘI DUNG] Gửi đến {cmd}: ")
            try:
                clients[cmd].sendall(f"[Server gửi bạn]: {msg}".encode())
            except:
                print(f"Không thể gửi đến {cmd}")
        else:
            print("Không tìm thấy người dùng này.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((serverName, serverPort))
    server.listen()
    print(f"[SERVER] Đang chạy tại {serverName}:{serverPort}")

    threading.Thread(target=send_to_client, daemon=True).start()

    while running:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except:
            break

    server.close()

if __name__ == "__main__":
    start_server()