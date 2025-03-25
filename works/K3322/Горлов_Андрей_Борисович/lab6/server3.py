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

                # Получаем HTTP-запрос от клиента
                request = conn.recv(1024).decode()
                print(f"Получен запрос от клиента: {request}")

                # Чтение HTML-файла
                try:
                    with open("index.html", "r") as file:
                        html_content = file.read()
                except FileNotFoundError:
                    html_content = "<h1>Ошибка: Файл index.html не найден</h1>"

                # Формируем HTTP-ответ
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: text/html; charset=UTF-8\r\n"
                response += "\r\n"
                response += html_content

                # Отправляем HTTP-ответ клиенту
                conn.sendall(response.encode())
                print("HTML-страница отправлена клиенту.")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nСервер завершил работу.")
