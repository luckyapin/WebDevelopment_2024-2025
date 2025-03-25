import socket

HOST = "127.0.0.1"  # Адрес сервера
PORT = 65432        # Порт

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))  # Подключение к серверу

        # Ввод коэффициентов квадратного уравнения
        print("Введите коэффициенты квадратного уравнения (a, b, c):")
        a = float(input("a: "))
        b = float(input("b: "))
        c = float(input("c: "))

        # Отправляем коэффициенты на сервер
        message = f"{a},{b},{c}"
        client_socket.sendall(message.encode())
        print(f"Отправлено серверу: {message}")

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode()
        print(f"Решение: {response}")

if __name__ == "__main__":
    try:
        start_client()
    except KeyboardInterrupt:
        print("\nКлиент завершил работу.")
