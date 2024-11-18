import requests
from src.models import Person, Planet, Starship

from src.utils.swapi import get_species_id

def fetch_data_from_api(url):
    """Helper function to fetch data from the SWAPI."""
    response = requests.get(url)
    response.raise_for_status()  # Will raise an error if the request fails
    return response.json()

def insert_people(session):
    """Fetch and insert data into the 'people' table."""
    url = "https://swapi.dev/api/people/"
    while url:
        data = fetch_data_from_api(url)
        for person in data['results']:
            new_person = Person(
                name=person['name'],
                height=int(person['height']) if person['height'] != 'unknown' else None,
                mass=float(person['mass'].replace(",", ".")) if person['mass'] != 'unknown' else None,
                hair_color=person['hair_color'],
                skin_color=person['skin_color'],
                eye_color=person['eye_color'],
                birth_year=person['birth_year'],
                gender=person['gender'],
                homeworld=person["homeworld"],
                species_id=get_species_id(person["species"][0]) if person["species"] != [] else 1
            )
            session.add(new_person)
        session.commit()
        url = data['next']  # Get the next page of results

def insert_planets(session):
    """Fetch and insert data into the 'planets' table."""
    url = "https://swapi.dev/api/planets/"
    while url:
        data = fetch_data_from_api(url)
        for planet in data['results']:
            new_planet = Planet(
                name=planet['name'],
                rotation_period=int(planet['rotation_period']) if planet['rotation_period'] != 'unknown' else None,
                orbital_period=int(planet['orbital_period']) if planet['orbital_period'] != 'unknown' else None,
                diameter=int(planet['diameter']) if planet['diameter'] != 'unknown' else None,
                climate=planet['climate'],
                gravity=planet['gravity'],
                terrain=planet['terrain'],
                surface_water=float(planet['surface_water']) if planet['surface_water'] != 'unknown' else None,
                population=int(planet['population']) if planet['population'] != 'unknown' else None,
                url=planet['url']
            )
            session.add(new_planet)
        session.commit()
        url = data['next']  # Get the next page of results

def insert_starships(session):
    """Fetch and insert data into the 'starships' table."""
    url = "https://swapi.dev/api/starships/"
    while url:
        data = fetch_data_from_api(url)
        for starship in data['results']:
            new_starship = Starship(
                name=starship['name'],
                model=starship['model'],
                manufacturer=starship['manufacturer'],
                cost_in_credits=int(starship['cost_in_credits']) if starship['cost_in_credits'] != 'unknown' else None,
                length=float(starship['length'].replace(",","")) if starship['length'] != 'unknown' else None,
                max_atmosphering_speed=int(starship['max_atmosphering_speed'].replace("km","")) if starship['max_atmosphering_speed'] != 'n/a' and starship['max_atmosphering_speed'] != 'unknown' else None,
                crew=int(starship['crew'].replace(",", "").replace("-", "")) if starship['crew'] != 'unknown' else None,
                passengers=int(starship['passengers'].replace(",","")) if starship['passengers'] != 'n/a' and starship['passengers'] != 'unknown' else None,
                cargo_capacity=int(starship['cargo_capacity']) if starship['cargo_capacity'] != 'unknown' else None,
                consumables=starship['consumables'],
                hyperdrive_rating=float(starship['hyperdrive_rating']) if starship['hyperdrive_rating'] != 'unknown' else None,
                mglt=int(starship['MGLT']) if starship['MGLT'] != 'unknown' else None,
                starship_class=starship['starship_class']
            )
            session.add(new_starship)
        session.commit()
        url = data['next']  # Get the next page of results
