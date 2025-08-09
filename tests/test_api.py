import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, SessionLocal
from app import models

# Тестовая БД (используем ту же, что и основное приложение)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/superhero_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    # Создаем тестового клиента без переопределения зависимостей
    # (так как в нашем приложении нет FastAPI dependency injection)
    with TestClient(app) as client:
        yield client

def test_create_hero(client, db):
    # Мокаем внешний API
    import app.main
    original_requests_get = app.main.requests.get
    
    mock_response = {
        "response": "success",
        "results": [{
            "name": "Batman",
            "powerstats": {
                "intelligence": "100",
                "strength": "26",
                "speed": "27",
                "power": "50"
            }
        }]
    }
    
    class MockResponse:
        def json(self):
            return mock_response
        
        @property
        def status_code(self):
            return 200
    
    app.main.requests.get = lambda *args, **kwargs: MockResponse()
    
    # Тест
    response = client.post("/hero/?name=Batman")
    assert response.status_code == 200
    assert response.json()["name"] == "Batman"
    
    # Проверяем, что герой добавился в БД
    hero = db.query(models.Hero).filter(models.Hero.name == "Batman").first()
    assert hero is not None
    assert hero.intelligence == 100
    
    # Восстанавливаем оригинальный метод
    app.main.requests.get = original_requests_get

def test_get_heroes(client, db):
    # Добавляем тестовых героев напрямую в БД
    hero1 = models.Hero(name="Superman", intelligence=90, strength=100, speed=95, power=90)
    hero2 = models.Hero(name="Flash", intelligence=70, strength=50, speed=100, power=80)
    db.add(hero1)
    db.add(hero2)
    db.commit()
    
    # Тестируем GET /hero/
    response = client.get("/hero/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Тестируем фильтрацию
    response = client.get("/hero/?intelligence=80,100")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Superman"