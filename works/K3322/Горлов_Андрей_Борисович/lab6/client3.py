import socket

HOST = "127.0.0.1"  # Адрес сервера
PORT = 65432        # Порт

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Подключение к серверу

        # Отправляем HTTP-запрос (пользуемся простым запросом GET)
        request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        client_socket.sendall(request.encode())
        print(f"Отправлен запрос серверу: {request}")

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode()
        print(f"Получен ответ от сервера:\n{response}")

if __name__ == "__main__":
    try:
        start_client()
    except KeyboardInterrupt:
        print("\nКлиент завершил работу.")
