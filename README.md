# test_superhero

Быстрый старт
Склонируйте репозиторий:

git clone https://github.com/ваш-репозиторий/superhero-api.git
cd superhero-api


Создайте файл .env в корне проекта:
echo "SUPERHERO_API_TOKEN=ваш_токен" > .env


Запустите проект:
docker-compose up --build

Запуск тестов
docker-compose run web pytest

Логирование
docker-compose logs -f web  # Логи сервера
docker-compose logs -f db   # Логи базы данных
