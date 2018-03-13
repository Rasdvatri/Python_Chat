import time
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import add_address_and_port, convert_float_to_str, bytes_to_dict, send_message
import jim.config as cfg
from subprocess import Popen, CREATE_NEW_CONSOLE


class Client():

    def __init__(self):
        self.type = cfg.TYPE
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(add_address_and_port('client'))


    def presence_message(self):
        """
        Формирую сообщение серверу
        :return: сообщение
        """
        message_time = time.time()
        message = {cfg.ACTION: cfg.PRESENCE,
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
                return 'OK', convert_float_to_str(server_response[cfg.TIME])
            elif server_response[cfg.RESPONSE] == cfg.BASIC_NOTICE:
                return 'BASIC_NOTICE', convert_float_to_str(server_response[cfg.TIME])
            elif server_response[cfg.RESPONSE] == cfg.ACCEPTED:
                return 'ACCEPTED', convert_float_to_str(server_response[cfg.TIME])
            elif server_response[cfg.RESPONSE] == cfg.WRONG_REQUEST:
                return 'WRONG_REQUEST', convert_float_to_str(server_response[cfg.TIME])
            elif server_response[cfg.RESPONSE] == cfg.SERVER_ERROR:
                return 'SERVER_ERROR', convert_float_to_str(server_response[cfg.TIME])
            else:
                return 'Неопределен ответ сервера'
        else:
            return 'Невреный ответ сервера'


    def write(self):
        try:
            while True:
                str_data = input('Enter data: ')
                bytes_data = str_data.encode(cfg.ENCODING)
                self.sock.send(bytes_data)
        except KeyboardInterrupt:
            pass


    def read(self):
        try:
            while True:
                data = self.sock.recv(cfg.BUFFER_SIZE)
                str_data = data.decode(cfg.ENCODING)
                print(str_data)
        except KeyboardInterrupt:
            pass


    def start(self):
        message = self.presence_message()
        send_message(self.sock, message)
        while True:
            #принимаю сообщение сервера
            tm = bytes_to_dict(self.sock.recv(1024))
            print(self.decode_message(tm))
        self.sock.close()


if __name__ == '__main__':
    client = Client()
    client.start()
