import socket

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 4096

# Cambia el nombre aquí por el que quieras pedir (o pásalo por input)
filename = "ejemplo.jpg"
save_as = "copia_" + filename

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(filename.encode())

    header = s.recv(BUFFER_SIZE).decode()
    if header.startswith("EXISTS"):
        filesize = int(header.split()[1])
        print(f"Servidor confirma existencia. Tamaño: {filesize} bytes")
        s.send(b"READY")

        received = 0
        with open(save_as, "wb") as f:
            while received < filesize:
                chunk = s.recv(BUFFER_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                # opcional: mostrar progreso simple
                print(f"\rRecibido {received}/{filesize} bytes", end="")
        print("\nDescarga completa. Archivo guardado como:", save_as)
    elif header.startswith("NO"):
        print("El servidor dice que el archivo no existe.")
    else:
        print("Respuesta inesperada del servidor:", header)
