
import pytest
import server
from flask import template_rendered
from contextlib import contextmanager

class DATASET:
    def __init__(self):
        self.clubs= {"clubs":[
            {
                "name":"Simply Lift",
                "email":"john@simplylift.co",
                "points":"15"
            },
            {
                "name":"Iron Temple",
                "email": "admin@irontemple.com",
                "points":"4"
            }
        ]}

        self.competitions = {"competitions": [
                {
                    "name": "Spring Festival",
                    "date": "2023-03-27 10:00:00",
                    "numberOfPlaces": "25",
                    "over": False
                },
                {
                    "name": "Fall Classic",
                    "date": "2020-10-22 13:30:00",
                    "numberOfPlaces": "13",
                    "over": True
                }
        ]}


@pytest.fixture(scope="function")
def client():
    app =  server.app
    app.config.update({
        "TESTING": True,
    })
    init_data()
    with app.test_client() as client:
        yield client

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture()
def template_info(client):
    
    def _http_method(method, url, data):
        if method == "post":
            return client.post(url, data=data)
        else:
            return client.get(url)

    
    def render_template_info(method="get", url=None, data="", status_code=200):
        
        with captured_templates(server.app) as templates:
            response = _http_method(method, url, data)
            assert response.status_code == status_code
            assert len(templates) == 1
            data = response.data.decode()
            template, context = templates[0]
            return template, context, data
    
    return render_template_info

def init_data():
    server.clubs = DATASET().clubs['clubs']
    server.competitions = DATASET().competitions["competitions"]
    server.MAX_PLACES_PER_CLUB = 12

def request_dataset(index_club, index_competition):
    club = DATASET().clubs["clubs"][index_club]
    competition = DATASET().competitions["competitions"][index_competition]
    return club, competition
       