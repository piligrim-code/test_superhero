from pydantic import BaseModel

class HeroBase(BaseModel):
    name: str
    intelligence: int
    strength: int
    speed: int
    power: int

class HeroCreate(HeroBase):
    pass

class Hero(HeroBase):
    id: int

    class Config:
        orm_mode = True

class HeroFilter(BaseModel):
    name: str = None
    intelligence: str = None
    strength: str = None
    speed: str = None
    power: str = None