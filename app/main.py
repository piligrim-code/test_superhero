import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base
import requests

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils import parse_filter_param
from dotenv import load_dotenv

load_dotenv()
Base.metadata.create_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SUPERHERO_API_TOKEN = os.getenv("SUPERHERO_API_TOKEN")
SUPERHERO_API_URL = "https://superheroapi.com/api"

@app.post("/hero/", response_model=schemas.Hero)
def create_hero(name: str, db: Session = Depends(get_db)):
    # Check if hero already exists
    db_hero = crud.get_hero(db, name=name)
    if db_hero:
        raise HTTPException(status_code=400, detail="Hero already exists")
    
    # Fetch hero data from external API
    response = requests.get(f"{SUPERHERO_API_URL}/{SUPERHERO_API_TOKEN}/search/{name}")
    data = response.json()
    
    if data.get("response") == "error" or not data.get("results"):
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # Find exact name match
    exact_match = None
    for hero in data["results"]:
        if hero["name"].lower() == name.lower():
            exact_match = hero
            break
    
    if not exact_match:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # Parse power stats
    stats = exact_match["powerstats"]
    try:
        hero_data = schemas.HeroCreate(
            name=exact_match["name"],
            intelligence=int(stats["intelligence"] or 0),
            strength=int(stats["strength"] or 0),
            speed=int(stats["speed"] or 0),
            power=int(stats["power"] or 0)
        )
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid hero data")
    
    return crud.create_hero(db=db, hero=hero_data)

@app.get("/hero/", response_model=list[schemas.Hero])
def get_heroes(
    name: str = None,
    intelligence: str = None,
    strength: str = None,
    speed: str = None,
    power: str = None,
    db: Session = Depends(get_db)
):
    filters = {
        "name": name,
        "intelligence": parse_filter_param(intelligence),
        "strength": parse_filter_param(strength),
        "speed": parse_filter_param(speed),
        "power": parse_filter_param(power)
    }
    
    heroes = crud.get_heroes_with_filters(db, filters)
    if not heroes:
        raise HTTPException(status_code=404, detail="No heroes found")
    
    return heroes