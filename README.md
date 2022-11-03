![example workflow](https://github.com/podlev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# REST API сервиса YaMDb

### Описание
Проект представляет собой API для проекта YaMDb  — базы отзывов о фильмах, книгах и музыке. Подробное описание [по ссылке](https://github.com/podlev/api_yamdb). Проект развернут по адресу [51.250.102.151](http://51.250.102.151/).

### Технологии 
- Python
- Django
- Django REST Framework
- SQLlite
- Simple-JWT
- Docker
- CI/CD

С использованием инструментов CI/CD (Continuous Integration и Continuous Deployment). При пуше в ветку master автоматически запускаются:

- Тестирование,
- Push нового образа на Docker Hub,
- Deploy на сервер,
- Отправка сообщения в телеграмм.

### Установка
- Склонировать репозиторий
```commandline
git clone github.com/podlev/api_yamdb.git
```

- Для работы с проектом локально создать и активировать виртуальное окружение, устанвоить зависимости

```commandline
python -m venv venv
source venv/scripts/activate (Windows)    
source venv/bin/activate (MacOS/Linux)
python3 -m pip install --upgrade pip
python pip install -r requirements.txt
```
- Для работы с проектом на сервере необходимо установить Docker и Docker-compose. 

- Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно
```
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/yamdb_final/
```
- Для использования CI/CD необходимо Secrets GitHub Actions переменные окружения:
  - SECRET_KEY - django secretkey
  - DOCKER_PASSWORD, DOCKER_USERNAME - имя пользователя и пароль dockerhub
  - USER, HOST, PASSPHRASE, SSH_KEY - имя пользователя, хост, passphrase и приватный ключ
  - TELEGRAM_TO, TELEGRAM_TOKEN - id, token telegram

- При пуше в ветку master приложение пройдет тесты, обновит образ на DockerHub и сделает деплой на сервер. 
- Внутри контейнера необходимо выполнить миграции и собрать статику приложения:
```commandline
docker container exec -it <CONTAINER ID> bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectastatic  --no-input
```
