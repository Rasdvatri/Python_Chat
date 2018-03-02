import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import dict_to_bytes, bytes_to_dict, send_message, get_message
from jim.config import *


def presence_message():
    """
    Формирую сообщение серверу
    :return: сообщение
    """
    message_time = time.time()
    message = {ACTION: PRESENCE,
               TIME: message_time}
    return message


def decode_message(server_response):
    """
    Разбор сообщения и вывод ответа сервера
    :param server_response: сообщение сервера
    :return: расшифрованный ответ
    """
    if RESPONSE in server_response and \
            isinstance(server_response[RESPONSE], int):
        if server_response[RESPONSE] == OK:
            return 'OK'
        elif server_response[RESPONSE] == BASIC_NOTICE:
            return 'BASIC_NOTICE'
        elif server_response[RESPONSE] == ACCEPTED:
            return 'ACCEPTED'
        elif server_response[RESPONSE] == WRONG_REQUEST:
            return 'WRONG_REQUEST'
        elif server_response[RESPONSE] == SERVER_ERROR:
            return 'SERVER_ERROR'
        else:
            return 'Неопределен ответ сервера'
    else:
        return 'Невреный ответ сервера'


if __name__ == "__main__":
    server = socket(AF_INET, SOCK_STREAM)
    # В командной строке принимается запрос с параметрами следующего вида:
    # python client.py <serv_addr> <srv_port>
    # FOR ME:
    # at home:
    # cd C:/Users/Admin/YandexDisk/!_Learning/!_Python/2_Python/lesson1
    # python client.py localhost 7777
    # at work:
    # cd D:/StruganovOV/py_scr/python2
    # d:\StruganovOV\Python36-32\python.exe client.py localhost 7777
    try:
        serv_addr = sys.argv[1]
    except IndexError:
        serv_addr = 'localhost'
    try:
        serv_port = int(sys.argv[2])
    except IndexError:
        serv_port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    # Коннектимся к серверу
    server.connect((serv_addr, serv_port))
    # Отправляю сообщение на сервер
    send_message(server, presence_message())
    # принимаю сообщение сервера
    tm = bytes_to_dict(server.recv(1024))

    server.close()
    print(decode_message(tm))
