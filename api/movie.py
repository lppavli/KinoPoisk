import os

import requests as requests
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker

from db.db import create_postgresql_connection, create_elasticsearch_connection
from db.models import Movies, Actors, MoviesActors

load_dotenv()

route = Blueprint("movie", __name__)
db_engine = create_postgresql_connection()
es = create_elasticsearch_connection()
Session = sessionmaker(bind=db_engine)


@route.get("/")
def test():
    return {"m": 1}


@route.get('/save_film')
def get_film_info():
    """
    Парсинг информации о фильме и сохранение данных в postgres и elasticsearch
    Пример запроса: http://****/save_film?link=https://www.kinopoisk.ru/film/412/
    """
    link = request.args.get('link')
    film_id = link.split('/')[-2]
    api_key = os.getenv('API_KEY')

    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}'
    headers = {
        'accept': 'application/json',
        'X-API-KEY': api_key
    }
    response = requests.get(url, headers=headers)
    url2 = f'https://kinopoiskapiunofficial.tech/api/v1/staff?filmId={film_id}'

    response2 = requests.get(url2, headers=headers)

    if response.status_code == 200:
        film_info = response.json()
        title = film_info['nameRu']
        description = film_info['description']
        year = film_info['year']
        country = film_info['countries'][0]['country']
        genre = film_info['genres'][0]['genre']
    else:
        return jsonify({'error': 'Failed to fetch film info'})
    if response2.status_code == 200:
        staff_info = response2.json()
        director = staff_info[0]["nameRu"]
    else:
        return jsonify({'error': 'Failed to fetch film info'})

    session = Session()
    # сохраняем фильм
    movie = Movies(title=title, description=description, year=year,
                   country=country, director=director, genre=genre)
    session.add(movie)
    session.commit()

    elasticsearch_index = 'films'
    document = {
        'title': title,
        'description': description,
        'actors': [staff['nameRu'] for staff in staff_info[1:] if staff['professionKey'] == 'ACTOR']
    }

    es.index(index=elasticsearch_index, id=film_id, body=document)
    # сохраняем актеров
    for staff in staff_info[1:]:
        if staff['professionKey'] == 'ACTOR':
            name = staff['nameRu']
            name_exist = session.query(Actors).filter(Actors.name == name).first()
            if not name_exist:
                actor = Actors(name=name)
                session.add(actor)
                session.commit()
            else:
                actor = name_exist
            movie_actor_relationship = MoviesActors(movie_id=movie.id, actor_id=actor.id)
            session.add(movie_actor_relationship)
            session.commit()
    session.close()
    return jsonify({"film": title, "year": year, "description": description})


@route.get('/movie')
def get_movie():
    """
    Метод поиска информации о фильме с помощью ElasticSearch
    Пример запроса: http://****/movie?title=шрэк
    """
    title = request.args.get('title', '')
    body = {
        "query": {
            "multi_match": {
                "query": title,
                "fuzziness": "auto",
            }
        },
    }
    search_results = es.search(index='films', body=body)
    documents = [hit["_source"] for hit in search_results['hits']['hits']]
    return jsonify(documents)
