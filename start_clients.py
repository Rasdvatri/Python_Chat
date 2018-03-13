import time
from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []  # Список клиентских процессов
while True:
    user = input("Запустить клиентские сессии (s) / Закрыть клиентов (x) / Выйти (q) ")
    if user == 'q':
        break
    elif user == 's':
        num_clients = int(input('Укажите количество клиентскких сессий: '))
        if num_clients > 1:
            for _ in range(num_clients - 1):
                # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
                # чтобы каждый процесс запускался в отдельном окне консоли
                # p_list.append(Popen('d:\StruganovOV\Python36-32\python.exe class_client.py localhost 7777 -r',
                #                     creationflags=CREATE_NEW_CONSOLE))
                p_list.append(Popen('python class_client.py localhost 7778 -r',
                                    creationflags=CREATE_NEW_CONSOLE))
            # p_list.append(Popen('d:\StruganovOV\Python36-32\python.exe class_client.py localhost 7777 -w',
            #                     creationflags=CREATE_NEW_CONSOLE))
            p_list.append(Popen('python class_client.py localhost 7778 -w',
                                creationflags=CREATE_NEW_CONSOLE))
        else:
            # p_list.append(Popen('d:\StruganovOV\Python36-32\python.exe class_client.py localhost 7777 -r',
            #                     creationflags=CREATE_NEW_CONSOLE))
            p_list.append(Popen('python class_client.py localhost 7778 -r',
                                creationflags=CREATE_NEW_CONSOLE))

            print('Запущено {} клиентов'.format(num_clients))
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
