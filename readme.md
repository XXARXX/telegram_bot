## иструкция:

из каталога проекта выполнить в командной строке

1. python -m venv venv
2. ./venv/Scripts/activate
2. python -m pip install -r requirements.txt
3. python run\.py db -c {путь-до-файла-базы-данных}
4. python run\.py config -t {токен-бота} -d {путь-до-файла-базы-данных}
5. python run\.py server [-ip] [-p]


## команды:

* Создание конфига: python run\.py config -t {токен-бота} -d {путь-до-файла-базы-данных}

    Файл 'config.xml' будет создан в рабочем каталоге программы с корректно заполненной структурой

* Создание базы данных: python run\.py db -c {путь-до-файла-базы-данных}

* Помощь: python run\.py {server, config, test, db} -h

* Запуск сервера в тестовом режиме: python run\.py server -d [-ip] [-p]

* Запуск сервера в обычном режиме: python run\.py server [-ip] [-p]

    Сервер может вызвать ошибку в случае не существующего пути до директории поиска файлов
    или в случае если конфиг заполнен не правильно

* Запуск тестов:
  1. python test -t {токен-бота} -d {путь-до-базы-данных} -c {айди-чата-используемого-для-тестов}
  2. python -m unittest