from sqlalchemy.orm import Session
from . import models

def get_hero(db: Session, name: str):
    return db.query(models.Hero).filter(models.Hero.name == name).first()

def create_hero(db: Session, hero):
    db_hero = models.Hero(
        name=hero.name,
        intelligence=hero.intelligence,
        strength=hero.strength,
        speed=hero.speed,
        power=hero.power
    )
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero

def get_heroes_with_filters(db: Session, filters: dict):
    query = db.query(models.Hero)
    
    if filters.get('name'):
        query = query.filter(models.Hero.name == filters['name'])
    
    stats = ['intelligence', 'strength', 'speed', 'power']
    for stat in stats:
        value = filters.get(stat)
        if value is None:
            continue
            
        if isinstance(value, tuple):
            min_val, max_val = value
            if min_val is not None:
                query = query.filter(getattr(models.Hero, stat) >= min_val)
            if max_val is not None:
                query = query.filter(getattr(models.Hero, stat) <= max_val)
        elif isinstance(value, int):
            query = query.filter(getattr(models.Hero, stat) == value)
    
    return query.all()