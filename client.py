import socket
import threading

serverName = '192.168.0.65'
serverPort = 65432

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print("\n[Server]:", data.decode())
            else:
                break
        except:
            break

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverName, serverPort))
        print(s.recv(1024).decode())  # nhận yêu cầu tên
        name = input(">> ")
        s.sendall(name.encode())

        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == 'exit':
                break
            s.sendall(msg.encode())

if __name__ == "__main__":
    run_client()
