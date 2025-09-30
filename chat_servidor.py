import socket
import threading

HOST = 'localhost'
PORT = 6000
clientes = []

def manejar_cliente(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            mensaje = conn.recv(1024).decode()
            if not mensaje:
                break
            print(f"{addr}: {mensaje}")

            # 🔥 Reenviar el mensaje a todos los clientes conectados
            for c in clientes:
                if c != conn:  # no reenviar al que lo mandó
                    try:
                        c.send(f"{addr}: {mensaje}".encode())
                    except:
                        clientes.remove(c)
        except:
            break

    # Si se desconecta el cliente
    print(f"Cliente {addr} desconectado")
    clientes.remove(conn)
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor de chat en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        clientes.append(conn)
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
