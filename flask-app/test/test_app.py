import pytest
from flask import Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test de la page d’accueil"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Utilisateurs" in response.data  # vérifie que le mot apparait dans la page

def test_add_user(client):
    """Test de l’ajout d’un utilisateur"""
    response = client.post('/add', data={'name': 'Alice', 'email': 'alice@example.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Alice" in response.data

def test_delete_user(client):
    """Test suppression utilisateur"""
    # Ajoute un utilisateur d’abord
    client.post('/add', data={'name': 'Bob', 'email': 'bob@example.com'}, follow_redirects=True)

    # Récupère la page et trouve l’ID de Bob
    response = client.get('/')
    assert b"Bob" in response.data

    # Exemple si delete prend en param l’id = 1
    response = client.post('/delete/1', follow_redirects=True)
    assert response.status_code == 200
