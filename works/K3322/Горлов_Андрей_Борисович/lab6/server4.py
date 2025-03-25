import socket
import threading

HOST = '127.0.0.1'  # Локальный хост
PORT = 65432  # Порт для подключения

clients = []  # Список всех подключенных клиентов
nicknames = []  # Список никнеймов клиентов


def broadcast(message, client):
    """Отправка сообщения всем клиентам."""
    for c in clients:
        c.send(message)


def handle_client(client):
    nickname = client.recv(1024).decode()
    nicknames.append(nickname)
    clients.append(client)

    print(f"Никнейм клиента: {nickname}")
    broadcast(f"{nickname} присоединился к чату\n".encode(), client)
    client.send("Вы можете начать общение!".encode())

    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)  # Рассылаем сообщение всем остальным клиентам
        except:
            # Если клиент отключился, удаляем его из списка
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} покинул чат".encode(), client)
            break


def receive_connections():
    """Принимает подключения от клиентов и создаёт новые потоки для их обработки."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Привязка к адресу
        server_socket.listen()  # Ожидание подключения
        print(f"Сервер запущен на {HOST}:{PORT}")

        while True:
            client, address = server_socket.accept()
            print(f"Подключен клиент: {address}")

            # Создаем новый поток для клиента
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    try:
        receive_connections()
    except KeyboardInterrupt:
        print("\nСервер завершил работу.")
