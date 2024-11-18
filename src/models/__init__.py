import requests
import json
from datetime import datetime
from src.models.models import *


def get_data_from_api(url):
    """
    A utility function to make requests to SWAPI and retrieve JSON data.
    Handles pagination in the API responses.
    """
    data = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            data.extend(json_data['results'])
            url = json_data['next']  # SWAPI paginates the data
        else:
            print(f"Error fetching data from {url}")
            break
    return data


def extract_and_load_people():
    url = "https://swapi.dev/api/people/"
    people_data = get_data_from_api(url)

    for person in people_data:
        new_person = Person(
            name=person['name'],
            height=float(person['height']) if person['height'] != 'unknown' else None,
            mass=float(person['mass']) if person['mass'] != 'unknown' else None,
            hair_color=person['hair_color'],
            skin_color=person['skin_color'],
            eye_color=person['eye_color'],
            birth_year=person['birth_year'],
            gender=person['gender']
        )
        session.add(new_person)
    session.commit()


def extract_and_load_planets():
    url = "https://swapi.dev/api/planets/"
    planets_data = get_data_from_api(url)

    for planet in planets_data:
        new_planet = Planet(
            name=planet['name'],
            rotation_period=int(planet['rotation_period']) if planet['rotation_period'] != 'unknown' else None,
            orbital_period=int(planet['orbital_period']) if planet['orbital_period'] != 'unknown' else None,
            diameter=int(planet['diameter']) if planet['diameter'] != 'unknown' else None,
            climate=planet['climate'],
            gravity=planet['gravity'],
            terrain=planet['terrain'],
            population=int(planet['population']) if planet['population'] != 'unknown' else None
        )
        session.add(new_planet)
    session.commit()


def extract_and_load_films():
    url = "https://swapi.dev/api/films/"
    films_data = get_data_from_api(url)

    for film in films_data:
        release_date = datetime.strptime(film['release_date'], '%Y-%m-%d')
        new_film = Film(
            title=film['title'],
            episode_id=film['episode_id'],
            director=film['director'],
            producer=film['producer'],
            release_date=release_date
        )
        session.add(new_film)
    session.commit()


if __name__ == "__main__":
    extract_and_load_people()
    extract_and_load_planets()
    extract_and_load_films()

    print("Data extraction and loading completed.")