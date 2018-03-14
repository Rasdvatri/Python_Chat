"""Константы для jim протокола, настройки"""

# Кодировка
ENCODING = 'utf-8'

# Константы
S_HOST = ''
C_HOST = 'localhost'
PORT = 7777
NUM_CLIENT = 5
TIMEOUT = 0
BUFFER_SIZE = 1024

TYPE = ['write', 'read']
CLIENT_INFO = 'client_info'

# Ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
INFO = 'info'


# Значения
PRESENCE = 'presence'

# Коды ответов (будут дополняться)
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/json объект
SERVER_ERROR = 500

# Кортеж из кодов ответов
RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)
