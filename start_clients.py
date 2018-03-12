import time
from subprocess import Popen, CREATE_NEW_CONSOLE

delay = 1
p_list = []  # Список клиентских процессов
while True:
    user = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")
    if user == 'q':
        break
    elif user == 's':
        for _ in range(5):
            # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
            # чтобы каждый процесс запускался в отдельном окне консоли
            # p_list.append(Popen('d:\StruganovOV\Python36-32\python.exe client.py localhost 7777',
            #                     creationflags=CREATE_NEW_CONSOLE))
            p_list.append(Popen('python client.py localhost 7777 r',
                                creationflags=CREATE_NEW_CONSOLE))

            time.sleep(delay)
        print('Запущено 10 клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
