import socket
import threading

# Fungsi untuk mengirim pesan ke server
def send_message(client_socket):
    while True:
        message = raw_input("[Client] Ketik pesan Anda: ")
        client_socket.send(message.encode('utf-8'))

# Fungsi untuk menerima pesan dari server
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print("Error: {}".format(e))
            break

# Konfigurasi client
host = '127.0.0.1'  # Ganti dengan alamat IP atau nama host server
port = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Menampilkan pesan "Menunggu terhubung ke server"
print("[Client] Menunggu terhubung ke server")

# Menerima pesan pertama dari server
first_message = client.recv(1024).decode('utf-8')
print(first_message)

# Membuat thread untuk mengirim pesan dan menerima pesan dari server
send_thread = threading.Thread(target=send_message, args=(client,))
receive_thread = threading.Thread(target=receive_message, args=(client,))

send_thread.start()
receive_thread.start()