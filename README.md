📦 Установка и запуск
Клонируйте репозиторий:

bash
git clone https://github.com/your_username/test_superhero.git
cd test_superhero
Создайте файл конфигурации:

bash
echo "SUPERHERO_API_TOKEN=your_api_token_here" > .env
Запустите сервисы:

bash
docker-compose up --build -d
После запуска API будет доступно по адресу:
http://localhost:8000

🚀 Использование API
Добавление героя
bash
curl -X POST "http://localhost:8000/hero/?name=Spider-Man"
Получение списка героев
bash
# Все герои
curl "http://localhost:8000/hero/"

# С фильтрацией
curl "http://localhost:8000/hero/?intelligence=80,100&strength=50,"
🧪 Тестирование
bash
docker-compose run web pytest -v
📊 Мониторинг
bash
# Логи сервера
docker-compose logs -f web

# Логи базы данных
docker-compose logs -f db
🛑 Остановка
bash
docker-compose down
