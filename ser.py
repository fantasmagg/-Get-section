import socket
import os

host = '0.0.0.0'
port = 5000
buffer_size = 4096
destination_path = "C:/ho"

if not os.path.exists(destination_path):
    os.makedirs(destination_path)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Servidor escuchando en {host}:{port}")

try:
    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexión aceptada de {address}")

        while True:
            # Recibir el nombre del archivo
            file_name_data = client_socket.recv(buffer_size).decode('utf-8', 'ignore').strip()
            if not file_name_data or file_name_data == "END":
                # Si no se reciben datos o se recibe "END", significa que el cliente cerró la conexión o terminó la transmisión
                break

            # Asegurarse de que el nombre del archivo no sea inválido
            if '\0' in file_name_data:
                print(f"Nombre de archivo no válido: {file_name_data}")
                continue

            full_path = os.path.join(destination_path, file_name_data)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Confirmar al cliente que está listo para recibir el archivo
            client_socket.sendall(b"ACK")

            # Abrir el archivo para escritura
            with open(full_path, "wb") as file:
                while True:
                    # Recibir datos del cliente
                    data = client_socket.recv(buffer_size)
                    if not data:
                        # No hay más datos, suponer que la transmisión ha terminado
                        break
                    if data.endswith(b"EOF"):
                        # Eliminar los bytes EOF del final y escribir los datos restantes
                        file.write(data[:-3])
                        break
                    file.write(data)

            # Enviar confirmación de que el archivo se recibió correctamente
            client_socket.sendall(b"ACK")
            print(f"Archivo {full_path} recibido correctamente.")

        client_socket.close()
        print("La conexión del cliente ha sido cerrada.")

except Exception as e:
    print(f"Error en el servidor: {e}")

finally:
    server_socket.close()
    print("Servidor cerrado.")
