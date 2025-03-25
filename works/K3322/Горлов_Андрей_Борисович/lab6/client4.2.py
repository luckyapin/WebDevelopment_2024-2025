import socket
import threading

HOST = '127.0.0.1'  # Адрес сервера
PORT = 65432        # Порт

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Запрашиваем имя у клиента
nickname = input("Введите свой никнейм: ")
client_socket.send(nickname.encode())

def receive_messages():
    """Получение сообщений от других клиентов."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Ошибка при получении сообщения.")
            break

def send_messages():
    """Отправка сообщений на сервер."""
    while True:
        message = input()
        client_socket.send(f"{nickname}: {message}".encode())

# Запускаем два потока для получения и отправки сообщений
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
