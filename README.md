## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.11**
- [Docker](https://www.docker.com/get-started): Необходим для контейнеризации приложения. Вы можете скачать и установить Docker с [официального сайта](https://www.docker.com/get-started).
- [Docker Compose](https://docs.docker.com/compose/install/): Используется для управления многоконтейнерными приложениями. Установите Docker Compose, следуя [инструкциям на официальном сайте](https://docs.docker.com/compose/install/).


## Установка
```shell
git clone https://github.com/web3artem/IndigoTest.git
cd IndigoTest
```

## Запуск приложения
1. Запуск основного приложения
```shell
docker-compose up web
```
2. Запуск тестов
```shell
docker-compose up test
```
Для тестов и для основного приложения используются разные базы данных. Тесты проверяют работу сервисного слоя по взаимодействию с бд, для каждого теста миграции накатываются заново.

3. После запуска приложения откройте браузер и перейдите по адресу `http://localhost:8000/api/docs`

## Логика приложения
В приложении реализованы возможность упрощенного создания пользователя без авторизации, создание фильмов, а также добавление определенного фильма в избранное.

В качестве базы данных использовался PostgreSQL, для миграции - Alembic, все упаковано в docker-контейнеры. В качестве линтера использовался ruff, для тестов - pytest.

Посмотреть документацию по каждому эндпоинту можно в http://localhost:8000/api/docs
