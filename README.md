# <span style="color: orange;">Запрос к API с вопросами</span>

---

## Стек:

1. Python 3.10
2. Postgresql 11
3. Flask
4. Docker
5. Docker-compose

Для запуска проекта клонируйте из репозитория файлы docker-compose.yaml, в корневой директории создайте файл .env 
и заполниете переменными окружения из .env.dist, выполните команду docker-compose up после чего выполнится загрузка 
docker-контейнера с DockerHub и приложением можно пользоваться.
В проекте реализован запрос к API для получения вопросов с ответами. Для этого необходимо отправить используя Postman
POST запрос по адресу 127.0.0.:8085/questions с числом желаемых вопросов Пример запроса:
{"questions_num": 2}.  В базу данных запишется указанное количество вопросов полученных с API, ответом на запрос
будет предпоследний вопрос из БД. Для сохранности данных после остановки контейнера используются volumes.
