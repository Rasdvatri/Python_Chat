import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import dict_to_bytes, bytes_to_dict, send_message, get_message
from jim.config import *


def presence_response(presence_message):
    """
    Формирование ответа клиенту
    :param presence_message: Словарь presence запроса
    :return: Словарь ответа
    """
    # Делаем проверки
    if ACTION in presence_message and \
                    presence_message[ACTION] == PRESENCE and \
                    TIME in presence_message and \
            isinstance(presence_message[TIME], float):
        # Если всё хорошо шлем ОК
        return {RESPONSE: 200}
    else:
        # Шлем код ошибки
        return {RESPONSE: 400, ERROR: 'Не верный запрос'}


def convert_float_to_str(time_float):
    """
    функция переводит время-float в читаемый формат ДД.ММ.ГГГГ ЧЧ:ММ
    :param time_float: время в FLOAT
    :return: время в STR
    """
    if isinstance(time_float, float):
        convert_time = time.strftime("%d.%m.%Y %H:%M", time.strptime(time.ctime(time_float)))
        return convert_time
    else:
        return TypeError


def past_time_to_dict(client_message):
    """
    функция формирет данные для печати
    :param client_message: сообщение от клиента
    :return: словарь с сконвертированным TIME
    """
    # проверяем тип данных на DICT
    if isinstance(client_message, dict):
        # содал новый словарь
        message_for_output = {}
        # скопировал все данные в новый словарь
        message_for_output.update(client_message)
        # обновил TIME сконвертированными данными
        message_for_output.update({TIME: convert_float_to_str(client_message[TIME])})
        # Данные для печати
        return message_for_output
    else:
        raise TypeError


if __name__ == "__main__":
    server = socket(AF_INET, SOCK_STREAM)  # Определяю протокол TCP
    # В командной строке принимается запрос с аргументами следующего вида:
    # python server.py <serv_addr> <port>
    # FOR ME
    # at home:
    # cd C:/Users/Admin/YandexDisk/!_Learning/!_Python/2_Python/lesson1
    # python server.py "" 7777
    # at work:
    # cd D:/StruganovOV/py_scr/python2
    # d:\StruganovOV\Python36-32\python.exe server.py "" 7777
    # at Windows PowerShell:
    # python server.py '""' 7777
    try:
        serv_addr = sys.argv[1]
    except IndexError:
        serv_addr = ''
    try:
        serv_port = int(sys.argv[2])
    except IndexError:
        serv_port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    server.bind((serv_addr, serv_port))  # принимаю адрес и порт в виде кортежа
    server.listen(5)  # количество подключений

    while True:
        client, serv_addr = server.accept()
        # accept() - блокирует приложение до тех пор, пока не придет сообщение от клиента.
        # Функция возвращает кортеж из двух параметров – объект самого соединения и адрес клиента.
        print("Получен запрос на соединение от {}".format(serv_addr))
        # получаю сообщение отклиента
        presence = get_message(client)
        print(past_time_to_dict(presence))
        # Формирую ответ
        response = presence_response(presence)
        # отправляю ответ клиенту
        send_message(client, response)
        client.close()
