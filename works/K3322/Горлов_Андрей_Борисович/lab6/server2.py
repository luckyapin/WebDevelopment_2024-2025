import socket
import math

HOST = "127.0.0.1"  # Локальный хост
PORT = 65432  # Порт


def solve_quadratic(a, b, c):
    """Решение квадратного уравнения ax^2 + bx + c = 0"""
    discriminant = b ** 2 - 4 * a * c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Корни уравнения: x1 = {x1}, x2 = {x2}"
    elif discriminant == 0:
        x = -b / (2 * a)
        return f"Один корень: x = {x}"
    else:
        return "Уравнение не имеет действительных корней"


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Привязка к адресу
        server_socket.listen(1)  # Ожидание одного подключения
        print(f"Сервер запущен на {HOST}:{PORT}")

        while True:  # Сервер будет работать бесконечно
            conn, addr = server_socket.accept()  # Принятие подключения
            with conn:
                print(f"Подключен клиент: {addr}")

                # Получаем сообщение от клиента
                data = conn.recv(1024).decode()
                if not data:
                    break  # Если данные не получены, разрываем соединение

                print(f"Получено от клиента: {data}")

                # Разбираем данные (коэффициенты уравнения)
                try:
                    a, b, c = map(float, data.split(","))
                    result = solve_quadratic(a, b, c)
                except ValueError:
                    result = "Ошибка: Неверный формат данных. Введите коэффициенты как числа."

                # Отправляем ответ клиенту
                conn.sendall(result.encode())
                print(f"Отправлено клиенту: {result}")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nСервер завершил работу.")
