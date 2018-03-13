import time
import select
import collections
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import convert_float_to_str, get_message, send_message, bytes_to_dict, dict_to_bytes, add_address_and_port
import jim.config as cfg


class Server():

    def __init__(self):
        """

        """
        self._clients = list()
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.bind(add_address_and_port('server'))
        self._sock.settimeout(0.2)
        self._sock.listen(5)
        self._requests = collections.deque()
        self.client_info = ''

    def connect(self):
        """

        :return:
        """
        try:
            client, address = self._sock.accept()
            print("Получен запрос на соединение от {}".format(address))
            self._clients.append(client)
        except OSError:
            pass


    def past_time_to_dict(self, client_message):
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
            message_for_output.update({cfg.TIME: convert_float_to_str(client_message[cfg.TIME])})
            # Данные для печати
            return message_for_output
        else:
            raise TypeError

    def presence_response(self, presence_message):
        """
        Формирование ответа клиенту
        :param presence_message: Словарь presence запроса
        :return: Словарь ответа
        """
        # Делаем проверки
        if cfg.ACTION in presence_message and \
                presence_message[cfg.ACTION] == cfg.PRESENCE and \
                cfg.TIME in presence_message and \
                isinstance(presence_message[cfg.TIME], float):
            # Если всё хорошо шлем ОК и время
            message_time = time.time()
            message = {cfg.RESPONSE: 200,
                       cfg.TIME: message_time,
                       cfg.INFO: self.client_info}
            return message
            # return {RESPONSE: 200}
        else:
            # Шлем код ошибки
            return {cfg.RESPONSE: 400, cfg.ERROR: 'Не верный запрос'}


    def read(self, client):
        """

        :param client:
        :return:
        """
        try:
            message = get_message(client)
            self._requests.append(message)
            print(client, message[cfg.TIME], message[cfg.MESSAGE])
        except (ConnectionResetError, BrokenPipeError):
            if client in self._clients:
                self._clients.remove(client)


    def write(self, client, requests):
        """

        :param client:
        :param requests:
        :return:
        """
        try:
            send_message(client, requests)
        except (ConnectionResetError, BrokenPipeError):
            if client in self._clients:
                self._clients.remove(client)

    def mainloop(self):
        """
        Основной цикл обработки запросов клиентов
        :return:
        """

        try:
            while True:
                try:
                    client, address = self._sock.accept()
                    self.client_info = address
                # accept() - блокирует приложение до тех пор, пока не придет сообщение от клиента.
                # Функция возвращает кортеж из двух параметров – объект самого соединения и адрес клиента.
                except OSError as e:
                    pass
                else:
                    print("Получен запрос на соединение от {}".format(address))
                    presence = get_message(client)
                    print(self.past_time_to_dict(presence))
                    response = self.presence_response(presence)
                    send_message(client, response)
                    self._clients.append(client)
                finally:
                    r = []
                    w = []
                    try:
                        r, w, e = select.select(self._clients, self._clients, [], 0)
                    except Exception as e:
                        pass
                    for client in r:
                        self.read(client)

                    if self._requests:
                        requests = self._requests.popleft()
                        for client in w:
                            self.write(client, requests)

        except KeyboardInterrupt:
            pass

    print('Эхо-сервер запущен')


if __name__ == '__main__':
    server = Server()
    server.mainloop()
