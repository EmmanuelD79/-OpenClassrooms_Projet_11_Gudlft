import pytest
from server import app
from flask import template_rendered

CLUB_1 = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "15"}
CLUB_2 = {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}
COMPETITION_1 = {"name": "Spring Festival", "date": "2023-03-27 10:00:00", "numberOfPlaces": "25"}
COMPETITION_2 = {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"}
MAX_PLACES_PER_CLUB = 12

def captured_templates(app, recorded, **extra):
    def record(sender, template, context):
        recorded.append((template, context))
    return template_rendered.connected_to(record, app)
<<<<<<< HEAD
 
=======
>>>>>>> 4-bug-clubs-shouldnt-be-able-to-book-more-than-12-places-per-competition
