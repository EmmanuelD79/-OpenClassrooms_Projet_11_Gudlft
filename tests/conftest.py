
import pytest
import server
from flask import template_rendered
from contextlib import contextmanager
from tests.dataset import Dataset


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
    
    def _http_method(method, url, data, **kwargs):
        if method == "post":
            return client.post(url, data=data, **kwargs)
        else:
            return client.get(url, **kwargs)

    
    def render_template_info(method="get", url=None, data="", status_code=200, **kwargs):
        
        with captured_templates(server.app) as templates:
            response = _http_method(method, url, data, **kwargs)
            assert response.status_code == status_code
            assert len(templates) == 1
            data = response.data.decode()
            template, context = templates[0]
            return template, context, data
    
    return render_template_info

def init_data():
    server.clubs = Dataset().clubs['clubs']
    server.competitions = Dataset().competitions["competitions"]
    server.MAX_PLACES_PER_CLUB = 12

def request_dataset(index_club, index_competition):
    club = Dataset().clubs["clubs"][index_club]
    competition = Dataset().competitions["competitions"][index_competition]
    return club, competition
       