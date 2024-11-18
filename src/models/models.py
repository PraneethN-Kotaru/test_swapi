from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

# Base class for all models
Base = declarative_base()


# Model for Star Wars characters (Person)
class Person(Base):
    __tablename__ = 'Person'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    height = Column(Integer)
    mass = Column(Float)
    hair_color = Column(String)
    skin_color = Column(String)
    eye_color = Column(String)
    birth_year = Column(String)
    gender = Column(String)
    homeworld = Column(String)
    species_id = Column(Integer)


class Planet(Base):
    __tablename__ = 'Planets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    diameter = Column(Integer)
    climate = Column(String)
    gravity = Column(String)
    terrain = Column(String)
    surface_water = Column(Float)
    population = Column(Integer)
    url = Column(String)


class Starship(Base):
    __tablename__ = 'Starships'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    manufacturer = Column(String)
    cost_in_credits = Column(Integer)
    length = Column(Float)
    max_atmosphering_speed = Column(Integer)
    crew = Column(Integer)
    passengers = Column(Integer)
    cargo_capacity = Column(Integer)
    consumables = Column(String)
    hyperdrive_rating = Column(Float)
    mglt = Column(Integer)
    starship_class = Column(String)

class Script(Base):
    __tablename__ = 'Scripts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    script_name = Column(String, nullable=False)  # The name of the script
    line_number = Column(String, nullable=False)  # Line number
    character = Column(String, nullable=False)  # Character speaking the dialogue
    dialogue = Column(String, nullable=False)  # The dialogue text


def create_session():
    engine = create_engine('sqlite:///star_wars.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()