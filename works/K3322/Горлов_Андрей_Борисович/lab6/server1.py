import socket

HOST = "127.0.0.1"  # Локальный хост
PORT = 65432  # Порт


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Привязка к адресу
        server_socket.listen(1)  # Ожидание одного подключения
        print(f"Сервер запущен на {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()  # Принятие подключения
            with conn:
                print(f"Подключен клиент: {addr}")

                # Получаем сообщение от клиента
                data = conn.recv(1024).decode()
                print(f"Получено от клиента: {data}")

                if data == "Hello, server":
                    # Отправляем ответ клиенту
                    response = "Hello, client"
                    conn.sendall(response.encode())
                    print(f"Отправлено клиенту: {response}")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nСервер завершил работу.")
