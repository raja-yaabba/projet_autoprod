import pytest
from controller import app, db, Task

# Utilisation d'une base de données de test
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@mysql-db:3306/demo_test"

@pytest.fixture
def client():
    # Mode test activé
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # Reset DB tables avant chaque test
            db.drop_all()
            db.create_all()
        yield client

        # Nettoyage après
        with app.app_context():
            db.drop_all()


def test_index(client):
    """Test de la page d’accueil"""
    response = client.get('/')
    assert response.status_code == 200
    # La page doit s'afficher même si aucune tâche n'existe
    data = response.data.decode('utf-8')
    assert "Tâches" in data or "Utilisateurs" in data


def test_add_task(client):
    """Test ajout d’une tâche"""
    response = client.post(
        "/add",
        data={"task": "Faire les courses", "description": "Acheter du lait"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Faire les courses" in response.data
    assert b"Acheter du lait" in response.data


def test_edit_task(client):
    """Test modification tâche"""
    # Ajout d'une tâche
    client.post("/add", data={"task": "Ancien titre", "description": "Ancienne desc"}, follow_redirects=True)

    with app.app_context():
        task = Task.query.first()
        assert task is not None
        task_id = task.id

    # Edition
    response = client.post(
        f"/edit/{task_id}",
        data={"task": "Nouveau titre", "description": "Nouvelle desc"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Nouveau titre" in response.data


def test_delete_task(client):
    """Test suppression tâche"""
    client.post("/add", data={"task": "A supprimer", "description": "test"}, follow_redirects=True)

    with app.app_context():
        task = Task.query.first()
        assert task is not None
        task_id = task.id

    response = client.post(f"/delete/{task_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"A supprimer" not in response.data
