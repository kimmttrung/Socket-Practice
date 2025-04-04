import socket
# AF_INET : IPv4
# SOCK_DGRAM: UDP

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', serverPort))
print('The server is ready to receive')
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    
    modifiedMessage = message.upper()

    print(message)
    
    serverSocket.sendto(modifiedMessage, clientAddress)