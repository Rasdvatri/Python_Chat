from subprocess import Popen, CREATE_NEW_CONSOLE

"""
Модуль запуска нескольких клиентоских окон
"""

p_list = []  # Список клиентских процессов
while True:
    # меню
    user = input("Запустить клиентские сессии (s) / Закрыть клиентов (x) / Выйти (q) ")
    # выход из цикла
    if user == 'q':
        print('Модуль запуска клиентов погашен')
        break
    # подключить клиентов
    elif user == 's':
        try:
            # указать количество
            num_clients = int(input('Укажите количество клиентскких сессий: '))
            # если клиентов больше двух, один будет писать, все остальные читать
            if num_clients > 1:
                # запуск читающих клиентов
                for _ in range(num_clients - 1):
                    # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
                    # чтобы каждый процесс запускался в отдельном окне консоли
                    p_list.append(Popen('python class_client.py localhost 7778 -r',
                                        creationflags=CREATE_NEW_CONSOLE))
                # запуск пишушего клиента
                p_list.append(Popen('python class_client.py localhost 7778 -w',
                                    creationflags=CREATE_NEW_CONSOLE))
            # запустить только на чтение
            elif num_clients == 1:
                p_list.append(Popen('python class_client.py localhost 7778 -r',
                                    creationflags=CREATE_NEW_CONSOLE))
            else:
                print('Количество не может быть нулевым')
                continue
        except ValueError:
            print('Количество не может быть не заполнено')
            continue
        print('Запущено {} клиентов'.format(num_clients))
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
        print('Активные окна закрыты')
