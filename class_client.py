import time
import sys
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import add_address_and_port, convert_float_to_str, send_message, get_message
import jim.config as cfg


class Client():

    def __init__(self):
        """
        Устанавливаю параметры по умолчанию
        """
        # Определяю протокол TCP/IP
        self.sock = socket(AF_INET, SOCK_STREAM)
        # Отправляю адрес и порт
        self.sock.connect(add_address_and_port('client'))


    def presence_message(self):
        """
        Формирую сообщение присутствия серверу
        :return: сообщение
        """
        # дата/время в float
        message_time = time.time()
        # структура jim  сообщения
        message = {
            cfg.ACTION: cfg.PRESENCE,
            cfg.TIME: message_time,
        }
        return message


    def decode_message(self, server_response):
        """
        Разбор сообщения и вывод ответа сервера
        :param server_response: сообщение сервера
        :return: расшифрованный ответ
        """
        if cfg.RESPONSE in server_response and \
                isinstance(server_response[cfg.RESPONSE], int):
            if server_response[cfg.RESPONSE] == cfg.OK:
                return 'OK', convert_float_to_str(server_response[cfg.TIME]),\
                       server_response[cfg.INFO]
            elif server_response[cfg.RESPONSE] == cfg.BASIC_NOTICE:
                return 'BASIC_NOTICE', convert_float_to_str(server_response[cfg.TIME]),\
                       server_response[cfg.INFO]
            elif server_response[cfg.RESPONSE] == cfg.ACCEPTED:
                return 'ACCEPTED', convert_float_to_str(server_response[cfg.TIME]),\
                       server_response[cfg.INFO]
            elif server_response[cfg.RESPONSE] == cfg.WRONG_REQUEST:
                return 'WRONG_REQUEST', convert_float_to_str(server_response[cfg.TIME]),\
                       server_response[cfg.INFO]
            elif server_response[cfg.RESPONSE] == cfg.SERVER_ERROR:
                return 'SERVER_ERROR', convert_float_to_str(server_response[cfg.TIME]),\
                       server_response[cfg.INFO]
            else:
                return 'Неопределен ответ сервера'
        else:
            return 'Невреный ответ сервера'


    def add_message_to_dict(self, message):
        """
        метод упаковки текста сообщения в словарь
        :param message: текст из окна ввода
        :return: возвращает словарь стандарта jim
        """
        message_dict = {
            cfg.ACTION: cfg.PRESENCE,
            cfg.TIME: convert_float_to_str(time.time()),
            cfg.MESSAGE: message
        }
        return message_dict

    def type_clients(self):
        """
        метод чтения ключа запуска клиента
        '-r' - чтение сообщений (по умолчанию)
        '-w' - отправка сообщение
        :return: возвращает ключ
        """
        try:
            type_client = sys.argv[3]
        except IndexError:
            type_client = '-r'
        return type_client


    def write(self):
        """
        консоль для ввода сообщений
        :return:
        """
        try:
            while True:
                # ввести сообщение
                message = input('Введите текст сообщения: ')
                # упаовать сообщение в словарь структуры jim
                message_dict = self.add_message_to_dict(message)
                # отправить сообщение на сервер
                send_message(self.sock, message_dict)
        except KeyboardInterrupt:
            pass


    def read(self):
        """
        чтение сообщений
        :return:
        """
        try:
            while True:
                # получаем сообщение сервера от пишущего клиента
                message = get_message(self.sock)
                # публикуем сообщение в консоли читающего клиента
                print(message[cfg.TIME], message[cfg.MESSAGE])
        except KeyboardInterrupt:
            pass


    def mainloop(self):
        """
        основной цикл взаимодействия клиентов с сервером
        :return:
        """
        # формирую сообщение присутствия
        message = self.presence_message()
        # отправляюсообщение присутствия
        send_message(self.sock, message)
        while True:
            # принимаю сообщение-ответ сервера
            tm = get_message(self.sock)
            # публикую сообщение-ответ сервера
            print(self.decode_message(tm))
            # Смотрим ключ запуска клиента
            if self.type_clients() == '-r':
                # запускаем клиент на прием сообщений в чате
                self.read()
            elif self.type_clients() == '-w':
                # запускаем клиент на отправку сообщений в чате
                self.write()
            else:
                pass
        self.sock.close()


if __name__ == '__main__':
    client = Client()
    client.mainloop()
