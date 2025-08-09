📦 Установка и запуск

Клонируйте репозиторий:

git clone https://github.com/piligrim-code/test_superhero.git

cd test_superhero

Создайте файл конфигурации:

echo "SUPERHERO_API_TOKEN=your_api_token_here" > .env

Запустите сервисы:

docker-compose up --build -d

После запуска API будет доступно по адресу:

http://localhost:8000

 Тестирование

docker-compose run web pytest -v

 Мониторинг

# Логи сервера

docker-compose logs -f web

# Логи базы данных

docker-compose logs -f db
 Остановка
 
docker-compose down
