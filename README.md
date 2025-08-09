# test_superhero

 Быстрый старт
Склонируйте репозиторий:

bash
git clone https://github.com/ваш-репозиторий/superhero-api.git
cd superhero-api
Создайте файл .env в корне проекта:

bash
echo "SUPERHERO_API_TOKEN=ваш_токен" > .env
Запустите проект:

bash
docker-compose up --build

Запуск тестов
bash
docker-compose run web pytest

Логирование
Просмотр логов:

bash
docker-compose logs -f web  # Логи сервера
docker-compose logs -f db   # Логи базы данных
