import socket
import threading

HOST = 'localhost'
PORT = 6000

def recibir(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print("\n" + data)
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=recibir, args=(s,), daemon=True).start()
    
    while True:
        msg = input("Escribe mensaje: ")
        s.send(msg.encode())
