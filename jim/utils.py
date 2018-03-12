import json
import time
import sys

# Кодировка
ENCODING = 'utf-8'


def add_address_and_port(sock):
    """
    Получение адреса и порта для коннекта сокета
    :param sock: идентификатор 'server'/'client'
    :return: кортеж из адреса и порта
    """
    # Определяем адрес
    addr = ''
    if sock == 'server':
        try:
            addr = sys.argv[1]
        except IndexError:
            addr = ''
    elif sock == 'client':
        try:
            addr = sys.argv[1]
        except IndexError:
            addr = 'localhost'
    # Определяем порт
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    # возвращаем кортеж
    return (addr, port)


def dict_to_bytes(message_dict):
    """
    Преобразование словаря в байты
    :param message_dict: словарь
    :return: bytes
    """
    # Проверям, что пришел словарь
    if isinstance(message_dict, dict):
        # Преобразуем словарь в json
        jmessage = json.dumps(message_dict)
        # Переводим json в байты
        bmessage = jmessage.encode(ENCODING)
        # Возвращаем байты
        return bmessage
    else:
        raise TypeError


def bytes_to_dict(message_bytes):
    """
    Получение словаря из байтов
    :param message_bytes: сообщение в виде байтов
    :return: словарь сообщения
    """
    # Если переданы байты
    if isinstance(message_bytes, bytes):
        # Декодируем
        jmessage = message_bytes.decode(ENCODING)
        # Из json делаем словарь
        message = json.loads(jmessage)
        # Если там был словарь
        if isinstance(message, dict):
            # Возвращаем сообщение
            return message
        else:
            # Нам прислали неверный тип
            raise TypeError
    else:
        # Передан неверный тип
        raise TypeError


def send_message(sock, message):
    """
    Отправка сообщения
    :param sock: сокет
    :param message: словарь сообщения
    :return: None
    """
    # Словарь переводим в байты
    bprescence = dict_to_bytes(message)
    # Отправляем
    sock.send(bprescence)


def get_message(sock):
    """
    Получение сообщения
    :param sock:
    :return: словарь ответа
    """
    # Получаем байты
    bresponse = sock.recv(1024)
    # переводим байты в словарь
    response = bytes_to_dict(bresponse)
    # возвращаем словарь
    return response


def convert_float_to_str(time_float):
    """
    функция переводит время-float в читаемый формат ДД.ММ.ГГГГ ЧЧ:ММ
    :param time_float: время в FLOAT
    :return: время в STR
    """
    if isinstance(time_float, float):
        convert_time = time.strftime("%d.%m.%Y %H:%M:%S", time.strptime(time.ctime(time_float)))
        return convert_time
    else:
        return TypeError
