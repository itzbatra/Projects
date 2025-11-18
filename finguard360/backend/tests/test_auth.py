import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register_and_login(client):
    r = client.post('/api/auth/register', json={'email':'t@example.com','password':'pass'})
    assert r.status_code == 201
    r = client.post('/api/auth/login', json={'email':'t@example.com','password':'pass'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'access_token' in data and 'refresh_token' in data
