import time
import select
import collections
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import convert_float_to_str, get_message, send_message, add_address_and_port
import jim.config as cfg


class Server():

    def __init__(self):
        """
        Устанавливаю параметры по умолчанию
        """
        # список сокетов подключенных клиентов
        self._clients = list()
        # определяю протокол TCP/IP
        self._sock = socket(AF_INET, SOCK_STREAM)
        # принимаю адрес и порт в виде кортежа
        self._sock.bind(add_address_and_port('server'))
        # устанавливаю timeout
        self._sock.settimeout(0.2)
        # устанавливаю максимальное количество соединений
        self._sock.listen(5)
        # контейнер для хранения пересылаемых сообщений
        self._requests = collections.deque()
        # информация о сокете клиента, отправляющего сообщения
        self.client_info = ''


    def past_time_to_dict(self, client_message):
        """
        Метод формирует данные для печати
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
            # Если всё хорошо шлем "ОК", время и информацию о клиенте
            message_time = time.time()
            message = {cfg.RESPONSE: 200,
                       cfg.TIME: message_time,
                       cfg.INFO: self.client_info}
            return message
            # return {RESPONSE: 200, TIME: float, INFO: IPandAddress}
        else:
            # Шлем код ошибки
            return {cfg.RESPONSE: 400, cfg.ERROR: 'Не верный запрос'}


    def read(self, client):
        """
        Метод получает сообщение write-клиента и сохраняет в _requests
        :param client: сокет клиента
        :return: выводит в консоль информацию Кто, Когда и Что отправил
        """
        try:
            # Получаю сообщение от клиента
            message = get_message(client)
            # Сохраняю сообщение в список
            self._requests.append(message)
            # Печатаю информацию в консоль сервера
            print('[i] Сообщение от: {0}'
                  '\n=== Обработанно на сервере: {1}'
                  '\n=== Текст сообщения: {2}'.format(self.client_info, \
                                                 message[cfg.TIME], \
                                                 message[cfg.MESSAGE]))
        # При разрыве соединения с клиентом исключить из общего списка
        except (ConnectionResetError, BrokenPipeError):
            if client in self._clients:
                self._clients.remove(client)


    def write(self, client, requests):
        """
        Метод пересылает сообщение read-клиентам
        :param client: сокеты read-клиентов
        :param requests: сообщение от write-клиента
        :return:
        """
        try:
            # Отправляю сообщение
            send_message(client, requests)
        # При разрыве соедиения с клиентом исключить из общего списка
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
                    # Принимаю соединения
                    client, address = self._sock.accept()
                    # accept() - блокирует приложение до тех пор, пока не придет сообщение от клиента.
                    # Функция возвращает кортеж из двух параметров – объект самого соединения и адрес клиента.
                    # Сохраняю адрес клиента для протоколов идентификации
                    self.client_info = address
                except OSError as e:
                    pass
                else:
                    print("Получен запрос на соединение от {}".format(address))
                    # Принимаю сообщение о присутствии от клиента
                    presence = get_message(client)
                    # публикую в консоль сервера данные о присутствии клиента
                    print(self.past_time_to_dict(presence))
                    # Формирую ответ-подтвердение регистрации присутствия клиента
                    response = self.presence_response(presence)
                    # Отправляю ответ клиенту
                    send_message(client, response)
                    # добавляю информацию о присоединевшемся клиента в список
                    self._clients.append(client)
                finally:
                    # Список read-клиентов
                    r = []
                    # Список write-клиентов
                    w = []
                    try:
                        # Функция опроса устройств
                        r, w, e = select.select(self._clients, self._clients, [], 0)
                    except Exception as e:
                        pass
                    # проверка списка читающих клиентов
                    for client in r:
                        # от появившихся принять сообщение и сохранить на сервере
                        self.read(client)
                    # Если есть сохраненные сообщения
                    if self._requests:
                        # collections.popleft() - удаляет и возвращает первый элемент очереди
                        requests = self._requests.popleft()
                        # проверка списка пишущих клиентов
                        for client in w:
                            # всем в списке разослать сохраненное сообщение
                            self.write(client, requests)

        except KeyboardInterrupt:
            pass

    print('Эхо-сервер запущен')


if __name__ == '__main__':
    server = Server()
    server.mainloop()
