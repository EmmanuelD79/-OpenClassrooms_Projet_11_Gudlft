
class TestIndex:
    
    def test_index_should_status_code_ok(self, client):
        response = client.get('/')
        assert response.status_code == 200
        
    def test_index_should_have_good_template(self, client):
        response = client.get('/')
        data = response.data.decode()
        assert "<title>GUDLFT Registration</title>" in data


class TestShowSummary:
    
    def test_should_status_code_ok(self, client):
        response = client.post('/showSummary', data={'email' : 'john@simplylift.co'})
        assert response.status_code == 200
    
class TestBook:
    
    def test_should_status_code_ok(self, client):
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        assert response.status_code == 200

class TestPurchasePlaces:
    
    def test_should_status_code_ok(self, client):
        response = client.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places' : 2})
        assert response.status_code == 200

class TestLogout:
    
    def test_should_status_code_redirect(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()
        assert "<title>GUDLFT Registration</title>" in data

    