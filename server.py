import socket
import threading
import time

# List untuk menyimpan daftar klien yang terhubung
clients = []

# Fungsi untuk menangani koneksi dengan klien
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message.lower() == "stop":
                print("[Server] Client {} telah terputus.".format(client_socket.getpeername()))
                client_socket.send("[Server] Terputus dari server.".encode('utf-8'))
                break

            # Broadcast pesan ke semua klien
            broadcast("[Server] " + message)

            # Tampilkan pesan di terminal server
            print("[Client]" + message)

            # Kirim pesan balik ke klien
            reply_message = "Pesan dari server kepada [Client]: Terima kasih atas pesan Anda!"
            client_socket.send(reply_message.encode('utf-8'))

        except Exception as e:
            print("Error: {}".format(e))
            break

    # Hapus klien dari daftar
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

# Fungsi untuk mengirim pesan broadcast ke semua klien
def broadcast(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    message = "[{}] {}".format(current_time, message)
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print("Error: {}".format(e))
            client.close()
            if client in clients:
                clients.remove(client)

# Konfigurasi server
host = '0.0.0.0'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print("[Server] Server berjalan di {}:{}".format(host, port))

# Menerima koneksi dari klien dan menangani setiap koneksi dalam thread terpisah
while True:
    client_socket, client_addr = server.accept()
    clients.append(client_socket)
    print("[Server] Terhubung dengan {}".format(client_addr))
    client_socket.send("[Server] Terhubung ke server.".encode('utf-8'))
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()