from server import loadClubs, loadCompetitions, app, clubs, competitions
from tests.units_test.conftest import captured_templates, CLUB_1, CLUB_2, COMPETITION_1, COMPETITION_2, MAX_PLACES_PER_CLUB
import json
import pytest


class TestJson:
    
    def test_loadClubs_should_get_clubs_data(self, monkeypatch ):
            
        def mock_get(*args, **kwargs):
            return {"clubs": [CLUB_1, CLUB_2]}
        monkeypatch.setattr(json, "load", mock_get)
        result = loadClubs()
        assert result[0]["name"] == "Simply Lift"
        assert result[1]["name"] == "Iron Temple"

    def test_loadCompetition_should_get_competitions_data(self, monkeypatch):
            
        def mock_get(*args, **kwargs):
            return {"competitions": [COMPETITION_1, COMPETITION_2]}
        monkeypatch.setattr(json, "load", mock_get)
        result = loadCompetitions()
        assert result[1]["name"] == "Fall Classic"
        assert result[0]["name"] == "Spring Festival"


class TestIndex:
    
    def test_index_should_status_code_ok_with_good_templates(self, **extra):
        templates = []
        with captured_templates(app, templates, **extra):
            rv = app.test_client().get('/')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'index.html'


class TestShowSummary:
    
    def test_showsummary_should_status_code_ok_with_good_template(self, **extra):
        templates = []
        with captured_templates(app, templates, **extra):
            rv = app.test_client().post('/showSummary', data={'email' : 'john@simplylift.co'})
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'


    def test_showsummary_should_redirect_to_index_if_unknow_email(self, **extra):
        templates = []
        with captured_templates(app, templates, **extra):
            rv = app.test_client().post('/showSummary', data={'email': 'bad@simplylift.co'}, follow_redirects=True)
            assert rv.status_code == 401
            template, context = templates[0]
            assert template.name == 'index.html'
            data = rv.data.decode()
            assert "<li>Sorry, that email wasn&#39;t found.</li>" in data
        
    def test_showsummary_should_undisplayed_booking_when_competition_is_over(self):
        response = app.test_client().post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
        data = response.data.decode()
        assert "<a href='/book/Fall%20Classic/Simply%20Lift'>Book Places</a>" not in data


class TestBook:
    
    def test_book_should_status_code_ok_with_good_template(self, **extra):
        club = CLUB_1["name"]
        competition = COMPETITION_1["name"]
        templates = []
        
        with captured_templates(app, templates, **extra):
            rv = app.test_client().get(f"/book/{competition}/{club}", follow_redirects=True)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'booking.html'
        
    def test_book_should_redirect_to_welcome_if_bad_url(self, **extra):
        templates = []
        
        with captured_templates(app, templates, **extra):
            rv = app.test_client().get("/book/wrong/bad", follow_redirects=True)
            assert rv.status_code == 400
            template, context = templates[0]
            assert template.name == 'index.html'
            data = rv.data.decode()
            assert "Something went wrong-please try again" in data
        
    def test_book_should_no_reservation_when_competition_is_over(self, **extra):
        club = CLUB_1["name"]
        competition = COMPETITION_2["name"]
        templates = []
        with captured_templates(app, templates, **extra):
            rv = app.test_client().get(f"/book/{competition}/{club}", follow_redirects=True)
            assert rv.status_code == 403
            template, context = templates[0]
            assert template.name == 'welcome.html'
            data = rv.data.decode()
            assert "Something went wrong-please try again" in data


class TestPurchasePlaces:
    
    def test_should_status_code_ok_with_good_template(self,  **extra):
        competition = COMPETITION_1["name"]
        club = CLUB_1["name"]
        placesRequired = 1
        templates = []
        
        with captured_templates(app, templates, **extra):
            rv = app.test_client().post('/purchasePlaces', data={"competition": competition, "club": club, "places" : placesRequired})
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'
 
        
    def test_should_deducted_points_of_clubs_balance(self, **extra):
        competition = COMPETITION_1["name"]
        club = CLUB_1["name"]
        placesRequired = 1
        expected = 12 
        templates = []
        
        with captured_templates(app, templates, **extra):
            rv = app.test_client().post('/purchasePlaces', data={"competition": competition, "club": club, "places" : placesRequired})
            assert rv.status_code == 200
            template, context = templates[0]
            assert int(context["club"]["points"]) == expected   
    
    def test_should_redirect_to_welcome_if_booking_is_more_than_available_points(self, **extra):
        CLUB_2["points"] = 4
        club = CLUB_2["name"]
        competition = COMPETITION_1["name"]
        placesRequired = 5  
        rv = app.test_client().post('/purchasePlaces', data={"competition": competition, "club": club, "places" : placesRequired}, follow_redirects=True)
        assert rv.status_code == 403
        data = rv.data.decode()
        assert "You should not book more than yours available points" in data
        
    def test_should_redirect_to_welcome_if_club_books_more_than_12_points(self, **extra):
        club = CLUB_1["name"]
        competition = COMPETITION_1["name"]
        placesRequired = 13
        rv = app.test_client().post('/purchasePlaces', data={"competition": competition, "club": club, "places" : placesRequired}, follow_redirects=True)
        assert rv.status_code == 403
        data = rv.data.decode()
        assert "You should book no more than 12 places per competition" in data
        
    def test_should_redirect_to_welcome_if_club_books_on_past_competition(self, **extra):
        club = CLUB_1["name"]
        competition = COMPETITION_2["name"]
        placesRequired = 1
        rv = app.test_client().post('/purchasePlaces', data={"competition": competition, "club": club, "places" : placesRequired}, follow_redirects=True)
        assert rv.status_code == 403
        data = rv.data.decode()
        assert "The competition is over, the booking is closed !" in data
        
        
class TestLogout:
    
    def test_should_status_code_redirect(self):
        response = app.test_client().get('/logout', follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()
        assert "<title>GUDLFT Registration</title>" in data

    