import json


def test_get_movie(client, test_db):
    response = client.get('/movie?title=шрэк')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0


def test_get_film_info_with_mocked_response(app, client, elasticsearch_connection, test_db):
    link = 'https://www.kinopoisk.ru/film/412/'
    response = client.get(f'/save_film?link={link}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['film'] == 'Принцесса-невеста'
    assert data['year'] == 1987
