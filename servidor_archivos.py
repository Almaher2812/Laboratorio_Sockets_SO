import socket
import os

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 4096  # tamaño de fragmento

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Servidor esperando en {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Conexión establecida con {addr}")
        filename = conn.recv(BUFFER_SIZE).decode().strip()
        print("Cliente pidió archivo:", filename)

        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            # enviar cabecera con existencia + tamaño
            header = f"EXISTS {filesize}"
            conn.send(header.encode())
            # esperar confirmación del cliente
            ack = conn.recv(BUFFER_SIZE).decode().strip()
            if ack == "READY":
                print("Cliente listo, comienza envío...")
                with open(filename, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        conn.sendall(bytes_read)
                print("Envío completado.")
            else:
                print("Cliente no listo. Ack:", ack)
        else:
            conn.send(b"NO")
            print("Archivo no existe:", filename)
